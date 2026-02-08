from Cellule import Cellule
from math import sqrt
from Except.GrilleError import GrilleError

# INFORMATION :
# Zone est constituée de Cellules
# Elle est encodé comme ceci :
# [c0,c1,c3
#  c4,c5,c6
#  c7,c8,c9]
# Pour une size de 3
# Taille par défaut : 3
class Zone:
    
    def __init__(self, zone : list[Cellule] = [], size : int = -1):
        if len(zone)>0:                                                 # Vérification du paramètre zone
            self.__zone : list[Cellule] = zone.clone()
        else:
            self.__zone=[]
            for _ in range (9):
                self.__zone.append(Cellule())
        if (size != -1):                                                # Vérification du paramètre size
            tmp = size
        else:
            tmp = sqrt(len(self.__zone))
        if (tmp % 1) == 0:                                              # Vérification de la cohérence de la size
            self.__size : int = tmp
        else:
            raise(GrilleError("Zone : Taille de la zone incorrect !"))
    
    def getSize(self) -> int:
        return self.__size()
    
    # Renvoie la ligne index de la zone
    # /!\ Attention /!\ l'index commence à 0
    def getRow(self, index : int) -> list[int]:
        out = []
        for i in range (self.__size):
            myi = index*self.__size+i
            if myi >=len(self.__zone):
                Error="Essaie d'accès à un index inexistant ("+str(myi)+") imax = "+str(len(self.__zone)-1)
                raise(GrilleError("Zone : getRow ->"+Error))
            out.append(self.zone[myi].getValue())
        return out
    
    # Renvoie la colonne index de la zone
    # /!\ Attention /!\ l'index commence à 0
    def getColumn(self, index : int) -> list[int]:
        out = []
        for i in range (self.__size):
            myi = index+(i*self.__size)
            if myi >=len(self.__zone):
                Error="Essaie d'accès à un index inexistant ("+str(myi)+") imax = "+str(len(self.__zone)-1)
                raise(GrilleError("Zone : getColum ->"+Error))
            out.append(self.zone[myi].getValue())
        return out
    
    # Renvoie la cellule aux coords row,col
    # /!\ La cellule N'EST PAS une copie /!\
    def getCelluleCoord(self, row : int, col : int) -> Cellule:
        myi = row*self.__size+col
        if myi>=len(self.__zone):
            Error="Essaie d'accès à une cellule inexistante ("+str(myi)+") max = "+str(len(self.__zone)-1)
            raise(GrilleError("Zone : getCelluleCoord ->"+Error))
        return self.__zone(myi)
    
    # Renvoie la cellule à l'index index
    # /!\ La cellule N'EST PAS une copie /!\
    def getCelluleIndex(self, index : int) -> Cellule:
        myi = index
        if myi>=len(self.__zone):
            Error="Essaie d'accès à une cellule inexistante ("+str(myi)+") max = "+str(len(self.__zone)-1)
            raise(GrilleError("Zone : getCelluleCoord ->"+Error))
        return self.__zone(myi)
    
    # Retourne un tableau contenant la liste des valeurs dans la zone
    def getValues(self) -> list[int]:
        out=[]
        for e in self.__zone:
            out.append(e.getValue())
        return out
    
    # Retourne la liste des valeurs de la zone
    # Info : La liste peut contientir des 0
    def containsValue(self, value : int) -> bool:
        return value in self.getValues()
    
    # Ajuste les candidats d'une cellule
    def adjustCandidates(cellule : Cellule, imp : list[int]) -> None: #inutile / superflu
        # Note : Nécessité de discuter avec Ilan afin de parler de la pertinence de cette fonction
        pass
    
    # Renvoie un clone de l'objet courant Zone
    def clone(self):# -> Zone (Erreur lors de la compilation)
        NewZone=[]
        for e in self.zone: # Ajouts des cellules cloné dans une liste
            NewZone.append(e.clone())
        return Zone(NewZone, self.__size)
    
    def toString(self) -> str:
        size = len(self.__zone)
        s = "["
        for i in range(size):
            s +=self.__zone[i].toString()
            if (i!=size-1):
                s+= ", "
        s += "]"
        return s