# Lab 5 — dowody (polecenia, odpowiedzi, logi)

Wszystko uruchamiane w jednym katalogu, PowerShell z curl.exe. Z odpowiedzi zostawione tylko linia statusu i ważne nagłówki/treść. Hasła ćwiczeniowego nie zapisuję: curl pyta o nie interaktywnie.

## 1. Zadanie 1

```text
docker compose up -d --build web
docker compose exec web httpd -t      -> Syntax OK
docker compose restart web
```

Przed zmianą:

```text
curl.exe -i http://127.0.0.1:8080/materialy/             HTTP/1.1 200 OK   <title>Index of /materialy</title> ... notatka.txt
curl.exe -i http://127.0.0.1:8080/materialy/notatka.txt  HTTP/1.1 200 OK   Publiczna notatka: ten plik ma pozostac dostepny pod znanym adresem.
curl.exe -i http://127.0.0.1:8080/wewnetrzne/            HTTP/1.1 200 OK   <title>Index of /wewnetrzne</title> ... plan.txt
curl.exe -i http://127.0.0.1:8080/wewnetrzne/plan.txt    HTTP/1.1 200 OK   Fikcyjny plan: ten katalog ma byc niedostepny przez HTTP.
```

```text
172.18.0.1 - - [04/Nov/2026:13:02:14 +0100] "GET /materialy/ HTTP/1.1" 200 305
172.18.0.1 - - [04/Nov/2026:13:02:19 +0100] "GET /materialy/notatka.txt HTTP/1.1" 200 69
172.18.0.1 - - [04/Nov/2026:13:02:22 +0100] "GET /wewnetrzne/ HTTP/1.1" 200 301
172.18.0.1 - - [04/Nov/2026:13:02:30 +0100] "GET /wewnetrzne/plan.txt HTTP/1.1" 200 58
```

Po dodaniu `Options -Indexes` (materialy) i `Require all denied` (wewnetrzne):

```text
GET /materialy/            HTTP/1.1 403 Forbidden
GET /materialy/notatka.txt HTTP/1.1 200 OK
GET /wewnetrzne/           HTTP/1.1 403 Forbidden
GET /wewnetrzne/plan.txt   HTTP/1.1 403 Forbidden
```

`docker compose logs web`:

```text
[Wed Nov 04 13:03:13.354277 2026] [autoindex:error] [client 172.18.0.1:48834] AH01276: Cannot serve directory /usr/local/apache2/htdocs/materialy/: No matching DirectoryIndex(index.html) found, and server-generated directory index forbidden by Options directive
172.18.0.1 - - [04/Nov/2026:13:03:13 +0100] "GET /materialy/ HTTP/1.1" 403 239
172.18.0.1 - - [04/Nov/2026:13:03:17 +0100] "GET /materialy/notatka.txt HTTP/1.1" 200 69
[Wed Nov 04 13:03:20.367303 2026] [authz_core:error] [client 172.18.0.1:48850] AH01630: client denied by server configuration: /usr/local/apache2/htdocs/wewnetrzne/
172.18.0.1 - - [04/Nov/2026:13:03:20 +0100] "GET /wewnetrzne/ HTTP/1.1" 403 239
[Wed Nov 04 13:03:23.797226 2026] [authz_core:error] [client 172.18.0.1:33706] AH01630: client denied by server configuration: /usr/local/apache2/htdocs/wewnetrzne/plan.txt
172.18.0.1 - - [04/Nov/2026:13:03:23 +0100] "GET /wewnetrzne/plan.txt HTTP/1.1" 403 239
```

Dwa różne komunikaty: `autoindex` (listowanie zabronione) vs `authz_core` (odmowa autoryzacji).

## 2. Zadanie 2

Baza utworzona wcześniej (hasło interaktywnie):

```text
docker compose run --rm --no-deps narzedzia -cB /auth/uzytkownicy student
```

Po dodaniu bloku `panel`:

```text
curl.exe -i http://127.0.0.1:8080/panel/raport.txt
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Basic realm="Laboratorium 5"

curl.exe -i -u student:zlehaslo http://127.0.0.1:8080/panel/raport.txt
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Basic realm="Laboratorium 5"

curl.exe -i -u student http://127.0.0.1:8080/panel/raport.txt      (hasło ***)
HTTP/1.1 200 OK
Raport cwiczeniowy: dostep po poprawnym uwierzytelnieniu.

curl.exe -i http://127.0.0.1:8080/
HTTP/1.1 200 OK
```

Log:

```text
172.18.0.1 - - [04/Nov/2026:13:08:32 +0100] "GET /panel/raport.txt HTTP/1.1" 401 421
[Wed Nov 04 13:08:36.753045 2026] [auth_basic:error] [client 172.18.0.1:42366] AH01617: user student: authentication failure for "/panel/raport.txt": Password Mismatch
172.18.0.1 - student [04/Nov/2026:13:08:36 +0100] "GET /panel/raport.txt HTTP/1.1" 401 421
172.18.0.1 - student [04/Nov/2026:13:08:50 +0100] "GET /panel/raport.txt HTTP/1.1" 200 58
172.18.0.1 - - [04/Nov/2026:13:10:35 +0100] "GET / HTTP/1.1" 200 351
```

## 3. Zadanie 3

```text
docker compose exec web ls -ln /lab-data/
-rw-r-----    1 0        2               48 Nov  4 10:16 ogolny.txt
-rw-------    1 0        2               61 Nov  4 10:16 poufny.txt
```

Użytkownik serwera z `httpd.conf`: `User daemon`, `Group daemon` (uid 2, gid 2). Data plików pochodzi z pakietu (COPY zachowuje mtime).

Przed Basic:

```text
curl.exe -i http://127.0.0.1:8080/cgi-bin/uprawnienia.cgi
HTTP/1.1 200 OK
Content-Type: text/plain; charset=utf-8

euid=2 egid=2
REMOTE_USER=-

/lab-data/ogolny.txt: OK -> LAB05: dokument dostepny dla grupy procesu WWW.
/lab-data/poufny.txt: ODMOWA ODCZYTU (Permission denied)
```

Po dodaniu Basic dla `/usr/local/apache2/cgi-bin`:

```text
curl.exe -i http://127.0.0.1:8080/cgi-bin/uprawnienia.cgi
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Basic realm="Laboratorium 5"

curl.exe -i -u student http://127.0.0.1:8080/cgi-bin/uprawnienia.cgi      (hasło ***)
HTTP/1.1 200 OK
Content-Type: text/plain; charset=utf-8

euid=2 egid=2
REMOTE_USER=student

/lab-data/ogolny.txt: OK -> LAB05: dokument dostepny dla grupy procesu WWW.
/lab-data/poufny.txt: ODMOWA ODCZYTU (Permission denied)
```

Log:

```text
172.18.0.1 - - [04/Nov/2026:13:06:38 +0100] "GET /cgi-bin/uprawnienia.cgi HTTP/1.1" 200 162
172.18.0.1 - - [04/Nov/2026:13:07:10 +0100] "GET /cgi-bin/uprawnienia.cgi HTTP/1.1" 401 421
172.18.0.1 - student [04/Nov/2026:13:07:18 +0100] "GET /cgi-bin/uprawnienia.cgi HTTP/1.1" 200 168
```

Basic zmienia tylko REMOTE_USER, UID/GID i wyniki odczytu są te same.
