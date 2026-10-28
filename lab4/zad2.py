"""Zadanie 2 - przechowywanie haseł (PBKDF2-HMAC-SHA256).

Rekord w hasla.txt: login:iteracje:sol_hex:skrot_hex
Skrót = PBKDF2-HMAC-SHA256 z bajtów UTF-8 hasła, sól 16 B, iteracje z rekordu, 32 B wyniku.
Weryfikacja: liczymy skrót z parametrami rekordu i porównujemy w stałym czasie.
"""

import hmac
import hashlib
import secrets


def wczytaj(plik="hasla.txt"):
    baza = {}
    with open(plik, encoding="utf-8") as f:
        for linia in f:
            linia = linia.strip()
            if not linia:
                continue
            login, iteracje, sol, skrot = linia.split(":")
            baza[login] = (int(iteracje), bytes.fromhex(sol), bytes.fromhex(skrot))
    return baza


def weryfikuj(login, haslo, baza):
    if login not in baza:          # nieznany login -> fałsz
        return False
    iteracje, sol, skrot = baza[login]
    policzony = hashlib.pbkdf2_hmac("sha256", haslo.encode("utf-8"), sol, iteracje, len(skrot))
    return hmac.compare_digest(policzony, skrot)  # porównanie w stałym czasie


def dodaj(login, haslo):
    sol = secrets.token_bytes(16)  # z bezpiecznego generatora
    iteracje = 600000
    skrot = hashlib.pbkdf2_hmac("sha256", haslo.encode("utf-8"), sol, iteracje, 32)
    return (iteracje, sol, skrot)


if __name__ == "__main__":
    baza = wczytaj()

    print("== Cztery przypadki ==")
    testy = [
        ("anna", "Kasztan-2026"),
        ("anna", "kasztan-2026"),
        ("piotr", "Żółw na łące"),
        ("kasia", "Kasztan-2026"),
    ]
    for login, haslo in testy:
        print(f"{login:6} {haslo!r:16} -> {weryfikuj(login, haslo, baza)}")

    print("\n== Nowe konta z tym samym hasłem ==")
    haslo = "To-Samo-Haslo"
    baza["test1"] = dodaj("test1", haslo)
    baza["test2"] = dodaj("test2", haslo)
    print(f"sole rozne:   {baza['test1'][1] != baza['test2'][1]}")
    print(f"skroty rozne: {baza['test1'][2] != baza['test2'][2]}")
    print(f"weryfikacja test1: {weryfikuj('test1', haslo, baza)}")
    print(f"weryfikacja test2: {weryfikuj('test2', haslo, baza)}")
