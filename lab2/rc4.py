import math
import string
import sys
import time
from itertools import product


def rc4(klucz, dane):
    # KSA
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + klucz[i % len(klucz)]) % 256
        S[i], S[j] = S[j], S[i]
    # PRGA + XOR
    i = j = 0
    wynik = bytearray()
    for bajt in dane:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        wynik.append(bajt ^ S[(S[i] + S[j]) % 256])
    return bytes(wynik)


def entropia(dane):
    licz = [0] * 256
    for b in dane:
        licz[b] += 1
    n = len(dane)
    return -sum(c / n * math.log2(c / n) for c in licz if c > 0)


print("Test rc4(rc4(x)) == x:", rc4(b"abc", rc4(b"abc", b"test 123")) == b"test 123")

szyfr = open(sys.argv[1], "rb").read()

start = time.time()
wyniki = []
for litery in product(string.ascii_lowercase, repeat=3):
    klucz = "".join(litery).encode()
    wyniki.append((entropia(rc4(klucz, szyfr[:512])), klucz))
czas = time.time() - start
wyniki.sort()  # rosnąco po entropii, przy remisie alfabetycznie po kluczu

print("Liczba prób:", len(wyniki), "czas:", round(czas, 2), "s")
for h, k in wyniki[:5]:
    print(k.decode(), round(h, 4))

klucz = wyniki[0][1]
tekst = rc4(klucz, szyfr)
open("rc4.txt", "wb").write(tekst)

print("Klucz:", klucz.decode())
print(repr(tekst[:100]))
print("Ponowne szyfrowanie zgodne:", rc4(klucz, tekst) == szyfr)
print("Entropia kryptogramu:", round(entropia(szyfr), 4))
print("Entropia tekstu:", round(entropia(tekst), 4))
