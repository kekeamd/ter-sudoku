from abc import ABC, abstractmethod
from Grille import Grille

class Solver(ABC): #transformation de la classe en classe static parce qu'on ne veut absolument pas instancier des solvers T-T
    @staticmethod
    @abstractmethod
    def solveGrille(grille : Grille) -> bool:
        pass


    @staticmethod
    def isValid(grille : Grille, row : int, column : int, value : int) -> bool:
        for c in range(9):
            if grille[row][c] == value:
                return False
        for l in range(9):
            if grille[l][column] == value:
                return False
        start_l = (row // 3) * 3
        start_c = (column // 3) * 3
        for l in range(start_l, start_l + 3):
            for c in range(start_c, start_c + 3):
                if grille[l][c] == value:
                    return False
        return True
