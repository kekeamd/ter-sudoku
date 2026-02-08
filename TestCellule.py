from Cellule import Cellule
import pytest as pt
from Except.GrilleError import GrilleError

# Test de l'initialisation d'une cellule vide
def test_initEmpty():
    myCel = Cellule()
    assert myCel.getValue() == 0
    assert myCel.getCandidates() == []

# Test de l'initialisation d'une cellule avec une valeur
def test_initValue():
    myCel = Cellule(0)
    assert myCel.getValue() == 0
    assert myCel.getCandidates() == []

# Test de l'initialisation d'une cellule avec valeur négative
def test_initValueNeg():
    with pt.raises(GrilleError):
        myCel = Cellule(-1)

# Test de l'initialisation d'une cellule ainsi que ces candidats (SANS CONFLITS)
def test_initCandidates():
    myCel = Cellule(5)
    assert myCel.getValue() == 5
    cand=[0,1,2,3,4,6,7,8,9]
    myCel.setCandidates(cand)
    assert myCel.getCandidates() == cand

# Test de l'initialisation d'une cellule ainsi que ces candidats (AVEC CONFLITS)
def test_initCandidates():
    myCel = Cellule(5)
    assert myCel.getValue() == 5
    cand=[0,1,2,3,4,5,6,7,8,9]
    myCel.setCandidates(cand)
    assert myCel.getCandidates() == [0,1,2,3,4,6,7,8,9]