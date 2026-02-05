from abc import ABC, abstractmethod

class Solver(ABC):
    def __init__(self, grille=None):
        self.grille = grille

    @abstractmethod
    def SolveGrille(self, grille):
        pass

    def EstValide(self, grille, ligne, colonne, valide):
        pass
