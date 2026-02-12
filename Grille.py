from abc import ABC, abstractmethod
from Zone import Zone
from Cellule import Cellule
from Difficulte import Difficulte
from Except.GrilleError import GrilleError
from GrilleUtils import *

#purpose: bah la grille de sudoku
#dependencies: Difficulte, Cellule ,Zone, GrilleUtils, GrilleError
class Grille(ABC):
    def __init__(self):
        self.__grille : list[Zone] = []
        self.__size : int = 3
        for _ in range(self.__size**2):
            self.__grille.append(Zone())
        self.__difficulte : Difficulte = None
    def __init__(self, zoneList : list[Zone] , sizeCote : int = 3):
        if ((sizeCote*sizeCote)!=len(zoneList) or len(zoneList) < 3):
            raise(GrilleError("Grille : deuxième argument invalide ou alors la taille de 'zoneList' est différente de la valeur par défaut (avez-vous pensé à préciser la taille?)"))
        self.__grille : list[Zone] = zoneList
        self.__size : int = sizeCote
        self.__difficulte : Difficulte = None
    

    #purpose: génère des valeurs et rempli la grille
    @abstractmethod
    def generateValues(self, difficulte : Difficulte) -> None:
        pass


    #purpose: renvoie la difficulté de la grille
    def getDifficulte(self)-> Difficulte:
        return self.__difficulte


    #purpose: défini la difficulté de la grille
    def setDifficulte(self, difficulte : Difficulte) -> None:
        self.__difficulte = difficulte

    
    #purpose: renvoie la taille du côté de la grille
    def getSize(self) -> int:
        return self.__size


    #purpose: renvoie la ligne numéro 'row'
    def getRow(self, row : int) -> list[int]: #row commence à 0
        rowValues = []
        for i in range(self.__size):
            zone = self.__grille[indexOfFirstZoneInRow(row, self.__size) + i] #avec i qui sert d'offset par rapport à la première zone de la ligne
            rowValues+= zone.getRow(indexRowOrColumnInZone(row, self.__size)) #on on concatène la liste de valeurs actuel avec la liste de valeurs dans la ligne de 'zone'
        return rowValues


    #purpose: renvoie la colonne numéro 'column'
    def getColumn(self, column : int) -> list[int]:
        colValues = []
        for i in range(self.__size):
            zone = self.__grille[indexOfFirstZoneInColumn(column, self.__size) + self.__size*i] #avec size*i qui sert d'offset par rapport à la première zone de la colonne
            colValues+= zone.getColumn(indexRowOrColumnInZone(column, self.__size)) #on on concatène la liste de valeurs actuel avec la liste de valeurs dans la colonne de 'zone'
        return colValues


    #purpose: renvoie vrai si la ligne numéro 'row' contient la valeur 'value' et faux sinon
    def rowContainsValue(self, row : int, value : int) ->  bool:
        return value in self.getRow(row)


    #purpose: renvoie vrai si la colonne numéro 'column' contient la valeur 'value' et faux sinon
    def columnContainsValue(self, column: int, value : int) ->  bool:
        return value in self.getColumn(column)


    #purpose : renvoie la cellule aux coordonnées ('row', 'column')
    def __getCelluleCoord(self, row : int, column : int) -> Cellule:
        zone = self.__grille[indexOfZone(row, column, self.__size)]
        cellule = zone.getCelluleCoord(row, column)
        return cellule


    #purpose: renvoie la cellule d'index 'index' de la zone 'zone'
    def __getCelluleIndex(self, zone : Zone, index : int) -> Cellule:
        cellule = zone.getCelluleIndex(index)
        return cellule


    #purpose: rectifie les listes de candidats de la cellule en fonction des candidats impossibles 'imp'
    def __adjustCandidatesCellule(self, cellule : Cellule, imp : list[int]) -> None:
        newCandidates = listDifference(cellule.getCandidates(), imp)
        cellule.setCandidates(newCandidates)


    #purpose: rectifie les listes de candidats des cellules de la zone 'zone'
    def __adjustCandidatesZone(self, zone : Zone) -> None:
        for i in range(self.__size**2):
            cellule =  self.__getCelluleIndex(zone, i)
            impossible = [valuesWithoutZero(zone.getValues())]
            self.__adjustCandidatesCellule(cellule, impossible)


    #purpose: rectifie les listes de candidats des cellules de la ligne 'row'
    def __adjustCandidatesRow(self, row : int) -> None:
        for i in range(self.__size**2):
            cellule =  self.__getCelluleCoord(row, i)
            impossible = [valuesWithoutZero(self.getRow(row))]
            self.__adjustCandidatesCellule(cellule, impossible)
            


    #purpose: rectifie les listes de candidats des cellules de la colonne 'column'
    def __adjustCandidatesColumn(self, column : int) -> None:
        for i in range(self.__size**2):
            cellule =  self.__getCelluleCoord(i, column)
            impossible = [valuesWithoutZero(self.getColumn(column))]
            self.__adjustCandidatesCellule(cellule, impossible)


    #purpose: rectifie les listes de candidats des cellules de la grille
    def adjustCandidates(self) -> None:
        size = self.__size**2
        for i in range(size):
            self.__adjustCandidatesZone(self.__grille[i])
            self.__adjustCandidatesRow(i)
            self.__adjustCandidatesColumn(i)


    #purpose: rectifie la liste de candidats de la cellule aux coordonnées ('row', 'column')
    def adjustCandidatesAfterAddingValueCoord(self, row : int, column : int) -> None:
        zone = self.__grille[indexOfZone(row, column, self.__size)]
        self.__adjustCandidatesZone(zone)
        self.__adjustCandidatesRow(row)
        self.__adjustCandidatesColumn(column)


    #purpose: rectifie la liste de candidats de la cellule d'index 'index' dans la zone 'zone'
    def adjustCandidatesAfterAddingValueIndex(self, zone : Zone, index : int) -> None:
        zoneI = -1
        for z in range(self.__size**2):
            if (self.__grille[z]==zone):
                zoneI = z
        if (zoneI==-1):
            raise(GrilleError("Grille : impossible d'identifier la zone en ajustant les candidats après modification de la valeur d'une cellule par index"))
        row = indexOfRow(zoneI, index, self.__size)
        column = indexOfColumn(zoneI, index, self.__size)
        self.__adjustCandidatesZone(zone)
        self.__adjustCandidatesRow(row)
        self.__adjustCandidatesColumn(column)


    #purpose: renvoie la valeur de la cellule aux coordonnées ('row', 'column')
    def getCelluleValueCoord(self, row : int, column : int) -> int:
        cellule = self.__getCelluleCoord(row, column)
        return cellule.getValue()


    #purpose: renvoie la valeur de la cellule d'index 'index' de la zone 'zone'
    def getCelluleValueIndex(self, zone : Zone, index : int) -> int:
        cellule = self.__getCelluleIndex(zone, index)
        return cellule.getValue()


    #purpose: défini la valeur de la cellule aux coordonnées ('row', 'column')
    def setCelluleValueCoord(self, row : int, column : int, value : int) -> None:
        cellule = self.__getCelluleCoord(row, column)
        cellule.setValue(value)


    #purpose: défini la valeur de la cellule d'index 'index' de la zone 'zone'
    def setCelluleValueIndex(self, zone : Zone, index : int, value : int) -> None:
        cellule = self.__getCelluleIndex(zone, index)
        cellule.setValue(value)


    #purpose: enlève la valeur de la cellule aux coordonnées ('row', 'column')
    def removeCelluleValueCoord(self, row : int, column : int) -> None:
        cellule = self.__getCelluleCoord(row, column)
        cellule.setValue(0)



    #purpose: enlève la valeur de la cellule d'index 'index' de la zone 'zone'
    def removeCelluleValueIndex(self, zone : Zone, index : int) -> None:
        cellule = self.__getCelluleIndex(zone, index)
        cellule.setValue(0)


    #purpose: clone la grille (duh!)
    def clone(self):# -> Grille
        newGrille = []
        for i in range(self.__size**2):
            newGrille.append(self.__grille[i].clone())
        return Grille(newGrille)


    #purpose: affiche la grille
    def printGrille(self) -> None:
        size = self.__size**2
        numCharPerCellule = valueNumCount(size)*size +1 # +1 pour l'espace
        numCharPerZoneDelimitation = (self.__size-1)*2 #x2 parce qu'il y a une barre et un espace (l'espace à gauche est compté dans numCharPerCellule)
        numCharPerLine = numCharPerCellule + numCharPerZoneDelimitation
        for row in range(size):
            line = ""
            for column in range(size):
                val = self.getCelluleValueCoord(row, column)
                line += valueToString(val, valueNumCount(size))
                if column % self.__size == self.__size-1 and column != size-1:
                    line += " | "
                else:
                    line += " "
            print(line)
            if row % self.__size == self.__size-1 and row != size-1:
                print("-" * numCharPerLine)

    #purpose: renvoie la grille sous forme de chaine de caractères
    def toString(self) -> str:
        size = self.__size**2
        s = "[ "
        for i in range(size):
            s +=self.__grille[i].toString()
            if (i!=size-1):
                s+= ", "
        s += " ]"
        return s