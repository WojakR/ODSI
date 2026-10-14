import sys


def szyfruj(dane, klucz):
    m = len(klucz)
    return bytes((p + klucz[i % m]) % 256 for i, p in enumerate(dane))


def odszyfruj(dane, klucz):
    m = len(klucz)
    return bytes((c - klucz[i % m]) % 256 for i, c in enumerate(dane))


tekst = open(sys.argv[1], "rb").read()
szyfr = szyfruj(tekst, b"ZAMEK")
open("vigenere.bin", "wb").write(szyfr)

print("Odszyfrowanie zgodne ze źródłem:", odszyfruj(szyfr, b"ZAMEK") == tekst)
print("Puste dane:", odszyfruj(szyfruj(b"", b"ZAMEK"), b"ZAMEK") == b"")
x = bytes([0, 255, 0, 255, 128])
print("Bajty 0 i 255:", odszyfruj(szyfruj(x, b"ZAMEK"), b"ZAMEK") == x)

print("Znany wynik BA/KO:", szyfruj(b"BA", b"KO") == bytes([141, 144]))  # 66+75, 65+79
print("Zawijanie szyfr. 255+2:", szyfruj(bytes([255]), bytes([2])) == bytes([1]))
print("Zawijanie odszyfr. 1-2:", odszyfruj(bytes([1]), bytes([2])) == bytes([255]))

for klucz in [b"SZYFR", b"KOD"]:
    c = szyfruj(b"BRAMABRAMABRAMA", klucz)
    print(klucz.decode(), c[0:5].hex(), c[5:10].hex(), c[10:15].hex())