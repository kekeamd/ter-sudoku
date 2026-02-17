from Historique import Historique
from Grille import Grille
from Except.GrilleError import GrilleError

#purpose: manipulation d'historique de grille
#dependencies: Historique, Grille, GrillError
class HistoriqueNavigable : 
    def __init__(self):
        self._historique = Historique()
        self._historiqueProgress = Historique()
    def __init__(self, historique : Historique):
        self._historique = historique
        self._historiqueProgress = historique.__copy__()


    #purpose: renvoie la première grille de l'historique
    def getFirstGrille(self) -> Grille:
        return self._historique.getGrille(0)


    #purpose: renvoie la grille actuelle de l'historique
    def getGrille(self) -> Grille:
        index = self._historiqueProgress.lenHistorique()-1
        return self._historiqueProgress.getGrille(index)


    #purpose: renvoie le numéro de la grille actuelle de l'historique
    def getNumGrille(self) -> int:
        index = self._historiqueProgress.lenHistorique()-1
        return index


    #purpose: ajoute une grille à la fin de l'historique
    def addGrille(self, grille : Grille) -> None:
        if self._historique.lenHistorique() == self._historiqueProgress.lenHistorique(): #si notre progression de l'historique est à la dernière grille et on en rajoute une alors il faut actualiser la progression
            self._historiqueProgress.addGrille(grille)
        self._historique.addGrille(grille)


    #purpose: enlève la dernière grille de l'historique et la renvoie
    def removeLastGrille(self) -> Grille:
        grilleRemovedFromProgress = None
        if self._historique.lenHistorique() == self._historiqueProgress.lenHistorique(): #si notre progression de l'historique est à la dernière grille et on l'enlève alors il faut actualiser la progression
            grilleRemovedFromProgress = self._historiqueProgress.removeLastGrille()
        grilleRemovedFromHistorique = self._historique.removeLastGrille()
        
        if (grilleRemovedFromProgress!=None and grilleRemovedFromProgress!=grilleRemovedFromHistorique):    #failsafe  (si jamais le != ne fonctionne pas, il faudra penser à faire un equals dans grille)
            raise(GrilleError("GestionnaireHistorique : grille à la fin de historique et progress non identique (removeLastGrille)"))

        return grilleRemovedFromHistorique


    #purpose: passe à la grille précédente de l'historique
    def previousGrille(self) -> None:
        if self._historiqueProgress.lenHistorique()>1:
            self._historiqueProgress.removeLastGrille()


    #purpose: passe à la grille suivante de l'historique
    def nextGrille(self) -> None:
        if self._historiqueProgress.lenHistorique()< self._historique.lenHistorique():
            index = self._historiqueProgress.lenHistorique()-1
            self._historiqueProgress.addGrille(self._historique.getGrille(index))


    #purpose: affiche la grille actuelle de l'historique
    def printGrille(self) -> None:
        grille = self.getGrille()
        grille.printGrille()