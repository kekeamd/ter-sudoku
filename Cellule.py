class Cellule:
    
    def __init__(self, value : int = 0):
        self.value=value
        self.candiate=[]
    
    def getValue(self) -> int:
        return self.value

    def setValue(self, value : int) -> None:
        self.value=value
    
    def getCandidate(self) -> list[int]:
        return self.candiate.copy()

    def setCandidate(self,candidate : list[int]) -> None:
        self.candiate=candidate.copy()
    
    def clone(self): # -> Cellule
        newCellule=Cellule(self.value)
        newCellule.setCandidate(self.candidate)
        return newCellule