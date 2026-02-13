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
# Taille par défaut (Si la zone est vide) : 3
# Si la zone n'est pas vide la taille par défaut est sqrt de len de la zone
# Si une liste vide ainsi qu'une taille sont données, alors le résultat sera une zone de taille taille vide
class Zone:
    
    def __init__(self, zone : list[Cellule] = [], size : int = -1):
        self.__zone : list[Cellule]= []
        if len(zone)>0:                                                   # Vérification du paramètre zone
            for e in zone:
                self.__zone.append(e.clone())
        if (size != -1):                                                  # Vérification du paramètre size
            tmp = size
        elif (len(zone)==0):
            tmp = 3
        else:
            tmp = sqrt(len(self.__zone))
        if (tmp % 1) == 0 and ((tmp*tmp)<=len(self.__zone) or zone==[]) and tmp>=0:     # Vérification de la cohérence de la size
            self.__size : int = int(tmp)
            if self.__zone==[]:                                           # Dans le cas ou on a un tableau vide mais une taille >0
                for _ in range (self.__size*self.__size):
                    self.__zone.append(Cellule())
        else:
            raise(GrilleError("Zone : Taille de la zone incorrect !"))
    
    def getSize(self) -> int:
        return self.__size
    
    # Renvoie la ligne row de la zone
    # /!\ Attention /!\ row commence à 0
    def getRow(self, row : int) -> list[int]:
        out = []
        for i in range (self.__size):
            myi = row*self.__size+i
            if myi >=len(self.__zone) or row<0 or row>=self.__size:
                Error="Essaie d'accès à une row inexistante ("+str(myi)+") imax = "+str(len(self.__zone)-1)
                raise(GrilleError("Zone : getRow ->"+Error))
            out.append(self.__zone[myi].getValue())
        return out
    
    # Renvoie la colonne column de la zone
    # /!\ Attention /!\ column commence à 0
    def getColumn(self, column : int) -> list[int]:
        out = []
        for i in range (self.__size):
            myi = column+(i*self.__size)
            if myi >=len(self.__zone) or column<0 or column>=self.__size:
                Error="Essaie d'accès à une column inexistante ("+str(myi)+") imax = "+str(len(self.__zone)-1)
                raise(GrilleError("Zone : getColumn ->"+Error))
            out.append(self.__zone[myi].getValue())
        return out
    
    # Renvoie la cellule aux coords row,column
    # /!\ La cellule N'EST PAS une copie /!\
    def getCelluleCoord(self, row : int, column : int) -> Cellule:
        myi = row*self.__size+column
        if myi>=len(self.__zone) or (row<0) or (column<0) or (row>=self.__size) or (column>=self.__size):
            Error="Essaie d'accès à une cellule inexistante ("+str(myi)+") max = "+str(len(self.__zone)-1)
            raise(GrilleError("Zone : getCelluleCoord ->"+Error))
        return self.__zone[myi]
    
    # Renvoie la cellule à l'index index
    # /!\ La cellule N'EST PAS une copie /!\
    def getCelluleIndex(self, index : int) -> Cellule:
        myi = index
        if myi>=len(self.__zone) or index<0:
            Error="Essaie d'accès à une cellule inexistante ("+str(myi)+") max = "+str(len(self.__zone)-1)
            raise(GrilleError("Zone : getCelluleCoord ->"+Error))
        return self.__zone[myi]
    
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
    
    
    # Renvoie un clone de l'objet courant Zone
    def clone(self):# -> Zone (Erreur lors de la compilation)
        NewZone=[]
        for e in self.__zone: # Ajouts des cellules cloné dans une liste
            NewZone.append(e.clone())
        return Zone(NewZone, self.__size)
    
    """ Va être utilisé ?
    def toString(self) -> str:
        size = len(self.__zone)
        s = "["
        for i in range(size):
            s +=self.__zone[i].toString()
            if (i!=size-1):
                s+= ", "
        s += "]"
        return s
    """