# ODSI — Laboratorium 5 (Bezpieczeństwo serwera WWW)

**Imię i nazwisko:** Wojciech Regulski
**Nr indeksu:** 337612
**GitHub:** https://github.com/WojakR/ODSI  **commit:** 

Środowisko: Docker 29.9.2, Compose v5.6.1, Apache/2.4.69 (Unix), Python 3.14.10. Reguły: `konfiguracja/dostep.conf`, CGI: `cgi-bin/uprawnienia.cgi`. Pełne odpowiedzi i logi: `dowody.md`.

## Zadanie 1 — dostęp do katalogów

| URL                      | przed              | po  |
|--------------------------|--------------------|-----|
| `/materialy/`            | 200 (lista plików) | 403 |
| `/materialy/notatka.txt` | 200                | 200 |
| `/wewnetrzne/`           | 200 (lista plików) | 403 |
| `/wewnetrzne/plan.txt`   | 200                | 403 |

Przed zmianą lista plików była widoczna w `/materialy/` i `/wewnetrzne/` (`Options Indexes` z `httpd.conf`).
Reguły: `materialy` → `Options -Indexes`, `wewnetrzne` → `Require all denied`.

Log odmowy (dowody.md):
`[authz_core:error] ... AH01630: client denied by server configuration: /usr/local/apache2/htdocs/wewnetrzne/plan.txt`

**Wniosek:** Parametr `-Indexes` ukrywa tylko automatyczną listę katalogu — plik o znanej nazwie dalej jest serwowany; `Require all denied` odmawia autoryzacji każdego żądania do katalogu, więc nawet znana nazwa daje 403.

## Zadanie 2 — Basic dla `/panel/`

`AuthType Basic`, `AuthName "Laboratorium 5"`, `AuthUserFile "/auth/uzytkownicy"`, `Require valid-user`.

| próba                              | kod                            |
|------------------------------------|--------------------------------|
| `/panel/raport.txt` bez danych     | 401                            |
| `/panel/raport.txt` błędne hasło   | 401 (log: `Password Mismatch`) |
| `/panel/raport.txt` poprawne hasło | 200                            |
| `/` bez logowania                  | 200                            |

Bez logowania: `WWW-Authenticate: Basic realm="Laboratorium 5"`.

**Wniosek:** Basic wysyła `login:hasło` tylko zakodowane w Base64 (to nie szyfrowanie) w nagłówku `Authorization` przy każdym żądaniu, więc każdy podsłuchujący zwykłe HTTP odczyta hasło — ochronę transmisji daje dopiero TLS.

## Zadanie 3 — uprawnienia CGI

`ls -ln /lab-data/`: `ogolny.txt` `-rw-r-----` (640) uid 0 gid 2; `poufny.txt` `-rw-------` (600) uid 0 gid 2.
CGI: **euid=2 egid=2** (`daemon`, `User/Group daemon` z `httpd.conf`).

|              | przed Basic              | po Basic, bez logowania | po Basic, poprawne hasło    |
|--------------|--------------------------|-------------------------|-----------------------------|
| kod HTTP     | 200                      | 401                     | 200                         |
| UID/GID      | 2/2                      | —                       | 2/2 (`REMOTE_USER=student`) |
| `ogolny.txt` | odczytany                | —                       | odczytany                   |
| `poufny.txt` | odmowa (PermissionError) | —                       | odmowa (PermissionError)    |

`ogolny.txt` czytamy przez prawo `r` dla grupy 2 (egid procesu), `poufny.txt` ma prawa tylko dla właściciela root (uid 0), a proces nie jest rootem → odmowa. Po zalogowaniu wynik bez zmian.

**Wniosek:** Basic to tylko autoryzacja w Apache (konto z pliku `/auth/uzytkownicy`, nie konto systemowe) — po zalogowaniu CGI dalej działa jako proces serwera (uid/gid 2), a jądro sprawdza prawa plików względem tego UID/GID, więc login WWW nie daje praw roota.
