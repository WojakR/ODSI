"""Sejf sekretow i kalkulator - aplikacja do laboratorium 7 (po poprawkach).

Uruchamiaj wylacznie lokalnie, w kontenerze z pakietu. Dane sa fikcyjne.

Zad.1/2: zapytanie SQL z parametrem ? zamiast sklejania napisu, ogolny
komunikat bledu dla uzytkownika i szczegoly w logu serwera.
Zad.3: wlasny parser kalkulatora (liczba operator liczba) zamiast eval.
"""
import re
import sqlite3
import operator

from flask import Flask, render_template, request

app = Flask(__name__)
BAZA = "file:/dane/sekrety.db?mode=ro"

# Zad.3 - jawna lista dozwolonych dzialan (biala lista zamiast blokowania slow).
DZIALANIA = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}
# liczba (ujemna, dziesietna), operator, liczba; spacje wokol operatora dozwolone.
WZORZEC = re.compile(r"\s*(-?\d+(?:\.\d+)?)\s*([+\-*/])\s*(-?\d+(?:\.\d+)?)\s*")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sekret")
def sekret():
    klucz = request.args.get("klucz", "")
    # Zad.2 - staly tekst zapytania, wartosc przekazana osobno jako parametr.
    zapytanie = "SELECT wlasciciel, sekret FROM sekrety WHERE klucz = ?"
    wiersze, blad = [], None
    try:
        with sqlite3.connect(BAZA, uri=True) as db:
            wiersze = db.execute(zapytanie, (klucz,)).fetchall()
    except sqlite3.Error:
        # Szczegoly tylko do logu, uzytkownik dostaje ogolny komunikat.
        app.logger.exception("Blad zapytania sekret dla klucza %r", klucz)
        blad = "Wystapil blad zapytania."
    return render_template("sekret.html", klucz=klucz, zapytanie=zapytanie, wiersze=wiersze, blad=blad)


@app.route("/kalkulator")
def kalkulator():
    wyrazenie = request.args.get("wyrazenie")
    # Brak parametru -> tylko formularz (HTTP 200).
    if wyrazenie is None:
        return render_template("kalkulator.html", wyrazenie="", wynik=None, blad=None)

    if len(wyrazenie) > 100:
        return render_template("kalkulator.html", wyrazenie=wyrazenie[:100],
                               wynik=None, blad="Wejscie za dlugie (limit 100 znakow)."), 400

    dopasowanie = WZORZEC.fullmatch(wyrazenie)
    if not dopasowanie:
        return render_template("kalkulator.html", wyrazenie=wyrazenie,
                               wynik=None, blad="Nieprawidlowe wyrazenie."), 400

    lewa, znak, prawa = dopasowanie.groups()
    a, b = float(lewa), float(prawa)
    if znak == "/" and b == 0:
        return render_template("kalkulator.html", wyrazenie=wyrazenie,
                               wynik=None, blad="Dzielenie przez zero."), 400

    wynik = DZIALANIA[znak](a, b)
    # Calkowity wynik pokaz bez zbednego .0
    if wynik == int(wynik):
        wynik = int(wynik)
    return render_template("kalkulator.html", wyrazenie=wyrazenie, wynik=wynik, blad=None)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
