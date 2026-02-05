from Interface import Interface  # import le classe parent (Interface)
from Difficulte import Difficulte

class InterfaceWeb(Interface): # extends Interface
    def __init__(self):
        super().__init__()

    # Méthodes obligatoires à définir
    def startPlaying(self):
        pass

    def askChoice(self) -> str:
        pass

    def askDifficulty(self) -> Difficulte:
        pass

    def playSudoku(self):
        pass

    # Méthodes suplémentaires