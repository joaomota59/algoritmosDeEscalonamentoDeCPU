from copy import deepcopy
import numpy as np
from random import randrange
import sys
'''A entrada é composta por uma série de pares de números inteiros 
separadas por um espaço em branco indicando o 
instante de chegada do processo e a duração de cada processo.

'''

entrada = sys.argv[1]
try:
    arquivo = open(entrada,'r')#abre o arquivo
except:
    print("Arquivo não encontrado!")
    exit(0)

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


def prioridadeDinamica(passoApasso = False):#algoritmo de prioridade Dinâmica, se passar True como parametro mostra passo a passo
    colunasHistorico = np.sum(matriz,0)[1] + 1 #soma a duracao total dos processos e mais 1 p fazer a timeline
    matrizHistorico = np.zeros((len(matriz),colunasHistorico), dtype=np.int)#matriz zerada que mostrara futuramente o timeline dos processos

    filaPDinamica = deepcopy(matriz[matriz[:,0].argsort()])#cria uma cópia da matriz

    matrizHistoricoAux = (np.zeros((len(filaPDinamica),1),dtype=np.int)).tolist()#vai armazenar as tuplas do timeline
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

                matrizHistoricoAux[processo].append((timelineCounter,timelineCounter+1))
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
    return matrizHistorico, matrizHistoricoAux
        

def loteria(passoApasso = False):
    colunasHistorico = np.sum(matriz,0)[1] + 1 #soma a duracao total dos processos e mais 1 p fazer a timeline
    matrizHistorico = np.zeros((len(matriz),colunasHistorico), dtype=np.int)#matriz zerada que mostrara futuramente o timeline dos processos
    matrixLoteria = deepcopy(matriz)#cria uma cópia da matriz original
    matrizHistoricoAux = (np.zeros((len(matrixLoteria),1),dtype=np.int)).tolist()#vai armazenar as tuplas do timeline
    if(passoApasso):
        print(matrixLoteria)
        print(matrizHistorico)
        print()
    timelineCounter = 0
    while(timelineCounter < colunasHistorico - 1):
        sorteiaProcesso = randrange(len(matrixLoteria)) #sorteia qual processo vai entrar em execução
        chegada = matrixLoteria[sorteiaProcesso][0]
        duracao = matrixLoteria[sorteiaProcesso][1]
        if (duracao == 0 or chegada>timelineCounter):#se for um processo que já foi executado por completo ou se for um processo que nao esteja no estado pronto, sorteia novamente
            continue
        if(passoApasso):
            print("Processo sorteado:",sorteiaProcesso)
        if(duracao - 2 >= 0):#se o processo gastar um quantum inteiro
            matrixLoteria[sorteiaProcesso][1] = duracao - 2
            matrizHistorico[sorteiaProcesso][timelineCounter] = 1

            matrizHistoricoAux[sorteiaProcesso].append((timelineCounter,timelineCounter+1))
            matrizHistoricoAux[sorteiaProcesso].append((timelineCounter+1,timelineCounter+2))
            
            matrizHistorico[sorteiaProcesso][timelineCounter+1] = 1
            matrizHistorico[sorteiaProcesso][timelineCounter+2] = 1
            timelineCounter+=2#um quantum corresponde a duas fatias de tempo
        else:#se precisar somente da metade do quantum(uma fatia de tempo)
            matrixLoteria[sorteiaProcesso][1] = duracao - 1
            matrizHistorico[sorteiaProcesso][timelineCounter] = 1
            matrizHistorico[sorteiaProcesso][timelineCounter+1] = 1

            matrizHistoricoAux[sorteiaProcesso].append((timelineCounter,timelineCounter+1))
            
            timelineCounter+=1#um quantum corresponde a duas fatias de tempo
        if(passoApasso):
            print(matrixLoteria)
            print(matrizHistorico)
            print()
    return matrizHistorico, matrizHistoricoAux


def roundRobin(passoApasso = False):
    colunasHistorico = np.sum(matriz,0)[1] + 1 #soma a duracao total dos processos e + 1 p fazer a timeline
    matrizHistorico = np.zeros((len(matriz),colunasHistorico), dtype=np.int)#matriz zerada que mostrara futuramente o timeline dos processos
    matrixRR = deepcopy(matriz).tolist() #cria uma cópia da matriz original
    matrizHistoricoAux = (np.zeros((len(matrixRR),1),dtype=np.int)).tolist()#vai armazenar as tuplas do timeline
    matrizAux = []#fila ciclica
    timelineCounter = 0
    for indice,linha in enumerate(matrixRR):#cria uma referencia para cada processo.. ex: P0, P1 , P2 ,P3
        linha[2] = indice
    for i in matrixRR:#observa quais processos podem entrar no estado pronto no instante 0
        if(i[0] <= timelineCounter):#se a chegada for menor/igual dq o timeline entao o processo está em estado pronto e entao pode entrar na fila
            matrizAux.append(i)
    for indice,linha in enumerate(matrizAux):#deleta os elementos adicionados na matrizAux da matrixRR
        try:
            del(matrixRR[matrixRR.index(linha)])
        except:#se n der certo deletar é pq n teve processos no arquivo texto no instante 0
            break
    if(passoApasso):
        #print("Cada linha da matriz: [Momento de Chegada, Duração do Processo, ID do processo]\n\n")
        print(np.asarray(matrizAux))
        print(matrizHistorico)
        print()
    while(timelineCounter < colunasHistorico - 1):
        duracao = matrizAux[0][1]#duracao do primeiro processo da fila
        if(duracao - 2 >= 0):#se o processo gastar um quantum inteiro(duas fatias de tempo)
            matrizAux[0][1] = duracao - 2 #reduz a duração do processo
            numeroDoProcesso = matrizAux[0][2]#Referência do processo

            matrizHistoricoAux[numeroDoProcesso].append((timelineCounter,timelineCounter+1))
            matrizHistoricoAux[numeroDoProcesso].append((timelineCounter+1,timelineCounter+2))
            
            matrizHistorico[numeroDoProcesso][timelineCounter] = 1
            matrizHistorico[numeroDoProcesso][timelineCounter+1] = 1
            matrizHistorico[numeroDoProcesso][timelineCounter+2] = 1
            timelineCounter+=2#um quantum corresponde a duas fatias de tempo
        else:#se o processo gastar só a metade do quantum
            matrizAux[0][1] = duracao - 1
            numeroDoProcesso = matrizAux[0][2]

            matrizHistoricoAux[numeroDoProcesso].append((timelineCounter,timelineCounter+1))
            
            matrizHistorico[numeroDoProcesso][timelineCounter] = 1
            matrizHistorico[numeroDoProcesso][timelineCounter+1] = 1
            timelineCounter+=1#metade de um quantum(uma fatia de tempo)

        contAux = 0 #conta quantos elementos foram adicionados a fila
        for i in matrixRR:#observa quais processos podem entrar no estado pronto
            if(i[0] <= timelineCounter):#se a chegada for menor/igual dq o timeline entao o processo está em estado pronto e entao pode entrar na fila
                matrizAux.append(i)
                contAux+=1        
        for quant in range(contAux):#deleta os elementos adicionados na matrizAux da matrixRR
            del(matrixRR[0])
        if(matrizAux[0][1] == 0):#se o processo tiver ficar com a duração igual a zero entao é retirado da fila
            del(matrizAux[0])
        else:
            matrizAux.append(matrizAux[0])#joga o processo do começo da fila para o final da fila
            del(matrizAux[0])#deleta o processo que foi para o final da fila do começo do vetor
        if(passoApasso):
            print(np.asarray(matrizAux))
            print(matrizHistorico)
            print()
            
    return matrizHistorico,matrizHistoricoAux


def rindex(alist, value):#ultima ocorrerencia de um elemento no vetor
    return len(alist) - alist[-1::-1].index(value) -1 #retorna  a posicao no vetor


def multiplicaArray(array,matrixHistorico):#multiplica o array por cada elemento da matrix exceto ele proprio
    somaOcorrencias = 0
    for lista in matrixHistorico:
       if list(array) != list(lista):#se nao for o proprio array
           aux = list(np.multiply(list(array),list(lista)))#multiplica linha x linha
           primeiroIndiceDoArray = list(array).index(1)#quando o processo começa
           ultimoIndiceDoArray = rindex(list(array),1)#quando o processo termina
           if lista[primeiroIndiceDoArray] == 1:
               aux[primeiroIndiceDoArray] = 0
           if lista[ultimoIndiceDoArray] == 1:
               aux[ultimoIndiceDoArray] = 0
           somaOcorrencias+=sum(aux)
    return somaOcorrencias/2

def somamultiplicaArray(matrixHistorico):#conta todas interseções entre o histico dos processos
    soma = 0
    for indice,i in enumerate(matrixHistorico):
        soma += multiplicaArray(i,matrixHistorico[indice:])
    return soma
           
        

def tempoDeRetornoMedio(matrizHistorico):
    somatorio = 0
    for indice,processo in enumerate(matrizHistorico):
        entrada = matriz[indice][0]#momento da chegada do processo
        termino = rindex(list(processo),1)#momento em que o processo termina por completo
        somatorio += termino - entrada
    return ("%.2f"%(float(somatorio/len(matrizHistorico))))

def tempoDeRespostaMedio(matrizHistorico):
    somatorio = 0
    for indice,processo in enumerate(matrizHistorico):
        entrada = matriz[indice][0]#momento da chegada do processo
        inicio = list(processo).index(1)#momento em que o processo inicia sua execução
        somatorio += inicio - entrada
    return ("%.2f"%(float(somatorio/len(matrizHistorico))))

def tempoDeEsperaMedio(matrizHistorico,matrizHistoricoAux):
    somatorio = 0
    for indice,processo in enumerate(matrizHistorico):
        quantDeExecucoes = len(matrizHistoricoAux[indice]) - 1 #-1 pois o que inicial que foi adicionado nao conta
        entrada = matriz[indice][0]#momento da chegada do processo
        termino = rindex(list(processo),1)#momento em que o processo termina por completo
        somatorio += termino - entrada - quantDeExecucoes #retorna o tempo que o processo estava no estado pronto porem nao estava em execucao
    return ("%.2f"%(float(somatorio/len(matrizHistorico))))

            
pD = prioridadeDinamica(False)
l = loteria(False)
rR = roundRobin(False)

print("PRI "+tempoDeRetornoMedio(pD[0])+" "+tempoDeRespostaMedio(pD[0])+" "+tempoDeEsperaMedio(pD[0],pD[1]))
print("LOT "+tempoDeRetornoMedio(l[0])+" "+tempoDeRespostaMedio(l[0])+" "+tempoDeEsperaMedio(l[0],l[1]))
print("RR "+tempoDeRetornoMedio(rR[0])+" "+tempoDeRespostaMedio(rR[0])+" "+tempoDeEsperaMedio(rR[0],rR[1]))

###Criar outra matrizHistorico em cada um!! -> <-
