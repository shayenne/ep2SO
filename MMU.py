#!/usr/bin/env python


# Recebe um endereco da memoria virtual e devolve o endereco
# da memoria fisica no qual esta mapeado.
# Caso o processo nao esteja mapeado na memoria fisica???def enderecoMMU(endereco):
    
mapa = None
tam = None
processos = {}

# Recebe o tamanho da memoria virtual (em bytes) e o tamanho da pagina (em bytes)e cria um mapa de paginas
def MMUcriaMapa(tmemoria, pagina):
    global mapa, tam
    tam = pagina
    mapa = [[0 for x in range((tmemoria/pagina))] for x in range(3)]
    print mapa


def MMUacessaPosicao(pid, pos):
    global processos, tam
    x =  MMUtraduzEndereco(processos[pid][0]*tam + pos)
    if x:
        # Escreve na posicao devolvida
        print "Escrevi na posicao ", x, "da memoria fisica"
    else:
        y = FirstFit(lstfisica, pid, 1)
        if y:
            #copiaPagina(vir, processos[pid][0]*tam, mem, y, tam)
            print "Copiei da memoria virtual para a fisica"
        # Chama o algoritmo de substituicao
        
    
# Guarda num dicionario o processo associado a sua base e limite (em paginas)
def MMUalocaEspaco(pid, inicio, paginas):
    global processos
    processos[pid] = [inicio, inicio+paginas]


# Recebe um endereco virtual (em bytes) e mapeia para um endereco da memoria fisica (em bytes)
def MMUtraduzEndereco(endvirtual):
    return False
    return endfisico

    

if __name__ == "__main__":
    MMUcriaMapa(256, 16)
    
