
import matplotlib.pyplot as plt

zbior_a = []
zbior_b = []

with open("zbiory.txt") as f:
    for line in f:
        parts = line.split()

        if len(parts) == 2:
            zbior_a.append(int(parts[0]))
            zbior_b.append(float(parts[1]))


def srednia_zbioru(zbior):
    wynik = 0
    for i in zbior:
        wynik += i
    wynik = wynik/len(zbior)

    return wynik

def odchylenie_standardowe(zbior):
    wynik = 0
    for i in zbior:
        wynik += (i-srednia_zbioru(zbior))**2
    wynik = wynik/(len(zbior)-1)

    wynik = wynik**(0.5)

    return wynik

def suma(zbior):
    wynik = 0
    for i in zbior:
        wynik += i
    return wynik
def suma_kwadratow(zbior):
    wynik = 0
    for i in zbior:
        wynik += i**2
    return wynik

def korelacja_prearsona(zbior_a , zbior_b):
    wynik = 0
    if len(zbior_b) != len(zbior_a):
        return print("zbiory muszą być równe")
    n = len(zbior_a)
    a = 0
    for i in range(n):
        a += (zbior_a[i]*zbior_b[i])
    wynik += n*a

    a = suma(zbior_a) * suma(zbior_b)
    wynik -= a

    a = ((n * suma_kwadratow(zbior_a)-suma(zbior_a)**2) * (n * suma_kwadratow(zbior_b)-suma(zbior_b)**2))**0.5
    wynik = wynik / a
    return wynik


def oblicznie_linii(zbior_a, zbior_b):
    r = korelacja_prearsona(zbior_a, zbior_b)
    sx = odchylenie_standardowe(zbior_a)
    sy = odchylenie_standardowe(zbior_b)
    mx = srednia_zbioru(zbior_a)
    my = srednia_zbioru(zbior_b)
    b = r * (sy/sx)
    a = my - (b * mx)
    return a, b

def przewidywanie_wartosci(zbior_a, zior_b, x):
    a, b = oblicznie_linii(zbior_a, zior_b)
    wynik = a + (b*x)
    print("wynik =", wynik)
    return wynik


przewidywanie_wartosci(zbior_a,zbior_b, 6)
a, b = oblicznie_linii(zbior_a, zbior_b)
print("a= ", a,"b= ", b)

x = [i for i in range (0, zbior_a[-1]+1)]
y = [b*i + a for i in x]

plt.plot(x, y)
plt.scatter(zbior_a, zbior_b)

plt.show()

przewidywanie_wartosci(zbior_a, zbior_b, 6)
