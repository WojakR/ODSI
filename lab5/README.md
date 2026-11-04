# Laboratorium 5 – Apache httpd: kontrola dostępu i CGI

## Środowisko
- Docker v29.9.2, Docker Compose v5.6.1, WSL 2
- httpd: Apache/2.4.69 (Unix), Python: 3.14.10

## Zawartość
- `konfiguracja/dostep.conf` – reguły dostępu
- `cgi-bin/uprawnienia.cgi` – program CGI
- Baza `auth/uzytkownicy` nie jest w repozytorium. Tworzy się ją lokalnie przez htpasswd.

## Uruchomienie
docker compose up -d --build web
curl.exe -i http://127.0.0.1:8080/