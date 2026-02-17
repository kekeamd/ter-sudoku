
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
    def solveGrille(grille : Grille) -> bool:
        taille = grille.getSize() * grille.getSize()
        SolverBacktrackStats.stats["appelsRecursifs"] += 1
        
        for i in range(taille):
            for j in range(taille):
                if grille.getCelluleValueCoord(i, j) == 0:
                    for val in range(1, taille + 1):
                        SolverBacktrackStats.stats["testsEffectues"] += 1
                        if SolverBacktrackStats.isValid(grille, i, j, val):
                            grille.setCelluleValueCoord(i, j, val)
                            if SolverBacktrackStats.solveGrille(grille):
                                SolverBacktrackStats.stats["valid"] = True
                                return True
                            grille.setCelluleValueCoord(i, j, 0)
                            SolverBacktrackStats.stats["nbBacktracks"] += 1
                    return False
        SolverBacktrackStats.stats["valid"] = True
        return True
