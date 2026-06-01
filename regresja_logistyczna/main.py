import math
import random

data = []

with open("australian 1.csv", "r") as file:
    for line in file:
        values = line.strip().split()
        row = [float(x) for x in values]
        data.append(row)


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

def sigmoid(x):
    return 1/(1+math.exp(-x))

#funkcje przetwarzające tablice ------------------------

def podzial_na_6(dane):
    random.shuffle(dane)
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

def oddzielenie_klasy(zbiory):
    atrybuty = []
    klasy = []
    for wiersz in zbiory:
        atrybuty.append(wiersz[:-1])  # pierwsze 14 kolumn
        klasy.append(int(wiersz[-1]))  # ostatnia kolumna

    return atrybuty, klasy


# obliczenia ------------------------

# średnie atrybutów
def srednie_atrybutow(zbior_tren):
    srednie = []
    trening_transponowany = transpozycja(zbior_tren)
    for x in trening_transponowany:
        srednie.append(srednia_zbioru(x))
    return srednie
# odchylenia standardowe
def odchylenia_atrybutow(zbior_tren):
    odchylenia = []
    srednie = srednie_atrybutow(zbior_tren)
    trening_transponowany = transpozycja(zbior_tren)
    for i in range(len(trening_transponowany)):
        suma = 0
        for x in trening_transponowany[i]:
            suma += (x - srednie[i])**2
        odchylenia.append(math.sqrt(suma/len(trening_transponowany[i])))

    return odchylenia
# funkcja robiąca krotke z średnią i odchyleniem
def statystyki(zbior_tren):
    srednie = srednie_atrybutow(zbior_tren)
    odchylenia = odchylenia_atrybutow(zbior_tren)
    statystyki = []
    for i in range(len(odchylenia)):
        statystyki.append((srednie[i], odchylenia[i]))
    return statystyki

# funkcja przeskalowująca wartości  ------------------------ [1]
def skalowanie(zbior, statystyki):
    przeskalowane = []
    for x in zbior:

        przeskal_ob = []
        for i in range(len(statystyki)):
            przeskal_ob.append((x[i] - statystyki[i][0])/statystyki[i][1])
        przeskalowane.append(przeskal_ob)

    return przeskalowane

#  nowy wektor z 14 wagami ------------------------- [2]
def nowy_wekor_wagi():
    wektor = []
    for x in range(14):
        wektor.append(0)
    return wektor

# pętla uczenia ------------------------------ [4]

def petla_uczenia(przeskalowane, trening_y, bias, wagi):
    ile_atrybutow = len(przeskalowane[0])
    ile_obiektow = len(trening_y)
    gradient = [0.0] * ile_atrybutow   # utworzenie biasu, learning rate, oraz deklaracja gradientu [3]
    gradient_b = 0.0
    alfa = 0.01

    for i in range (ile_obiektow):   # dla każdego obiektu
        x = przeskalowane[i]
        y_true = trening_y[i]
        z = bias
        for j in range(ile_atrybutow):         # (a)
            z += wagi[j] * x[j]

        y_pred = sigmoid(z)                    # (b)
        error = y_pred - y_true                # (c)

        for j in range(ile_atrybutow):
            gradient[j] += error * x[j]        # (d)

        gradient_b += error                    # (e)

    for j in range(ile_atrybutow):             # (f)
        gradient[j] /= ile_obiektow

    for j in range(ile_atrybutow):
        wagi[j] -= alfa * gradient[j]          # (g)

    bias -= alfa * gradient_b                  # (h)


# główna pętla w której podaje się ilość powtórzeń (100)

def glowna_petla_uczenia(ile_razy, trening_x, trening_y, bias, wagi):
    staty = statystyki(trening_x)
    przeskalowane = skalowanie(trening_x, staty)
    for i in range (ile_razy):
        petla_uczenia(przeskalowane, trening_y, bias, wagi)

    return bias, wagi

# predykowanie klasy [2]

def predykcje(bias, wagi, test_x):
    wynik = []
    for i in range(len(test_x)):        # liczenie z (a)
        z = bias
        for j in range(len(wagi)):
            z += wagi[j] * test_x[i][j]

        prawdopodobienstwo = sigmoid(z)   # prawdopodobieństwo (b)

        if prawdopodobienstwo >= 0.5:     # zamiana na klasę (c)
            wynik.append(1)
        else:
            wynik.append(0)
    return wynik

def kroswalidacjaregresja(folds):
    wynik = []
    real_wartosci = []

    for i in range(len(folds)):
        train = []
        test = folds[i]

        for j in range(len(folds)):
            if j != i:
                train.extend(folds[j])

        train_x, train_y = oddzielenie_klasy(train)
        staty = statystyki(train_x)
        test_x, test_y = oddzielenie_klasy(test)
        test_x = skalowanie(test_x, staty)     # skalowanie test
        real_wartosci.extend(test_y)

        bias, wagi = glowna_petla_uczenia(100, train_x, train_y, 0.0, nowy_wekor_wagi())
        wynik.extend(predykcje(bias, wagi, test_x))

    count = 0
    pomylki = {"TruePos": 0,
               "FalsePos": 0,
               "TrueNeg": 0,
               "FalseNeg": 0}
    for i in range(len(real_wartosci)):
        if wynik[i] == real_wartosci[i]:
            count += 1
        if wynik[i] == 1 and real_wartosci[i] == 1:
            pomylki["TruePos"] += 1
        elif wynik[i] == 0 and real_wartosci[i] == 0:
            pomylki["TrueNeg"] += 1
        elif wynik[i] == 1 and real_wartosci[i] == 0:
            pomylki["FalsePos"] += 1
        else:
            pomylki["FalseNeg"] += 1


    accuracy = count / len(real_wartosci)
    accuracy = accuracy * 100
    print(f"accuracy : {accuracy:.2f}%")
    print("                      Klasa rzeczywista")
    print(f"            ----------------------------")
    print("                    pozytywna | negatywna")
    print(f"            ----------------------------")
    print(f"   Klasa    | pozytywna | {pomylki["TruePos"]} | {pomylki["FalsePos"]}     |")
    print(f"predykowana | negatywna | {pomylki["FalseNeg"]}  | {pomylki["TrueNeg"]}    |")




zbiory = podzial_na_6(data)

kroswalidacjaregresja(zbiory)



