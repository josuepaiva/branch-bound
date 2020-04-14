
##
##         RASCUNHO
##          PSEUDO

# -*- coding: utf-8 -*-
import math

zdual = -1
zprimal = -1
interacoes = 0

tipo = false

MaxOrMin = 'Min'
MaxOrMin = 'Max'

if(MaxOrMin == 'Min'):
    tipo = true
 else:
     tipo = false

class Pli:
    def __init__(self, coefFuncObj, restricoesEsq, restricoesDir):
        self.coefFuncObj = coefFuncObj
        self.restricoesEsq = restricoesEsq
        self.restricoesDir = restricoesDir

class OrtoolsPli:
    def __init__(self, pli):
        self.pli = pli
    
    def montar():
        print("monta pli")

class NoArvore:

    def __init__(self, pli=None, esquerda=None, direita=None, zprimal, zdual):
        self.pli = pli
        self.esquerda = esquerda
        self.direita = direita
        self.zprimal =  zprimal
        self.zdual = zdual

    def __repr__(self):
        return '%s <- %s -> %s' % (self.esquerda and self.esquerda.pli,  
                                    self.pli, 
                                    self.direita and self.direita.pli)

    def resolve(PLI pli):
        print("resolve")

    """retorna o valor mais próximo de 0,5 entre duas variáveis"""
    def verify(xi, xj):
        value1 = abs(0.5 - xi)
        value2 = abs(0.5 - xj)

        if(value1 < value2):
            return xi
        else:
            return xj

    def truncaCima(x):
        return math.ceil(x)

    def truncaBaixo(x):
        return math.floor(x)

    def ramificacao(pli):
        novono = NoArvore(pli)
        novono.esquerda = None
        raiz.direita  = None

funcobj = [2,3,5]
restricoesEsq = [2,3,5]
restricoesDir = [2,3,5]

primeiraRlx = resolve(params)
variaveis e o z

pli = Pli(funcobj, restricoesEsq, restricoesDir)


def integralidade(xi, xj):
    if(isinstance(xi, int)):
        if(isinstance(xj, int)):
            return true
    return false

def inviabilidade():
    """checa se a solução é inviável"""

def limitante(valorPrimal, valorDual, z):
    if(MAX):
        if(z < valorPrimal):
            return true
        else:
            return false
    else:
        if(z < valorDual):
            return true
        else:
            return false

def atualizaPrimal(x):
    print("atualiza primal")

def atualizaDual(x):
    print("atualiza dual")

while(true):
    """resolve pli"""
    """compara pli"""
    """ramifica pli"""
    """checka se final"""


print("Arvore: ", raiz)