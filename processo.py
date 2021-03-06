#!/usr/bin/env python
import time
from gerenciador import gerente, GERremoveProcesso
from MMU import MMUacessaPosicao, MMUterminaProcesso

class Processo:

    def __init__(self, t0, nome, tf, b, lista):
        self.pid = None
        self.t0 = t0
        self.nome = nome
        self.tf = tf
        self.b = b
        self.acesso = lista


    # Funcao que pede para alocar o espaco em bytes do processo na memoria virtual
    def alocaEspaco(self, espaco):
        gerente(espaco, self.pid)



    def lePosicao(self, posicao):
        # Chama a MMU, pedindo para ver a posicao
        MMUacessaPosicao(self.pid, posicao)




    # Funcao que sera executada por threads simulando um processo
    def iniciaContagem(self, inicio):
        # Espera chegar o seu tempo de inicio
        espera = self.t0 - (time.time() - inicio)
        if espera > 0:
            time.sleep(espera)
        #print "O processo quer alocar ", self.pid
        # Pede para ser carregado na memoria
        self.alocaEspaco(self.b)

        # Para cada posicao a ser acessada, espera seu tempo
        for entry in self.acesso:
            espera = entry[1] - (time.time() - inicio)
            if espera > 0:
                time.sleep(espera)
            # Pede para acessar a posicao
            self.lePosicao(entry[0])

        # Espera chegar o seu fim
        espera = (self.tf) - (time.time() - inicio)
        if espera > 0:
            time.sleep(espera)

        #print "O processo terminou ", self.pid
        # Avisa que terminou
        GERremoveProcesso(self.pid)
        MMUterminaProcesso(self.pid)


def main():
    proc = Processo(2, "primeiro", 4,  [[1, 2],[3, 3], [4, 5], [6, 7], [10, 8]])
    ini = time.time()
    proc.iniciaContagem(ini)

if __name__ == "__main__":
    main()
