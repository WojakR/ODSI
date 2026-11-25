# Dowody – Laboratorium 8

## Zadanie 1 – `python zad1.py`

```text
testy potegowania OK
n = 1466056398307 e = 65537 liczba blokow: 30
p = 1048601
q = 1398107
czas faktoryzacji: 0.031 s
phi = 1466053951600
d = 1396416556673
(e*d) mod phi = 1
tekst: 'Klucz RSA o długości 41 bitów rozkładasz na czynniki w ułamku sekundy. Bezpieczne RSA ma co najmniej 2048 bitów.  '
```

Testy w kodzie: `4^13 mod 497 = 445`, `12345^0 mod 97 = 1`, `7^0 mod 2 = 1`, porównanie z wbudowanym `pow` dla `3^200 mod 1000003`. Tekst kończy się dwiema spacjami (dopełnienie ostatniego bloku). Bajty łączone przed dekodowaniem – znaki `ł`, `ś` itd. przechodzą przez granice bloków.

## Zadanie 2 – `python zad2.py`

```text
faktura.txt BŁĄD
protokol.txt OK
regulamin.txt BŁĄD
umowa.txt OK
dlugosc podpisu: 384 B
podpis.txt przed zmiana: OK
kopia po zmianie bajtu 0: b'Maboratorium 8: WojakR'
podpis.txt po zmianie: BŁĄD
```

`podpis.txt` = `Laboratorium 8: WojakR` (22 B, bez znaku nowego wiersza). Zmiana: bajt 0 XOR 0x01 (`L` → `M`), tylko w pamięci – plik w repo jest niezmieniony. `InvalidSignature` jest łapany, więc program przechodzi przez wszystkie dokumenty.

## Zadanie 3 – `python zad3.py`

```text
rozmiar paczka.bin: 452 B
L = 256
--- tekst ---
Gratulacje, paczka odszyfrowana poprawnie.
Słowo kontrolne do odpowiedzi: [pominięte]
Klucz AES tej wiadomości był losowy i zabezpieczony tylko algorytmem RSA-OAEP.
-------------
odpowiedz.bin: 430 B, L = 384
zmieniona kopia: odrzucona (InvalidTag)
uciety do 1 B: odrzucony - ValueError plik za krotki (brak naglowka)
uciety do 100 B: odrzucony - ValueError plik uciety: 100 B < 286 B
uciety do 285 B: odrzucony - ValueError plik uciety: 285 B < 286 B
```

- `paczka.bin`: 452 B = 2 + 256 + 12 + 182 (166 B tekstu + 16 B tagu); klucz z pakietu ma 2048 bitów.
- `odpowiedz.bin`: 430 B = 2 + 384 + 12 + 32 (16 B treści + 16 B tagu); klucz prowadzącego ma 3072 bity. Klucz AES z `AESGCM.generate_key`, nonce z `os.urandom(12)`.
- Krok 3: w kopii zmieniony bajt kryptogramu o offsecie 2+L+12+5 (XOR 0xFF) → `AESGCM.decrypt` rzuca `InvalidTag` i nie zwraca żadnego tekstu.
