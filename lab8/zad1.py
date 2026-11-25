# Zadanie 1 - RSA na malych liczbach
import time

PLIK = "pliki-dla-studentow/male_rsa.txt"


def potega_mod(a, k, n):
    # metoda kwadratow i mnozen
    wynik = 1
    a = a % n
    while k > 0:
        if k % 2 == 1:
            wynik = (wynik * a) % n
        a = (a * a) % n
        k = k // 2
    return wynik


def faktoryzuj(n):
    if n % 2 == 0:
        return 2, n // 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return d, n // d
        d += 2
    return None


# testy potegowania
assert potega_mod(4, 13, 497) == 445
assert potega_mod(12345, 0, 97) == 1
assert potega_mod(7, 0, 2) == 1
assert potega_mod(3, 200, 1000003) == pow(3, 200, 1000003)
print("testy potegowania OK")

# wczytanie pliku
dane = {}
with open(PLIK, "rb") as f:
    for linia in f.read().decode("utf-8").splitlines():
        if "=" in linia:
            klucz, wartosc = linia.split("=", 1)
            dane[klucz.strip()] = wartosc.strip()

n = int(dane["n"])
e = int(dane["e"])
c = [int(x) for x in dane["c"].split(",")]
print("n =", n, "e =", e, "liczba blokow:", len(c))

start = time.perf_counter()
p, q = faktoryzuj(n)
czas = time.perf_counter() - start
assert p * q == n
print("p =", p)
print("q =", q)
print("czas faktoryzacji: %.3f s" % czas)

phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)
assert (e * d) % phi == 1
print("phi =", phi)
print("d =", d)
print("(e*d) mod phi =", (e * d) % phi)

bajty = b""
for blok in c:
    m = potega_mod(blok, d, n)
    bajty += m.to_bytes(4, "big")
tekst = bajty.decode("utf-8")
print("tekst:", repr(tekst))
