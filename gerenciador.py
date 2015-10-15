#!/usr/bin/env python

import sys
import math
import threading
from Lista import *
from MMU import *
#import MMU as m
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
    quick = [[] for i in range(5)]
    initLock()
    

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
            
            print "Devolvi no quick ", inicio
    #finally:
    #    lock.release()
    # Ate aqui, o processo pediu um espaco em paginas para algum gerenciador
    # Em 'inicio' esta a posicao inicial do espaco que sera alocado para este processo     
       
    # Passar esta 'inicio' e 'paginas' para a MMU
    # Escreve na memoria virtual todas as posicoes alocadas para o processo o seu pid
        print "TUDO QUE USO", inicio, tam, paginas
        escreveMemoria(vir, inicio*tam, (inicio+paginas)*tam, pid)
        MMUalocaEspaco(pid, inicio, paginas)
    finally:
        lock.release()
        
    


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
    lista.show("Lista que passou pelo FirstFit")
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
    global quick
    # Guarda os ponteiros para lugares vazios
    # de 16, 32, 64, 128 e 256 bytes
    p = lista.head
    while p is not None:
        if p.data[0] == "L":
            for i in xrange(5):
                if p.data[2] == math.pow(2, i):
                    print "Inseri ", p.data, "no quick ",i 
                    quick[i].append(p)
                    break
        p = p.next
    
    lstvirtual.show("Organizei com o Quick")
    pos = None

    if quick[0] != [] and processo == 1:
        for i in quick[0]:
            print "q0: ", i.data,
        print ""

        #encontra na primeira lista
        pos = quick[0].pop(0)
        #x = int(pos.data[1])
        #print "Q1Essa ea a posicao ", pos.data[1], x
        pos.data[0] = pid
        return pos.data[1]
    
    elif quick[1] != [] and processo <= 2:
        if processo != 2:
            pos = quick[1].pop(0)
            pos.data[2] = 1
            lista.insert(["L", pos.data[1]+1, 1], pos)
            return QuickFit(lista, pid, processo)
        else:
            pos = quick[1].pop(0)
            pos.data[0] = pid
            return pos.data[1]
            
    elif quick[2] != [] and processo <= 4:
        if processo != 4:
            if processo <= 4/2:
                pos = quick[2].pop(0)
                # Metade do valor anterior
                pos.data[2] = 2
                lista.insert(["L", pos.data[1]+2, 2], pos)
                lista.show("VIRTUAL QUICK")
                return QuickFit(lista, pid, processo)
            else:
                menor = quick[2][0].data[1]
                for p in quick[2]:
                    if p.data[1] < menor:
                        menor = p.data[1]
                        rem = p

                pos = quick[2].pop(quick[2].index(p))
                lista.show("VIRTUAL QUICK")
                return FirstFit(lista, pid, processo)
            
        else:
            pos = quick[2].pop(0)
            pos.data[0] = pid
            return pos.data[1]
        
    elif quick[3] != [] and processo <= 8:
        if processo != 8:
            if processo <= 8/2:
                pos = quick[3].pop(0)
                # Metade do valor anterior
                pos.data[2] = 4
                lista.insert(["L", pos.data[1]+4, 4], pos)
                lista.show("VIRTUAL QUICK")
                return QuickFit(lista, pid, processo)
            else:
                menor = quick[3][0].data[1]
                for p in quick[3]:
                    if p.data[1] < menor:
                        menor = p.data[1]
                        rem = p

                pos = quick[3].pop(quick[3].index(p))
                lista.show("VIRTUAL QUICK")
                return FirstFit(lista, pid, processo)
            
        else:
            pos = quick[3].pop(0)
            pos.data[0] = pid
            return pos.data[1]
        
    elif quick[4] != [] and processo <= 16:
        print ""
    else:
        return FirstFit(lista, pid, processo)
        

        

# Remove o processo pid da memoria virtual
def GERremoveProcesso(pid):
    lock1 = threading.RLock()
    lstvirtual.show("Antes de remover")
    acquireLock()
    try:
        if ger != "3":
            curr = lstvirtual.head
            while curr is not None:
                if curr.data[0] == pid:
                    liberaEspaco(lstvirtual, curr)
                    break
                curr = curr.next

            lstvirtual.show("Lista Virtual apos remocao do processo")
            print "-- Removi o processo de pid ", pid
        else:
            print "Ainda nao fizemos o QuickFit :("
    finally:
        lstvirtual.show("Depois de remover")
        releaseLock()


# Recebe uma lista ligada e o no que deve remover, faz a compressao de acordo 
# com os espacos livres adjacentes
def liberaEspaco(lst, node):
    if node.prev is not None and node.prev.data[0] == "L" and node.next is not None and node.next.data[0] == "L":
        local = node.prev
        new = ["L", node.prev.data[1], node.next.data[2]+node.data[2]+node.prev.data[2]]
        lst.remove(node.next.data)
        lst.remove(node.data)
        local.data = new
        
    
    elif node.prev is not None and node.prev.data[0] == "L":
        local = node.prev
        new = ["L", node.prev.data[1], node.data[2]+node.prev.data[2]]
        lst.remove(node.data)
        local.data = new
        
        
        
    elif node.next is not None and node.next.data[0] == "L":
        local = node
        new = ["L", node.data[1], node.next.data[2]+node.data[2]]
        lst.remove(node.next.data)
        local.data = new
        print "REALMENTE ENTREI AQUI"

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
