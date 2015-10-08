#!/usr/bin/env python
import time
from gerenciador import gerente


class Processo:

    def __init__(self, t0, nome, tf, b, lista):
        self.pid = nome
        self.t0 = t0
        self.nome = nome
        self.tf = tf
        self.b = b
        self.acesso = lista


    # Funcao que pede para alocar o espaco em bytes do processo na memoria virtual
    def alocaEspaco(self, espaco):
        print "Sou o processo {}. Quero alocar o meu espaco de {} bytes!!!".format(self.nome, espaco)
        print ""
        gerente(espaco, self.pid)

    def lePosicao(self, posicao):
        # Chama a MMU, pedindo para ver a posicao + base
        #MMUacessaPosicao(posicao)
        print "Sou o processo {}. Quero ver a posicao {}".format(self.nome, posicao)

    # Funcao que sera executada por threads simulando um processo
    def iniciaContagem(self, inicio):
        espera = self.t0 - (time.time() - inicio)
        if espera > 0:
            time.sleep(espera)
        print time.time() - inicio
        self.alocaEspaco(self.b)

        for entry in self.acesso:
            espera = entry[1] - (time.time() - inicio)
            if espera > 0:
                time.sleep(espera)
            print time.time()-inicio
            self.lePosicao(entry[0])

        espera = self.tf - self.t0 -(time.time() - inicio)
        if espera > 0:
            time.sleep(espera)
        print "O processo {} acabou. :(".format(self.nome)

def main():
    proc = Processo(2, "primeiro", 4,  [[1, 2],[3, 3], [4, 5], [6, 7], [10, 8]])
    ini = time.time()
    proc.iniciaContagem(ini)

if __name__ == "__main__":
    main()
