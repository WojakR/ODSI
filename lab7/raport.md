# ODSI — Laboratorium 7 (SQL Injection i Code Injection)

**Imię i nazwisko:** Wojciech Regulski
**Nr indeksu:** 337612
**GitHub:** https://github.com/WojakR/ODSI  **commit:**

Środowisko: Docker 29.9.2, obraz `python:3.12-alpine` (Alpine 3.24.4), Flask 3.1.3. Aplikacja „Sejf sekretów" pod `http://127.0.0.1:8080`, kontener tylko do odczytu, użytkownik `app` (UID 1000). Poprawki w `pliki-dla-studentow/aplikacja/app.py`. Pełne ładunki, polecenia i logi: `dowody.md`.

## Zadanie 1 — SQL Injection

Podatność: `app.py` sklejał klucz z zapytaniem: `"... WHERE klucz = '" + klucz + "'"`. Apostrof z wejścia zamyka literał i wejście staje się składnią SQL.

| # | wejście (klucz) | liczba wierszy |
|---|---|---|
| 1 | `1234` (legalny) | 1 |
| 2 | `'` | 0 (błąd `OperationalError: unrecognized token`) |
| 3 | `' OR '1'='1` | **4** (wszystkie sekrety) |
| 4 | `' UNION SELECT type, name FROM sqlite_master -- ` | 2 (nazwy tabel) |
| 5 | `' UNION SELECT login, email FROM konta -- ` | 2 (dane z drugiej tabeli) |

**Zapytanie po wstawieniu danych (atak 3):**
`SELECT wlasciciel, sekret FROM sekrety WHERE klucz = '' OR '1'='1'`

**Tabele bazy (z `sqlite_master`):** `sekrety(klucz, wlasciciel, sekret)` oraz `konta(login, rola, email)`. Druga tabela `konta` — kolumny `login, rola, email`; odczytane wiersze: `admin administrator: admin@lab7.example`, `anna uzytkownik: anna@lab7.example`.

**Wniosek:** Apostrof w wejściu zamknął literał napisu, więc dopisane `OR '1'='1'` oraz `UNION SELECT` zostały wykonane jako struktura zapytania, a nie jako szukana wartość.

## Zadanie 2 — Zapytanie z parametrami

Poprawka: stały tekst zapytania + wartość w krotce, ogólny komunikat błędu, szczegóły do logu.

```python
zapytanie = "SELECT wlasciciel, sekret FROM sekrety WHERE klucz = ?"
wiersze = db.execute(zapytanie, (klucz,)).fetchall()
# except sqlite3.Error: app.logger.exception(...); blad = "Wystapil blad zapytania."
```

| wejście (klucz) | wierszy PRZED | wierszy PO |
|---|---|---|
| `1234` | 1 | 1 |
| `'` | 0 (błąd SQLite) | 0 (bez błędu) |
| `' OR '1'='1` | 4 | 0 |
| `' UNION ... sqlite_master -- ` | 2 | 0 |
| `' UNION ... konta -- ` | 2 | 0 |
| `d'Artagnan` (legalny z apostrofem) | 0 (błąd SQLite) | **1** (`Jeden za wszystkich`) |

Po poprawce żaden atak nie zwraca danych ani komunikatu SQLite (log serwera czysty), a legalny klucz `d'Artagnan` działa poprawnie.

**Wniosek:** Wartość parametru jest przekazywana do SQLite osobno od tekstu zapytania i traktowana jako dane, więc apostrof nie zamyka już literału i nie zmienia struktury. Parametr może zastąpić **wartość, nie nazwę tabeli ani kolumny** — te muszą pochodzić z jawnej listy w kodzie.

## Zadanie 3 — Code Injection w kalkulatorze

Podatność: `eval(wyrazenie)` wykonuje dowolny kod Pythona. Przez samo pole wyrażenia (bez zmiany kodu):

| wyrażenie (krok 2) | skrócony wynik |
|---|---|
| `__import__('os').listdir('/etc')` | `['services','shadow','ssl','os-release','group',...]` |
| `open('/etc/os-release').read()` | `NAME="Alpine Linux" … VERSION_ID=3.24.4` |
| `__import__('os').getuid()` | `1000` |

**UID procesu aplikacji:** 1000 (użytkownik `app`, nie root). `/etc/shadow` → `Permission denied` — brak uprawnień roota ogranicza skutki, ale nie usuwa podatności.

Poprawka: własny parser (liczba, operator, liczba) zamiast `eval` — limit 100 znaków, `re.fullmatch`, słownik działań `+ - * /`, osobna obsługa dzielenia przez zero. Testy po poprawce:

| wejście | HTTP | wynik |
|---|---|---|
| `2+3` | 200 | 5 |
| `7 / 2` | 200 | 3.5 |
| `-1.5*4` | 200 | -6 |
| `1/0` | 400 | Dzielenie przez zero |
| `__import__('os').listdir('/etc')` | 400 | Nieprawidłowe wyrażenie |
| `open('/etc/os-release').read()` | 400 | Nieprawidłowe wyrażenie |
| `__import__('os').getuid()` | 400 | Nieprawidłowe wyrażenie |
| puste `?wyrazenie=` | 400 | Nieprawidłowe wyrażenie |

(`/kalkulator` bez parametru → HTTP 200, sam formularz. Dodatkowo `2+3abc` i 101 znaków → HTTP 400.)

**Wniosek:** Lista dozwolonych działań dopuszcza tylko z góry opisaną gramatykę, więc każde inne wejście jest odrzucane; blokowanie słów (np. `import`) zawsze można obejść innym wyrażeniem (`open`, `__builtins__`, inna pisownia), bo `eval` nadal wykonuje dowolny kod.
