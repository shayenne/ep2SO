import os
import mmap
import readline
import funcoes as f
import struct
import time
import threading
from processo import *
from arquivos import *

def makeEmptyBin(filename, size):
    with open(filename, 'wb') as f:
        for i in xrange(size):
            f.seek(i)
            f.write(b'\xff')
        f.close()


def memory_map(filename, access=mmap.ACCESS_WRITE):
    size = os.path.getsize(filename)
    fd = os.open(filename, os.O_RDWR)
    return mmap.mmap(fd, size, access=access)

def escreveMemoria(arqmem, ini, fim, pid):
    # Acessa uma posicao especifica do arquivo de memoria
    mapmem = memory_map(arqmem)

    for i in xrange(ini, fim):
        mapmem[i] = chr(pid)

    print mapmem[0:len(mapmem)]
    mapmem.close()
                    


def leMemoria(arqmem, pos):
    # Acessa uma posicao especifica do arquivo de memoria
    mapmem = memory_map(arqmem)
    print mapmem[pos]
    mapmem.close()
    
    
def copiaPagina(orig, oini, dest, dini, tam):
    print "CHEGUEI NO COPIA PAGINA"
    maporig = memory_map(orig)
    mapdest = memory_map(dest)
    for i in xrange(tam):
        mapdest[dini + i] = maporig[oini + i]
    mapdest.close()
    maporig.close()
    

def main():
    m = "ep2.mem"
    n = "ep2.vir"
    makeEmptyBin(n, 32)
    makeEmptyBin(m, 32)
    
    escreveMemoria(n, 1, 7, 50)
    
    copiaPagina(n, 0, m, 8, 16)
    
    #escreveMemoria(m, 1, 11, 42)
    
    #copiaPagina(m, 0, n, 8, 16)
    
if __name__ == "__main__":
    main()
