import os
import platform
import msvcrt as ms

from translation import translation

def ClearScreen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def Wait(language):
    print(translation[language]["PRESS_ANY_KEY_TO_CONTINUE"])
    ms.getch()

def NextChampion(champ1, champ2):
    nameChamp1 = []
    nameChamp2 = []
    for c in champ1: # pivot
        if c != ' ':
            nameChamp1.append(ord(c))
    for c in champ2: # first
        if c != ' ':
            nameChamp2.append(ord(c))

    if len(champ1) > len(champ2):
        for i in range(len(champ1) - len(champ2)):
            nameChamp2.append(-1)
    if len(champ2) > len(champ1):
        for i in range(len(champ2) - len(champ1)):
            nameChamp1.append(-1)
            
    for i in range(len(nameChamp1)):
        if nameChamp1[i] == nameChamp2[i]:
            continue
        elif nameChamp1[i] < nameChamp2[i]:
            return champ1
        else:
            return champ2
    return False

def Sort(champList):
    newChampList = []
    while champList[:-1]:
        first = champList[0]
        for a in champList[1:]:
            first = NextChampion(first, a)
        newChampList.append(first)
        champList.pop(champList.index(first))
    return newChampList