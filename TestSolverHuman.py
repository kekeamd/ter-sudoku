from SolverHuman import SolverHuman
from GrilleBacktrack import GrilleBacktrack
from Zone import Zone
from Cellule import Cellule
import pytest as pt


def test_dernierNombreFonctionnePourUneZone():
    grille = GrilleBacktrack([Zone([Cellule() for _ in range(9)]) for _ in range(9)])
    for i in range(9):
        grille.setCelluleValueZoneIndex(6, i, i+1)
    grille.removeCelluleValueZoneIndex(6, 2)
    grille.adjustCandidates()
    assert SolverHuman.dernierNombre(grille)
    assert grille.getCelluleValueZoneIndex(6, 2)== 3


def test_dernierNombreFonctionnePourUneLigne():
    grille = GrilleBacktrack([Zone([Cellule() for _ in range(9)]) for _ in range(9)])
    for i in range(9):
        grille.setCelluleValueCoord(3, i, i+1)
    grille.removeCelluleValueCoord(3, 7)
    grille.adjustCandidates()
    assert SolverHuman.dernierNombre(grille)
    assert grille.getCelluleValueCoord(3, 7)== 8


def test_dernierNombreFonctionnePourUneColonne():
    grille = GrilleBacktrack([Zone([Cellule() for _ in range(9)]) for _ in range(9)])
    for i in range(9):
        grille.setCelluleValueCoord(i, 4, i+1)
    grille.removeCelluleValueCoord(0, 4)
    grille.adjustCandidates()
    assert SolverHuman.dernierNombre(grille)
    assert grille.getCelluleValueCoord(0, 4)==1


def test_paireCacheeFonctionnePourUneZone():
    grille = GrilleBacktrack([Zone([Cellule() for _ in range(9)]) for _ in range(9)])
    grille.adjustCandidates()
    for i in range(2, 9):
        grille._getCelluleZoneIndex(5, i).setCandidates([1, 2, 3, 6, 7, 8, 9])
    assert SolverHuman.paireCachee(grille)
    for i in range(2, 9):
        assert 4 not in grille.getCelluleCandidatesZoneIndex(5, i) and 5 not in grille.getCelluleCandidatesZoneIndex(5, i)
    assert grille.getCelluleCandidatesZoneIndex(5, 0)==[4, 5] and grille.getCelluleCandidatesZoneIndex(5, 1)==[4, 5]


def test_paireCacheeFonctionnePourUneLigne():
    grille = GrilleBacktrack([Zone([Cellule() for _ in range(9)]) for _ in range(9)])
    grille.adjustCandidates()
    for i in range(2, 9):
        grille._getCelluleCoord(2, i).setCandidates([1, 2, 3, 6, 7, 8, 9])
    assert SolverHuman.paireCachee(grille)
    for i in range(2, 9):
        assert 4 not in grille.getCelluleCandidatesCoord(2, i) and 5 not in grille.getCelluleCandidatesCoord(2, i)
    assert grille.getCelluleCandidatesCoord(2, 0)==[4, 5] and grille.getCelluleCandidatesCoord(2, 1)==[4, 5]


def test_paireCacheeFonctionnePourUneColonne():
    grille = GrilleBacktrack([Zone([Cellule() for _ in range(9)]) for _ in range(9)])
    grille.adjustCandidates()
    for i in range(2, 9):
        grille._getCelluleCoord(i, 6).setCandidates([1, 2, 3, 6, 7, 8, 9])
    assert SolverHuman.paireCachee(grille)
    for i in range(2, 9):
        assert 4 not in grille.getCelluleCandidatesCoord(i, 6) and 5 not in grille.getCelluleCandidatesCoord(i, 6)
    assert grille.getCelluleCandidatesCoord(0, 6)==[4, 5] and grille.getCelluleCandidatesCoord(1, 6)==[4, 5]