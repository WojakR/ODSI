# ODSI - Laboratorium 4 (Funkcje skrótu)

Rozwiązania w czystym Pythonie 3 (tylko biblioteka standardowa: `hashlib`, `hmac`, `secrets`).

## Uruchomienie

```bash
python zad1.py        # sumy kontrolne SHA-256 + efekt lawinowy
python zad2.py        # weryfikacja haseł PBKDF2 + demonstracja soli
python zad3.py        # atak białych znaków (kolizja h24)
```

Wszystkie pliki czytane są binarnie (końce wierszy LF bez zmian).

## Zadania

- **zad1** — czyta `SHA256SUMS.txt`, dla każdego pliku wypisuje `OK` / `BLAD` / `BRAK`
  (brak pliku nie przerywa programu). Na końcu liczy różnicę bitów między
  SHA-256 z `"Ala ma kota."` i `"Ola ma kota."`.
- **zad2** — czyta `hasla.txt` (`login:iteracje:sól_hex:skrót_hex`), `weryfikuj(login, hasło)`
  liczy PBKDF2-HMAC-SHA256 z parametrami rekordu i porównuje w stałym czasie
  (`hmac.compare_digest`); nieznany login → fałsz. Sprawdza cztery przypadki oraz
  `dodaj()` — dwa konta z tym samym hasłem i różną solą.
- **zad3** — z `oryginal.txt` i `zmieniony.txt` (po 13 wierszy) generuje po 2^13 wariantów
  (spacja przed `\n` wiersza `i`, gdy bit `i` ustawiony). `h24` = pierwsze 3 bajty SHA-256.
  Znajduje parę (oryginał, zmieniony) o równym `h24` (kolizja) i liczy, ile wariantów
  zmienionego trafia w `h24` niezmienionego oryginału.
