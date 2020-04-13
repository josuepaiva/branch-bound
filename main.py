# -*- coding: utf-8 -*-
"""Main Branch Bound"""

"""Dupla: 	Josué de Paiva Bernardino
	  		Thomas Ribeiro de Araujo"""
"""Como executar código:
	Primeiro é preciso instalar os módulos numpy e ortools utilizando o pip
	executando o seguinte comando: pip install numpy & pip install ortools.
	Logo em seguinda ir no terminal na basta do arquivo e executar python main.py
"""

import math
import numpy as np

# from ortools.linear_solver import pywraplp

from params import Params
from solverp import SolverP

IntOrNot = False
LessMoreOrEqual = 'LessMoreOrEqual'
raizb = 0
solvers = None

# //frags
integralidade = 0
limitante = 0
inviavel = 0

zdual = 0
zprimal = 0

class SubSolucao:
    def __init__(self, solucao, z):
        self.solucaovariaveis = solucao
        self.z = z

def integralidadeFunc(array):
    for i in array:
        if(isinstance(i, int) != True):
            return False
    
    return True


def checklimitante(zPrimal, zDual, z):
	if(MaxOrMin == 'Max'):
		if(z < zPrimal):
			return True
		else:
			return False
	else:
		if(z < zDual):
			return True
		else:
			return False

MAXORMIM = input('\nO PROBLEMA É DE ? \n[MAXIMIZACAO] - 1 \n[MINIMIZACAO] - 2\nDigite: ')
if MAXORMIM ==  2:
	MaxOrMin = 'Min'
	zdual = -1
	zprimal = 0
else:
	MaxOrMin = 'Max'
	zdual = 0
	zprimal = -1


def coletadados(path):
	"""# **Lendo arquivo**"""
	arquivo = open(path,'r')
	numeros = []

	for linha  in arquivo:
	  linha = linha.strip()
	  numeros.append(linha)

	arquivo.close()
	return numeros

def pegaRestricoes(dados):
	aux = dados[0].split(' ')
	numVariaveis = aux[0]
	numRestricoes = aux[1]
	coefFuncObj = dados[1].split(' ')
	
	arrayaux = dados[2:len(dados)]

	arrayRestricoesEsquerda = []
	arrayRestricoesDireita = []
	aux2 = arrayaux[0].split(' ')

	for x in arrayaux:
		aux2 = x.split(' ')
		arrayRestricoesEsquerda.append(aux2[0:int(numVariaveis)])
		arrayRestricoesDireita.append(aux2[int(numVariaveis)])

	params = Params(numVariaveis, numRestricoes, np.double(coefFuncObj), 
					np.double(arrayRestricoesEsquerda), np.double(arrayRestricoesDireita), 
					1 if LessMoreOrEqual == "LessMoreOrEqual" else 0,1 if MaxOrMin == "Max" else 0)

	return params

class NoBranchbound:
	def __init__(self, z, variaveis, esquerda=None, direita=None):
		self.z = z
		self.variaveis = variaveis
		self.esquerda = esquerda
		self.direita = direita

def createArrayNumpy(array):
    return np.double(array)

def insere(raiz, nodo):
	if raiz is None:
		raiz = nodo

	    # Nodo deve ser inserido na subárvore direita.
	elif raiz.z < nodo.z:
		if raiz.direita is None:
			raiz.direita = nodo
		else:
			insere(raiz.direita, nodo)

		# Nodo deve ser inserido na subárvore esquerda.
	else:
		if raiz.esquerda is None:
			raiz.esquerda = nodo
		else:
			insere(raiz.esquerda, nodo)  	

def minimo(raiz):
	valor = 100000000000
	nodo = raiz
	while nodo.esquerda is not None :
		nodo = nodo.esquerda
		if isinstance(nodo.z):
			if nodo.z < valor:
				valor = nodo.z
	return valor

def maximo(raiz):
	maior = -1000000
	nodo = raiz
	while nodo.direita is not None:
		nodo = nodo.direita
		if isinstance(nodo.z):
			if nodo.z > maior:
				maior = nodo.z
	return maior

def verify(array):	
	results = [0]*2
	value = 50000000000000

	for i in range(0,len(array)):
		aux = abs(0.5 - array[i])
		print(aux)
		if aux < value:
			value = aux
			results[0] = value
			results[1] = i

	return results

def min(array):
	valor = 8000000000000000

	for i in range(0,len(array)):
		if array[i] < valor:
			valor = array[i]
	return valor

def limpaArray(indice, array):
	result = [0]*len(array)

	for i in range(0,len(array)):
		if indice != i:
			result[i] = 0
		else:
			result[i] = 1

	return result

def acrescentaRestricao(nova, params):
    	restriEsqOld = params.getRestricoesEsq()

def branch_bound(problema):
	global raizb
	global zdual
	global zprimal
	global inviavel
	global integralidade
	global limitante

	if raizb == 0:
		print("Primeira chamada!")
		solucao = problema.resolve2()
		print("Problema inicial")
		print(solucao)
		print("")
		raizb = NoBranchbound(solucao[1], solucao[0])
	else:
		solucao = problema.resolve2()
		# insere(raizb, NoBranchbound(solucao[1], solucao[0]))
	
	if integralidadeFunc(solucao[0]):
		integralidade = 1
		zprimal = solucao[1]
		return
	if checklimitante(zprimal, zdual,solucao[0]):
		limitante = 1
		return
	if solucao == None:
		inviavel = 1
		return
	if inviavel == 0 and integralidade == 0:
		# Faz o calculo do criterio de ramificação e retorna a menor
		varialveEscolhida = verify(solucao[0])
		print("")
		print("Variavel escolhida")
		print(varialveEscolhida)
		# Trunca para cima
		maior = math.ceil(varialveEscolhida[0])
		# Trunca para baixo
		menor = math.floor(varialveEscolhida[0])

		print("Valor menor e Maior ")
		print(menor)
		print(maior)
		
		# Zera as variaveis que não foram escolhidas
		novaRestricao = limpaArray(varialveEscolhida[1], solucao[0])
		print("")
		print("Nova restrição")
		print(novaRestricao)
		problemaMenor = problema;
		# Restrição menor
		problemaMenor.setRestricao(1, novaRestricao, menor)

		# Restrição maior
		problemaMaior = problema
		problemaMaior.setRestricao(0, novaRestricao, maior)

		# print("")
		# print("Resultado 1")
		# print(problemaMenor.resolve2())

		print("")
		print("Resultado 2")
		print(problemaMaior.resolve2())

		
		# print("Nova restrinção")
		# print(novaRestricao)

		# # Pega valor da restricão do lado direito
		# novaRestricaoDir = menor

		# aux = problema.restricoesEsq.tolist()
		# print("")
		# print(aux)
		# aux.append(novaRestricao)
		# print("")
		# print(aux)
		# aux2 = problema.restricoesDir.tolist()
		# aux2.append(novaRestricaoDir)

		# # Cria subproblema 1
		# subprob1 = Params(problema.numVariaveis, numRestricao, problema.coefFuncObj
		# 				  ,np.double(aux), np.double(aux2), 1, 1 if MaxOrMin == "Max" else 0)
		
		# solver1 = SolverP(subprob1)
	
		# print("")
		# print("Sub problema 1")
		# print("Função objetivo")
		# print(subprob1.coefFuncObj)
		# print("Restrições Lado esquerdo")
		# print(subprob1.restricoesEsq)
		# print("Restrições Lado direito")
		# print(subprob1.restricoesDir)
		# print("Maior ou Menor")
		# print(subprob1.maiorMenor)
		# print("Max ou Min")
		# print(subprob1.maxOrMin)
		# print("-------------------------")
		# print("")
		# novaRestricaoDir = maior
		# aux2 = problema.restricoesDir.tolist()
		# aux2.append(novaRestricaoDir)

		# print("Nova restrição problema 2")
		# print(novaRestricaoDir)
		# # Cria subproblema 2
		# subprob2 = Params(problema.numVariaveis, numRestricao, problema.coefFuncObj
		# 				  ,np.double(aux), np.double(aux2), 0, 1 if MaxOrMin == "Max" else 0)
		# solver2 = SolverP(subprob2)

		# print("Sub problema 2")
		# print("Função objetivo")
		# print(subprob2.coefFuncObj)
		# print("Restrições Lado esquerdo")
		# print(subprob2.restricoesEsq)
		# print("Restrições Lado direito")
		# print(subprob2.restricoesDir)
		# print("Maior ou Menor")
		# print(subprob2.maiorMenor)
		# print("Max ou Min")
		# print(subprob2.maxOrMin)
		# print("-------------------------")
		
		# branch_bound(subprob1)
		# branch_bound(subprob2)

		# result1 = solvers.resolve(subprob1)
		
		# print(result1)
		# print(result2)
		
		# # result1 = solver.resolve(sub1)
		# solucoes = [1]
		# solucoes.append(result1.z)
		# insere(raizb, result1)
		# sub2
		# result2 = solver.resolve(sub2)
		# solucoes.append(result1.z)
		# insere(raizb, result2)
		
		# if MaxOrMin == "Max":
		# 	maiorZ = max(solucoes)
		# 	zdual = maiorZ
		# else: 
		# 	menorZ = min(solucoes)			
		# 	zprimal = menorZ
	else:
		return

path = 'Problema3.txt'
numeros = coletadados(path)

params = pegaRestricoes(numeros)

solvers = SolverP(params)

branch_bound(solvers)


# print("Fim!")
# solver =  SolverP(params)
# solver.setParams(params)
# solver.iniciaVariaveis(1)
# solver.setObjFunction(1,params.coefFuncObj)
# solver.setRestricoes(1)
# aux40 = solver
# print(solver.resolve2())
# aux40.setRestricao(1, [1,0], 2)
# solver.setRestricao(0, [1,0], 3)
# print(solver.resolve2())
# print(aux40.resolve2())
    
