
from SolverBacktrack import SolverBacktrack
from Grille import Grille

class SolverBacktrackStats(SolverBacktrack): #transformation de la classe en classe static parce qu'on ne veut absolument pas instancier des solvers T-T
    stats = {
            "appelsRecursifs": 0,
            "testsEffectues": 0,
            "nbBacktracks": 0,
            "valid": False
        }
    @staticmethod
    def solveGrille(self,grille : Grille) -> bool:
        taille=grille.getSize()*grille.getSize()
        self.stats["appelsRecursifs"] += 1
        for i in range(taille):
            for j in range(taille):
                if grille.getCelluleValueCoord(i, j) == 0:
                    for val in range(1, 10):
                        self.stats["testsEffectues"] += 1
                        if self.isValid(grille, i, j, val):
                            grille.setCelluleValueCoord(i, j, val)
                            if self.solveGrille(grille):
                                self.stats["valid"] = True
                                return True
                            grille.setCelluleValueCoord(i, j, 0)
                            self.stats["nbBacktracks"] += 1
                    return False
        self.stats["valid"] = True
        return True
