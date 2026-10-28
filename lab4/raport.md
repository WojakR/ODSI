# ODSI — Laboratorium 4 (Funkcje skrótu)

**Imię i nazwisko:** Wojciech Regulski
**Nr indeksu:** 337612
**Język:** Python
**GitHub:** https://github.com/WojakR/ODSI  **commit:** 

## Zadanie 1

Weryfikacja `SHA256SUMS.txt`:

plik                       wynik

dokumenty/budzet.csv       BLAD
dokumenty/dane.bin         OK
dokumenty/harmonogram.txt  BRAK
dokumenty/kontakt.txt      OK
dokumenty/regulamin.txt    OK

`budzet.csv` został podmieniony (inny skrót), `harmonogram.txt` nie istnieje.
Efekt lawinowy: `"Ala ma kota."` vs `"Ola ma kota."` → **131/256 bitów różnych (51,2%)**.

## Zadanie 2

PBKDF2-HMAC-SHA256 z parametrami rekordu, porównanie w stałym czasie (`hmac.compare_digest`).
Cztery przypadki:

login     hasło      wynik

anna  `Kasztan-2026` prawda
anna  `kasztan-2026` fałsz
piotr `Żółw na łące` prawda
kasia `Kasztan-2026` fałsz (nieznany login)

Nowe konta `test1` i `test2` z **tym samym hasłem**: sole różne, skróty różne, oba weryfikują się poprawnie — losowa sól eliminuje równe skróty dla równych haseł.

## Zadanie 3

`h24` = pierwsze 3 bajty SHA-256. Każdy dokument (13 wierszy) ma 8192 warianty.

- **Kolizja między dokumentami:** oryginał `v=7282` i zmieniony `v=1761` mają równe `h24 = aac6b9`.
- **Przeciwobraz:** do `h24` niezmienionego oryginału (`9a8fd6`) pasuje **0 z 8192** wariantów zmienionego.

Potwierdza paradoks urodzinowy: dowolną parę o równym skrócie znajdujemy łatwo, trafienie w ustalony skrót — praktycznie nie.

## Pytania przy odbiorze

1. **Dlaczego suma obok pliku nie chroni przed podmianą?** Atakujący zmienia plik i od nowa liczy sumę — obie wartości są jawne, więc podmienia też sumę. Chroni tylko suma z zaufanego źródła albo HMAC/podpis (tajny klucz).
2. **Co daje sól, a co liczba iteracji?** Sól sprawia, że równe hasła mają różne skróty i blokuje tablice tęczowe. Iteracje podnoszą koszt pojedynczej próby, spowalniając atak słownikowy/siłowy.
3. **Dlaczego kolizję znaleźć łatwiej niż przeciwobraz?** Przeciwobraz to trafienie w ustalony skrót (~2^n). Kolizja to dowolna para o równym skrócie — paradoks urodzinowy daje ~2^(n/2).