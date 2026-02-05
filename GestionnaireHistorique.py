import Historique
import Grille

#purpose: manipulation d'historique de grille
#dependencies: Historique, Grille
class GestionnaireHistorique : 
    def __init__(self):
        self.__historique = Historique()
        self.__historiqueProgress = Historique()
    def __init__(self, historique : Historique):
        self.__historique = historique
        self.__historiqueProgress = historique.__copy__()


    #purpose: renvoie la première grille de l'historique
    def getFirstGrille(self) -> Grille:
        pass


    #purpose: renvoie la grille actuelle de l'historique
    def getGrille(self) -> Grille:
        pass


    #purpose: renvoie le numéro de la grille actuelle de l'historique
    def getNumGrille(self) -> int:
        pass


    #purpose: ajoute une grille à la fin de l'historique
    def addGrille(self, grille : Grille) -> None:
        pass


    #purpose: enlève la dernière grille de l'historique et la renvoie
    def delLastGrille(self) -> Grille:
        pass

    
    #purpose: passe à la grille précédente de l'historique
    def previousGrille(self) -> None:
        pass


    #purpose: passe à la grille suivante de l'historique
    def nextGrille(self) -> None:
        pass


    #purpose: affiche la grille actuelle de l'historique
    def printGrille(self) -> None:
        pass