from SolverHuman import SolverHuman
from Grille import Grille

class SolverHumanStats(SolverHuman): #transformation de la classe en classe static parce qu'on ne veut absolument pas instancier des solvers T-T
    @staticmethod
    def solveGrille(grille : Grille) -> bool:
        pass