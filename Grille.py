from abc import ABC, abstractmethod
from Zone import Zone
from Cellule import Cellule
from Difficulte import Difficulte
from Except.GrilleError import GrilleError
from GrilleUtils import *

#purpose: bah la grille de sudoku
#dependencies: Difficulte, Cellule ,Zone, GrilleUtils, GrilleError
class Grille(ABC):
    def __init__(self, sizeCote : int = 3): #faire un constructeur avec que la taille
        self._grille : list[Zone] = []
        self._size : int = sizeCote
        for _ in range(self._size**2):
            self._grille.append(Zone(size=sizeCote))
        self._difficulte : Difficulte = None
    def __init__(self, zoneList : list[Zone] , sizeCote : int = 3):
        if ((sizeCote*sizeCote)!=len(zoneList) or len(zoneList) < 3):
            raise(GrilleError("Grille : deuxième argument invalide ou alors la taille de 'zoneList' est différente de la valeur par défaut (avez-vous pensé à préciser la taille?)"))
        self._grille : list[Zone] = zoneList
        self._size : int = sizeCote
        self._difficulte : Difficulte = None
    

    #purpose: génère des valeurs et rempli la grille
    @abstractmethod
    def generateValues(self, difficulte : Difficulte) -> None:
        pass


    #purpose: renvoie la difficulté de la grille
    def getDifficulte(self)-> Difficulte:
        return self._difficulte


    #purpose: défini la difficulté de la grille
    def _setDifficulte(self, difficulte : Difficulte) -> None:
        self._difficulte = difficulte

    
    #purpose: renvoie la taille du côté de la grille
    def getSize(self) -> int:
        return self._size


    #purpose: renvoie la ligne numéro 'row'
    def getRow(self, row : int) -> list[int]: #row commence à 0
        rowValues = []
        for i in range(self._size):
            zone = self._grille[indexOfFirstZoneInRow(row, self._size) + i] #avec i qui sert d'offset par rapport à la première zone de la ligne
            rowValues+= zone.getRow(indexRowOrColumnInZone(row, self._size)) #on on concatène la liste de valeurs actuel avec la liste de valeurs dans la ligne de 'zone'
        return rowValues


    #purpose: renvoie la colonne numéro 'column'
    def getColumn(self, column : int) -> list[int]:
        colValues = []
        for i in range(self._size):
            zone = self._grille[indexOfFirstZoneInColumn(column, self._size) + self._size*i] #avec size*i qui sert d'offset par rapport à la première zone de la colonne
            colValues+= zone.getColumn(indexRowOrColumnInZone(column, self._size)) #on on concatène la liste de valeurs actuel avec la liste de valeurs dans la colonne de 'zone'
        return colValues


    #purpose: renvoie la zone numéro 'zone'
    def getZone(self, zone : int) -> list[int]:
        z = self._getZone(zone)
        return z.getValues()



    #purpose: renvoie vrai si la ligne numéro 'row' contient la valeur 'value' et faux sinon
    def rowContainsValue(self, row : int, value : int) ->  bool:
        return value in self.getRow(row)


    #purpose: renvoie vrai si la colonne numéro 'column' contient la valeur 'value' et faux sinon
    def columnContainsValue(self, column: int, value : int) ->  bool:
        return value in self.getColumn(column)


    #purpose: renvoie la zone d'index 'zone'
    def _getZone(self, zone : int) -> Zone: #zone commence à 0
        return self._grille[zone]


    #purpose : renvoie la cellule aux coordonnées ('row', 'column')
    def _getCelluleCoord(self, row : int, column : int) -> Cellule:
        zone = self._grille[zoneIndexFromCoord(row, column, self._size)]
        cellule = zone.getCelluleCoord(indexRowOrColumnInZone(row, self._size), indexRowOrColumnInZone(column, self._size))
        return cellule


    #purpose: renvoie la cellule d'index relatif 'index' de la zone 'zone'
    def _getCelluleZoneIndex(self, zone : int, index : int) -> Cellule:
        z = self._getZone(zone)
        cellule = z.getCelluleIndex(index)
        return cellule


    #purpose: renvoie la cellule d'index absolu 'index'
    def _getCelluleIndex(self, index : int) -> Cellule: #exemple : pour une grille 9x9, l'index va de 0 à 80
        rowIndex = rowIndexFromCelluleIndex(index, self._size)
        columnIndex = columnIndexFromCelluleIndex(index, self._size)
        return self._getCelluleCoord(rowIndex, columnIndex)


    #purpose: renvoie la valeur de la cellule aux coordonnées ('row', 'column')
    def getCelluleValueCoord(self, row : int, column : int) -> int:
        cellule = self._getCelluleCoord(row, column)
        return cellule.getValue()


    #purpose: renvoie la valeur de la cellule d'index relatif 'index' de la zone 'zone'
    def getCelluleValueZoneIndex(self, zone : int, index : int) -> int: 
        cellule = self._getCelluleZoneIndex(zone, index)
        return cellule.getValue()


    #purpose: renvoie la valeur de la cellule d'index absolu 'index'
    def getCelluleValueIndex(self, index : int) -> int: 
        cellule = self._getCelluleIndex(index)
        return cellule.getValue()


    #purpose: défini la valeur de la cellule aux coordonnées ('row', 'column')
    def setCelluleValueCoord(self, row : int, column : int, value : int) -> None:
        cellule = self._getCelluleCoord(row, column)
        cellule.setValue(value)


    #purpose: défini la valeur de la cellule d'index relatif 'index' de la zone 'zone'
    def setCelluleValueZoneIndex(self, zone : int, index : int, value : int) -> None: 
        cellule = self._getCelluleZoneIndex(zone, index)
        cellule.setValue(value)


    #purpose: défini la valeur de la cellule d'index absolu 'index'
    def setCelluleValueIndex(self, index : int, value : int) -> None: 
        cellule = self._getCelluleIndex(index)
        cellule.setValue(value)


    #purpose: enlève la valeur de la cellule aux coordonnées ('row', 'column')
    def removeCelluleValueCoord(self, row : int, column : int) -> None:
        cellule = self._getCelluleCoord(row, column)
        cellule.setValue(0)



    #purpose: enlève la valeur de la cellule d'index relatif 'index' de la zone 'zone'
    def removeCelluleValueZoneIndex(self, zone : int, index : int) -> None: 
        cellule = self._getCelluleZoneIndex(zone, index)
        cellule.setValue(0)


    #purpose: enlève la valeur de la cellule d'index absolu 'index'
    def removeCelluleValueIndex(self, index : int) -> None: 
        cellule = self._getCelluleIndex(index)
        cellule.setValue(0)


    #purpose: renvoie la liste des candidats de la cellule aux coordonnées ('row', 'column')
    def getCelluleCandidatesCoord(self, row : int, column : int) -> list[int]:
        cellule = self._getCelluleCoord(row, column)
        return cellule.getCandidates()
    

    #purpose: renvoie la liste des candidats de la cellule d'index relatif 'index' de la zone 'zone'
    def getCelluleCandidatesZoneIndex(self, zone : int, index : int) -> list[int]:
        cellule = self._getCelluleZoneIndex(zone, index)
        return cellule.getCandidates()


    #purpose: renvoie la liste des candidats de la cellule d'index absolu 'index'
    def getCelluleCandidatesIndex(self, index : int) -> list[int]:
        cellule = self._getCelluleIndex(index)
        return cellule.getCandidates()


    #purpose: rectifie les listes de candidats de la cellule en fonction des candidats impossibles 'imp'
    def _adjustCandidatesCellule(self, cellule : Cellule, imp : list[int]) -> None:
        newCandidates = listDifference(cellule.getCandidates(), imp)
        cellule.setCandidates(newCandidates)


    #purpose: rectifie les listes de candidats des cellules de la zone 'zone'
    def _adjustCandidatesZone(self, zone : int) -> None: #zone commence
        z = self._getZone(zone)
        impossible = valuesWithoutZero(z.getValues())
        for i in range(self._size**2):
            cellule =  self._getCelluleZoneIndex(zone, i)
            self._adjustCandidatesCellule(cellule, impossible)


    #purpose: rectifie les listes de candidats des cellules de la ligne 'row'
    def _adjustCandidatesRow(self, row : int) -> None:
        impossible = valuesWithoutZero(self.getRow(row))
        for i in range(self._size**2):
            cellule =  self._getCelluleCoord(row, i)
            self._adjustCandidatesCellule(cellule, impossible)
            


    #purpose: rectifie les listes de candidats des cellules de la colonne 'column'
    def _adjustCandidatesColumn(self, column : int) -> None:
        impossible = valuesWithoutZero(self.getColumn(column))
        for i in range(self._size**2):
            cellule =  self._getCelluleCoord(i, column)
            self._adjustCandidatesCellule(cellule, impossible)


    #purpose: rectifie les listes de candidats des cellules de la grille
    def adjustCandidates(self) -> None:
        size = self._size**2
        for i in range(size**2):
            self._getCelluleIndex(i).setCandidates([v for v in range(1, size+1)])
        for i in range(size):
            self._adjustCandidatesZone(i)
            self._adjustCandidatesRow(i)
            self._adjustCandidatesColumn(i)


    #purpose: rectifie la liste de candidats de la cellule aux coordonnées ('row', 'column')
    def adjustCandidatesAfterAddingValueCoord(self, row : int, column : int) -> None:
        zone = self._grille[zoneIndexFromCoord(row, column, self._size)]
        self._adjustCandidatesZone(zone)
        self._adjustCandidatesRow(row)
        self._adjustCandidatesColumn(column)


    #purpose: rectifie la liste de candidats de la cellule d'index relatif 'index' dans la zone 'zone'
    def adjustCandidatesAfterAddingValueZoneIndex(self, zone : int, index : int) -> None:
        row = indexOfRow(zone, index, self._size)
        column = indexOfColumn(zone, index, self._size)
        self._adjustCandidatesZone(zone)
        self._adjustCandidatesRow(row)
        self._adjustCandidatesColumn(column)


    #purpose: rectifie la liste de candidats de la cellule d'index absolu 'index'
    def adjustCandidatesAfterAddingValueIndex(self, index : int) -> None:
        row = rowIndexFromCelluleIndex(index, self._size)
        column = columnIndexFromCelluleIndex(index, self._size)
        zone = zoneIndexFromCoord(row, column, self._size)
        self._adjustCandidatesZone(zone)
        self._adjustCandidatesRow(row)
        self._adjustCandidatesColumn(column)


    #purpose: affiche la grille
    def printGrille(self) -> None:
        size = self._size**2
        numCharPerCellule = valueNumCount(size)+1 # +1 pour l'espace
        numCharPerZoneDelimitation = (self._size-1)*2 #x2 parce qu'il y a une barre et un espace (l'espace à gauche est compté dans numCharPerCellule)
        numCharPerLine = size*numCharPerCellule + numCharPerZoneDelimitation
        for row in range(size):
            line = ""
            for column in range(size):
                val = self.getCelluleValueCoord(row, column)
                line += valueToString(val, valueNumCount(size))
                if column % self._size == self._size-1 and column != size-1:
                    line += " | "
                else:
                    line += " "
            print(line)
            if row % self._size == self._size-1 and row != size-1:
                print("-" * numCharPerLine)


    #purpose: clone la grille
    @abstractmethod
    def clone(self):# -> Grille
        pass