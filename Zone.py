from Cellule import Cellule

class Zone:
    
    def __init__(self, zone : list[Cellule] = [], size : int = -1):
        self.zone = zone # Voir si il y a pas un problème avec les copies de pointeurs...
        self.size = size
    
    def getSize(self) -> int:
        return self.taille()
    
    def getRow(self, index : int) -> list[int]:
        return []
    
    def getColumn(self, index : int) -> list[int]:
        return []
    
    def getCelluleCoord(self, row : int, col : int) -> Cellule:
        return None
    
    def getCelluleIndex(self, index : int) -> Cellule:
        return None
    
    def getValues(self) -> list[int]:
        return []
    
    def containValue(self, value : int) -> bool:
        return False
    
    def AjustCandidate(cellule : Cellule, imp : list[int]) -> None:
        pass
    
    def clone(self):# -> Zone
        return Zone()