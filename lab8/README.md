# Laboratorium 8 – RSA i podpis cyfrowy

Język: Python 3.14, biblioteka `cryptography` (50.0.2).

```text
pip install cryptography
```

## Uruchomienie
Wszystko z katalogu `lab8`:

```text
python zad1.py   # faktoryzacja n, klucz d, odszyfrowanie male_rsa.txt
python zad2.py   # weryfikacja 4 dokumentow RSA-PSS, wlasny podpis podpis.txt(.sig)
python zad3.py   # odszyfrowanie paczka.bin, utworzenie odpowiedz.bin
```

Pierwsze uruchomienie `zad2.py` generuje parę RSA 3072 i zapisuje klucz prywatny do `moj_klucz_prywatny.pem` (lokalnie, w `.gitignore`), kolejne go wczytują. `klucz_prywatny.pem` z pakietu też jest w `.gitignore` – żeby uruchomić `zad3.py`, trzeba go wgrać do `pliki-dla-studentow/`.

## Zawartość
- `zad1.py` – własne potęgowanie modularne (kwadraty i mnożenia) + dzielenie próbne; `d = pow(e, -1, phi)`
- `zad2.py` – RSA-PSS (SHA-256, MGF1-SHA256, sól 32 B)
- `zad3.py` – RSA-OAEP-SHA256 + AES-256-GCM, sprawdzanie formatu przed odszyfrowaniem
- `podpis.txt`, `podpis.txt.sig`, `moj_klucz_publiczny.pem` – własny podpis
- `odpowiedz.bin` – odpowiedź dla prowadzącego: `L(2 B, =384) | klucz AES zaszyfrowany OAEP (384 B) | nonce (12 B) | kryptogram + tag (32 B)`
- `raport.md`, `dowody.md`
