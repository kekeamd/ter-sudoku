from Solver import Solver
from Grille import Grille
import copy


class SolverBacktrack(Solver): #transformation de la classe en classe static parce qu'on ne veut absolument pas instancier des solvers T-T
    @staticmethod
    def solveGrille(grille : Grille) -> bool:
        for i in range(9):
            for j in range(9): 
                if grille[i][j] == 0: 
                    for val in range(1, 10):
                        if Solver.isValid(grille, i, j, val):
                            grille[i][j] = val
                            if SolverBacktrack.solveGrille(grille):
                                return True
                            grille[i][j] = 0
                    return False
        return True


    @staticmethod
    def SolutionIsUnique(grille : Grille) -> bool:
            copie=Grille.clone(grille) 
            return SolverBacktrack.countPossibilityLimit(copie) == 1


    @staticmethod
    def countPossibilityLimit(grille : Grille) -> int:
        count = 0
        for i in range(9):
            for j in range(9): 
                if grille[i][j] == 0: 
                    for val in range(1, 10):
                        if Solver.isValid(grille, i, j, val):
                            grille[i][j] = val
                            count += SolverBacktrack.countPossibilityLimit(grille)
                            if count >= 2:
                                return count
                            grille[i][j] = 0
                    return count
        return 1


    @staticmethod
    def countPossibility(grille : Grille) -> int:
        count = 0
        for i in range(9):
            for j in range(9): 
                if grille[i][j] == 0: 
                    for val in range(1, 10):
                        if Solver.isValid(grille, i, j, val):
                            grille[i][j] = val
                            count += SolverBacktrack.countPossibility(grille)
                            grille[i][j] = 0
                    return count
        return 1
