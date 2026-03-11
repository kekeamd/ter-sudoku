from SolverHuman import SolverHuman
from GrilleBacktrack import GrilleBacktrack
import pytest as pt


def test_singletonCacheFonctionnePourUneZone():
    grille = GrilleBacktrack()
    grille.adjustCandidates()
    for i in range(9):
        if i==7:
            continue
        grille._getCelluleZoneIndex(3, i).setCandidates([1, 2, 3, 5, 6, 7, 8, 9])
    assert SolverHuman.singletonCache(grille)
    assert grille.getCelluleValueZoneIndex(3, 7)==4


def test_singletonCacheFonctionnePourUneLigne():
    grille = GrilleBacktrack()
    grille.adjustCandidates()
    for i in range(9):
        if i==3:
            continue
        grille._getCelluleCoord(6, i).setCandidates([1, 2, 3, 4, 5, 6, 8, 9])
    assert SolverHuman.singletonCache(grille)
    assert grille.getCelluleValueCoord(6, 3)==7


def test_singletonCacheFonctionnePourUneColonne():
    grille = GrilleBacktrack()
    grille.adjustCandidates()
    for i in range(9):
        if i==1:
            continue
        grille._getCelluleCoord(i, 2).setCandidates([1, 2, 3, 4, 5, 6, 7, 8])
    assert SolverHuman.singletonCache(grille)
    assert grille.getCelluleValueCoord(1, 2)==9


def test_dernierNombreFonctionnePourUneZone():
    grille = GrilleBacktrack()
    for i in range(9):
        grille.setCelluleValueZoneIndex(6, i, i+1)
    grille.removeCelluleValueZoneIndex(6, 2)
    grille.adjustCandidates()
    assert SolverHuman.dernierNombre(grille)
    assert grille.getCelluleValueZoneIndex(6, 2)== 3


def test_dernierNombreFonctionnePourUneLigne():
    grille = GrilleBacktrack()
    for i in range(9):
        grille.setCelluleValueCoord(3, i, i+1)
    grille.removeCelluleValueCoord(3, 7)
    grille.adjustCandidates()
    assert SolverHuman.dernierNombre(grille)
    assert grille.getCelluleValueCoord(3, 7)== 8


def test_dernierNombreFonctionnePourUneColonne():
    grille = GrilleBacktrack()
    for i in range(9):
        grille.setCelluleValueCoord(i, 4, i+1)
    grille.removeCelluleValueCoord(0, 4)
    grille.adjustCandidates()
    assert SolverHuman.dernierNombre(grille)
    assert grille.getCelluleValueCoord(0, 4)==1


def test_paireCacheeFonctionnePourUneZone():
    grille = GrilleBacktrack()
    grille.adjustCandidates()
    for i in range(2, 9):
        grille._getCelluleZoneIndex(5, i).setCandidates([1, 2, 3, 6, 7, 8, 9])
    assert SolverHuman.paireCachee(grille)
    for i in range(2, 9):
        assert 4 not in grille.getCelluleCandidatesZoneIndex(5, i) and 5 not in grille.getCelluleCandidatesZoneIndex(5, i)
    assert grille.getCelluleCandidatesZoneIndex(5, 0)==[4, 5] and grille.getCelluleCandidatesZoneIndex(5, 1)==[4, 5]


def test_paireCacheeFonctionnePourUneLigne():
    grille = GrilleBacktrack()
    grille.adjustCandidates()
    for i in range(2, 9):
        grille._getCelluleCoord(2, i).setCandidates([1, 2, 3, 6, 7, 8, 9])
    assert SolverHuman.paireCachee(grille)
    for i in range(2, 9):
        assert 4 not in grille.getCelluleCandidatesCoord(2, i) and 5 not in grille.getCelluleCandidatesCoord(2, i)
    assert grille.getCelluleCandidatesCoord(2, 0)==[4, 5] and grille.getCelluleCandidatesCoord(2, 1)==[4, 5]


def test_paireCacheeFonctionnePourUneColonne():
    grille = GrilleBacktrack()
    grille.adjustCandidates()
    for i in range(2, 9):
        grille._getCelluleCoord(i, 6).setCandidates([1, 2, 3, 6, 7, 8, 9])
    assert SolverHuman.paireCachee(grille)
    for i in range(2, 9):
        assert 4 not in grille.getCelluleCandidatesCoord(i, 6) and 5 not in grille.getCelluleCandidatesCoord(i, 6)
    assert grille.getCelluleCandidatesCoord(0, 6)==[4, 5] and grille.getCelluleCandidatesCoord(1, 6)==[4, 5]


def test_candidatEnfermeFonctionnePourUneZone():
    grille = GrilleBacktrack()
    grille._getCelluleZoneIndex(0, 7).setCandidates([2])
    grille._getCelluleZoneIndex(0, 8).setCandidates([2])
    for i in range(3, 9):
        grille._getCelluleCoord(2, i).setCandidates([2])
    assert SolverHuman.candidatEnferme(grille)
    for i in range(9):
        if i!=1 and i!=2:
            assert 2 not in grille.getCelluleCandidatesCoord(2, i)


def test_candidatEnfermeFonctionnePourUneLigne():
    grille = GrilleBacktrack()
    grille._getCelluleCoord(1, 3).setCandidates([5])
    grille._getCelluleCoord(1, 5).setCandidates([5])
    for i in range(6, 9):
        grille._getCelluleZoneIndex(1, i).setCandidates([5])
    assert SolverHuman.candidatEnferme(grille)
    for i in range(9):
        if i!=3 and i!=5:
            assert 5 not in grille.getCelluleCandidatesZoneIndex(1, i)


def test_candidatEnfermeFonctionnePourUneColonne():
    grille = GrilleBacktrack()
    grille._getCelluleCoord(3, 1).setCandidates([8])
    grille._getCelluleCoord(5, 1).setCandidates([8])
    for i in range(9):
        if i%3==2:
            grille._getCelluleZoneIndex(3, i).setCandidates([8])
    grille._getCelluleCoord(3, 3).setCandidates([8])
    assert SolverHuman.candidatEnferme(grille)
    for i in range(9):
        if i!=1 and i!=7:
            assert 8 not in grille.getCelluleCandidatesZoneIndex(3, i)