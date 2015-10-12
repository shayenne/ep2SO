#!/usr/bin/env python

from arquivos import *
from Lista import *
import gerenciador
import threading

# Recebe um endereco da memoria virtual e devolve o endereco
# da memoria fisica no qual esta mapeado.
# Caso o processo nao esteja mapeado na memoria fisica???def enderecoMMU(endereco):
    
mapa = None
tam = None
processos = {}
vir = None
mem = None
lstfisica = None

# Recebe o tamanho da memoria virtual (em bytes), o tamanho da pagina (em bytes)
# os nomes dos arquivos de memoria fisica e virtual
# e cria um mapa de paginas que contem endereco do page frame em que a pagina
# esta mapeada, bit Presente/Ausente e o bit R.
#
# Mapa da MMU
#    0           1        2 
#|  P/A  |  PageFrame  |  R  | 
def MMUcriaMapa(tmem, tvir, pagina, virtual, fisica):
    global mapa, tam, vir, mem, lstfisica
    vir = virtual
    mem = fisica
    tam = pagina
    lstfisica = List()
    lstfisica.append(["L", 0, int(tmem/tam)])
    mapa = [[0 for x in range(3)] for x in range(tvir/pagina)]


# Imprime o estado da lista de memoria Fisica
def MMUimprimeFisica():
    lstfisica.show("Status da Memoria Fisica")

# Acessa uma posicao de um processo, transformando o endereco virtual em fisico
def MMUacessaPosicao(pid, pos):
    global processos, tam

    lock = threading.Lock()
    lock.acquire()
    try:
        print ">> O pid ", pid, "esta tentando acessar a posicao ", pos
        leuPosicao =  MMUtraduzEndereco(processos[pid][0],  pos)
        
        if leuPosicao is not None:
            print "Li a posicao ", leuPosicao, "da memoria fisica"
            leMemoria(mem, leuPosicao)
        else:
            encontrouEspaco = gerenciador.FirstFit(lstfisica, pid, 1)
            ##
            lstfisica.show("Fisica")
            ##
            if encontrouEspaco is not None:
                # Calcula qual pagina do processo deve ser carregada
                local = pos / tam
        
                if pos != 0 and pos % tam == 0:
                    local -= 1

                copiaPagina(vir, (processos[pid][0]+local)*tam, mem, encontrouEspaco*tam, tam)
                mapa[processos[pid][0]+local][0] = 1
                mapa[processos[pid][0]+local][1] = encontrouEspaco
                print mapa
                #copiaPagina(mem, encontrouEspaco*tam, vir, (processos[pid][0]+local)*tam, tam)
                print "Copiei da memoria virtual para a fisica"
                # Chama o algoritmo de substituicao
    finally:
        lock.release()
    
# Guarda num dicionario o processo associado a sua base e limite (em paginas)
def MMUalocaEspaco(pid, inicio, paginas):
    global processos
    processos[pid] = [inicio, paginas] 
    

# Recebe a base (em paginas) e uma posicao (em bytes) e mapeia para um endereco da memoria fisica (em bytes)
def MMUtraduzEndereco(base, pos):
    local = pos / tam
    # Correcao de indices
    if pos != 0 and pos%tam == 0:
        local -= 1

    # Verificar se a pagina esta mapeada na memoria fisica
    if mapa[base + local][0] == 1:
        print "Encontrei a pagina na memoria fisica"
        return mapa[base+local][1]*tam + pos
    else:        
        print "Nao encontrei a pagina na memoria fisica"
        return None

    

def MMUterminaProcesso(pid):
    # Nao e so isso, tem que reestruturar a fila
    #for i in xrange(processos[pid][1]):
    #    lstfisica.remove([pid, processos[pid][0] + i, 1])
    curr = lstfisica.head
    while curr is not None:
        if curr.data[0] == pid:
            while curr.data[0] == pid:
                gerenciador.liberaEspaco(lstfisica, curr)
                curr = curr.next
            break
        curr = curr.next


    lstfisica.show("Fisica apos remocao do processo")

if __name__ == "__main__":
    MMUcriaMapa(256, 16)
    
