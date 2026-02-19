from Solver import Solver
from Grille import Grille


class SolverHuman(Solver): #transformation de la classe en classe static parce qu'on ne veut absolument pas instancier des solvers T-T
    @staticmethod
    def solveGrille(grille : Grille) -> bool:
        pass

    
    @staticmethod
    def singleton() -> bool:
        pass
