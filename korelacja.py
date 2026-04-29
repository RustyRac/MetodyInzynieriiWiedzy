zbior_a = [1,2,3,4,5]
zbior_b = [4,6,9,11,18]
print(len(zbior_b))

def srednia_zbioru(zbior):
    wynik = 0
    for i in zbior:
        wynik += i
    wynik = wynik/len(zbior)

    return wynik

def odchylenie_standardowe(zbior):
    if len(zbior) == 1:
        return print("zbiór musi być duższy niż 1")
    wynik = 0
    for i in zbior:
        wynik += (i-srednia_zbioru(zbior))**2
    wynik = wynik/(len(zbior)-1)

    wynik = wynik**(0.5)



    return wynik

print(odchylenie_standardowe(zbior_b))
