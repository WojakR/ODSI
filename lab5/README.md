# Laboratorium 5 – Apache httpd: kontrola dostępu i CGI

## Środowisko
- Docker v29.9.2, Docker Compose v5.6.1, WSL 2
- httpd: Apache/2.4.69 (Unix), Python: 3.14.10

## Zawartość
- `konfiguracja/dostep.conf` – reguły dostępu (zad. 1: `materialy` bez listy, `wewnetrzne` zablokowane; zad. 2–3: Basic dla `panel` i `cgi-bin`)
- `cgi-bin/uprawnienia.cgi` – program CGI (Python 3): wypisuje euid/egid i próbuje czytać `/lab-data/ogolny.txt` i `/lab-data/poufny.txt`
- `raport.md` – raport, `dowody.md` – pełne odpowiedzi i logi
- Baza `auth/uzytkownicy` nie jest w repozytorium. Tworzy się ją lokalnie przez htpasswd.

## Uruchomienie
```text
docker compose run --rm --no-deps narzedzia -cB /auth/uzytkownicy student
docker compose up -d --build web
docker compose exec web httpd -t
curl.exe -i http://127.0.0.1:8080/
```

## Sprawdzenie
```text
curl.exe -i http://127.0.0.1:8080/materialy/              # 403
curl.exe -i http://127.0.0.1:8080/materialy/notatka.txt   # 200
curl.exe -i http://127.0.0.1:8080/wewnetrzne/plan.txt     # 403
curl.exe -i http://127.0.0.1:8080/panel/raport.txt        # 401
curl.exe -i -u student http://127.0.0.1:8080/panel/raport.txt          # 200
curl.exe -i -u student http://127.0.0.1:8080/cgi-bin/uprawnienia.cgi   # 200
```
