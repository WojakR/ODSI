# Laboratorium 7 – SQL Injection i Code Injection

Celowo podatna aplikacja „Sejf sekretów" + kalkulator (Flask, SQLite) z wprowadzonymi poprawkami.

## Środowisko
- Docker 29.9.2, Docker Compose, WSL 2
- Obraz `python:3.12-alpine` (Alpine 3.24.4), Flask 3.1.3
- Kontener: system plików tylko do odczytu, użytkownik `app` (UID 1000)

## Zawartość
- `pliki-dla-studentow/aplikacja/app.py` – poprawiona aplikacja:
  - `/sekret` – zapytanie z parametrem `?` i krotką zamiast sklejania napisu (zad. 1–2), ogólny komunikat błędu + `app.logger.exception` (zad. 2)
  - `/kalkulator` – własny parser `liczba operator liczba` zamiast `eval` (zad. 3): limit 100 znaków, `re.fullmatch`, słownik działań `+ - * /`, obsługa dzielenia przez zero i pustego pola (HTTP 400)
  - `templates/kalkulator.html` – dodane wyświetlanie komunikatu błędu
- `raport.md` – raport (jedna strona)
- `dowody.md` – pełne ładunki, polecenia i wyniki przed/po

## Uruchomienie
Wszystkie polecenia w katalogu `pliki-dla-studentow`:

```text
docker compose up -d --build
curl.exe -i "http://127.0.0.1:8080/sekret?klucz=1234"
curl.exe -i "http://127.0.0.1:8080/kalkulator?wyrazenie=2*21"
```

Po każdej zmianie w `aplikacja/`: `docker compose restart web`. Zatrzymanie: `docker compose down`.

## Sprawdzenie poprawek
```text
# SQL Injection nie zwraca już cudzych danych:
curl.exe -G --data-urlencode "klucz=' OR '1'='1" http://127.0.0.1:8080/sekret   # Liczba wierszy: 0
curl.exe -G --data-urlencode "klucz=d'Artagnan" http://127.0.0.1:8080/sekret    # legalny klucz z apostrofem działa
# Code Injection zablokowany, poprawne działania działają:
curl.exe -i -G --data-urlencode "wyrazenie=-1.5*4" http://127.0.0.1:8080/kalkulator                 # 200, wynik -6
curl.exe -i -G --data-urlencode "wyrazenie=__import__('os').getuid()" http://127.0.0.1:8080/kalkulator  # 400
curl.exe -i -G --data-urlencode "wyrazenie=1/0" http://127.0.0.1:8080/kalkulator                    # 400
```

Dane w bazie są fikcyjne. Nie zmieniano `Dockerfile`, `compose.yaml` ani `utworz_baze.py`.
