# self = this in java
# __init__ = constructeur

from Interface import Interface  # import le classe parent (Interface)
from Difficulte import Difficulte


class InterfaceConsole(Interface): # extends Interface

    def __init__(self): # constructeur InterfaceConsole()
        super().__init__()

    def startPlaying(self): # demande le choix: si 1: jouer Sudoku; si 2: quitter
        pass

    def askChoice(self) -> str: # soit generer une grille et jouer, soit quitter
        pass

    def askDifficulty(self) -> Difficulte: # demande la difficulté à propos de nbr de retraites
        pass

    def playSudoku(self): # prends la difficulté, la grille complete, fait la grille prete à resoudre et appele gameLoop
        pass

    def gameLoop(self): # soit entrer une valeur(appelle playMove()), soit donner la grille complete, soit quitter
        pass

    def playMove(self): # entrer une certain valeur sur un certian ligne et colenne, verifie si cest bon en comparaison avec la grille complete
        pass

    def giveFullGrid(self): # donne une grille complete pour traité dans playSudoku
        pass

    def quit(self): # ou tout simplement break
        pass