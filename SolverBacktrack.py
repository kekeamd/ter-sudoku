from Solver import Solver
from Grille import Grille


class SolverBacktrack(Solver): #transformation de la classe en classe static parce qu'on ne veut absolument pas instancier des solvers T-T
    @staticmethod
    def solveGrille(self,grille : Grille) -> bool:
        taille=grille.getSize()*grille.getSize()
        for i in range(taille):
            for j in range(taille): 
                if grille.getCelluleValueCoord(i, j) == 0: 
                    for val in range(1, taille+1):
                        if Solver.isValid(grille, i, j, val):
                            grille.setCelluleValueCoord(i, j, val)
                            if self.solveGrille(grille):
                                return True
                            grille.setCelluleValueCoord(i, j, 0)
                    return False
        return True


    @staticmethod

    def solutionIsUnique(self,grille : Grille) -> bool:
            copie=Grille.clone(grille) 
            return self.countPossibilityLimit(copie) == 1


    @staticmethod
    def countPossibilityLimit(self,grille : Grille,limit=2) -> int:
        taille=grille.getSize()*grille.getSize()
        count = 0
        for i in range(taille):
            for j in range(taille): 
                if grille.getCelluleValueCoord(i, j) == 0: 
                    for val in range(1, taille+1):
                        if self.isValid(grille, i, j, val):
                            grille.setCelluleValueCoord(i, j, val)
                            count += self.countPossibilityLimit(grille)
                            if count >= limit:
                                return count
                            grille.setCelluleValueCoord(i, j, 0)
                    return count
        return 1


    @staticmethod
    def countPossibility(self,grille : Grille) -> int:
        taille=grille.getSize()*grille.getSize()
        count = 0
        for i in range(taille):
            for j in range(taille): 
                if grille.getCelluleValueCoord(i, j) == 0: 
                    for val in range(1, taille+1):
                        if self.isValid(grille, i, j, val):
                            grille.setCelluleValueCoord(i, j, val)
                            count += self.countPossibility(grille)
                            grille.setCelluleValueCoord(i, j, 0)
                    return count
        return 1
