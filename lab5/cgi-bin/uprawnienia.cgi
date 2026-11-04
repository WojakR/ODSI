#!/usr/bin/python3
# Zadanie 3 - z jakimi prawami dziala proces CGI.
# Wypisuje efektywny UID/GID i probuje odczytac dwa pliki z /lab-data.
# Nie czyta zadnych parametrow od uzytkownika.
import os

PLIKI = ["/lab-data/ogolny.txt", "/lab-data/poufny.txt"]

print("Content-Type: text/plain; charset=utf-8")
print()

print(f"euid={os.geteuid()} egid={os.getegid()}")
print(f"REMOTE_USER={os.environ.get('REMOTE_USER', '-')}")
print()

for sciezka in PLIKI:
    try:
        with open(sciezka, encoding="utf-8") as f:
            print(f"{sciezka}: OK -> {f.read().strip()}")
    except PermissionError:
        print(f"{sciezka}: ODMOWA ODCZYTU (Permission denied)")
    except OSError as e:
        print(f"{sciezka}: BLAD {e.__class__.__name__}")
