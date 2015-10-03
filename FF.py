#!/usr/bin/env python

import sys
import math

last = 0
# Recebe uma lista ligada e devolve a posicao de memoria em que o
# processo pode ocupar (caso exista) ou None (caso nao exista)
def FirstFit(lista, processo):
    i = 0
    
    while (i < len(lista)):
        if lista[i][0] == "L" and lista[i][2] > processo:
            i += 1
            return lista[i-1][1]
        i+=1
        
    return None


def NextFit(lista, processo):
    global last
    i = last
    
    for i in xrange(len(lista)):
        ind = (i+last)%len(lista)
        if lista[ind][0] == "L" and lista[ind][2] > processo:
            last = ind + 1
            return lista[ind][1]

        
    #return None

# Este e o BestFit, nao Quick :(
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


def QuickFit(lista, processo):
    pos = None
    # A lista possui tamanhos comuns
    # e extremos. Em 2, 3, 4, 5, 6 temos os tamanhos: 4k, 8k, 16k, 32k, 64k
    # Em 0, 1 temos tamanhos: menores que 4k, maiores que 64k e intermediarios
    # Em 7, temos nodes ocupados por processos
    if processo < 3:
        for l in lista[0]:
            if l[2] > processo:
                pos = l
                break
        #encontra na primeira lista
    
    elif processo > 64:
        #encontra na segunda lista
        for l in lista[1]:
            if l[2] > processo:
                pos = l
                break
    else:
        #aloca processo nesta posicao
        for l in lista[math.log(processo, 2)]:
            pos = l
            break


    if pos != None:
        l[0] = processo
        if l[2] - processo >= 1:
            encaixaSobra(lista, l[1]+processo, l[2] - processo)
        encaixaNovo(l[0], l[1], processo)
    else:
        return False            
