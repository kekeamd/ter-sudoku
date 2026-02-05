from abc import ABC, abstractmethod

class Solver(ABC):
    def __init__(self, grille=None):
        self.grille = grille

    @abstractmethod
    def solveGrille(self, grille):
        pass

    def isValid(self, grille, ligne, colonne, valide):
        pass
