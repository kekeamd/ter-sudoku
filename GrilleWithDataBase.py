from Grille import Grille
#from GrilleBacktrack import GrilleBacktrack
from Cellule import Cellule
from Zone import Zone
import Parser as p
from FileInteraction import FileInteraction
from Except.GrilleError import GrilleError
from random import randint
from GrilleUtils import *
from Difficulte import Difficulte

class GrilleWithDataBase(Grille):
    
    # Probablement pas le bon constructeur A MODIFIER
    def __init__(self, sizeCote : int = 3, zoneList : list[Zone] = []):
        if zoneList==[]:
            for _ in range(sizeCote**2):
                zoneList.append(Zone(size=sizeCote))
        super().__init__(zoneList,sizeCote)
        self._parser = p.Parser()

    # A IMPLEMENTER !
    def generateValues(self, difficulte : Difficulte) -> None:
        pass

    # Fais une rotation de la grille
    # way -> 'D' ou 'G', définira le sens de rotation
    # nbRot définira le nombre de rotation que l'on souhaite effectuer
    def rotate(self,way : chr = 'D', nbRot : int = 1) -> None:
        if way != 'D' and way != 'G':
            error = "Mauvaise utilisation : "+way+" & ATTENDU : 'D' ou 'G'"
            raise(GrilleError("GrilleWithDataBase : rotate ->",error))
        elif nbRot <0:
            if way == 'D':
                way = 'G'
            else:
                way = 'D'
        elif nbRot > 0:
            Iway = 1 if way == 'D' else 0
            nbRot = nbRot%4
            save : Grille = self.clone()
            for i in range (self._size**4):
                newIndex=i
                for _ in range(nbRot):
                    newIndex=self._indexOfRotate(newIndex,Iway)
                self.setCelluleValueIndex(newIndex,save.getCelluleValueIndex(i))
                self._getCelluleIndex(newIndex).setCandidates(save.getCelluleCandidatesIndex(i))

    # flip la grille de manière symétrique
    # l'axe de symétrie est déterminer de cette manière :
    # 0 -> verticale
    # 1 -> horizontale
    # 2 -> diagonale Gauche NON IMPLEMENTER
    # 3 -> diagonale Droit NON IMPLEMENTER
    def flip(self,sym : int = 0) -> None:
        if not(sym in [0,1,2,3]):
            error = "Mauvaise utilisation : "+sym+" & ATTENDU : (0 -> verticale) | (1 -> horizontale) | (2 -> diagonale Gauche) | (3 -> diagonale Droit)"
            raise(GrilleError("GrilleWithDataBase : flip ->",error))
        else:
            save = self.clone()
            for i in range(self._size**4):
                if sym==0 or sym==1:
                    newIndex=self._flipIndexClassic(i,sym)
                else:
                    newIndex=self._flipIndexAdvanced(i,sym)
                self.setCelluleValueIndex(newIndex,save.getCelluleCandidatesIndex(i))
                self._getCelluleIndex(newIndex).setCandidates(save.getCelluleCandidatesIndex(i))

    # fais un changement de nombre dans la grille
    # replace tous les numberToReplace par newNumber
    # Si pas défini ou avec un nombre négatif prendra un nombre aléatoire
    def changeNumber(self,numberToReplace : int = -1, newNumber : int = -1) -> None:
        size = (self._size**2)-1
        while(numberToReplace<0 or numberToReplace==newNumber):
            numberToReplace = randint(1,size)
        while(newNumber<0):
            newNumber = randint(1,size)
        if newNumber>size or numberToReplace>size:
            error ="Mauvaise utilisation : numberToReplace = "+numberToReplace+" , newNumber ="+newNumber+" & ATTENDU : >0 & <="+size
            raise("GrilleWithDataBase : changeNumber ->",error)
        else:
            pass

    # Pas sûr que cette methode doit être ici ?
    # Vérifie à quel point 2 grilles sont similaires
    # Ici on va vérifier : 
    # - le nomre de Cellule vide qui ont le même emplacement (sameEmtpyCell)
    # - le nombre de Cellule qui ont le même nombre au même endroit (sameNumber)
    # - le nombre de Cellule qui ont la même valeur (sameEmtpyCell + sameNumber = sim)
    # strict va déterminer la condition d'acceptation :
    # True -> respect de sameEmptyCell ET sameNumber
    # False -> respect de sim
    def verifSame(toCompare : Grille, sameEmptyCell : int, sameNumber : int, strict : bool = True) -> bool:
        sim = sameEmptyCell + sameNumber
        emptyCellCount = 0
        numberCount = 0
        # Contenu
        if strict:
            return (emptyCellCount<=sameEmptyCell and numberCount<=sameNumber)
        else:
            return (emptyCellCount+numberCount)<=sim

    # Renvoie l'index absolu d'une cellule après 1 rotation
    # Rotation Droite si way = 1 sinon Gauche
    def _indexOfRotate(self,index : int, way : int = 1) -> int:
        size=self._size**2-1
        rowIndex=rowIndexFromCelluleIndex(index,self._size)
        colIndex=columnIndexFromCelluleIndex(index,self._size)
        if (size+1)%2!=0 and (rowIndex==(size/2)) or (colIndex==(size/2)): # On est dans des cases qui ne changent pas !
            return index
        elif (rowIndex <= size/2) and way==1:   # Partie haute de la grille si way==1 sinon basse
            if (colIndex <= size/2):            # Côté Gauche
                return (rowIndex*size)+size-colIndex
            else:                               # Côté Droit
                return (size-rowIndex)*size+colIndex
        else:                                   # Partie basse de la Grille si way==1 sinon haute
            if (colIndex <= size/2):            # Côté Gauche
                return (size-rowIndex)*size+colIndex
            else:                               # Côté Droit
                return (rowIndex*size)+size-colIndex
    
    # Renvoie l'index de la nouvelle cellule suite à une symétrie
    # Gère uniquement cas 0 et 1
    def _flipIndexClassic(self,index : int, sym : int) -> int:
        size=self._size**2-1
        rowIndex=rowIndexFromCelluleIndex(index,self._size)
        colIndex=columnIndexFromCelluleIndex(index,self._size)
        if (size+1)%2!=0 and (rowIndex==(size/2)) or (colIndex==(size/2)): # On est dans des cases qui ne changent pas !
            return index
        elif sym==0:                                        # Axe de symétrie verticale
            return (rowIndex*size)+size-colIndex
        elif sym==1:                                        # Axe de symétrie horizontale
            return (size-rowIndex)*size+colIndex
        else:
            raise(GrilleError("GrilleWithDataBase : _flipIndexClassic -> cas non géré ! sym =",str(sym)))
    
    # Renvoie l'index de la nouvelle cellule suite à une symétrie
    # Gère uniquement cas 2 et 3
    def _flipIndexAdvanced(self,index : int, sym : int) -> int:
        size=self._size**2-1
        rowIndex=rowIndexFromCelluleIndex(index,self._size)
        colIndex=columnIndexFromCelluleIndex(index,self._size)
        if (size+1)%2!=0 and rowIndex==(size//2) and colIndex==(size//2): # Case du milieu, son index ne change jamais
            return index
        elif sym==2:                                        # Axe de symétrie diagonale gauche
            if rowIndex==colIndex: # On est dans des cases qui ne changent pas !
                return index
            else:
                return (colIndex*size)+rowIndex
        elif sym==3:                                        # Axe de symétrie diagonale droit
            if rowIndex!=colIndex and (rowIndex+colIndex)==size: # On est dans des cases qui ne changent pas !
                return index
            else:
                return (size-colIndex)*size+size-rowIndex
        else:
            raise(GrilleError("GrilleWithDataBase : _flipIndexAdvanced -> cas non géré ! sym =",str(sym)))
    
    def clone(self):# -> GrilleBacktrack
        newGrille = []
        for i in range(self._size**2):
            newGrille.append(self._grille[i].clone())
        return GrilleWithDataBase(newGrille, self._size)