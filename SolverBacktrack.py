from Solver import Solver
from Grille import Grille


class SolverBacktrack(Solver): #transformation de la classe en classe static parce qu'on ne veut absolument pas instancier des solvers T-T
    @staticmethod
    def solveGrille(grille : Grille) -> bool:
        pass


    @staticmethod
    def SolutionIsUnique(grille : Grille) -> bool:
        pass


    @staticmethod
    def countPossibilityLimit(grille : Grille) -> int:
        pass


    @staticmethod
    def countPossibility(grille : Grille) -> int:
        pass
