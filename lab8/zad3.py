# Zadanie 3 - szyfrowanie hybrydowe RSA-OAEP + AES-256-GCM
import os
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag

LOGIN = "WojakR"
HASLO = b"Lab8-cwiczenie"

OAEP = padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(), label=None)


def wczytaj(sciezka):
    with open(sciezka, "rb") as f:
        return f.read()


def odszyfruj(dane, klucz_prywatny):
    k = (klucz_prywatny.key_size + 7) // 8
    if len(dane) < 2:
        raise ValueError("plik za krotki (brak naglowka)")
    L = int.from_bytes(dane[0:2], "big")
    if L != k:
        raise ValueError("L=%d, a modul ma %d B" % (L, k))
    if len(dane) < L + 30:
        raise ValueError("plik uciety: %d B < %d B" % (len(dane), L + 30))
    zaszyfrowany_klucz = dane[2:2 + L]
    nonce = dane[2 + L:2 + L + 12]
    kryptogram = dane[2 + L + 12:]
    klucz_aes = klucz_prywatny.decrypt(zaszyfrowany_klucz, OAEP)
    if len(klucz_aes) != 32:
        raise ValueError("klucz AES ma zla dlugosc")
    # decrypt sprawdza tag i rzuca InvalidTag zanim cokolwiek zwroci
    return L, AESGCM(klucz_aes).decrypt(nonce, kryptogram, None)


def zaszyfruj(tekst, klucz_publiczny):
    klucz_aes = AESGCM.generate_key(bit_length=256)  # os.urandom pod spodem
    nonce = os.urandom(12)
    zaszyfrowany_klucz = klucz_publiczny.encrypt(klucz_aes, OAEP)
    kryptogram = AESGCM(klucz_aes).encrypt(nonce, tekst, None)
    return len(zaszyfrowany_klucz).to_bytes(2, "big") + zaszyfrowany_klucz + nonce + kryptogram


# 1. odszyfrowanie paczki
klucz_prywatny = serialization.load_pem_private_key(
    wczytaj("pliki-dla-studentow/klucz_prywatny.pem"), password=HASLO)
paczka = wczytaj("pliki-dla-studentow/paczka.bin")
print("rozmiar paczka.bin:", len(paczka), "B")
L, tekst = odszyfruj(paczka, klucz_prywatny)
tekst = tekst.decode("utf-8")
print("L =", L)
print("--- tekst ---")
print(tekst)
print("-------------")

# slowo kontrolne - szukam linii ze slowem kontrolnym, w razie czego trzeba poprawic recznie
slowo = None
for linia in tekst.splitlines():
    if "kontrolne" in linia.lower() and ":" in linia:
        slowo = linia.split(":", 1)[1].strip()
if slowo is None:
    raise SystemExit("nie znalazlem slowa kontrolnego")

# 2. odpowiedz dla prowadzacego
klucz_prowadzacego = serialization.load_pem_public_key(wczytaj("pliki-dla-studentow/klucz_prowadzacego.pem"))
odp = zaszyfruj((slowo + "\n" + LOGIN).encode("utf-8"), klucz_prowadzacego)
with open("odpowiedz.bin", "wb") as f:
    f.write(odp)
print("odpowiedz.bin:", len(odp), "B, L =", int.from_bytes(odp[0:2], "big"))

# 3. zmiana jednego bajtu kryptogramu w kopii
kopia = bytearray(paczka)
kopia[2 + L + 12 + 5] ^= 0xFF
try:
    odszyfruj(bytes(kopia), klucz_prywatny)
    print("zmieniona kopia: ODSZYFROWANO (zle!)")
except InvalidTag:
    print("zmieniona kopia: odrzucona (InvalidTag)")

# dodatkowo: plik uciety
for dl in (1, 100, L + 29):
    try:
        odszyfruj(paczka[:dl], klucz_prywatny)
        print("uciety do", dl, "B: przyjety (zle!)")
    except (ValueError, InvalidTag) as e:
        print("uciety do", dl, "B: odrzucony -", type(e).__name__, e)
