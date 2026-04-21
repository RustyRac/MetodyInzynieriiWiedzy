from itertools import combinations

with open("tabela.txt") as f:
    tablica1 = [list(map(int, line.split())) for line in f]
decyzja1 = [wiersz.pop() for wiersz in tablica1]

def sledzenie_kombinacji(wiersz, numer_kombinacji, dlugosc_kombinacji):
    numery_arg = list(range(1,len(wiersz)+1))
    comb1 = list(combinations(numery_arg, dlugosc_kombinacji))
    comb2 = list(combinations(wiersz, dlugosc_kombinacji))
    wynik = ""
    for i in range(dlugosc_kombinacji):
        wynik += f"arg{comb1[numer_kombinacji][i]} = {comb2[numer_kombinacji][i]} "
    return wynik

def covering(tablica, decyzje):
    obiekty = tablica
    rozpatrzone = []
    potencjalnie_rozpatrzone = []
    for i in range (1, len(tablica[0])+1):
        if set(range(len(obiekty))).issubset(set(rozpatrzone)):
            break
        print('=====================================',i)
        for j in range (len(obiekty)):
            if j in rozpatrzone:
                continue

            support = 0
            d = decyzje[j]
            combCur = list(combinations(obiekty[j], i))

            for c in range (len(combCur)):
                for p in range(len(obiekty)):
                    combPoz = list(combinations(obiekty[p], i))
                    if combCur[c] == combPoz[c] and d == decyzje[p]:
                        support+=1
                        potencjalnie_rozpatrzone.append(p)
                    elif combPoz[c] != combCur[c]:
                        continue
                    else:
                        support = 0
                        potencjalnie_rozpatrzone = []
                        break
                if support != 0:
                    break
            if support == 1:
                print(f"Reguła: obiekt{j+1} {sledzenie_kombinacji(obiekty[j], c, i)} => (d= {d})")
                rozpatrzone.append(j)
                rozpatrzone.extend(potencjalnie_rozpatrzone)
            if support > 1:
                print(f"Reguła: obiekt{j+1} {sledzenie_kombinacji(obiekty[j], c, i)} => (d= {d}) [{support}]")
                rozpatrzone.append(j)
                rozpatrzone.extend(potencjalnie_rozpatrzone)
    return

covering(tablica1, decyzja1)