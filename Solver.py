from abc import ABC, abstractmethod
from Grille import Grille
from Zone import Zone
from GrilleUtils import indexOfZone

class Solver(ABC): #transformation de la classe en classe static parce qu'on ne veut absolument pas instancier des solvers T-T
    @staticmethod
    @abstractmethod
    def solveGrille(grille : Grille) -> bool:
        pass


    @staticmethod
    def isValid(grille: Grille, row: int, column: int, value: int) -> bool:
        n = grille.getSize()
        N = n * n

        # ligne / colonne
        if grille.columnContainsValue(column, value) or grille.rowContainsValue(row, value):
            return False

        # bloc
        start_row = (row // n) * n
        start_col = (column // n) * n
        for r in range(start_row, start_row + n):
            for c in range(start_col, start_col + n):
                if grille.getCelluleValueCoord(r, c) == value:
                    return False

        return True

