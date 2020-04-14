class Params:
    def __init__(self, numVariaveis, numRestricoes, coefFuncObj, restricoesEsq, restricoesDir, maiorMenor=None, maxOrMin=None):
        self.numVariaveis = numVariaveis
        self.numRestricoes = numRestricoes
        self.coefFuncObj = coefFuncObj
        self.restricoesEsq = restricoesEsq
        self.restricoesDir = restricoesDir
        self.maiorMenor = maiorMenor
        self.maxOrMin = maxOrMin

    def setRestricoesEsq(self, restricoesEsq):
        self.restricoesEsq = restricoesEsq
    
    def setRestricoesDir(self, restricoesDir):
        self.restricoesDir = restricoesDir

    def getRestricoesEsq(self):
        return self.restricoesEsq
    
    def getRestricoesDir(self):
        return self.restricoesDir
    
    def getMaiorMenor(self):
        return self.maiorMenor
    
    def setMaiorMenor(self, maior):
        self.maior = maior

    def getMaxOrMin(self):
        return self.maxOrMin
        
    def setMaxOrMin(self, maxorMi):
        self.maxOrMin = maxorMi
