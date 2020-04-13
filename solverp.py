# -*- coding: utf-8 -*-

from ortools.linear_solver import pywraplp

class SolverP:
    def __init__(self, parans=None, solver=None, infinity=None, x=None, objective=None):
        self.solver = pywraplp.Solver('RESOLUCAO_DE_PROGRAMACAO_LINEAR', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
        self.infinity = self.solver.infinity()
        self.x = {}
        self.objective =  self.solver.Objective()
        self.parans = parans

        self.iniciaVariaveis(1)
        self.setRestricoes(self.parans.maiorMenor)
        self.setObjFunction(self.parans.maxOrMin, self.parans.coefFuncObj)

    def iniciaVariaveis(self, IntOrNot):
        # Se for 1 cria variáveis reais
        if IntOrNot:
            for j in range(int(self.parans.numVariaveis)):
                self.x[j] = self.solver.NumVar(0, self.infinity, 'x[%i]' % j)
        else:
            for j in range(int(self.parans.numVariaveis)):
                self.x[j] = self.solver.IntVar(0, self.infinity, 'x[%i]' % j)

    # Seta as restrições do lado direito e esquerdo
    def setRestricoes(self, LessMoreOrEqual):
        # Se for 1 é <= caso contrário >=
        if LessMoreOrEqual:
            # print("menor ou igual")
            for i in range(int(self.parans.numRestricoes)):
                constraint = self.solver.Constraint(-self.solver.infinity(), self.parans.restricoesDir[i])
                for j in range(int(self.parans.numVariaveis)):
                    constraint.SetCoefficient(self.x[j], self.parans.restricoesEsq[i][j])
        else:
            # print("maior ou igual")
            for i in range(int(self.parans.numRestricoes)):
                constraint = self.solver.Constraint(self.parans.restricoesDir[i], self.solver.infinity())
                for j in range(int(self.parans.numVariaveis)):
                    constraint.SetCoefficient(self.x[j], self.parans.restricoesEsq[i][j])
    
    def setRestricao(self, LessMoreOrEqual, restricaoCof, valor):
        # Se for 1 é <= caso contrário >=
        # Coef devem ser um array tipo [1 0 0 0] onde 1 indica que aquela variavel vai ter valor 1
        if LessMoreOrEqual:
            constraint = self.solver.Constraint(-self.solver.infinity(), valor)
            for i in range(int(self.parans.numVariaveis)):
                constraint.SetCoefficient(self.x[i], restricaoCof[i])
        else:
            constraint = self.solver.Constraint(valor, self.solver.infinity())
            for i in range(int(self.parans.numVariaveis)):
                constraint.SetCoefficient(self.x[i], restricaoCof[i])
            
    # Seta a função objetivo 
    def setObjFunction(self, maxormin, funcObj):
        for j in range(int(self.parans.numVariaveis)):
            self.objective.SetCoefficient(self.x[j], funcObj[j])
            # 1 para Maximizar e 0 Minimizar"""
        if maxormin:
            self.objective.SetMaximization()
        else:
            self.objective.SetMinimization()

    def setParams(self, params):
        self.parans = params

    def getParams(self):
        return self.parans
    
    def getSolver(self):
        return self.solver

    # Resolve o PLI                                                                                                                                                                                                                                                                                                                                                                                                             
    def resolve2(self):

        status = self.solver.Solve()
        solucao = []                                                
        if(status == pywraplp.Solver.OPTIMAL):
            # print('VALOR OTIMO = {}'.format( self.solver.Objective().Value()))
            for j in range(int(self.parans.numVariaveis)):
                solucao.append(self.x[j].solution_value()) 
                # print(' {}  = {}'.format(self.x[j].name(),self.x[j].solution_value()))                                      
                # print('\n------------ INFO ADICIONAIS ------------\n')
                # print('PROBLEMA SOLUCIONADO EM {} MILESEGUNDOS'.format(self.solver.wall_time()))
                # print('PROBLEMA SOLUCIONADO EM {} INTERACOES'.format(1+self.solver.iterations()))
        elif status == pywraplp.Solver.INFEASIBLE:
            print('PROBLEMA INVIAVEL')
        elif status == pywraplp.Solver.UNBOUNDED:
            print('PROBLEMA ILIMITADO')
        else:
            print('NAO TEM SOLUCAO OTIMA')
        return solucao, self.solver.Objective().Value()
    
    def resolve(self, problema):
        numVariaveis = problema.numVariaveis
        numRestricoes = problema.numRestricoes
        coefFuncObj = problema.coefFuncObj
        restricoesEsq = problema.restricoesEsq
        restricoesDir = problema.restricoesDir

        self.setParams(problema)
        self.iniciaVariaveis(1)
        self.setRestricoes(problema.maiorMenor)
        self.setObjFunction(problema.maxOrMin, coefFuncObj)

        status = self.solver.Solve()
        solucao = []                                                
        if(status == pywraplp.Solver.OPTIMAL):
            # print('VALOR OTIMO = {}'.format( self.solver.Objective().Value()))
            for j in range(int(self.parans.numVariaveis)):
                solucao.append(self.x[j].solution_value()) 
                print(' {}  = {}'.format(self.x[j].name(),self.x[j].solution_value()))                                      
                # print('\n------------ INFO ADICIONAIS ------------\n')
                # print('PROBLEMA SOLUCIONADO EM {} MILESEGUNDOS'.format(self.solver.wall_time()))
                # print('PROBLEMA SOLUCIONADO EM {} INTERACOES'.format(1+self.solver.iterations()))
        elif status == pywraplp.Solver.INFEASIBLE:
            print('PROBLEMA INVIAVEL')
        elif status == pywraplp.Solver.UNBOUNDED:
            print('PROBLEMA ILIMITADO')
        else:
            print('NAO TEM SOLUCAO OTIMA')

        aux = self.solver.Objective().Value()
        self.solver = pywraplp.Solver('RESOLUCAO_DE_PROGRAMACAO_LINEAR', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
        self.infinity = self.solver.infinity()
        self.x = {}
        self.objective =  self.solver.Objective()
        self.parans = {}
        return solucao, aux
    def resolvesub(self):
        print("sub solver")