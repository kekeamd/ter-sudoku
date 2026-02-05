from abc import ABC, abstractmethod
import Difficulte, Zone, Grille

#purpose: bah la grille de sudoku
#dependencies: Difficulte, Zone, Grille
class Grille(ABC):
    def __init__(self):
        self.__grille = []
        self.__difficulte = None
    def __init__(self, zoneList : list , sizeCote : int = 3): #sizeCote à revoir (est-ce vraiment utile?? checks supplémentaire à faire???)
        self.__grille = zoneList
        self.__difficulte = None
    

    #purpose: génère des valeurs et rempli la grille
    @abstractmethod
    def generateValues(self, difficulte : Difficulte) -> None:
        pass


    #purpose: renvoie la difficulté de la grille
    def getDifficulte(self)-> Difficulte:
        pass


    #purpose: défini la difficulté de la grille
    def setDifficulte(self, difficulte : Difficulte) -> None:
        pass


    #purpose: renvoie vrai si la ligne numéro 'line' contient la valeur 'value' et faux sinon
    def lineContainsValue(self, line : int, value : int) ->  bool:
        pass


    #purpose: renvoie vrai si la colonne numéro 'column' contient la valeur 'value' et faux sinon
    def lineContainsValue(self, column: int, value : int) ->  bool:
        pass


    #purpose: renvoie la ligne numéro 'line'
    def getLine(self, line : int) -> list:
        pass


    #purpose: renvoie la colonne numéro 'column'
    def getColumn(self, column : int) -> list:
        pass


    #purpose: rectifie les listes de candidats des cellules de la zone 'zone'
    def __adjustCandidatesZone(self, zone : Zone) -> None:
        pass


    #purpose: rectifie les listes de candidats des cellules de la ligne 'line'
    def __adjustCandidatesLine(self, line : int) -> None:
        pass


    #purpose: rectifie les listes de candidats des cellules de la colonne 'column'
    def __adjustCandidatesColumn(self, column : int) -> None:
        pass


    #purpose: rectifie les listes de candidats des cellules de la grille
    def adjustCandidates(self) -> None:
        pass


    #purpose: rectifie la liste de candidats de la cellule aux coordonnées ('line', 'column')
    def adjustCandidatesAfterAddingValueCoord(self, line : int, column : int) -> None:
        pass


    #purpose: rectifie la liste de candidats de la cellule d'index 'index' dans la zone 'zone'
    def adjustCandidatesAfterAddingValueIndex(self, zone : Zone, index : int) -> None:
        pass


    #purpose: défini la valeur de la cellule aux coordonnées ('line', 'column')
    def setCelluleValueCoord(self, line : int, column : int) -> None:
        pass


    #purpose: défini la valeur de la cellule d'index 'index' dans la zone 'zone'
    def setCelluleValueIndex(self, zone : Zone, index : int) -> None:
        pass


    #purpose: enlève la valeur de la cellule aux coordonnées ('line', 'column')
    def removeCelluleValueCoord(self, line : int, column : int) -> None:
        pass


    #purpose: enlève la valeur de la cellule d'index 'index' dans la zone 'zone'
    def removeCelluleValueIndex(self, zone : Zone, index : int) -> None:
        pass


    #purpose: clone la grille (duh!)
    def clone(self) -> Grille:
        pass


    #purpose: affiche la grille
    def printGrille(self) -> None:
        pass


    #purpose: renvoie la grille sous forme de chaine de caractères
    def toString(self) -> str:
        pass