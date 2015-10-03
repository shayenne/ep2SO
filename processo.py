#!/usr/bin/env python
import time





class Processo:

    def __init__(self, t0, nome, b, lista):
        self.t0 = t0
        self.nome = nome
        self.b = b
        self.acesso = lista

    def alocaEspaco(self, espaco):
        print "Quero alocar o meu espaco de {} bytes!!!".format(espaco)

    def lePosicao(self, posicao):
        print "Sou o processo {}. Quero ver a posicao {}".format(self.nome, posicao)

    def iniciaContagem(self, inicio):
        espera = self.t0 - (time.time() - inicio)
        if espera > 0:
            time.sleep(espera)
        
        self.alocaEspaco(self.b)

        for entry in self.acesso:
            espera = entry[1] - (time.time() - inicio)
            if espera > 0:
                time.sleep(espera)
        
            self.lePosicao(entry[0])



def main():
    proc = Processo(2, "primeiro", 4,  [[1, 2],[3, 3], [4, 5], [6, 7], [10, 8]])
    ini = time.time()
    proc.iniciaContagem(ini)

if __name__ == "__main__":
    main()
