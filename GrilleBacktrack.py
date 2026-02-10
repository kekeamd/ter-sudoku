from Grille import Grille 
from Difficulte import Difficulte
from SolverBacktrack import SolverBacktrack
from Except.GrilleError import GrilleError

#purpose: la grille de jeu avec le contenu généré par backtrack
#dependencies: Grille, Difficulte , SolveBacktrack, GrillError
class GrilleBacktrack(Grille):
    def __init__():
        super()
    def __init__(zoneList : list , size : int = 3):
        super(zoneList, size)

    
    #purpose: renvoie le nombre de retraits(aka de cellules vides)
    def emptyCelluleCount(self) -> int:
        if self.__difficulte == Difficulte.FACILE:
            return 40
        elif self.__difficulte == Difficulte.MOYEN:
            return 50
        elif self.__difficulte == Difficulte.DIFFICILE:
            return 60
        elif self.__difficulte == Difficulte.EXTREME:
            return 65
        elif self.__difficulte == Difficulte.GODMODE:
            return 70


    #purpose retire une valeur de la grille et la renvoie (sans aucun checks)
    def __removeValue(self) -> int: #s'inspirer de ./old/genererGrille.retirevaleur()
        pass


    #purpose retire 'nbValues' valeurs de la grille (tout en conservant l'unicite)
    def __removeValues(self, nbValues : int) -> None: #s'inspirer de ./old/genererGrille.GrilleGen()
        pass



    #purpose: génère des valeurs et rempli la grille entièrement
    def generateEntireGrille(self) -> None:
        if (not SolverBacktrack.solveGrille(self)):
            raise(GrilleError("GrilleBacktrack : La génération de la grille entière a échoué."))


    #purpose: génère des valeurs et rempli la grille
    def generateValues(self, difficulte : Difficulte) -> None:
        self.generateEntireGrille()
        #removeValues et plus
        pass
