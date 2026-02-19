from GrilleBacktrack import GrilleBacktrack
from Grille import Grille
from Zone import Zone
from Cellule import Cellule
import pytest as pt
from Except.GrilleError import GrilleError


# Test le constructeur vide
def test_initEmpty():
    grille : Grille = GrilleBacktrack()
    assert grille.getDifficulte() == None
    assert grille.getSize() == 3
    for i in range(9):
        assert grille.getRow(i) == [0]*9


# Test le constructeur avec paramètres
def test_initParameters():
    zoneList = [Zone([Cellule(v) for v in range(i, i+9)]) for i in range(1, 26, 3)]
    grille : Grille = GrilleBacktrack(zoneList)
    assert grille.getDifficulte() == None
    assert grille.getSize()**2 == len(zoneList)
    assert grille.getCelluleValueCoord(3, 1) == 11


# Test que la méthode renvoie bien la liste des valeurs
def test_getRowIsValueList():
    grille : Grille = GrilleBacktrack([Zone([Cellule(v) for v in range(i, i+9)]) for i in range(1, 26, 3)])
    assert grille.getRow(0)==[i for i in range(1, 10)]


# Test que la méthode renvoie bien la liste des valeurs
def test_getColumnIsValueList():
    grille : Grille = GrilleBacktrack([Zone([Cellule(v) for v in range(i, i+9)]) for i in range(1, 26, 3)])
    assert grille.getColumn(0)==[i for i in range(1, 26, 3)]


# Test que la méthode renvoie true quand la ligne contient la valeur
def test_rowContainsValue():
    grille : Grille = GrilleBacktrack([Zone([Cellule(v) for v in range(i, i+9)]) for i in range(1, 26, 3)])
    assert grille.rowContainsValue(0, 3)==True


# Test que la méthode renvoie false quand la ligne ne contient pas la valeur
def test_rowDoesntContainsValue():
    grille : Grille = GrilleBacktrack([Zone([Cellule(v) for v in range(i, i+9)]) for i in range(1, 26, 3)])
    assert grille.rowContainsValue(0, 13)==False


# Test que la méthode renvoie true quand la colonne contient la valeur
def test_columnContainsValue():
    grille : Grille = GrilleBacktrack([Zone([Cellule(v) for v in range(i, i+9)]) for i in range(1, 26, 3)])
    assert grille.columnContainsValue(0, 13)==True


# Test que la méthode renvoie false quand la colonne ne contient pas la valeur
def test_columnDoesntContainsValue():
    grille : Grille = GrilleBacktrack([Zone([Cellule(v) for v in range(i, i+9)]) for i in range(1, 26, 3)])
    assert grille.columnContainsValue(0, 3)==False


# Test que la méthode renvoie la bonne cellule
def test_getCelluleValueCoordReturnsRightValue():
    grille : Grille = GrilleBacktrack([Zone([Cellule(v) for v in range(i, i+9)]) for i in range(1, 26, 3)])
    assert grille.getCelluleValueCoord(3, 1)==11


# Test que la méthode renvoie la bonne cellule
def test_getCelluleValueZoneIndexReturnsRightValue():
    zone = Zone([Cellule(0), Cellule(0), Cellule(0), Cellule(0), Cellule(0), Cellule(0), Cellule(16), Cellule(0), Cellule(0)])
    grille : Grille = GrilleBacktrack([zone]+[Zone([Cellule(v) for v in range(i, i+9)]) for i in range(4, 26, 3)])
    assert grille.getCelluleValueZoneIndex(0, 6)==16


# Test que la méthode renvoie la bonne cellule
def test_getCelluleValueIndexReturnsRightValue():
    grille : Grille = GrilleBacktrack([Zone([Cellule(v) for v in range(i, i+9)]) for i in range(1, 26, 3)])
    assert grille.getCelluleValueIndex(28)==11


#Test que la méthode initialise bien les candidats
def test_adjustCandidatesInit():
    grille : Grille =  GrilleBacktrack([Zone([Cellule() for _ in range(9)]) for _ in range(9)])
    grille.adjustCandidates()
    for cell in range(grille.getSize()**4):
        assert grille.getCelluleCandidatesIndex(cell)==[i+1 for i in range(grille.getSize()**2)]

# Test que la méthode ajuste correctement les candidats de la cellule
def test_adjustCandidatesCellule():
    grille : Grille =  GrilleBacktrack([Zone([Cellule() for _ in range(9)]) for _ in range(9)])
    grille.adjustCandidates()
    grille.setCelluleValueCoord(2, 5, 7)
    cellule = grille._getCelluleCoord(2, 0)
    grille._adjustCandidatesCellule(cellule, [7])
    assert grille.getCelluleCandidatesCoord(2, 0)==[1, 2, 3, 4, 5, 6, 8, 9]
"""
    def __init__(self, zoneList : list[Zone] , sizeCote : int = 3):
        if ((sizeCote*sizeCote)!=len(zoneList) or len(zoneList) < 3):
            raise(GrilleError("Grille : deuxième argument invalide ou alors la taille de 'zoneList' est différente de la valeur par défaut (avez-vous pensé à préciser la taille?)"))
        self.__grille : list[Zone] = zoneList
        self.__sizeCote : int = sizeCote
        self.__difficulte : Difficulte = None    
"""