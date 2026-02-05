from abc import ABC, abstractmethod
from .Difficulte import Difficulte

# ABC = Abstract Base Class
# ABC existe pour forcer Python à se comporter comme Java avec les classes abstraites

class Interface(ABC): # ne peux pas l'instancier, sert de modele
    def __init__(self):
        self.grilleDeJeu = None
        self.grilleComplete = None
    
    @abstractmethod # Toute classe qui hérite de Interface doit implémenter cette méthode
    def startPlaying(self):
        pass

    @abstractmethod
    def demanderChoix(self) -> str:
        pass

    @abstractmethod
    def demanderDifficulte(self) -> Difficulte:
        pass

    @abstractmethod
    def jouerSudoku(self):
        pass