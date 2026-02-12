from Grille import Grille

#purpose: historique de grilles
#dependencies: Grille 
class Historique :
    def __init__(self):
        self.__historique = []
    def __init__(self, grille : Grille):
        self.__historique = [grille]
    def __init__(self, grilleList : list[Grille]):
        self.__historique = grilleList


    #purpose:
    def getHistorique(self) -> list[Grille]:
        return self.__historique

    
    #purpose: taille de l'historique
    def lenHistorique(self) -> int:
        return len(self.__historique)


    #purpose: renvoie la grille à l'index 'index' de l'historique
    def getGrille(self, index) -> Grille:
        return self.__historique[index]


    #purpose: ajoute une grille à la fin de l'historique
    def addGrille(self, grille : Grille) -> None:
        self.__historique.append(grille)


    #purpose: enlève la dernière grille de l'historique et la renvoie
    def removeLastGrille(self) -> Grille:
        return self.__historique.pop()

