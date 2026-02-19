from SolverHuman import SolverHuman
from GrilleBacktrack import GrilleBacktrack
from Zone import Zone
from Cellule import Cellule
import pytest as pt


def test_dernierNombreFonctionnePourUneLigne():
    grille = GrilleBacktrack([Zone([Cellule() for _ in range(9)]) for _ in range(9)])
    for i in range(9):
        grille.setCelluleValueIndex(3*9 + i, i+1)
    grille.removeCelluleValueIndex(3*9 + 7)
    assert SolverHuman.dernierNombre(grille)
    assert grille.getCelluleValueIndex(3*9 + 7)== 8


def test_dernierNombreFonctionnePourUneColonne():
    grille = GrilleBacktrack([Zone([Cellule() for _ in range(9)]) for _ in range(9)])
    for i in range(9):
        grille.setCelluleValueIndex(4+ i*9, i+1)
    grille.removeCelluleValueIndex(4)
    assert SolverHuman.dernierNombre(grille)
    assert grille.getCelluleValueIndex(4)==1


def test_dernierNombreFonctionnePourUneZone():
    grille = GrilleBacktrack([Zone([Cellule() for _ in range(9)]) for _ in range(9)])
    for i in range(9):
        grille.setCelluleValueZoneIndex(6, i, i+1)
    grille.removeCelluleValueZoneIndex(6, 2)
    assert SolverHuman.dernierNombre(grille)
    assert grille.getCelluleValueZoneIndex(6, 2)== 3