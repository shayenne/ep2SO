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
quick = None
#

# Inicializa a lista ligada da memoria virtual
def criaListaVirtual(t):
    global lstvirtual, last, tam, quick
    lstvirtual = List()
    lstvirtual.append(["L", 0, int(t/tam)])
    last = lstvirtual.head
    # QuickFit
    quick = [[]*5]
    

# Define globalmente o gerenciador, o tamanho de pagina e o 
# tamanho da memoria virtual
def defineGerenciador(num, t, virtual):
    global ger, vir, tam
    vir = virtual
    ger = num
    tam = t


# Imprime o estado da memoria virtual
def GERimprimeVirtual():
    lstvirtual.show("Status da Memoria Virtual")


# Atribui um espaco para um processo que chega, de acordo com 
# o algoritmo escolhido
def gerente(espaco, pid):
    global lstvirtual, tam, vir

    lock = threading.Lock()

    lock.acquire()
    try:
        inicio = None
        paginas = int(espaco / tam)
        if espaco % tam != 0:
            paginas += 1 
        if ger == "1":
            inicio = FirstFit(lstvirtual, pid, paginas)
            print "O processo de pid ", pid," ganhou ", paginas, "paginas e inicia em ", inicio
        elif ger == "2":
            inicio = NextFit(lstvirtual, pid, paginas)
        elif ger == "3":
            inicio = QuickFit(lstvirtual, pid, paginas)
    finally:
        lock.release()
    # Ate aqui, o processo pediu um espaco em paginas para algum gerenciador
    # Em 'inicio' esta a posicao inicial do espaco que sera alocado para este processo     
       
    # Passar esta 'inicio' e 'paginas' para a MMU
    # Escreve na memoria virtual todas as posicoes alocadas para o processo o seu pid
    escreveMemoria(vir, inicio*tam, (inicio+paginas)*tam, pid)
    MMUalocaEspaco(pid, inicio, paginas)
    
        
    


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

# Recebe uma lista ligada, o pid do processo e o tamanho que o processo
# quer ocupar em paginas
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
    

# Recebe uma lista ligada, o pid do processo e o tamanho que o processo
# quer ocupar em paginas, guarda os ponteiros de onde estao diferentes tamanhos
# de espacos livres
def QuickFit(lista, pid, processo):
    # Guarda os ponteiros para lugares vazios
    # de 16, 32, 64, 96 e 128 bytes
    global quick

    pos = None

    if quick[0] != [] and processo <= 1:
        #encontra na primeira lista
        print ""
    elif quick[1] != [] and processo <= 2:
        #encontra na segunda lista
        print ""
    elif quick[2] != [] and processo <= 4:
        print ""
    elif quick[3] != [] and processo <= 6:
        print ""
    elif quick[4] != [] and processo <= 8:
        print ""
    else:
        return FirstFit(lista, pid, processo)
        

        

# Remove o processo pid da memoria virtual
def GERremoveProcesso(pid):
    if ger != "3":
        curr = lstvirtual.head
        while curr is not None:
            if curr.data[0] == pid:
                liberaEspaco(lstvirtual, curr)
                break
        lstvirtual.show("Lista Virtual apos remocao do processo")
        print "-- Removi o processo de pid ", pid
    else:
        print "Ainda nao fizemos o QuickFit :("



# Recebe uma lista ligada e o no que deve remover, faz a compressao de acordo 
# com os espacos livres adjacentes
def liberaEspaco(lst, node):
    if node.prev is not None and node.prev.data[0] == "L" and node.next is not None and node.next.data[0] == "L":
        local = node.prev.prev
        new = ["L", node.prev.data[1], node.next.data[2]+node.data[2]+node.prev.data[2]]
        lst.remove(node.prev.data)
        lst.remove(node.data)
        lst.remove(node.next.data)
        lst.insert(new, local)
        
    
    elif node.prev is not None and node.prev.data[0] == "L":
        local = node.prev.prev
        new = ["L", node.prev.data[1], node.data[2]+node.prev.data[2]]
        lst.remove(node.prev.data)
        lst.remove(node.data)
        lst.insert(new, local)
        
        
    elif node.next is not None and node.next.data[0] == "L":
        local = node.prev
        new = ["L", node.data[1], node.next.data[2]+node.data[2]]
        lst.remove(node.data)
        lst.remove(node.next.data)
        lst.insert(new, local)
        

    else:
        node.data[0] = "L"
        
    



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
