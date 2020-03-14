# -*- coding: utf-8 -*-


"""Dupla: Josué de Paiva Bernardino
	  Thomas Ribeiro de Araujo"""
"""Como executar código:
	Primeiro é preciso instalar os módulos numpy e ortools utilizando o pip
	executando o seguinte comando: pip install numpy & pip install ortools.
	Logo em seguinda ir no terminal na basta do arquivo e executar python projeto1PO.py
"""

import numpy as np
from ortools.linear_solver import pywraplp

IntOrNot = False
LessMoreOrEqual = 'MoreOrEqual'

MAXORMIM = input('\nO PROBLEMA É DE ? \n[MAXIMIZACAO] - 1 \n[MINIMIZACAO] - 2\nDigite: ')
if MAXORMIM ==  2:
	MaxOrMin = 'Min'
else:
    MaxOrMin = 'Max'

class Params:
    def __init__(self, numVariaveis, numRestricoes, coefFuncObj, restricoesEsq, restricoesDir):
        self.numVariaveis = numVariaveis
        self.numRestricoes = numRestricoes
        self.coefFuncObj = coefFuncObj
        self.restricoesEsq = restricoesEsq
        self.restricoesDir = restricoesDir
 
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

	flagFOLGA_EXECESSO = True
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
		flagFOLGA_EXECESSO = False
		print('PROBLEMA INVIAVEL')
	elif status == pywraplp.Solver.UNBOUNDED:
		flagFOLGA_EXECESSO = False
		print('PROBLEMA ILIMITADO')
  	else:
		flagFOLGA_EXECESSO = False
		print('NAO TEM SOLUCAO OTIMA')
	return solucao,flagFOLGA_EXECESSO
	

def folga_execesso(solucao, restricoesEsq, restricoesDir):
  folga_execesso=[]
  
  somatorio = 0
  for i in range(0, len(restricoesEsq)): 
    for j in range(0, len(restricoesEsq[i])): 
      somatorio = somatorio + restricoesEsq[i][j]*solucao[j] 

    somatorio = abs(abs(somatorio) - abs(restricoesDir[i])) 
    folga_execesso.append(somatorio)
    somatorio = 0
  
  return folga_execesso



def folgas_complementares (solucao, folga_execesso):
  print("\n------------ X* x Y* ------------")
  complemento = []
  tamsolucao = len(solucao)
  tamfolga = len(folga_execesso)

  print(solucao)

  if tamsolucao == tamfolga:
	  for i in range (len(folga_execesso)):
		complemento.append(solucao[i]*folga_execesso[i])
  elif tamsolucao > tamfolga:
	falta = tamsolucao - tamfolga
	for i in range(falta):
		folga_execesso.append(0)

	for i in range (len(folga_execesso)):
			complemento.append(solucao[i]*folga_execesso[i])
  elif tamsolucao < tamfolga:
	falta = tamfolga - tamsolucao
	for i in range(falta):
		solucao.append(0)

	for i in range (len(folga_execesso)):
			complemento.append(solucao[i]*folga_execesso[i])

  return complemento


path = 'Problema.txt'
numeros = coletadados(path)

params = pegaRestricoes(numeros)

print("\n------------ PRIMAL ------------")
print(MaxOrMin)
print('F.O: {}'.format( params.coefFuncObj))
print('Sujeito a :')
print('RESTRICAO LADO ESQUERDO:\n {}'.format(params.restricoesEsq))
print('RESTRICOES LADO DIREITO:\n {}'.format(params.restricoesDir))
solucao , flagFOLGA_EXECESSO= resolve(IntOrNot, LessMoreOrEqual, MaxOrMin, params)


if( flagFOLGA_EXECESSO != False):
	variaveis= folga_execesso(solucao, params.restricoesEsq, params.restricoesDir)
	if(MaxOrMin=='Max'):
		print('\n------------ VARIAVEIS DE EXECESSO ------------')
		cont=1
		for i in variaveis:	
			print(" X[{}] = {} ".format(cont+int(params.numVariaveis),i))
			cont=cont+1 
	else:
		print('\n------------ VARIAVEIS DE FOLGA ------------')
		cont=1
		for i in variaveis:	
			print(" X[{}] = {} ".format(cont+int(params.numVariaveis),i))
			cont=cont+1
	complemento = folgas_complementares(solucao,variaveis)
	
	cont=0
	
	for j in complemento:
		print(j)
		print('x*[{}] * y*[{}] = {}'.format(cont,cont,j))
		cont=cont+1


"""Pegar valores para o dual"""
restesqT = np.transpose(params.restricoesEsq)
restdirT =  params.coefFuncObj
coefOBj = params.restricoesDir
numVAR =params.numRestricoes
numRESTR =params.numVariaveis

paransDual = Params(numVAR,numRESTR , np.double(coefOBj),np.double(restesqT)  ,np.double(restdirT))

IntOrNot = False
LessMoreOrEqual = 'LessOrEqual'
if (MaxOrMin == 'Max'):
    MaxOrMin = 'Mim'
else:
    MaxOrMin = 'Max'
print("\n\n------------ DUAL ------------\n")
print(MaxOrMin)
print('F.O: {}'.format(coefOBj) )
print('Sujeito a :')
print('RESTRICAO LADO ESQUERDO:\n {}'.format(restesqT))
print('RESTRICOES LADO DIREITO:\n {}'.format(restdirT))

solucao,flagFOLGA_EXECESSO=resolve(IntOrNot, LessMoreOrEqual, MaxOrMin, paransDual)

if( flagFOLGA_EXECESSO != False):
	variaveis= folga_execesso(solucao, restesqT, restdirT)


	if(MaxOrMin=='Max'):
		print('\n------------ VARIAVEIS DE EXECESSO ------------')
		cont=1
		for i in variaveis:	
			print(" X[{}] = {} ".format(cont+int(numVAR),i))
			cont=cont+1 
	else:
		print('\n------------ VARIAVEIS DE FOLGA ------------')
		cont=1
		for i in variaveis:	
			print(" X[{}] = {} ".format(cont+int(numVAR),i))
			cont=cont+1 
	complemento = folgas_complementares(solucao,variaveis)
	
	cont=0
	
	for j in complemento:
		print('x*[{}] * y*[{}] = {}'.format(cont,cont,j))
		cont=cont+1
