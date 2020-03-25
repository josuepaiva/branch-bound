class Pli:
    def __init__(self, coefFuncObj, restricoesEsq, restricoesDir, objetivo):
        self.coefFuncObj = coefFuncObj
        self.restricoesEsq = restricoesEsq
        self.restricoesDir = restricoesDir
        self.objetivo = objetivo
    
    def addRestricao(self, restricoesDir, restricoesEsq ):
        self.restricoesDir.append(restricoesDir)
        self.restricoesEsq.append(restricoesEsq)

