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
comparacoes = None
#

def imprimeComparacoes():
    global comparacoes
    print "O numero de comparacoes foi ", comparacoes

# Inicializa a lista ligada da memoria virtual
def criaListaVirtual(t):
    global lstvirtual, last, tam, quick, comparacoes
    lstvirtual = List()
    lstvirtual.append(["L", 0, int(t/tam)])
    last = lstvirtual.head
    # QuickFit
    quick = [[] for i in range(5)]
    initLock()
    comparacoes = 0

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

        elif ger == "2":
            inicio = NextFit(lstvirtual, pid, paginas)

        elif ger == "3":
            inicio = QuickFit(lstvirtual, pid, paginas)
            

        escreveMemoria(vir, inicio*tam, (inicio+paginas)*tam, pid)
        MMUalocaEspaco(pid, inicio, paginas)
    finally:
        lock.release()
        
    


# Recebe uma lista ligada, o pid do processo e o tamanho que o processo
# quer ocupar em paginas
def FirstFit(lista, pid, processo):
    # TESTE#
    global comparacoes
    atual = lista.head
    while atual is not None:
        comparacoes += 1
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
    #lista.show("Lista que passou pelo FirstFit")
    #
    if atual is not None:
        return atual.data[1]

    return None

# Recebe uma lista ligada, o pid do processo e o tamanho que o processo
# quer ocupar em paginas
def NextFit(lista, pid, processo):
    global last, comparacoes #TESTES#

    old = last
    atual = last
    while atual is not None:
        comparacoes += 1
        if atual.data[0] == "L" and atual.data[2] >= processo:
            pos = atual.data[1]

            atual.data[0] = pid
            if processo < atual.data[2]:
                dif = atual.data[2] - processo
                atual.data[2] = processo
                lista.insert(["L", atual.data[1]+processo, dif], atual)
                last = atual
            break
        if atual.next == None:
            atual = lista.head

        if atual.next == old:
            atual = None
            break
        
        atual = atual.next
    # APAGAR
    #lista.show("Virtual")
    #
    if atual is not None:
        return atual.data[1]

    return None
    

# Recebe uma lista ligada, o pid do processo e o tamanho que o processo
# quer ocupar em paginas, guarda os ponteiros de onde estao diferentes tamanhos
# de espacos livres
def QuickFit(lista, pid, processo):
    global quick, comparacoes
    # Guarda os ponteiros para lugares vazios
    # de 16, 32, 64, 128 e 256 bytes

    #####################################################
    # Reorganizacao da lista apos remocao de processo
    paginas = 0
    if processo == 0:
        
        p = lista.head
        while p is None:
            # Qual e o node que contem o novo espaco livre
            if p.data[1] == pid:
                paginas = p.data[2]
                break
            p = p.next
            
        # Olha para todas as listas do quick, remove o que estiver no intervalo
        for q in quick:
            i = 0
            while i < len(q):
                if q[i].data[1] in xrange(pid, pid+paginas):
                    q.remove(q[i])
                i += 1
                    
        if paginas in [1, 2, 4, 8, 16]:
            quick[paginas].append(p)
        return
    #####################################################

    p = lista.head
    while p is not None:
        if p.data[0] == "L":
            for i in xrange(5):
                if p.data[2] == math.pow(2, i):
                    if p not in quick[i]:
                        quick[i].append(p)
                    break
        p = p.next
    
    
    pos = None
    
    if quick[0] != [] and processo == 1:
        comparacoes += 1
        for i in quick[0]:
            print "q0: ", i.data,
        print ""

        #encontra na primeira lista
        pos = quick[0].pop(0)
        pos.data[0] = pid
        return pos.data[1]
    
    elif quick[1] != [] and processo <= 2:
        comparacoes += 1
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
        comparacoes += 1
        if processo != 4:
            if processo <= 4/2:
                pos = quick[2].pop(0)
                # Metade do valor anterior
                pos.data[2] = 2
                lista.insert(["L", pos.data[1]+2, 2], pos)
        
                return QuickFit(lista, pid, processo)
            else:
                uso = 4 - processo
                
                p = quick[2].pop()
                p.data[0] = pid
                p.data[2] = processo

                new = ["L", p.data[1]+processo, uso]

                lista.insert(new, p)
        
                return p.data[1]
          
        else:
            pos = quick[2].pop(0)
            pos.data[0] = pid
            return pos.data[1]
        

    elif quick[3] != [] and processo <= 8:
        comparacoes += 1
        if processo != 8:
            if processo <= 8/2:
                pos = quick[3].pop(0)
                # Metade do valor anterior
                pos.data[2] = 4
                lista.insert(["L", pos.data[1]+4, 4], pos)
        
                return QuickFit(lista, pid, processo)
            else:
                uso = 8 - processo
                
                p = quick[3].pop()
                p.data[0] = pid
                p.data[2] = processo

                new = ["L", p.data[1]+processo, uso]

                lista.insert(new, p)
        
                return p.data[1]
                            
        else:
            pos = quick[3].pop(0)
            pos.data[0] = pid
            return pos.data[1]
        
    elif quick[4] != [] and processo <= 16:
        comparacoes += 1
        if processo != 16:
            if processo <= 16/2:
                pos = quick[4].pop(0)
                # Metade do valor anterior
                pos.data[2] = 8
                lista.insert(["L", pos.data[1]+8, 8], pos)
        
                return QuickFit(lista, pid, processo)
            else:
                uso = 16 - processo
                
                p = quick[4].pop()
                p.data[0] = pid
                p.data[2] = processo
                new = ["L", p.data[1]+processo, uso]
                lista.insert(new, p)
        
                return p.data[1]
                
        else:
            pos = quick[4].pop(0)
            pos.data[0] = pid
            return pos.data[1]

    else:
        search = FirstFit(lista, pid, processo)
        if search is None:
            # Junta espacos que sao vizinhos
            p = lista.head
            while p is not None:
                if p.data[0] == "L" and p.next is not None and p.next.data[0] == "L":
                    if p.data[2] in [1, 2, 4, 8, 16]:
                        quick[p.data[2]].remove(p)
                    if p.next.data[2] in [1, 2, 4, 8, 16]:
                        quick[p.next.data[2]].remove(p.next)

                    soma = p.data[2] + p.next.data[2]
                    p.data[2] = soma
                    lista.remove(p.next.data)
                else:
                    p = p.next

            return FirstFit(lista, pid, processo)

        else:
            return search

        

# Remove o processo pid da memoria virtual
def GERremoveProcesso(pid):
    global lstvirtual
    lock1 = threading.Lock()

    acquireLock()
    try:
        remove = False
        curr = lstvirtual.head
        while curr is not None:
            if curr.data[0] == pid:
                base = liberaEspaco(lstvirtual, curr)
                break
            curr = curr.next
 

        if ger == "3":
            # Organiza os espacos que foram agrupados
            QuickFit(lstvirtual, base, 0)
            
    finally:
        releaseLock()


# Recebe uma lista ligada e o no que deve remover, faz a compressao de acordo 
# com os espacos livres adjacentes
def liberaEspaco(lst, node):
    global last
    if node.prev is not None and node.prev.data[0] == "L" and node.next is not None and node.next.data[0] == "L":
        local = node.prev
        new = ["L", node.prev.data[1], node.next.data[2]+node.data[2]+node.prev.data[2]]
        if last == node or last == node.next:
            last = node.prev
        lst.remove(node.next.data)
        lst.remove(node.data)
        local.data = new
        return new[1]
        

    
    elif node.prev is not None and node.prev.data[0] == "L":
        local = node.prev
        new = ["L", node.prev.data[1], node.data[2]+node.prev.data[2]]
        if last == node:
            last = node.prev
        lst.remove(node.data)
        local.data = new
        return new[1]
        
        
        
    elif node.next is not None and node.next.data[0] == "L":
        local = node
        new = ["L", node.data[1], node.next.data[2]+node.data[2]]
        if last == node.next:
            last = node
        lst.remove(node.next.data)
        local.data = new
        return new[1]


    else:
        node.data[0] = "L"
        return node.data[1]
    



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
