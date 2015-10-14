import MMU as m
import time

subs = None

def defineSubstituidor(num):
    global subs
    subs = num
    m.initLock()

def substitui(lista):
    global subs

    if subs == "1":
        frame = NRU(lista)
    elif subs == "2":
        frame = FIFO(lista)
    elif subs == "3":
        frame = SC(lista)
    elif subs == "4":
        frame = LRU(lista)

    return frame

def NRU(lista):
    while True:
        proc = lista.head
        while proc is not None:
            if proc.data[2] == 0:
                return proc.data[1]
            proc = proc.next



def FIFO(lista):
    return lista.head.data[1]



def SC(lista):
    m.acquireLock()
    p = lista.head
    while p is not None:
        if p.data[2] == 1:
            p.data[2] = 0
            data = p.data
            lista.remove(data)
            lista.append(data)
        else:
            m.releaseLock()
            return p.data[1]
        p = p.next



def LRU(lista):
    p = lista.head
    menor = p.data[3]
    frame = p.data[1]
    while p is not None:
        if p.data[3] < menor:
            menor = p.data[3]
            frame = p.data[1]
        p = p.next

    return frame
