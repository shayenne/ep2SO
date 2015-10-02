import time

def alocaEspaco(tempo):
    print "Passaram {} segundos, quero alocar o meu espaco!!!".format(tempo)

def lePosicao(tempo, posicao):
    print "Passaram {} segundos, quero ver a posicao {}".format(tempo, posicao)

def iniciaContagem(inicio):
    t0 = 2
    espera = t0 - time.clock() - inicio
    time.sleep(espera)
    print "Esperei ", espera
    alocaEspaco(t0)
    a = [3, 4, 5, 6]
    for i in a:
        espera = i - time.clock() - inicio
        print time.clock() - inicio
        time.sleep(espera)
        print time.clock() - inicio
        print "Esperei ", espera, inicio, time.clock()
        lePosicao(i, 20)

def main():
    ini = time.clock()
    iniciaContagem(ini)

if __name__ == "__main__":
    main()
