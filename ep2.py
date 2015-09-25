#!/usr/bin/env python

import readline
import funcoes as f

if __name__ == "__main__":
    prompt = raw_input("[ep2]: ").split()
    
    while prompt[0] != "sai":
        
        if prompt[0] == "carrega":
            try:
                print "Tenho que carregar o arquivo {}.".format(prompt[1])
                arquivo = open(prompt[1], 'r')
                total, virtual = map(int, arquivo.readline().split())
                mem = open('/tmp/ep2.mem', 'wb')
                mem.write((b'1')*total)
                mem.close()
                vir = open('/tmp/ep2.vir', 'wb')
                vir.write((b'1')*virtual)
                vir.close()
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
