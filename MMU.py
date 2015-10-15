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
contador = None


# TESTES
def initContador():
    global contador
    contador = 0

def imprimeContador():
    global contador
    print "Houveram ", contador, " Page Faults"


# Recebe o tamanho da memoria virtual (em bytes), o tamanho da pagina (em bytes)
# os nomes dos arquivos de memoria fisica e virtual
# e cria um mapa de paginas que contem endereco do page frame em que a pagina
# esta mapeada, bit Presente/Ausente e o bit R.
#
# Mapa da MMU
#    0           1        2        3
#|  P/A  |  PageFrame  |  R  |  Counter  |
def MMUcriaMapa(tmem, tvir, pagina, virtual, fisica):
    global mapa, tam, vir, mem, lstfisica, fila, lockmapa, contador
    lockmapa = threading.Lock()
    vir = virtual
    mem = fisica
    tam = pagina
    fila = List()
    lstfisica = List()
    lstfisica.append(["L", 0, int(tmem/tam)])
    mapa = [[0 for x in range(4)] for x in range(tvir/pagina)]
    # Testes
    contador = 0
    #

# Imprime o estado da lista de memoria Fisica
def MMUimprimeFisica():
    lstfisica.show("Status da Memoria Fisica")

# Inicializa o semaforo, quando necessario
def initLock():
    global lockmapa
    lockmapa = threading.Lock()

    
def acquireLock():
    global lockmapa
    lockmapa.acquire()

def releaseLock():
    global lockmapa
    lockmapa.release()

def MMUatualizaContador():
    global lockmapa, fila
    
    lockmapa.acquire()

    p = fila.head
    while p is not None:
        p.data[3] += p.data[2]
        p = p.next

    lockmapa.release()
    
    
# Acessa uma posicao de um processo, transformando o endereco virtual em fisico
def MMUacessaPosicao(pid, pos):
    global processos, tam, lockmapa, fila, contador

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

            lockmapa.acquire()
            # Procura na lista de frames e seta o bit R
            p = fila.head
            while p is not None:
                if p.data[1] == mapa[base+local][1]:
                    p.data[2] = 1
                    break
                p = p.next
            
            # Seta o bit R (Request/Read)
            mapa[base+local][2] = 1
            
            
            # Atualiza o contador
            mapa[base+local][3] += 1

            lockmapa.release()
        else:
            encontrouEspaco = gerenciador.FirstFit(lstfisica, pid, 1)
            
            ##
            #lstfisica.show("Fisica")
            ##
            

            if encontrouEspaco is not None:
                
                copiaPagina(vir,(base+local)*tam, mem, encontrouEspaco*tam, tam)
                
                lockmapa.acquire()
                # Insere o processo na fila de frames
                fila.append([pid, encontrouEspaco, 1, 0])
                # Seta o bit para Presente
                mapa[base+local][0] = 1
                # Coloca o page frame em que esta o pagina
                mapa[base+local][1] = encontrouEspaco
                # Seta o bit R (Request/Read)
                mapa[base+local][2] = 1
                # Atualiza o contador
                mapa[base+local][3] += 1
                lockmapa.release()
                #print mapa
 
                #print "Copiei da memoria virtual para a fisica"
                # Chama o algoritmo de substituicao
            else:
                #print "VOU TER QUE SUBSTITUIR "
                # Encontra o frame que deve ser substituido
                frame = paginacao.substitui(fila)
                #print "Vou trocar o frame ", frame
                
                copiaPagina(vir, (base+local)*tam, mem, frame*tam, tam)

                lockmapa.acquire()
                # Remove o processo que estava na fila de frames
                # TESTE#
                contador += 1
                rmpid = None
                p = fila.head
                while p is not None:
                    if p.data[1] == frame:
                        rmpid = p.data[0]
                        #print "Inseri o frame ", frame
                        
                        #fila.show("FILA ANTES")
                        #print "Removi o frame ", frame
                        fila.remove(p.data)
                        # Insere o novo processo na fila de frames
                        #fila.show("FILA DURANTE")
                        fila.append([pid, frame, 1, 0])
                        #fila.show("FILA DEPOIS")
                        break
                    p = p.next

                f = lstfisica.head
                while f is not None:
                    if f.data[1] == frame:
                        f.data[0] = pid
                        break
                    f = f.next
                
                #print "Esse e o rmpid ", rmpid
                # Define o bit para Ausente
                for i in xrange(processos[rmpid][1]):
                    #print i, processos[rmpid][0]
                    if mapa[processos[rmpid][0]+i][1] == frame:
                        mapa[processos[rmpid][0]+i][0] = 0
                        break

               
                # Seta o bit para Presente
                mapa[base+local][0] = 1
                # Coloca o page frame em que esta o pagina
                mapa[base+local][1] = frame
                # Seta o bit R (Request/Read)
                mapa[base+local][2] = 1
                # Atualiza o contador
                mapa[base+local][3] += 1
                lockmapa.release()
                #MMUimprimeFisica()
            MMUacessaPosicao(pid, pos)
            
    finally:
        lock3.release()
    
# Guarda num dicionario o processo associado a sua base e limite (em paginas)
def MMUalocaEspaco(pid, base, paginas):
    global processos
    processos[pid] = [base, paginas]
    

# Recebe a base (em paginas) e uma posicao (em bytes) e mapeia para um endereco da memoria fisica (em bytes)
def MMUtraduzEndereco(base, pos):
    local = pos / tam

    # Verificar se a pagina esta mapeada na memoria fisica
    if mapa[base + local][0] == 1:
        return mapa[base+local][1]*tam + pos % tam
    else:        
        return None

    

def MMUterminaProcesso(pid):
    
    lock2 = threading.Lock()
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


        del processos[pid]
        #lstfisica.show("Fisica apos remocao do processo")

    finally:
        lock2.release()

# A cada intervalo de tempo (definido no ep2.py) reseta os bits R de todos os
# processos que estao mapeados na memoria fisica
def resetaR():
    global mapa, fila
   
    lockmapa.acquire()
    p = fila.head
    while p is not None:    
        p.data[2] = 0
        p = p.next
        
    for i in xrange(len(mapa)):
        mapa[i][2] = 0
    
    lockmapa.release()



if __name__ == "__main__":
    MMUcriaMapa(256, 16)
    
