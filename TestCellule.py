from Cellule import Cellule
import pytest as pt
from Except.GrilleError import GrilleError

# Test de l'initialisation d'une cellule vide
def test_initEmpty():
    myCel = Cellule()
    assert myCel.getValue() == 0
    assert myCel.getCandidates() == []
    assert myCel.getPosition() == -1

# Test de l'initialisation d'une cellule avec une valeur
def test_initValue():
    myCel = Cellule(0)
    assert myCel.getValue() == 0
    assert myCel.getCandidates() == []
    assert myCel.getPosition() == -1

# Test de l'initialisation d'une cellule avec valeur négative
def test_initValueNeg():
    with pt.raises(GrilleError):
        myCel = Cellule(-1)

# Test de l'initialisation d'une cellule ainsi que ces candidats (SANS CONFLITS)
def test_initCandidates():
    myCel = Cellule(5)
    assert myCel.getValue() == 5
    cand=[1,2,3,4,6,7,8,9]
    myCel.setCandidates(cand)
    assert myCel.getCandidates() == cand
    assert myCel.getPosition() == -1

# Test de l'initialisation d'une cellule ainsi que ces candidats (AVEC CONFLITS)
def test_initCandidatesConflicts():
    myCel = Cellule(5)
    assert myCel.getValue() == 5
    cand=[1,2,3,4,5,6,7,8,9]
    myCel.setCandidates(cand)
    assert myCel.getCandidates() == [1,2,3,4,6,7,8,9]
    assert myCel.getPosition() == -1

# Test de l'assignation d'une position conforme à une cellule
def test_setPosition():
    myCel = Cellule(5)
    position = 10
    myCel.setPosition(position)
    assert myCel.getPosition() == position

# Test de l'assignation d'une position négative à une cellule
def test_setPositionNeg():
    myCel = Cellule(5)
    oldPos = myCel.getPosition()
    position = -10
    with pt.raises(GrilleError):
        myCel.setPosition(position)
    assert myCel.getPosition() == oldPos