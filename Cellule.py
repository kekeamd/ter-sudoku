from Except.GrilleError import GrilleError
class Cellule:
    
    def __init__(self, value : int = 0):
        self._value : int = 0
        if value!=0:
            self.setValue(value)
        self._candidates : list[int] = []
        self._position : int = -5
    
    def getValue(self) -> int:
        return self._value

    def setValue(self, value : int) -> None:
        if value < 0:
            Error = "Valeur impossible ! ("+str(value)+")"
            raise(GrilleError("Cellule : setValue -> "+Error))
        else:
            self._value : int = value
    
    def getCandidates(self) -> list[int]:
        return self._candidates.copy()

    def setCandidates(self,candidates : list[int]) -> None:
        newCand=[]
        for e in candidates:
            if e != self._value:
                newCand.append(e)
        self._candidates=newCand

    def getPosition(self) -> int:
        return self._position

    def setPosition(self, position : int) -> None:
        if position<0:
            Error = "Position négative ! ("+str(position)+")"
            raise(GrilleError("Cellule : setPosition -> "+Error))
        elif self._position >= 0:
            Error = "Tentative de changer la position de la cellule alors qu'elle est déjà établie ! ("+str(self._position)+"->"+str(position)+")"
            raise(GrilleError("Cellule : setPosition -> "+Error))
        else:
            self._position = position

    def clone(self): # -> Cellule (Erreur lors de la compilation)
        newCellule=Cellule(self._value)
        newCellule.setCandidates(self._candidates.copy())
        newCellule.setPosition(self._position)
        return newCellule