from Parser import Parser
from Grille import Grille 
from Difficulte import Difficulte
from Zone import Zone
from SolverBacktrack import SolverBacktrack
from Except.GrilleError import GrilleError
from random import shuffle

#purpose: la grille de jeu avec le contenu généré par backtrack
#dependencies: Parser, Grille, Difficulte , SolveBacktrack, GrillError, shuffle
class GrilleBacktrack(Grille):
    #def __init__(): #overwritten
    #    super()
    def __init__(self, zoneList=None, size: int = 3):
        if zoneList is None:
            zoneList = [Zone() for _ in range(size * size)]
        super().__init__(zoneList, size)

    
    #purpose: renvoie le nombre de retraits(aka de cellules vides)
    def emptyCelluleCount(self) -> int: #gardez en tête qu'il n'y a pas de réponse exact pour ça donc j'ai fait des approximations(à revoir?)
        celluleCount = self.__size**4                       #nombre de cellule dans la grille
        minCelluleCount = (17//3)*self.__size               #nombre minimal de cellule avec une valeur pour grille autre que 9x9(approximatif)
        if (self.__size==3):
            minCelluleCount = 17                            #nombre minimal de cellule avec une valeur pour grille 9x9 (exact)
        potentialMaximum = celluleCount-minCelluleCount     #nombre maximal de cellule vide
        offset = 2**(self.__size-1)                         #nombre qu'il faut enlever pour éviter que ce soit trop dure
        if self.__difficulte == Difficulte.FACILE: #pour une grille 9*9: 28
            return potentialMaximum-(9*offset)
        elif self.__difficulte == Difficulte.MOYEN: #pour une grille 9x9: 40
            return potentialMaximum-(6*offset)
        elif self.__difficulte == Difficulte.DIFFICILE:#pour une grille 9x9: 48
            return potentialMaximum-(4*offset)
        elif self.__difficulte == Difficulte.EXTREME: #pour une grille 9x9: 56
            return potentialMaximum-(2*offset)
        elif self.__difficulte == Difficulte.GODMODE: #pour une grille 9x9: 60
            return potentialMaximum-offset
        elif self.__difficulte == None:
            raise(GrilleError("GrilleBacktrack : "))


    #purpose retire une valeur de la grille et renvoie sa valeur avec ses coordonnées
    def __removeValue(self) -> tuple[int, int, int]:# retour:  valeur, ligne, colonne
        rows=[i for i in range (9)]
        columns=[i for i in range (9)]
        shuffle(rows)
        shuffle(columns)
        tempGrille = self.clone()
        for row in rows:
            for col in columns:
                oldValue = self.getCelluleValueCoord(row, col)                          # On sauvegarde la valeur de la case
                if oldValue!=0:                                                         # On teste si la case est vide 
                    tempGrille.removeCelluleValueCoord(row, col)                        # Si elle ne l'est pas alors on la vide
                    if (SolverBacktrack.solutionIsUnique(tempGrille)):         # On vérifie qu'il n'y ait qu'une seule possibilité de résolution
                        return oldValue, row, col                                       # Si oui alors on renvoie valeur, ligne, colonne
                    else:                                                               # Sinon
                        tempGrille.setCelluleValueCoord(row, col, oldValue)             # On remets l'ancienne valeur
        return -1, -1, -1

    #purpose retire 'nbValues' valeurs de la grille
    def __removeValues(self, nbValues : int) -> None:
        tempGrille=self.clone()
        removedCells=[]
        i=0
        nbRemoved=0
        maxIteration = 9*nbValues
        while(i<=maxIteration) and (nbRemoved<=nbValues):
            val, row, col = self.__removeValue()        # On tente de supprimer une valeur
            if (val!=-1):                               # Si c'est possible alors j'ajoute la valeur à l'historique
                removedCells.append([val, row, col])
                nbRemoved+=1
            else:                                       # Sinon on va rétabli la dernière valeur supprimé
                if len(removedCells)<1:
                    raise(GrilleError("GrilleBacktrack : Impossible de supprimer des valeurs ! (Tableau Hist Vide)")) # Plus de valeurs à rétablir !
                else:
                    Cell=removedCells.pop()
                    self.setCelluleValueCoord(Cell[1], Cell[2], Cell[0])
                    nbRemoved-=1               # On diminue de 1 car on à rétabli une valeur supprimé
            i+=1
        if i>maxIteration:
            raise(GrilleError("GrilleBacktrack : Impossible de générer la grille avec le nombre de valeur demander.(ForceStop)"))



    #purpose: génère des valeurs et rempli la grille entièrement
    def generateEntireGrille(self) -> None:
        if (not SolverBacktrack.solveGrille(self)):
            raise(GrilleError("GrilleBacktrack : La génération de la grille entière a échoué."))
        return self


    #purpose: génère des valeurs et rempli la grille
    def generateValues(self, difficulte : Difficulte, grille : Grille = None) -> None:#avec grille la grille complète (optionnel)
        self.__setDifficulte(difficulte)
        if grille == None:
            self.generateEntireGrille()
        else:
            self.grille = grille
        Parser.grilleToFile(self, fileName="grilleSolution") #à modifier en fonction de comment on veux organiser les files
        nbValuesToRemove = self.emptyCelluleCount()
        self.__removeValues(nbValuesToRemove)
        Parser.grilleToFile(self, fileName="grilleInitale") #à modifier en fonction de comment on veux organiser les files


    #purpose: clone la grille (duh!)
    def clone(self):# -> Grille
        newGrille = []
        for i in range(self.__size**2):
            newGrille.append(self.__grille[i].clone())
        return Grille(newGrille)