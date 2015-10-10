#!/usr/bin/env python

from arquivos import *
from Lista import *
import gerenciador

# Recebe um endereco da memoria virtual e devolve o endereco
# da memoria fisica no qual esta mapeado.
# Caso o processo nao esteja mapeado na memoria fisica???def enderecoMMU(endereco):
    
mapa = None
tam = None
processos = {}
vir = None
mem = None
lstfisica = None

# Recebe o tamanho da memoria virtual (em bytes) e o tamanho da pagina (em bytes)e cria um mapa de paginas que contem endereco do page frame em que a pagina esta mapeada, bit Presente/Ausente e o bit R.
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


def MMUacessaPosicao(pid, pos):
    global processos, tam
    print ">>TO TENTANDO ACESSAR AQUI", pos
    leuPosicao =  MMUtraduzEndereco(processos[pid][0],  pos)
    if leuPosicao:
        print "Li a posicao ", leuPosicao, "da memoria fisica"
        leMemoria(mem, leuPosicao)
    else:
        encontrouEspaco = gerenciador.FirstFit(lstfisica, pid, 1)
        lstfisica.show("Fisica")
        print encontrouEspaco
        if encontrouEspaco:
            local = pos / tam
            if pos % tam == 0:
                local -= 1
            print "INICIO DA COPIA DA VIRTUAL: ", processos[pid][0]+local
            copiaPagina(vir, (processos[pid][0]+local)*tam, mem, encontrouEspaco*tam, tam)
            #copiaPagina(mem, encontrouEspaco*tam, vir, (processos[pid][0]+local)*tam, tam)
            print "Copiei da memoria virtual para a fisica"
        # Chama o algoritmo de substituicao
        
    
# Guarda num dicionario o processo associado a sua base e limite (em paginas)
def MMUalocaEspaco(pid, inicio, paginas):
    global processos
    processos[pid] = [inicio, inicio+paginas] 
    print processos

# Recebe a base (em paginas) e uma posicao (em bytes) e mapeia para um endereco da memoria fisica (em bytes)
def MMUtraduzEndereco(base, pos):
    local = pos / tam
    # Correcao de indices
    if pos%tam == 0:
        local -= 1

    # Verificar se a pagina esta mapeada na memoria fisica
    if mapa[base + local][0] == 1:
        print "Encontrei a pagina na memoria fisica"
        return mapa[base+local][1]*tam + pos
    else:        
        print "Nao encontrei a pagina na memoria fisica"
        return False

    

if __name__ == "__main__":
    MMUcriaMapa(256, 16)
    
