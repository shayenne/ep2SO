#!/usr/bin/env python
import time
from gerenciador import gerente
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
        print "Sou o processo {}. Quero alocar o meu espaco de {} bytes!!!".format(self.nome, espaco)
        print ""
        gerente(espaco, self.pid)



    def lePosicao(self, posicao):
        # Chama a MMU, pedindo para ver a posicao
        print "Sou o processo {}. Quero ver a posicao {}".format(self.nome, posicao)
        MMUacessaPosicao(self.pid, posicao)




    # Funcao que sera executada por threads simulando um processo
    def iniciaContagem(self, inicio):
        # Espera chegar o seu tempo de inicio
        espera = self.t0 - (time.time() - inicio)
        if espera > 0:
            time.sleep(espera)
        
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
        espera = self.tf - self.t0 -(time.time() - inicio)
        if espera > 0:
            time.sleep(espera)
        # Avisa que terminou
        MMUterminaProcesso(self.pid)
        print "O processo {} acabou. :(".format(self.nome)

def main():
    proc = Processo(2, "primeiro", 4,  [[1, 2],[3, 3], [4, 5], [6, 7], [10, 8]])
    ini = time.time()
    proc.iniciaContagem(ini)

if __name__ == "__main__":
    main()
