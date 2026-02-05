import Grille

#purpose: historique de grilles
#dependencies: Grille 
class Historique :
    def __init__(self):
        self.__historique = []
    def __init__(self, grille : Grille):
        self.__historique = [grille]
    def __init__(self, grilleList : list):
        self.__historique = grilleList


    #purpose:
    def getHistorique(self) -> list:
        pass

    
    #purpose: taille de l'historique
    def lenHistorique(self) -> int:
        pass


    #purpose: renvoie la grille à l'index 'index' de l'historique
    def getGrille(self, index) -> Grille:
        pass


    #purpose: ajoute une grille à la fin de l'historique
    def addGrille(self, grille : Grille) -> None:
        pass


    #purpose: enlève la dernière grille de l'historique et la renvoie
    def delLastGrille(self) -> Grille:
        pass

