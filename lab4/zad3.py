"""Zadanie 3 - kolizje i paradoks urodzinowy (model h24).

h24(dane) = pierwsze 3 bajty SHA-256 (6 znaków hex).
oryginal.txt i zmieniony.txt maja po 13 wierszy zakończonych \\n.
Wariant v (0..8191): dla wiersza i = 0..12 dopisz spację przed jego \\n,
gdy (v >> i) & 1 == 1. Wariant 0 to plik bez zmian.

1. h24 wszystkich 8192 wariantów oryginału -> slownik h24 -> v.
2. Przegląda warianty zmienionego i znajduje parę (v_oryg, v_zmien) o równym h24.
3. Liczy, ile wariantów zmienionego ma h24 równe h24 niezmienionego oryginału (wariant 0).
"""

import hashlib


def wiersze(plik):
    return open(plik, "rb").read().split(b"\n")[:13]


def wariant(linie, v):
    out = bytearray()
    for i in range(13):
        out += linie[i]
        if (v >> i) & 1:
            out += b" "
        out += b"\n"
    return bytes(out)


def h24(dane):
    return hashlib.sha256(dane).digest()[:3].hex()


if __name__ == "__main__":
    oryg = wiersze("oryginal.txt")
    zmien = wiersze("zmieniony.txt")

    # krok 1: slownik h24 -> numer wariantu oryginału
    slownik = {}
    for v in range(8192):
        slownik.setdefault(h24(wariant(oryg, v)), v)

    # krok 2 i 3 w jednej pętli po wariantach zmienionego
    cel = h24(wariant(oryg, 0))  # h24 niezmienionego oryginału
    para = None
    pasujace = 0
    for vz in range(8192):
        h = h24(wariant(zmien, vz))
        if h == cel:
            pasujace += 1
        if para is None and h in slownik:
            para = (slownik[h], vz, h)

    print("== Kolizja miedzy dokumentami ==")
    if para:
        vo, vz, h = para
        print(f"para (oryginal v={vo}, zmieniony v={vz}), h24 = {h}")
    else:
        print("nie znaleziono pary")

    print("\n== Dopasowanie do niezmienionego oryginalu ==")
    print(f"h24 oryginalu (v=0) = {cel}")
    print(f"wariantow zmienionego o tym h24: {pasujace} z 8192")
