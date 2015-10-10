#!/usr/bin/env python

import sys
import math
from Lista import *
from MMU import *

# Variaveis globais
ger = None
lstvirtual = None
tam = None
last = None
vir = None
#


def criaListaVirtual(t):
    global lstvirtual, last, tam
    lstvirtual = List()
    lstvirtual.append(["L", 0, int(t/tam)])
    last = lstvirtual.head
    

def defineGerenciador(num, t, virtual ):
    global ger, vir, tam
    vir = virtual
    ger = num
    tam = t
    

def gerente(espaco, pid):
    global lstvirtual, tam, vir

    print 'ESTOU AQUI',  tam, espaco, ger
    inicio = None
    paginas = int(espaco / tam)
    if espaco % tam != 0:
        paginas += 1 
    if ger == "1":
        inicio = FirstFit(lstvirtual, pid, paginas)
        print pid, paginas
    elif ger == "2":
        inicio = NextFit(lstvirtual, pid, paginas)
    elif ger == "3":
        inicio = QuickFit(lstvirtual, pid, paginas)
    print inicio, paginas
    # Ate aqui, o processo pediu um espaco em paginas para algum gerenciador
    # Em 'inicio' esta a posicao inicial do espaco que sera alocado para este processo     
       
    # Passar esta 'inicio' e 'paginas' para a MMU
    escreveMemoria(vir, inicio*tam, (inicio+paginas)*tam, pid)
    MMUalocaEspaco(pid, inicio, paginas)
    return 


# Recebe uma lista ligada, o pid do processo e o tamanho que o processo
# quer ocupar em paginas
def FirstFit(lista, pid, processo):
    atual = lista.head
    while atual is not None:
        if atual.data[0] == "L" and atual.data[2] >= processo:
            pos = atual.data[1]

            atual.data[0] = pid
            if processo < atual.data[2]:
                dif = atual.data[2] - processo
                atual.data[2] = processo
                lista.insert(["L", atual.data[1]+processo, dif], atual)

            break
        atual = atual.next
    # APAGAR
    lista.show("Virtual")
    #
    if atual is not None:
        return atual.data[1]

    return None

def NextFit(lista, pid, processo):
    global last
    old = last
    atual = last
    while atual is not None:
        if atual.data[0] == "L" and atual.data[2] >= processo:
            pos = atual.data[1]

            atual.data[0] = pid
            if processo < atual.data[2]:
                dif = atual.data[2] - processo
                atual.data[2] = processo
                lista.insert(["L", atual.data[1]+processo, dif], atual)
                last = atual.next
            break
        if atual.next == None:
            atual = lista.head

        if atual.next == old:
            atual = None
            break
        
        atual = atual.next
    # APAGAR
    lista.show("Virtual")
    #
    if atual is not None:
        return atual.data[1]

    return None
    

        


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


if __name__ == "__main__":
    lista = List()

    lista.append(["L", 0, 2])
    lista.append(["P", 2, 12])
    lista.append(["L", 14, 5])
    lista.append(["L", 19, 10])
    lista.show("Fisica")
    FirstFit(lista, 10, 3)
    lista.show("Virtual")
    FirstFit(lista, 20, 10)
    lista.show("Virtual")
