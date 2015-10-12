#!/usr/bin/env python

from arquivos import *
from Lista import *
import gerenciador
import threading
import paginacao 

# Recebe um endereco da memoria virtual e devolve o endereco
# da memoria fisica no qual esta mapeado.
# Caso o processo nao esteja mapeado na memoria fisica???def enderecoMMU(endereco):
    
mapa = None
tam = None
processos = {}
vir = None
mem = None
lstfisica = None
fila = None

lockmapa = None

# Recebe o tamanho da memoria virtual (em bytes), o tamanho da pagina (em bytes)
# os nomes dos arquivos de memoria fisica e virtual
# e cria um mapa de paginas que contem endereco do page frame em que a pagina
# esta mapeada, bit Presente/Ausente e o bit R.
#
# Mapa da MMU
#    0           1        2        3
#|  P/A  |  PageFrame  |  R  |  Counter  |
def MMUcriaMapa(tmem, tvir, pagina, virtual, fisica):
    global mapa, tam, vir, mem, lstfisica, fila, lockmapa
    lockmapa = threading.Lock()
    vir = virtual
    mem = fisica
    tam = pagina
    fila = List()
    lstfisica = List()
    lstfisica.append(["L", 0, int(tmem/tam)])
    mapa = [[0 for x in range(4)] for x in range(tvir/pagina)]


# Imprime o estado da lista de memoria Fisica
def MMUimprimeFisica():
    lstfisica.show("Status da Memoria Fisica")

# Acessa uma posicao de um processo, transformando o endereco virtual em fisico
def MMUacessaPosicao(pid, pos):
    global processos, tam

    lock3 = threading.Lock()
    lock3.acquire()
    try:
        print ">> O pid ", pid, "esta tentando acessar a posicao ", pos
        leuPosicao =  MMUtraduzEndereco(processos[pid][0],  pos)
        
        # Calcula qual pagina do processo deve ser carregada
        local = pos / tam
        base = processos[pid][0]

        if leuPosicao is not None:
            print "Li a posicao ", leuPosicao, "da memoria fisica"
            leMemoria(mem, leuPosicao)
            # Seta o bit R (Request/Read)
            mapa[base+local][2] = 1
            # Atualiza o contador
            mapa[base+local][3] += 1
        else:
            encontrouEspaco = gerenciador.FirstFit(lstfisica, pid, 1)
            
            ##
            lstfisica.show("Fisica")
            ##
            

            if encontrouEspaco is not None:
                fila.append([pid, encontrouEspaco])
                copiaPagina(vir,(base+local)*tam, mem, encontrouEspaco*tam, tam)
                # Seta o bit para Presente
                lockmapa.acquire()
                mapa[base+local][0] = 1
                # Coloca o page frame em que esta o pagina
                mapa[base+local][1] = encontrouEspaco
                # Seta o bit R (Request/Read)
                mapa[base+local][2] = 1
                # Atualiza o contador
                mapa[base+local][3] += 1
                lockmapa.release()
                print mapa
 
                print "Copiei da memoria virtual para a fisica"
                # Chama o algoritmo de substituicao
            else:
                frame = paginacao.substitui(mapa)
                copiaPagina(vir, (base+local)*tam, mem, frame*tam, tam)
            MMUacessaPosicao(pid, pos)
            
    finally:
        lock3.release()
    
# Guarda num dicionario o processo associado a sua base e limite (em paginas)
def MMUalocaEspaco(pid, inicio, paginas):
    global processos
    processos[pid] = [inicio, paginas]
    

# Recebe a base (em paginas) e uma posicao (em bytes) e mapeia para um endereco da memoria fisica (em bytes)
def MMUtraduzEndereco(base, pos):
    local = pos / tam

    # Verificar se a pagina esta mapeada na memoria fisica
    if mapa[base + local][0] == 1:
        print "Encontrei a pagina na memoria fisica"
        return mapa[base+local][1]*tam + pos % tam
    else:        
        print "Nao encontrei a pagina na memoria fisica"
        return None

    

def MMUterminaProcesso(pid):
    # Nao e so isso, tem que reestruturar a fila
    #for i in xrange(processos[pid][1]):
    #    lstfisica.remove([pid, processos[pid][0] + i, 1])
    lock2 = threading.RLock()
    lock2.acquire()
    try:
        curr = lstfisica.head
        while curr is not None:
            if curr.data[0] == pid:
                gerenciador.liberaEspaco(lstfisica, curr)
                
            curr = curr.next

        # Retira o processo do mapa
        base = processos[pid][0]
        paginas = processos[pid][1]
        for i in xrange(paginas):
            mapa[base+i] = [0 for x in range(4)]

  
        lstfisica.show("Fisica apos remocao do processo")

    finally:
        lock2.release()

def resetaR():
    global mapa
    print "Estou resetando os R :D"
    lockmapa.acquire()
    for i in xrange(len(mapa)):
        mapa[i][2] = 0
    print mapa
    lockmapa.release()



if __name__ == "__main__":
    MMUcriaMapa(256, 16)
    
