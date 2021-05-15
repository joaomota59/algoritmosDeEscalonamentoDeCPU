from copy import deepcopy
import numpy as np
'''A entrada é composta por uma série de pares de números inteiros 
separadas por um espaço em branco indicando o 
instante de chegada do processo e a duração de cada processo.

'''

arquivo = open('entrada.txt','r')#abre o arquivo

linhas = arquivo.readlines()#le as linhas do arquivo e coloca na variavel linha

arquivo.close()#fecha o arquivo

matriz = []#[(chegada duracao prioridade), (chegada duracao prioridade) ...]

prioridadeInicial = 5 ##prioridade incial para cada processo foi adotada como 5

for linha in linhas:
    matriz.append(list(map(int,linha.replace("\n","").split()))+[prioridadeInicial])

##orderna a matriz de acordo com a chegada dos processos
matriz = np.asarray(matriz)
matriz = matriz[matriz[:,0].argsort()]

#matriz é a matriz original passada como entrada
#print(matriz)


def maxNaMatriz(matrix, coluna, vetFlags):#retorna o maior elemento da matriz referente a coluna de prioridade
    aux = []
    for indice,linha in enumerate(matrix):
        if vetFlags[indice] != 1:# desconsidera tds processos que tem duração 0
            aux.append(linha[coluna])
    return max(aux)


def prioridadeDinamica(passoApasso = False):#algoritmo de prioridade Dinâmica
    timelineCounter = -1 
    colunasHistorico = np.sum(matriz,0)[1] + 1
    matrizHistorico = np.zeros((len(matriz),colunasHistorico), dtype=np.int)#matriz zerada que mostrara futuramente o timeline dos processos
    filaPDinamica = deepcopy(matriz)#cria uma cópia da matriz original
    if(passoApasso):
        print(filaPDinamica)
        print(matrizHistorico)
        print()
    #print(maiorPrioridade)
    timelineCounter = 0
    auxFlags = np.zeros(len(matriz), dtype = np.int) #auxilia para informar processos que serao desconsiderados quando ficarem com duração 0
    #print(aux)
    while(timelineCounter < colunasHistorico - 1):
        #maiorPrioridade = np.amax(filaPDinamica,0)[2]#pega o processo de maior prioridade
        maiorPrioridade = maxNaMatriz(filaPDinamica,2,auxFlags) #ve qual é a maior prioridade entre os processos
        flag = False #pega o primeiro processo quando a maior prioridade
        for processo in range(len(filaPDinamica)):
            chegada = filaPDinamica[processo][0]
            duracao = filaPDinamica[processo][1]
            prioridade = filaPDinamica[processo][2]
            if(prioridade == maiorPrioridade and not flag and duracao > 0):
                if (duracao - 1 != 0):#so diminui a prioridade se a diferenca for maior que zero
                    filaPDinamica[processo][2] = prioridade - 1
                else:#se o processo ficar com duração zero será desconsiderado na proxima vez
                    auxFlags[processo] = 1
                filaPDinamica[processo][1] = duracao - 1
                matrizHistorico[processo][timelineCounter+1] = 1
                matrizHistorico[processo][timelineCounter] = 1
                flag = True
            else:#se nao for o processo de maior prioridade entao aumenta a prioridade
                if( chegada <= timelineCounter and duracao > 0): #mas so icrementa se o processo está no estado pronto, ou se o processo já tiver chegado
                    filaPDinamica[processo][2] = prioridade + 1
                    
        #contador da linha do tempo
        timelineCounter+=1
        if(passoApasso):
            print(filaPDinamica)
            print(matrizHistorico)
            print()
    return matrizHistorico
        

pD = prioridadeDinamica(False)

