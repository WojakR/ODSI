# Lab 3 - Szyfrowanie blokowe

Język: Python 3
Wymagana biblioteka: crytography

## Uruchomienie

```
pip install cryptography
python zad1.py
python zad2.py
python zad3.py
```

Żeby zadania 2 i 3 się uruchomiły w katalogu musi skryptów muszą też się znaleźć pliki `slaby_ecb.bin`, `wiadomosc.txt`.

## Zadanie 1

### Wyniki:

```
ECB (64 B)
C[0] = 9cdd85de85b48bed892f02d8a5cbdacb
C[1] = 9cdd85de85b48bed892f02d8a5cbdacb
C[2] = 9cdd85de85b48bed892f02d8a5cbdacb
C[3] = 9cdd85de85b48bed892f02d8a5cbdacb
rowne bloki: [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]

CBC (64 B)
C[0] = 1010cb302ceeb93d8db78a004c347960
C[1] = a306967ffebac3a04758bbe71681eb47
C[2] = f5606f2068e206954c3111c62728f5df
C[3] = 23606b32095aa9cfe8a0c5f7797ebfef
rowne bloki: brak

ECB odszyfrowane == wejscie: True
CBC odszyfrowane == wejscie: True
```

### Wnioski:

W ECB każdy blok jest szyfrowany niezależnie tym samym kluczem, więc równe bloki jawne dają równe bloki kryptogramu, a w CBC każdy blok jest XOR-owany z poprzednim blokiem kryptogramu, więc te same bloki dają różne wyniki. Ostatnie 2 linijku wyniku pokazują, że kod zarówno dla EBC,jak i CBC działa poprawnie

## Zadanie 2:

### Wyniki:

```
puste: 0 B -> kryptogram 16 B, OK
16 B: 16 B -> kryptogram 32 B, OK
wiadomosc.txt: 247 B -> kryptogram 256 B, OK
Plik wiadomosc.enc odszyfrowany bez zmian, OK
rozna sol: True
rozne IV: True
rozne kryptogramy: True
```

3 pierwsze linijki to testy (szyfrownaie -> odszyfrowanie, porównanie bajtów i długości kryptogramu).
3 ostatnie linijki pokazują, że ponowne szyfrowanie z nową solą i IV (wcześniej to było: sól 16 B + IV 16 B + kryptogram 256 B) daje poprawny wynik

### Wnioski:

Sól zmienia klucz wyprowadzany przez PBKDF2 z tego samego hasła, a IV zmienia kryptogram CBC przy tym samym kluczu i tekście; obie wartości mogą być jawne i zapisane razem z kryptogramem, bo tajne jest tylko hasło, ale CBC nie zapewnia integralności, więc modyfikacja kryptogramu nie powinna zostać wykryta.

## Zadanie 3:

### Wyniki:

```
top 5:
m: 4.4536
b: 7.9472
x: 7.9490
o: 7.9493
2: 7.9502
klucz: m
pierwszy wiersz: Record 000. The archive contains laboratory notes about symmetric encryption and careful handling of binary files.
```

### Wnioski:

Jest 36 kluczy, bo mamy 26 liter alfabetu i 10 cyfr. Ranking może zawieść dla danych skompresowanych ze względu na entropię bliską 8 bitów/bajt, więc poprawny kandydat nie wyróżni się niskim H.