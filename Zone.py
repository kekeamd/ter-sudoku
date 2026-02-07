from Cellule import Cellule
from Zone import Zone

class Zone:
    
    def __init__(self, zone : list[Cellule] = [], size : int = -1):
        self.__zone = zone # Voir si il y a pas un problème avec les copies de pointeurs...
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
    
    def containsValue(self, value : int) -> bool:
        return False
    
    def adjustCandidates(cellule : Cellule, imp : list[int]) -> None: #inutile / superflu
                                                                      #ps pour keke: oui j'ai essayé d'utiliser la fonction dans grille, mais va essayer de l'utiliser pour adjustRow et adjustCol, il faut trouver dans quel zone appartient la cellule à chaque itération...
        pass
    
    def clone(self) -> Zone:# -> Zone (réglé en mettant import Zone en haut)
        return Zone()
    
    def toString(self) -> str:
        size = len(self.__zone)
        s = "["
        for i in range(size):
            s +=self.__zone[i].toString()
            if (i!=size-1):
                s+= ", "
        s += "]"
        return s