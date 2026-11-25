# Zadanie 2 - podpisy RSA-PSS
import os
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature

KATALOG = "pliki-dla-studentow/dokumenty"
LOGIN = "WojakR"

PSS = padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=32)


def wczytaj(sciezka):
    with open(sciezka, "rb") as f:
        return f.read()


def zapisz(sciezka, dane):
    with open(sciezka, "wb") as f:
        f.write(dane)


def weryfikuj(klucz_pub, dane, podpis):
    try:
        klucz_pub.verify(podpis, dane, PSS, hashes.SHA256())
        return "OK"
    except InvalidSignature:
        return "BŁĄD"


# 1. weryfikacja dokumentow
klucz_podpisu = serialization.load_pem_public_key(wczytaj("pliki-dla-studentow/klucz_podpisu.pem"))
for nazwa in sorted(os.listdir(KATALOG)):
    if not nazwa.endswith(".txt"):
        continue
    dok = wczytaj(os.path.join(KATALOG, nazwa))
    podpis = wczytaj(os.path.join(KATALOG, nazwa + ".sig"))
    print(nazwa, weryfikuj(klucz_podpisu, dok, podpis))

# 2. wlasna para kluczy i podpis
# klucz prywatny trzymam lokalnie w moj_klucz_prywatny.pem (jest w .gitignore)
if os.path.exists("moj_klucz_prywatny.pem"):
    moj_klucz = serialization.load_pem_private_key(wczytaj("moj_klucz_prywatny.pem"), password=None)
else:
    moj_klucz = rsa.generate_private_key(public_exponent=65537, key_size=3072)
    zapisz("moj_klucz_prywatny.pem", moj_klucz.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption()))

moj_pub = moj_klucz.public_key()
zapisz("moj_klucz_publiczny.pem", moj_pub.public_bytes(
    serialization.Encoding.PEM,
    serialization.PublicFormat.SubjectPublicKeyInfo))

tresc = ("Laboratorium 8: " + LOGIN).encode("utf-8")
zapisz("podpis.txt", tresc)
podpis = moj_klucz.sign(tresc, PSS, hashes.SHA256())
zapisz("podpis.txt.sig", podpis)
print("dlugosc podpisu:", len(podpis), "B")

# weryfikacja z plikow (klucz publiczny z pliku PEM)
pub_z_pliku = serialization.load_pem_public_key(wczytaj("moj_klucz_publiczny.pem"))
print("podpis.txt przed zmiana:", weryfikuj(pub_z_pliku, wczytaj("podpis.txt"), wczytaj("podpis.txt.sig")))

# 3. kopia z jednym zmienionym bajtem
kopia = bytearray(wczytaj("podpis.txt"))
kopia[0] ^= 0x01  # 'L' -> 'M'
print("kopia po zmianie bajtu 0:", bytes(kopia))
print("podpis.txt po zmianie:", weryfikuj(pub_z_pliku, bytes(kopia), wczytaj("podpis.txt.sig")))
