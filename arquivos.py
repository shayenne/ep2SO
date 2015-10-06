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

def escreveMemoria(arqmem, pos, pid):
    # Acessa uma posicao especifica do arquivo de memoria
    mapmem = memory_map(arqmem)
    print len(mapmem)
    print mapmem[0:len(mapmem)]
    print mapmem[0]
    print pos, pid
    mapmem[pos] = chr(pid)
    mapmem.close()
                    
    #with open(mem, 'rb') as a:
    #    print map(ord, a.read(5))
    
    
def copiaPagina(orig, oini, dest, dini, tam):
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
    
    escreveMemoria(m, 2, 50)
    
    copiaPagina(m, 0, n, 2, 16)
    
    escreveMemoria(m, 11, 42)
    
    copiaPagina(m, 0, n, 8, 16)
    
if __name__ == "__main__":
    main()
