#!/usr/bin/env python

import readline
import funcoes as f
import struct
import time
import threading
from processo import *
from arquivos import *
from gerenciador import * 
from MMU import *

global tampag

if __name__ == "__main__":
    global tampag
    tampag = 16
    # Variaveis importantes
    arquivo = None
    espaco = None
    substitui = None
    intervalo = None
	
    prompt = raw_input("[ep2]: ").split()
    proc = []
    mem = 'ep2.mem'
    vir = 'ep2.vir'
    
    while prompt[0] != "sai":
        
        if prompt[0] == "carrega":
            try:
                arquivo = open(prompt[1], 'r')

                total, virtual = map(int, arquivo.readline().split())
                    
                trace =  arquivo.readlines()
                ind = 0
                for t in trace:
                    t = t.split()
                    t[0] = int(t[0])
                    t[2:len(t)] = map(int, t[2:len(t)])
                    par = []
                    for i in xrange(4, len(t), 2):
                        x, y = t[i:i+2]
                        par.append([x, y])
                    p = Processo(t[0], t[1], t[2], t[3], par)
                    p.pid = ind
                    ind += 1
                    proc.append(p)

                arquivo.close()      
                
            except IOError:
                print "Arquivo inexistente"
            except IndexError:
                print "Digite o caminho do arquivo"
            

        if prompt[0] == "espaco":
            try:
                espaco = prompt[1]
            except IndexError:
                print "O algoritmo de gerenciamento de espaco livre nao foi definido"
            
            
        if prompt[0] == "substitui":
            try:
                substitui = prompt[1]
            except IndexError:
                print "O algoritmo de paginacao nao foi definido"
           
                    
        if prompt[0] == "executa":
            # APAGAR
            espaco = "1"
            substitui = "1"
            #
            try:
                intervalo = prompt[1]
            except IndexError:
                print "O intervalo de tempo nao foi definido"
            if not arquivo:
                print "O arquivo nao foi carregado."
            if not espaco:
                print "O algoritmo de gerenciamento de espaco livre nao foi definido."
            if not substitui:
                print "O algoritmo de paginacao nao foi definido."
                
            if arquivo and espaco and substitui and intervalo:
                # Inicializa os arquivos de memoria total e virtual
                makeEmptyBin(mem, total)
                makeEmptyBin(vir, virtual)

                # Define o gerenciador de espaco livre a ser usado
                # Junto com o tamanho da pagina
                defineGerenciador(espaco, tampag, vir)

                # Cria a lista da memoria virtual
                criaListaVirtual(virtual)

                # Cria mapa da MMU
                MMUcriaMapa(total, virtual, tampag, mem, vir)
                
                # Acessa uma posicao especifica do arquivo de memoria
                mapmem = memory_map(mem)
                print len(mapmem)
                print mapmem[0:10]
                print mapmem[0]
                #mapmem[4] = chr(64)
                #mapmem[0] = chr(2)
                #mapmem[2] = chr(16)
                mapmem.close()
                
                #escreveMemoria(mem, 2, 8)    
                #with open(mem, 'rb') as a:
                #    print map(ord, a.read(5))
                
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
