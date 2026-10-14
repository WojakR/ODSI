# Lab 2 – Kryptografia historyczna
Wojciech Regulski, 337612

## Zadanie 1 – Cezar

Top 5 (udział bajtów 32–126, 9, 10, 13):

1 k = 230 ocena = 1.0 (`Wkh#Qljkw#Ihuu...`)
2 k = 233 ocena = 1.0 (`The Night Ferry\n\nThe night ferry...`)
3 k = 228 ocena = 0.994753
4 k = 229 ocena = 0.994753
5 k = 231 ocena = 0.994753

Wybrane przesunięcie: k = 233, bo tylko ono daje sensowny angielski tekst. k = 230 ma taką samą ocenę, bo przesuwa tekst o 3, a te znaki też są drukowalne.

Entropia nie pomoże: przesunięcie tylko zamienia wartości bajtów miejscami, więc histogram ma te same liczności dla każdego k i entropia jest zawsze taka sama.

## Zadanie 2 - Vigenere

Wyniki:

SZYFR 95ac9a9393 95ac9a9393 95ac9a9393
KOD 8da1859890 869d90918c 91968c9c85

Testy: odszyfrowanie vigenere.bin zgodne z tekst_pl.txt – True; puste dane – True; bajty 0 i 255 – True, Znany wynik BA/KO - True, Zawijanie szyfr. 255+2 - True, Zawijanie odszyfr. 1-2 - True

BRAMA powtarza się co 5 bajtów. Klucz SZYFR ma długość 5, więc każde BRAMA jest szyfrowane tymi samymi literami klucza i fragmenty kryptogramu są identyczne. Klucz KOD ma długość 3, więc każde BRAMA trafia na inny fragment klucza (KODKO, DKODK, ODKOD). Atakujący w pierwszym przypadku widzi powtórzenie i może z niego zgadnąć długość klucza.

## Zadanie 3 – RC4

Test `rc4(rc4(x)) == x` – True. Liczba prób: 17576, czas: 3.7 s.

Wyniki:

tat 4.391
neg 7.4304
mcn 7.4512
oxo 7.4536
tnx 7.4592

Klucz: tat. Tekst jest sensowny („The Clockmaker's Apprentice...”), ponowne szyfrowanie zgodne z kryptogramem – True.
Entropia kryptogramu: 7.9271, entropia odszyfrowania: 4.3259.

RC4 to XOR ze strumieniem klucza, więc odszyfrowanie i ponowne zaszyfrowanie dowolnym kluczem zawsze odtworzy kryptogram – ten test nie sprawdza, czy klucz jest dobry. Ranking entropii mógłby zawieść, gdyby tekst jawny sam miał wysoką entropię (np. dane skompresowane) albo gdyby próbka była za krótka.

## Wnioski

**Co uważasz?** Uważam, że żaden z tych trzech szyfrów nie jest dzisiaj bezpieczny. Cezara da się złamać w ułamku sekundy, bo ma tylko 256 kluczy. Vigenère ukrywa pojedyncze litery, ale zdradza powtórzenia, jeśli tekst powtarza się w odstępie będącym wielokrotnością długości klucza. RC4 jako algorytm jest szybki i prosty, ale ma znane słabości, a z krótkim kluczem pada w kilka sekund, co sam sprawdziłem. Zaciekawiło mnie to, że automatyczne kryteria (udział drukowalnych znaków, entropia) tylko zawężają listę kandydatów, a ostatecznie i tak trzeba sprawdzić, czy tekst ma sens, co pokazał remis k = 230 i k = 233 w Cezarze. Innymi słowy, o bezpieczeństwie decyduje nie tylko algorytm, ale też długość klucza i to, czy się go nie powtarza.

**Dlaczego RC4 nie jest już używany.** Pierwsze bajty strumienia RC4 nie są losowe, więc da się z nich wyciągać informacje o tekście. Słaby algorytm KSA sprawia, że przy kluczach różniących się niewiele da się odzyskać klucz. Użycie dwa razy tego samego klucza daje ten sam strumień, a wtedy XOR dwóch kryptogramów to XOR dwóch tekstów jawnych. RC4 nie chroni też integralności, ponieważ zmiana bitu w kryptogramie zmienia ten sam bit w tekście. W tym zadaniu dodatkowo klucz miał tylko 17576 możliwości, więc przeszukanie wszystkich trwało kilka sekund.

**Jak rozpoznać poprawnie odszyfrowany tekst.** Kilkoma kryteriami naraz np. udział znaków drukowalnych, częstość liter mniej więcej zgodna z językiem (w angielskim dużo e, t, a i spacji), obecność jakiegoś pożądanego słowa, poprawne kodowanie i na końcu ręczne sprawdzenie, czy tekst ma sens. Samo jedno kryterium może dać remis, jak k = 230 i 233 w zad. 1.

**Dlaczego entropia nie wystarcza.** Entropia patrzy tylko na to, ile razy występują wartości, a nie na to, które to wartości. Np w Cezarze jest identyczna dla każdego k, bo częstotliwość symboli pozostaje taka sama. Nie odróżni sensownego tekstu od bełkotu o podobnym rozkładzie, zawiedzie przy krótkich próbkach i przy danych, które same mają wysoką entropię (np. skompresowane). W RC4 zadziałała, bo zły klucz daje prawie losowe bajty. Wynik i tak trzeba potwierdzić sensownością tekstu.