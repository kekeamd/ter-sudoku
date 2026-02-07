from Cellule import Cellule

class Cellule:
    
    def __init__(self, value : int = 0):
        self.__value=value
        self.__candidates=[]
    
    def getValue(self) -> int:
        return self.__value

    def setValue(self, value : int) -> None:
        self.__value=value
    
    def getCandidates(self) -> list[int]:
        return self.__candidates.copy()

    def setCandidates(self,candidates : list[int]) -> None:
        self.__candidates=candidates.copy()
    
    def clone(self) -> Cellule: # -> Cellule (reglé en mettant import Cellule en haut)
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