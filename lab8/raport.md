# ODSI — Laboratorium 8 (RSA i podpis cyfrowy)

**Imię i nazwisko:** Wojciech Regulski
**Nr indeksu:** 337612
**Język:** Python 3.14 + `cryptography` 50.0.2
**GitHub:** https://github.com/WojakR/ODSI (katalog `lab8`)  **commit:** 31fccd1

Kod: `zad1.py`, `zad2.py`, `zad3.py`. Pełne wyjścia programów: `dowody.md`.

## Zadanie 1 — RSA na małych liczbach

Własne potęgowanie (kwadraty i mnożenia): `4^13 mod 497 = 445` ✔, `a^0 mod n = 1` ✔.

| | wartość |
|---|---|
| n | 1466056398307 (41 bitów) |
| p | **1048601** |
| q | **1398107** |
| φ(n) | 1466053951600 |
| d | **1396416556673** ((e·d) mod φ = 1 ✔) |
| czas faktoryzacji | **0,031 s** (dzielenie próbne do √n) |

**Tekst:** „Klucz RSA o długości 41 bitów rozkładasz na czynniki w ułamku sekundy. Bezpieczne RSA ma co najmniej 2048 bitów.” (+ 2 spacje dopełnienia)

**Wniosek:** Dzielenie próbne wymaga ok. √n ≈ 2^1024 prób dla klucza 2048-bitowego, czyli nieporównanie więcej operacji, niż da się wykonać na jakimkolwiek sprzęcie (tu wystarczyło ~2^20).

## Zadanie 2 — Podpisy RSA-PSS

| dokument | wynik |
|---|---|
| faktura.txt | **BŁĄD** |
| protokol.txt | OK |
| regulamin.txt | **BŁĄD** |
| umowa.txt | OK |

Własny podpis (RSA 3072, `podpis.txt` = `Laboratorium 8: WojakR`): **przed zmianą OK**, po zmianie jednego bajtu w kopii (`L`→`M`) **BŁĄD**. W repo: `podpis.txt`, `podpis.txt.sig` (384 B), `moj_klucz_publiczny.pem`.

**Wniosek:** Poprawny podpis z kluczem z niezaufanego źródła potwierdza tylko, że plik podpisał właściciel *tego* klucza, ale nie potwierdza tożsamości autora — atakujący może podmienić i dokument, i klucz publiczny.

## Zadanie 3 — Szyfrowanie hybrydowe

| | wartość |
|---|---|
| L dla `paczka.bin` | **256** (RSA 2048; plik 452 B) |
| L dla `odpowiedz.bin` | **384** (RSA 3072 prowadzącego; plik 430 B) |
| 1. wiersz tekstu | „Gratulacje, paczka odszyfrowana poprawnie.” |
| krok 3 (zmieniony bajt kryptogramu) | **odrzucony — `InvalidTag`**, brak tekstu jawnego |

Przed odszyfrowaniem sprawdzane: ≥ 2 B nagłówka, L = długość modułu, rozmiar ≥ L + 30 (pliki ucięte do 1, 100 i 285 B odrzucone). `odpowiedz.bin`: losowy klucz AES-256 i nonce z CSPRNG, treść `słowo kontrolne\nWojakR`.

**Wniosek:** RSA-OAEP zaszyfruje tylko krótką wiadomość (dla 2048 bitów max 190 B) i jest bardzo wolne, a AES-GCM szyfruje szybko dane dowolnej długości i dodatkowo sprawdza integralność tagiem — więc RSA używamy tylko do przekazania 32-bajtowego klucza AES.
