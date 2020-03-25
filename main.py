# -*- coding: utf-8 -*-
"""Main Branch Bound"""

import numpy as np
from ortools.linear_solver import pywraplp

from params import Params
from solverp import SolverP

IntOrNot = False
LessMoreOrEqual = 'MoreOrEqual'

param1 = Params(20, 40, "sads", 20, "alow")

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

def resolve(IntOrNot, LessMoreOrEqual, MaxOrMin, parans):
    	solver = pywraplp.Solver('RESOLUCAO_DE_PROGRAMACAO_LINEAR', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

  	infinity = solver.infinity()
  	x = {}

	if IntOrNot == False:
		for j in range(int(parans.numVariaveis)):
			x[j] = solver.NumVar(0, infinity, 'x[%i]' % j)
	else:
		for j in range(int(parans.numVariaveis)):
			x[j] = solver.IntVar(0, infinity, 'x[%i]' % j)

	solucao = []
	if LessMoreOrEqual == 'LessOrEqual':
		for i in range(int(parans.numRestricoes)):

		   constraint = solver.RowConstraint(0, parans.restricoesDir[i], '')

		   for j in range(int(parans.numVariaveis)):

			  constraint.SetCoefficient(x[j], parans.restricoesEsq[i][j])

	if LessMoreOrEqual == 'MoreOrEqual':
		for i in range(int(parans.numRestricoes)):
		  constraint = solver.RowConstraint(parans.restricoesDir[i], infinity, '')
		  for j in range(int(parans.numVariaveis)):
		    constraint.SetCoefficient(x[j], parans.restricoesEsq[i][j])

	
	objective = solver.Objective()

	for j in range(int(parans.numVariaveis)):
		objective.SetCoefficient(x[j], parans.coefFuncObj[j])
	  
	if MaxOrMin == 'Max':
		objective.SetMaximization()
	else:
		objective.SetMinimization()

	status = solver.Solve()
	print('\n------------ RESPOSTA ------------\n')
	if status == pywraplp.Solver.OPTIMAL:
		print('VALOR OTIMO = {}'.format( solver.Objective().Value()))
		for j in range(int(parans.numVariaveis)):
			solucao.append(x[j].solution_value()) 
			print(' {}  = {}'.format(x[j].name(),x[j].solution_value()))
		print('\n------------ INFO ADICIONAIS ------------\n')
		print('PROBLEMA SOLUCIONADO EM {} MILESEGUNDOS'.format(solver.wall_time()))
		print('PROBLEMA SOLUCIONADO EM {} INTERACOES'.format(1+solver.iterations()))
	elif status == pywraplp.Solver.INFEASIBLE:
		print('PROBLEMA INVIAVEL')
	elif status == pywraplp.Solver.UNBOUNDED:
		print('PROBLEMA ILIMITADO')
  	else:
		print('NAO TEM SOLUCAO OTIMA')
	return solucao, solver.Objective().Value()


path = 'Problema3.txt'
numeros = coletadados(path)

params = pegaRestricoes(numeros)

solver =  SolverP()
solver.setParams(params)
solver.iniciaVariaveis(1)
solver.setObjFunction(1,params.coefFuncObj)
solver.setRestricoes(1)
# solver.setRestricao(1, [1, 0], 3)
solver.resolve()

# print("\n------------ PRIMAL ------------")
# print(MaxOrMin)
# print('F.O: {}'.format( params.coefFuncObj))
# print('Sujeito a :')
# print('RESTRICAO LADO ESQUERDO:\n {}'.format(params.restricoesEsq))
# print('RESTRICOES LADO DIREITO:\n {}'.format(params.restricoesDir))

zprimal = 0
zdual = 0

if (MaxOrMin == 'Max'):
    zdual = 0
    zprimal = -1
else:
    zdual = -1
    zprimal = 0

def integralidade(array):
    for i in array:
        if(isinstance(i, int) != True):
            return False
    return True

def limitante(zPrimal, zDual, z):
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




    
