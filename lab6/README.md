# Laboratorium 6 – Cross-Site Scripting (XSS)

Celowo podatna aplikacja „Tablica ogłoszeń" (Flask) z wprowadzonymi poprawkami XSS.

## Środowisko
- Docker 29.9.2, Docker Compose v5.6.1, WSL 2
- Obraz `python:3.12-alpine`, Flask 3.1.3

## Zawartość
- `pliki-dla-studentow/aplikacja/` – poprawiona aplikacja:
  - `app.py` – `escape(q)` w `/szukaj` (zad. 1), `SESSION_COOKIE_HTTPONLY = True` (zad. 2), nagłówek CSP w `@app.after_request` (zad. 3)
  - `templates/tablica.html` – przywrócone kodowanie (`{{ tresc }}` zamiast `|safe`)
  - `templates/podglad.html` + `static/podglad.js` – skrypt przeniesiony do pliku i `textContent` zamiast `innerHTML`
- `pliki-dla-studentow/zbieracz/` – serwer napastnika (bez zmian)
- `raport.md` – raport, `dowody.md` – pełne ładunki, polecenia i logi

## Uruchomienie
Wszystkie polecenia w katalogu `pliki-dla-studentow`:

```text
docker compose up -d --build
curl.exe -i http://127.0.0.1:8080/
curl.exe -i http://localhost:8081/test
```

Po każdej zmianie w `aplikacja/`: `docker compose restart web`. Zatrzymanie: `docker compose down`.

## Sprawdzenie poprawek
```text
curl.exe -i "http://127.0.0.1:8080/szukaj?q=<script>alert(1)</script>"   # ładunek zakodowany w <h1>
curl.exe -i -d "login=anna&haslo=anna-lab6" http://127.0.0.1:8080/logowanie   # Set-Cookie: ...; HttpOnly
curl.exe -i http://127.0.0.1:8080/   # Content-Security-Policy w nagłówkach
```

Konta ćwiczeniowe (dane fikcyjne): `anna`/`anna-lab6`, `student`/`student-lab6`.
