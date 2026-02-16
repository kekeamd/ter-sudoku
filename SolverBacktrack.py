from Solver import Solver
from Grille import Grille


class SolverBacktrack(Solver):
    @staticmethod
    def solveGrille(grille: Grille) -> bool:
        taille = grille.getSize() * grille.getSize()
        for i in range(taille):
            for j in range(taille):
                if grille.getCelluleValueCoord(i, j) == 0:
                    for val in range(1, taille + 1):
                        if Solver.isValid(grille, i, j, val):
                            grille.setCelluleValueCoord(i, j, val)
                            if SolverBacktrack.solveGrille(grille):
                                return True
                            grille.setCelluleValueCoord(i, j, 0)
                    return False
        return True


    @staticmethod
    def solutionIsUnique(grille : Grille) -> bool:
            copie=Grille.clone(grille) 
            return SolverBacktrack.countPossibilityLimit(copie) == 1


    @staticmethod
    def countPossibilityLimit(grille : Grille,limit : int = 2) -> int:
        taille=grille.getSize()*grille.getSize()
        count = 0
        for i in range(taille):
            for j in range(taille): 
                if grille.getCelluleValueCoord(i, j) == 0: 
                    for val in range(1, taille+1):
                        if Solver.isValid(grille, i, j, val):
                            grille.setCelluleValueCoord(i, j, val)
                            count += SolverBacktrack.countPossibilityLimit(grille)
                            if count >= limit:
                                return count
                            grille.setCelluleValueCoord(i, j, 0)
                    return count
        return 1


    @staticmethod
    def countPossibility(grille : Grille) -> int:
        taille=grille.getSize()*grille.getSize()
        count = 0
        for i in range(taille):
            for j in range(taille): 
                if grille.getCelluleValueCoord(i, j) == 0: 
                    for val in range(1, taille+1):
                        if Solver.isValid(grille, i, j, val):
                            grille.setCelluleValueCoord(i, j, val)
                            count += SolverBacktrack.countPossibility(grille)
                            grille.setCelluleValueCoord(i, j, 0)
                    return count
        return 1
