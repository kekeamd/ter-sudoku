
import SolverBacktrack
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
        SolverBacktrackStats.stats["appelsRecursifs"] += 1
        for i in range(9):
            for j in range(9):
                if grille[i][j] == 0:
                    for val in range(1, 10):
                        SolverBacktrackStats.stats["testsEffectues"] += 1
                        if SolverBacktrack.isValid(grille, i, j, val):
                            grille[i][j] = val
                            if SolverBacktrackStats.solveGrille(grille):
                                SolverBacktrackStats.stats["valid"] = True
                                return True
                            grille[i][j] = 0
                            SolverBacktrackStats.stats["nbBacktracks"] += 1
                    return False
        SolverBacktrackStats.stats["valid"] = True
        return True
