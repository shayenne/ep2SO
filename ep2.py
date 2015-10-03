#!/usr/bin/env python

import readline
import funcoes as f
import struct
import time
import threading
from processo import *
from arquivos import *

if __name__ == "__main__":
    prompt = raw_input("[ep2]: ").split()
    proc = []
    mem = 'ep2.mem'
    vir = 'ep2.vir'
    
    while prompt[0] != "sai":
        
        if prompt[0] == "carrega":
            try:
                print "Tenho que carregar o arquivo {}.".format(prompt[1])
                arquivo = open(prompt[1], 'r')
                total, virtual = map(int, arquivo.readline().split())

                # Acessa uma posicao especifica do arquivo de memoria
                #mapmem = memory_map(mem)
                #print len(mapmem)
                #print mapmem[0:10]
                #print mapmem[0]
                #mapmem[4] = chr(64)
                #mapmem[0] = chr(2)
                #mapmem[2] = chr(16)
                #mapmem.close()
                    
                #with open(mem, 'rb') as a:
                #    print map(ord, a.read(5))
                    
                trace =  arquivo.readlines()
                for t in trace:
                    t = t.split()
                    t[0] = int(t[0])
                    t[2:len(t)] = map(int, t[2:len(t)])
                    par = []
                    for i in xrange(4, len(t)-2):
                        x, y = t[i:i+2]
                        par.append([x, y])
                    p = Processo(t[0], t[1], t[2], t[3], par)
                    proc.append(p)
                #print total, virtual
                #print trace
                arquivo.close()
                #f.imprimeTempo(trace)
                
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

            # Inicializa os arquivos de memoria total e virtual
            makeEmptyBin(mem, total)
            makeEmptyBin(vir, virtual)
            threads = []
            inicio = time.time()
            for p in proc:
                t = threading.Thread(target=p.iniciaContagem, args=(inicio, ))
                threads.append(t)
            for t in threads:
                t.start()
            for t in threads:
                t.join()


        prompt = raw_input("[ep2]: ").split()
