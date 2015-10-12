
subs = None

def defineSubstituidor(num):
    global subs
    subs = num

def substitui(mapa, lista):
    global subs

    if subs == "1":
        frame = NRU(mapa)
    elif subs == "2":
        frame = FIFO(lista)
    elif subs == "3":
        frame = SC(mapa, lista)
    elif subs == "4":
        frame = LRU(mapa)

    return frame

def NRU(mapa):
    while True:
        for proc in mapa:
            if proc[0] == 1:
                if proc[2] == 0:
                    return proc[1]
