from abc import ABC, abstractmethod
from Grille import Grille

class Solver(ABC): #transformation de la classe en classe static parce qu'on ne veut absolument pas instancier des solvers T-T
    @abstractmethod
    @staticmethod
    def solveGrille(grille : Grille) -> bool:
        pass


    @staticmethod
    def isValid(grille : Grille, row : int, column : int) -> bool:
        pass
