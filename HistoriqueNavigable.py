from Historique import Historique
from Grille import Grille
from Except.GrilleError import GrilleError

#purpose: manipulation d'historique de grille
#dependencies: Historique, Grille, GrillError
class HistoriqueNavigable : 
    def __init__(self):
        self.__historique = Historique()
        self.__historiqueProgress = Historique()
    def __init__(self, historique : Historique):
        self.__historique = historique
        self.__historiqueProgress = historique.__copy__()


    #purpose: renvoie la première grille de l'historique
    def getFirstGrille(self) -> Grille:
        return self.__historique.getGrille(0)


    #purpose: renvoie la grille actuelle de l'historique
    def getGrille(self) -> Grille:
        index = self.__historiqueProgress.lenHistorique()-1
        return self.__historiqueProgress.getGrille(index)


    #purpose: renvoie le numéro de la grille actuelle de l'historique
    def getNumGrille(self) -> int:
        index = self.__historiqueProgress.lenHistorique()-1
        return index


    #purpose: ajoute une grille à la fin de l'historique
    def addGrille(self, grille : Grille) -> None:
        if self.__historique.lenHistorique() == self.__historiqueProgress.lenHistorique(): #si notre progression de l'historique est à la dernière grille et on en rajoute une alors il faut actualiser la progression
            self.__historiqueProgress.addGrille(grille)
        self.__historique.addGrille(grille)


    #purpose: enlève la dernière grille de l'historique et la renvoie
    def removeLastGrille(self) -> Grille:
        grilleRemovedFromProgress = None
        if self.__historique.lenHistorique() == self.__historiqueProgress.lenHistorique(): #si notre progression de l'historique est à la dernière grille et on l'enlève alors il faut actualiser la progression
            grilleRemovedFromProgress = self.__historiqueProgress.removeLastGrille()
        grilleRemovedFromHistorique = self.__historique.removeLastGrille()
        
        if (grilleRemovedFromProgress!=None and grilleRemovedFromProgress!=grilleRemovedFromHistorique):    #failsafe  (si jamais le != ne fonctionne pas, il faudra penser à faire un equals dans grille)
            raise(GrilleError("GestionnaireHistorique : grille à la fin de historique et progress non identique (removeLastGrille)"))

        return grilleRemovedFromHistorique


    #purpose: passe à la grille précédente de l'historique
    def previousGrille(self) -> None:
        if self.__historiqueProgress.lenHistorique()>1:
            self.__historiqueProgress.removeLastGrille()


    #purpose: passe à la grille suivante de l'historique
    def nextGrille(self) -> None:
        if self.__historiqueProgress.lenHistorique()< self.__historique.lenHistorique():
            index = self.__historiqueProgress.lenHistorique()-1
            self.__historiqueProgress.addGrille(self.__historique.getGrille(index))


    #purpose: affiche la grille actuelle de l'historique
    def printGrille(self) -> None:
        grille = self.getGrille()
        grille.printGrille()