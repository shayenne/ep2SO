#!/usr/bin/env python

import readline

if __name__ == "__main__":
    prompt = raw_input("[ep2]: ").split()
    
    while prompt[0] != "sai":
        
        if prompt[0] == "carrega":
            try:
                print "Tenho que carregar o arquivo {}.".format(prompt[1])
                arquivo = open(prompt[1], 'r')
                print arquivo.readline()
                arquivo.close()
            except IOError:
                print "Arquivo inexistente"
            except IndexError:
                print "Digite o caminho do arquivo"
            
        if prompt[0] == "espaco":
            print "O numero do gerenciador eh {}.".format(prompt[1])
            
        if prompt[0] == "substitui":
            print "O numero do substituidor eh {}.".format(prompt[1])
                    
        if prompt[0] == "executa":
            print "Vou imprimir resultados de {} em {} segundos.".format(prompt[1], prompt[1])
        
        prompt = raw_input("[ep2]: ").split()
