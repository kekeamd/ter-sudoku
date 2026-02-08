from Grille import Grille
from Zone import Zone
from Cellule import Cellule
import pytest as pt
from Except.GrilleError import GrilleError


# Test le constructeur vide
def test_initEmpty():
    grille = Grille()
    assert grille.getDifficulte() == None
    assert grille.getSize() == 3
    for i in range(9):
        assert grille.getRow(i) == [0]*9


# Test le constructeur avec paramètres
def test_initParameters():
    zoneList = [Zone([Cellule(v) for v in range(i, i+9)]) for i in range(1, 26, 3)]
    grille = Grille(zoneList)
    assert grille
    assert grille.getDifficulte() == None
    assert grille.getSize()**2 == len(zoneList)
    assert grille.getCelluleValueCoord(3, 1) == 11


# Test que la méthode renvoie bien la liste des valeurs
def test_getRowIsValueList():
    grille = Grille([Zone([Cellule(v) for v in range(i, i+9)]) for i in range(1, 26, 3)])
    assert grille.getRow(0)==[i for i in range(1, 10)]


# Test que la méthode renvoie bien la liste des valeurs
def test_getColumnIsValueList():
    grille = Grille([Zone([Cellule(v) for v in range(i, i+9)]) for i in range(1, 26, 3)])
    assert grille.getRow(0)==[i for i in range(1, 26, 3)]


# Test que la méthode renvoie true quand la ligne contient la valeur
def test_rowContainsValue():
    grille = Grille([Zone([Cellule(v) for v in range(i, i+9)]) for i in range(1, 26, 3)])
    assert grille.rowContainsValue(0, 3)==True


# Test que la méthode renvoie false quand la ligne ne contient pas la valeur
def test_rowDoesntContainsValue():
    grille = Grille([Zone([Cellule(v) for v in range(i, i+9)]) for i in range(1, 26, 3)])
    assert grille.rowContainsValue(0, 13)==False


# Test que la méthode renvoie true quand la colonne contient la valeur
def test_columnContainsValue():
    grille = Grille([Zone([Cellule(v) for v in range(i, i+9)]) for i in range(1, 26, 3)])
    assert grille.rowContainsValue(0, 13)==True


# Test que la méthode renvoie false quand la colonne ne contient pas la valeur
def test_columnDoesntContainsValue():
    grille = Grille([Zone([Cellule(v) for v in range(i, i+9)]) for i in range(1, 26, 3)])
    assert grille.rowContainsValue(0, 3)==False


# Test que la méthode renvoie la bonne cellule
def test_getCelluleCoordReturnsRightCellule():
    grille = Grille([Zone([Cellule(v) for v in range(i, i+9)]) for i in range(1, 26, 3)])
    assert grille.__getCelluleCoord(3, 1).getValue()==11


# Test que la méthode renvoie la bonne cellule
def test_getCelluleIndexReturnsRightCellule():
    zone = Zone([Cellule(0), Cellule(0), Cellule(0), Cellule(0), Cellule(0), Cellule(0), Cellule(16), Cellule(0), Cellule(0)])
    grille = Grille([zone]+[Zone([Cellule(v) for v in range(i, i+9)]) for i in range(4, 26, 3)])
    assert grille.__getCelluleIndex(zone, 6).getValue()==16

# Test que la méthode clone correctement la classe
def test_cloneIsCorrect():
    grille = Grille([Zone([Cellule(v) for v in range(i, i+9)]) for i in range(1, 26, 3)])
    grille2 = grille.clone()
    assert grille.getRow(6) == grille2.getRow(6)

"""
    def __init__(self, zoneList : list[Zone] , sizeCote : int = 3):
        if ((sizeCote*sizeCote)!=len(zoneList) or len(zoneList) < 3):
            raise(GrilleError("Grille : deuxième argument invalide ou alors la taille de 'zoneList' est différente de la valeur par défaut (avez-vous pensé à préciser la taille?)"))
        self.__grille : list[Zone] = zoneList
        self.__sizeCote : int = sizeCote
        self.__difficulte : Difficulte = None    


    #purpose: rectifie les listes de candidats de la cellule en fonction des candidats impossibles 'imp'
    def __adjustCandidatesCellule(self, cellule : Cellule, imp : list[int]) -> None:
        newCandidates = listDifference(cellule.getCandidates(), imp)
        cellule.setCandidates(newCandidates)


    #purpose: rectifie les listes de candidats des cellules de la zone 'zone'
    def __adjustCandidatesZone(self, zone : Zone) -> None:
        for i in range(self.__sizeCote*self.__sizeCote):
            cellule =  self.__getCelluleIndex(zone, i)
            impossible = [valuesWithoutZero(zone.getValues())]
            self.__adjustCandidatesCellule(cellule, impossible)


    #purpose: rectifie les listes de candidats des cellules de la ligne 'row'
    def __adjustCandidatesRow(self, row : int) -> None:
        for i in range(self.__sizeCote*self.__sizeCote):
            cellule =  self.__getCelluleCoord(row, i)
            impossible = [valuesWithoutZero(self.getRow(row))]
            self.__adjustCandidatesCellule(cellule, impossible)
            


    #purpose: rectifie les listes de candidats des cellules de la colonne 'column'
    def __adjustCandidatesColumn(self, column : int) -> None:
        for i in range(self.__sizeCote*self.__sizeCote):
            cellule =  self.__getCelluleCoord(i, column)
            impossible = [valuesWithoutZero(self.getColumn(column))]
            self.__adjustCandidatesCellule(cellule, impossible)


    #purpose: rectifie les listes de candidats des cellules de la grille
    def adjustCandidates(self) -> None:
        size = self.__sizeCote*self.__sizeCote
        for i in range(size):
            self.__adjustCandidatesZone(self.__grille[i])
            self.__adjustCandidatesRow(i)
            self.__adjustCandidatesColumn(i)


    #purpose: rectifie la liste de candidats de la cellule aux coordonnées ('row', 'column')
    def adjustCandidatesAfterAddingValueCoord(self, row : int, column : int) -> None:
        zone = self.__grille[indexOfZone(row, column, self.__sizeCote)]
        self.__adjustCandidatesZone(zone)
        self.__adjustCandidatesRow(row)
        self.__adjustCandidatesColumn(column)


    #purpose: rectifie la liste de candidats de la cellule d'index 'index' dans la zone 'zone'
    def adjustCandidatesAfterAddingValueIndex(self, zone : Zone, index : int) -> None:
        zoneI = -1
        for z in range(self.__sizeCote*self.__sizeCote):
            if (self.__grille[z]==zone):
                zoneI = z
        if (zoneI==-1):
            raise(GrilleError("Grille : impossible d'identifier la zone en ajustant les candidats après modification de la valeur d'une cellule par index"))
        row = indexOfRow(zoneI, index, self.__sizeCote)
        column = indexOfColumn(zoneI, index, self.__sizeCote)
        self.__adjustCandidatesZone(zone)
        self.__adjustCandidatesRow(row)
        self.__adjustCandidatesColumn(column)
"""