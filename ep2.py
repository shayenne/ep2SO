#!/usr/bin/env python

import readline
import funcoes as f
import struct
from arquivos import *

if __name__ == "__main__":
    prompt = raw_input("[ep2]: ").split()
    mem = 'ep2.mem'
    vir = 'ep2.vir'
    
    while prompt[0] != "sai":
        
        if prompt[0] == "carrega":
            try:
                print "Tenho que carregar o arquivo {}.".format(prompt[1])
                arquivo = open(prompt[1], 'r')
                total, virtual = map(int, arquivo.readline().split())
                
                # Inicializa os arquivos de memoria total e virtual
                makeEmptyBin(mem, total)
                makeEmptyBin(vir, virtual)

                # Acessa uma posicao especifica do arquivo de memoria
                mapmem = memory_map(mem)
                print len(mapmem)
                print mapmem[0:10]
                print mapmem[0]
                mapmem[4] = chr(64)
                mapmem[0] = chr(2)
                mapmem[2] = chr(16)
                mapmem.close()
                    
                with open(mem, 'rb') as a:
                    print map(ord, a.read(5))
                    
                trace =  arquivo.readlines()
                for i in xrange(len(trace)):
                    trace[i] = trace[i].split()
                    trace[i][0] = int(trace[i][0])
                    trace[i][2:len(trace)] = map(int, trace[i][2:len(trace)])
                print total, virtual
                print trace
                arquivo.close()
                f.imprimeTempo(trace)
                
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
