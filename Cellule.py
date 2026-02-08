from Except.GrilleError import GrilleError
class Cellule:
    
    def __init__(self, value : int = 0):
        self.__value : int = 0
        self.setValue(value)
        self.__candidates : list[int] = []
    
    def getValue(self) -> int:
        return self.__value

    def setValue(self, value : int) -> None:
        if value < 0:
            Error = "Valeur impossible ! ("+str(value)+")"
            raise(GrilleError("Cellule : setValue -> "+Error))
        else:
            self.__value : int = value
    
    def getCandidates(self) -> list[int]:
        return self.__candidates.copy()

    def setCandidates(self,candidates : list[int]) -> None:
        newCand=[]
        for e in candidates:
            if e != self.__value:
                newCand.append(e)
        self.__candidates=newCand
    
    def clone(self): # -> Cellule (Erreur lors de la compilation)
        newCellule=Cellule(self.__value)
        newCellule.setCandidates(self.__candidates.copy())
        return newCellule
    
    def toString(self) -> str:
        if (self.__value!=0):
            return self.__value
        size = len(self.__candidates)
        s = "["
        for i in range(size):
            s +=self.__candidates[i].toString()
            if (i!=size-1):
                s+= ","
        s += "]"
        return s