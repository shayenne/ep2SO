#!/usr/bin/env python

import sys

# Recebe uma lista ligada e devolve a posição de memória em que o
# processo pode ocupar (caso exista) ou None (caso não exista)
def FirstFit(lista, processo):
    i = 0
    
    while (i < len(lista)):
        if lista[i][0] == "L" and lista[i][2] > processo:
            return lista[i][1]
        
    return None


def NextFit(lista, processo):
    i = 0
    
    while (i < len(lista)):
        if lista[i][0] == "L" and lista[i][2] > processo:
            yield lista[i][1]
        
    return None

# Este é o BestFit, não Quick :(
def BestFit(lista, processo):
    i = 0
    menor[0] = sys.maxint 
    while (i < len(lista)):
        if lista[i][0] == "L" and lista[i][2] > processo and lista[i][2] < menor[0]:
            menor[0] = lista[i][2]
            menor[1] = lista[i][1]

    if menor[0] != sys.maxint:
        return menor[1]
    
    return None
