import sys

DOZWOLONE = set(range(32, 127)) | {9, 10, 13}

def odszyfruj(dane, k):
    return bytes((c - k) % 256 for c in dane)


def ocena(tekst):
    dobre = sum(1 for b in tekst if b in DOZWOLONE)
    return dobre / len(tekst)


dane = open(sys.argv[1], "rb").read()

wyniki = []
for k in range(256):
    wyniki.append((ocena(odszyfruj(dane,k)), k))
wyniki.sort(key=lambda w: (-w[0], w[1]))

print("Najlepsze przesunięcia:")
for nr, (s,k) in enumerate(wyniki[:5], 1):
    print(nr, "k =", k, "ocena =", round(s, 6), repr(odszyfruj(dane, k)[:50]))

nr = int(input("Wybierz kandydata (1-5): "))
k = wyniki[nr - 1][1]
open("cezar.txt", "wb").write(odszyfruj(dane, k))
print("Zapisano cezar.txt, k =", k)