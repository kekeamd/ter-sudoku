from Zone import Zone
from Except.GrilleError import GrilleError
import pytest as pt
from Cellule import Cellule

# Test de création de Zone sans paramètres
def test_init():
    myZ = Zone()
    assert myZ.getSize() == 3
    assert myZ.getValues() == [0,0,0,0,0,0,0,0,0]

# Test de création de Zone avec une zone passé en params
def test_initZone():
    zone = []
    values = []
    for i in range (9):
        zone.append(Cellule(i+1))
        values.append(i+1)
    myZ = Zone(zone)
    assert myZ.getSize() == 3
    assert myZ.getValues() == values

# Test de création de Zone avec une zone passé en params de taille incohérente
def test_initZoneIncorrect():
    zone = []
    for i in range (10):
        zone.append(Cellule(i+1))
    with pt.raises(GrilleError):
        myZ = Zone(zone)

# Test de création de Zone avec une zone passé en params et une taille inférieur à celle de la Zone
def test_initZoneWithSize():
    zone = []
    for i in range (9):
        zone.append(Cellule(i+1))
    myZ = Zone(zone,2)
    assert myZ.getSize() == 2
    assert myZ.getValues() == [1,2,4,5]

# Test de création de Zone avec une zone passé en params et une taille trop grande
def test_initZoneWithSize():
    zone = []
    for i in range (9):
        zone.append(Cellule(i+1))
    with pt.raises(GrilleError):
        myZ = Zone(zone,4)

# Test de création de Zone avec une zone passé en params et une taille < -1
def test_initZoneWithSizeNeg():
    zone = []
    for i in range (9):
        zone.append(Cellule(i+1))
    with pt.raises(GrilleError):
        myZ = Zone(zone,-2)

# Test de récupération des valeurs d'une col & row avec bons index
def test_claimRowAndCol():
    zone = []
    for i in range (9):
        zone.append(Cellule(i+1))
    myZ = Zone(zone)
    assert myZ.getColumn(0) == [1,4,7]
    assert myZ.getColumn(1) == [2,5,8]
    assert myZ.getColumn(2) == [3,6,9]
    assert myZ.getRow(0) == [1,2,3]
    assert myZ.getRow(1) == [4,5,6]
    assert myZ.getRow(2) == [7,8,9]
    
# Test de récupération des valeurs d'une col & row avec MAUVAIS index
def test_claimRowAndColError():
    zone = []
    for i in range (9):
        zone.append(Cellule(i+1))
    myZ = Zone(zone)
    with pt.raises(GrilleError):
        myZ.getColumn(3)
    with pt.raises(GrilleError):
        myZ.getRow(3)

# Test de récupération d'une cellule avec bons index (Coords + index)
def test_claimCelCoordsIndex():
    zone = []
    for i in range (9):
        zone.append(Cellule(i+1))
    myZ = Zone(zone)
    assert myZ.getCelluleCoord(0,0).getValue()==1
    assert myZ.getCelluleCoord(1,1).getValue()==5
    assert myZ.getCelluleCoord(2,2).getValue()==9
    assert myZ.getCelluleIndex(0).getValue()==1
    assert myZ.getCelluleIndex(2).getValue()==3
    assert myZ.getCelluleIndex(3).getValue()==4
    assert myZ.getCelluleIndex(6).getValue()==7
    assert myZ.getCelluleIndex(8).getValue()==9

# Test de récupération d'une cellule avec MAUVAIS INDEX (Coords + index)
def test_claimCelCoordsIndexError():
    zone = []
    for i in range (9):
        zone.append(Cellule(i+1))
    myZ = Zone(zone)
    with pt.raises(GrilleError):
        myZ.getCelluleCoord(-1,0).getValue()
    with pt.raises(GrilleError):
        myZ.getCelluleCoord(0,-1).getValue()
    with pt.raises(GrilleError):
        myZ.getCelluleCoord(-5,-5).getValue()
    with pt.raises(GrilleError):
        myZ.getCelluleCoord(3,3).getValue()
    with pt.raises(GrilleError):
        myZ.getCelluleCoord(3,0).getValue()
    with pt.raises(GrilleError):
        myZ.getCelluleCoord(0,3).getValue()
    with pt.raises(GrilleError):
        myZ.getCelluleIndex(-1).getValue()
    with pt.raises(GrilleError):
        myZ.getCelluleIndex(9).getValue()

# Test de récupération de la liste des valeurs de la zone + Vérification contains (True and False)
def test_ListValsAndContains():
    zone = []
    for i in range (9):
        zone.append(Cellule(i+1))
    myZ = Zone(zone)
    assert myZ.getValues() == [1,2,3,4,5,6,7,8,9]
    assert myZ.containsValue(4) == True
    assert myZ.containsValue(10) == False
    assert myZ.containsValue(0) == False