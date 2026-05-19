import math
import random

data = []

with open("iris.data", "r") as f:
    for line in f:
        row = line.strip().split(",")
        row[:-1] = [float(x) for x in row[:-1]]
        data.append(row)

random.shuffle(data)
#funkcje pomocnicze ---------------
def transpozycja(macierz):
    wynik = []

    for j in range(len(macierz[0])):
        new_row = []
        for i in range(len(macierz)):
            new_row.append(macierz[i][j])
        wynik.append(new_row)

    return wynik
def suma(zbior):
    wynik = 0
    for i in zbior:
        wynik += i
    return wynik

def srednia_zbioru(zbior):
    wynik = 0
    for i in zbior:
        wynik += i
    wynik = wynik/len(zbior)

    return wynik

#funkcje pomocnicze ---------------

#podział na data na pięć części---
def podzial_na_5(dane):
    czesci = []
    rozmiar = len(dane) // 5
    reszta = len(dane) % 5
    start = 0

    for i in range(5):
        end = start + rozmiar
        if i < reszta:
            end += 1
        czesci.append(dane[start:end])
        start = end

    return czesci

folds = podzial_na_5(data)
#------------------------
test = folds[0]
train = []
for i in range(1, 5):
    train.extend(folds[i])
#zamiana na słownik P(C)
def policzenie_klas(train):
    policzone = {}

    for row in train:
        label = row[-1]
        if label not in policzone:
            policzone[label] = 0

        policzone[label] += 1

    return policzone


def pc_calc(train):
    policzone = policzenie_klas(train)
    prob_klas = {}

    for label, count in policzone.items():
        prob_klas[label] = count / len(train)

    return prob_klas

print("PC: ",pc_calc(train))
#-------------------
#zamiana train na słownik
def wydzielenie_klas(train):
    wydzielone = {}
    for row in train:
        label = row[-1]
        if label not in wydzielone:
            wydzielone[label] = []
        wydzielone[label].append(row[:-1])
    return wydzielone

print("Wydzielenie klas ", wydzielenie_klas(train))
#------------
#wyliczenie średniej i wariancji słownik z tablicą krotek
def statystyki_atrybutow(train):
    klasy = wydzielenie_klas(train)
    statystyki = {}

    for label, rows in klasy.items():
        features = transpozycja([r for r in rows]) #transpozycja aby móc zsumować atrybuty
        statystyki[label] = []

        for col in features:
            srednia = srednia_zbioru(col)
            var = sum((x - srednia) ** 2 for x in col) / len(col)

            statystyki[label].append((srednia, var))

    return statystyki


print("Statystyki ", statystyki_atrybutow(train))

statystyki = statystyki_atrybutow(train)
#-----------
#2. słownik logarytmów P(C) dla każdej klasy
def log_train(train):
    pc = pc_calc(train)
    prob_log = {}

    for label in pc:
        prob_log[label] = math.log(pc[label])


    return prob_log

print("Logarytm PC ", log_train(train))
# PAIC funkcja licząca do sumy
def log_paic(x, srednia, wariancja):

    if wariancja == 0:
        wariancja = 1e-9

    wynik = (
        1 / math.sqrt(2 * math.pi * wariancja)
    ) * math.exp(
        -((x - srednia) ** 2) / (2 * wariancja)
    )

    return math.log(wynik)
#-------------------------bayes dla jednego folda
def naive_bayes(test, train):
    statystyki = statystyki_atrybutow(train)
    pc_log = log_train(train)
    wynik = []
    #pętla przez każdy obiekt []
    for obiekt in test:
        best_score = -math.inf
        best_label = ""

        #pętla dla każdego irisa
        for label in statystyki:
            score = pc_log[label]
            #pętla przechodząca przez argumenty i licząca scpre
            for i in range(len(obiekt)-1):
                srednia, wariancja = statystyki[label][i]
                score += log_paic(obiekt[i], srednia, wariancja)

            if score > best_score:
                best_score = score
                best_label = label

        wynik.append(best_label)

    return wynik

bayes = naive_bayes(test, train)

count = 0
for i in range(len(bayes)):
    if bayes[i] == test[i][-1]:
        count += 1
print(count)
print("wynik: ", naive_bayes(test, train))

#------------- pętla przechodząca przez każdy z foldów jako testowy
def kroswalidacjaibayes(folds):
    predykcje = []
    przetestowane = []

    for i in range(len(folds)):
        test = folds[i]
        train = []
        for j in range(len(folds)):
            if j != i:
                train.extend(folds[j])
        bayes = naive_bayes(test, train)
        predykcje.extend(bayes)
        przetestowane.extend(test)

    count = 0
    for i in range(len(predykcje)):
        if predykcje[i] == przetestowane[i][-1]:
            count += 1
    print(count,"/",len(predykcje))
    print("accuracy: ", count / len(predykcje))

    return count / len(predykcje)

kroswalidacjaibayes(folds)
