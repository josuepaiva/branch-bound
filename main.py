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
LessMoreOrEqual = 'MoreOrEqual'
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
    	global zdual
	if(MaxOrMin == 'Max'):
		if(z > zDual):
			return True
		else:
			return False
	else:
		if(z < zDual):
			zdual = z
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
	value = -1

	for i in range(0,len(array)):
		aux = abs(0.5 - array[i])
		print(aux)
		if aux > value:
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
		print("Solucao")
		print(solucao)

		# insere(raizb, NoBranchbound(solucao[1], solucao[0]))
	if integralidadeFunc(solucao[0]):
		integralidade = 1
		insere(raizb, NoBranchbound(solucao[1], solucao[0]))
		if zprimal < solucao[1]:
			zprimal = solucao[1]
			insere(raizb, NoBranchbound(solucao[1], solucao[0]))
			return
		return
	if checklimitante(zprimal, zdual,solucao[0]):
		limitante = 1
		insere(raizb, NoBranchbound(solucao[1], solucao[0]))
		return
	if solucao == None:
		inviavel = 1
		print("Inviável")
		return
	if inviavel == 0 and integralidade == 0:
		# Faz o calculo do criterio de ramificação e retorna a menor
		variaveis = problema.x
		
		variavelEscolhida = verify(solucao[0])
		print("")
		print("Variavel escolhida")
		print(variavelEscolhida)

		novoSolver = SolverP(problema.getParams())
		novoSolver.setRestricao(variavelEscolhida[1], 0)
		print("solver1")
		print(novoSolver.getSolver().NumConstraints())
		
		novoSolver2 = SolverP(problema.getParams())
		novoSolver2.setRestricao(variavelEscolhida[1], 1)
		print("solver2")
		print(novoSolver2.getSolver().NumConstraints())
		# solucao1 = novoSolver.resolve2()
		# solucao2 = novoSolver2.resolve2()

		# menorZ = minimo(solucao1. solucao2)

		# atualizarDual(menorZ)

		branch_bound(novoSolver)
		branch_bound(novoSolver2)

		# print("")
		# print("Resultado 1")
		# print(solucao1)

		# print("")
		# print("Resultado 2")
		# print(solucao2)

		# if integralidadeFunc(solucao[0]):
		# 	integralidade = 1
		# 	zprimal = solucao[1]
		# 	return
		# if checklimitante(zprimal, zdual,solucao[0]):
		# 	limitante = 1
		# 	return
		# if solucao == None:
		# 	inviavel = 1
		# 	return

		# if MaxOrMin == "Max":
		# 	maiorZ = max(solucoes)
		# 	zdual = maiorZ
		# else: 
		# 	menorZ = min(solucoes)			
		# 	zprimal = menorZ
	else:
		return

path = 'problemafinal.txt'
numeros = coletadados(path)

params = pegaRestricoes(numeros)


# print("Direita")
# print(params.getRestricoesDir())
# print("Esquerda")
# print(params.getRestricoesEsq())
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
# solver.setRestricao(1, [1,0], 2)
# print(solver.resolve2())
# print(aux40.resolve2())
    
