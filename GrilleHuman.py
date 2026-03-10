from Grille import Grille
from GrilleBacktrack import GrilleBacktrack
from SolverHuman import SolverHuman
from SolverHumanStats import SolverHumanStats
from Difficulte import Difficulte

class GrilleHuman(GrilleBacktrack):
    # L'idee cest que on ne choisit plus la difficulte par nombre de cases enlevees, mais par les techniques
    # humaines necessaires pour resoudre la grille
    # Ici on modifie directement la grille de jeu via self, et on retourne les stats de la meilleure grille 
    # qu'on a pu generer pour la difficulte cible
    def generateValuesHumanRated(self, target: Difficulte, solution: Grille) -> dict:
        # 1) copier la solution dans self, self = grille entierement remplie
        N = self.getSize() * self.getSize()
        for i in range(N):
            for j in range(N):
                self.setCelluleValueCoord(i, j, solution.getCelluleValueCoord(i, j))

        # paramètres (à ajuster)
        max_attempts = 100 #limite de nbr de tentatives
        holes = 0 # compte le nbr de case suprimees

        min_holes = {
            Difficulte.FACILE: 28, 
            Difficulte.MOYEN: 34, 
            Difficulte.DIFFICILE: 40, 
            Difficulte.EXTREME: 48,
            Difficulte.GODMODE: 55
            }.get(target, 32)

        for _ in range(max_attempts):
            # essaie une suppression (unicité gérée dans _removeValue via solutionIsUnique)
            val, r, c = self._removeValue()
            if val == -1:
                break
            holes += 1

            test = self.clone()
            stats = SolverHumanStats.solveWithStats(test, raise_on_stuck=False) # recupere les stats
            rated = SolverHuman.rateFromStats(stats) # recupere la diffiuculté

            # condition de réussite
            if holes >= min_holes and rated == target:
                return stats

            # si on a dépassé la difficulté => on annule (règle simple)
            if target == Difficulte.FACILE and rated != Difficulte.FACILE:
                self.setCelluleValueCoord(r, c, val)
                holes -= 1
            elif target == Difficulte.MOYEN and rated == Difficulte.DIFFICILE:
                self.setCelluleValueCoord(r, c, val)
                holes -= 1

        # a la fin, self contient la grille finale pret pour resoudre et on fait un dernier solve pour obtenir les stats
        final_test = self.clone()
        final_stats = SolverHumanStats.solveWithStats(final_test, raise_on_stuck=False)
        return final_stats