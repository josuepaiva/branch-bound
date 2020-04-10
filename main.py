# -*- coding: utf-8 -*-
"""Main Branch Bound"""

import numpy as np
import math

from ortools.linear_solver import pywraplp

from params import Params
from solverp import SolverP

IntOrNot = False
LessMoreOrEqual = 'MoreOrEqual'


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

# print(param1.testemethod())
MaxOrMin = "Max"
# MAXORMIM = input('\nO PROBLEMA É DE ? \n[MAXIMIZACAO] - 1 \n[MINIMIZACAO] - 2\nDigite: ')
# if MAXORMIM ==  2:
# 	MaxOrMin = 'Min'
# else:
#     MaxOrMin = 'Max'

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

	params = Params(numVariaveis, numRestricoes, np.double(coefFuncObj), np.double(arrayRestricoesEsquerda), np.double(arrayRestricoesDireita))

	return params

# //frags
integralidade = 0
limitante = 0
inviavel = 0

zdual = 0
zprimal = 0

if MaxOrMin == "MAX":
	zdual = 0
	zprimal = -1
else: 
	zdual = -1
	zprimal = 0

class NoBranchbound:
	def __init__(self, z, variaveis, esquerda=None, direita=None):
		self.z = z
		self.variaveis
		self.esquerda = esquerda
		self.direita = direita

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

raiz = None


def verify(array):	
	results = []

	for i in array:
		results.append(abs(0.5 - array[i]))

def min(array):
	valor = 8000000000000000

	for i in array:
		if array[i] < valor:
			valor = array[i]
	return valor
    
def branch_bound(problema1):
	if raiz is None:
		raiz = NoBranchbound(solver.resolve(problema1))
	else:
		solucao = solver.resolve(problema1)
		insere(raiz, solucao)
	
	if integralidadeFunc(solucao.variaveis):
		integralidade = 1
		zprimal = solucao.z
		return
	if checklimitante(zdual, zprimal, solucao.z):
		limitante = 1
		return
	if solucao == None:
		inviavel = 1
		return
	if inviavel == 0 and integralidade == 0:
		# Faz o calculo do criterio de ramificação
		menores = verify(solucao.variaveis)
		# Retorna a variável de menor valor
		variavel = min(menores)
		# Trunca para cima
		maior = math.ceil(variavel)
		# Trunca para baixo
		menor = math.floor(variavel)
		# Criar novo subproblema
		sub1
		result1 = solver.resolve(sub1)
		solucoes = []
		solucoes.append(result1.z)
		insere(raiz, result1)
		sub2
		result2 = solver.resolve(sub2)
		solucoes.append(result1.z)
		insere(raiz, result2)
		
		if MaxOrMin == "Max":
			maiorZ = max(solucoes)
			zdual = maiorZ
		else: 
			menorZ = min(solucoes)			
			zprimal = menorZ
		
		
		branch_bound(sub1)
		branch_bound(sub2)	
	else:
		return

path = 'Problema3.txt'
numeros = coletadados(path)

params = pegaRestricoes(numeros)

solver =  SolverP()
solver.setParams(params)
solver.iniciaVariaveis(1)
solver.setObjFunction(1,params.coefFuncObj)
solver.setRestricoes(1)


# zprimal = 0
# zdual = 0

# if (MaxOrMin == 'Max'):
#     zdual = 0
#     zprimal = -1
# else:
#     zdual = -1
#     zprimal = 0

# def integralidade(array):
#     for i in array:
#         if(isinstance(i, int) != True):
#             return False
#     return True

# def limitante(zPrimal, zDual, z):
#     if(MaxOrMin == 'Max'):
#         if(z < zPrimal):
#             return True
#         else:
#             return False
#     else:
#         if(z < zDual):
#             return True
#         else:
#             return False

# while(1):
#     solucao = resolve(IntOrNot, LessMoreOrEqual, MaxOrMin, params)
#     condicaoParada = True
    
#     if (MaxOrMin == 'Max'):
#         zdual = solucao[1]
#     else:
#         zprimal = solucao[1]

#     if(len(solucao[0]) > 0):
#         if(integralidadeso(solucao[0])):
#             print("Limitado por integralidade")
#             print("Solucao "+solucao)
        
#         if()
#     else:
#         print("Não tem solução")




    
