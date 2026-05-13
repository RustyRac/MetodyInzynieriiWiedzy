import csv
import random

dane = []

with open('australian.csv', newline='', encoding="utf-8") as plik:
    for linia in plik:
        wartosci = list(map(float, linia.strip().split()))
        dane.append(wartosci)

print(dane[0])

random.shuffle(dane)
print(dane[0])


def podzial_na_6(dane):
    czesci = []
    rozmiar = len(dane) // 6
    reszta = len(dane) % 6
    start = 0
    end = 0

    for i in range(6):
        end = start + rozmiar
        end += reszta
        czesci.append(dane[start:end])
        start += rozmiar

    return czesci


czesci = podzial_na_6(dane)
print(podzial_na_6(dane))

for i in czesci:
    print(len(i))
