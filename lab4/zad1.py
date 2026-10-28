"""Zadanie 1 - sumy kontrolne SHA-256.

Format pliku SHA256SUMS.txt: skrot_hex, dwie spacje, scieżka.
Dla każdego wiersza: OK (zgadza się), BLAD (inny skrót) albo BRAK (nie ma pliku).
Brak pliku nie przerywa programu.
Na końcu: demonstracja efektu lawinowego (Ala/Ola ma kota).
"""

import hashlib


def sha256_pliku(sciezka):
    with open(sciezka, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def sprawdz_sumy(plik_sum="SHA256SUMS.txt"):
    with open(plik_sum, encoding="utf-8") as f:
        for linia in f:
            linia = linia.rstrip("\n")
            if not linia:
                continue
            oczekiwany, sciezka = linia.split("  ", 1)
            try:
                policzony = sha256_pliku(sciezka)
            except FileNotFoundError:
                print(f"BRAK  {sciezka}")
                continue
            if policzony == oczekiwany:
                print(f"OK    {sciezka}")
            else:
                print(f"BLAD  {sciezka}")


def roznica_bitow(a, b):
    """Liczba różnych bitów między skrótami SHA-256 dwóch tekstow."""
    ha = hashlib.sha256(a.encode()).digest()
    hb = hashlib.sha256(b.encode()).digest()
    roznych = 0
    for x, y in zip(ha, hb):
        roznych += bin(x ^ y).count("1")
    return roznych


if __name__ == "__main__":
    print("== Weryfikacja SHA256SUMS.txt ==")
    sprawdz_sumy()

    print("\n== Efekt lawinowy ==")
    t1, t2 = "Ala ma kota.", "Ola ma kota."
    d = roznica_bitow(t1, t2)
    print(f'"{t1}" vs "{t2}"')
    print(f"różnych bitów: {d} z 256 ({d / 256 * 100:.1f}%)")
