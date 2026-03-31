from Grille import Grille
from GrilleBacktrack import GrilleBacktrack
from SolverHuman import SolverHuman
from SolverHumanStats import SolverHumanStats
from Difficulte import Difficulte
from Technique import Technique

# Utilisé pendant le solve pour l'interrompre aussitôt qu'on sait que la grille est trop dure, sans finir de la résoudre
DIFFICULTY_MAX_TECHNIQUE = {
    Difficulte.FACILE:    Technique.DERNIER_NOMBRE,   # arrêter si on dépasse "dernier nombre"
    Difficulte.MOYEN:     Technique.SINGLETON_CACHE,  # arrêter si on dépasse "singleton caché"
    Difficulte.DIFFICILE: Technique.PAIR_CACHEE,      # arrêter si on dépasse "paire cachée"
    Difficulte.EXTREME:   Technique.CANDIDAT_ENFERME, # arrêter si on dépasse "candidat enfermé"
    Difficulte.GODMODE:   None,                       # pas de plafond, grille insolvable par nos techniques
}

class GrilleHuman(GrilleBacktrack):
    @staticmethod
    def matches_target(stats: dict, target: Difficulte) -> bool:
        counts = stats["counts"]
        max_tech = stats["maxTechnique"]

        if target == Difficulte.FACILE:
            return max_tech in (None, Technique.DERNIER_NOMBRE)

        if target == Difficulte.MOYEN:
            return (
                max_tech in (Technique.SINGLETON_NU, Technique.SINGLETON_CACHE)
                and counts[Technique.SINGLETON_CACHE] > 0
            )

        if target == Difficulte.DIFFICILE:
            return (
                max_tech in (Technique.PAIR_NU, Technique.PAIR_CACHEE)
                and (
                    counts[Technique.PAIR_NU] > 0
                    or counts[Technique.PAIR_CACHEE] > 0
                )
            )

        if target == Difficulte.EXTREME:
            return (
                max_tech == Technique.CANDIDAT_ENFERME
                and counts[Technique.CANDIDAT_ENFERME] > 0
            )

        if target == Difficulte.GODMODE:
            return stats["stuck"]

        return False
 
 
    # L'idee cest que on ne choisit plus la difficulte par nombre de cases enlevees, mais par les techniques
    # humaines necessaires pour resoudre la grille
    # Ici on modifie directement la grille de jeu via self, et on retourne les stats de la meilleure grille 
    # qu'on a pu generer pour la difficulte cible
    def generateValuesHumanRated(self, target: Difficulte, solution: Grille) -> dict:
        
        # Le cas speciale pour Difficile
        if target == Difficulte.DIFFICILE:
            return self.generateValuesDifficile(solution)
        
        # 1) copier la solution dans self, self = grille entierement remplie
        N = self.getSize() * self.getSize()
        for i in range(N):
            for j in range(N):
                self.setCelluleValueCoord(i, j, solution.getCelluleValueCoord(i, j))

        # paramètres (à ajuster)
        max_attempts = 100
        holes = 0

        min_holes = {
            Difficulte.FACILE: 28,
            Difficulte.MOYEN: 34,
            Difficulte.DIFFICILE: 40,
            Difficulte.EXTREME: 48,
            Difficulte.GODMODE: 55
        }.get(target, 32)

        max_holes = {
            Difficulte.FACILE: 36,
            Difficulte.MOYEN: 42,
            Difficulte.DIFFICILE: 55,
            Difficulte.EXTREME: 58,
            Difficulte.GODMODE: 64
        }.get(target, 81)

        max_technique = DIFFICULTY_MAX_TECHNIQUE.get(target)

        for _ in range(max_attempts):
            # essaie une suppression (unicité gérée dans _removeValue via solutionIsUnique)
            val, r, c = self._removeValue()
            if val == -1:
                break
            holes += 1

            # nouveau : ne pas dépasser le nombre max de trous
            if holes > max_holes:
                self.setCelluleValueCoord(r, c, val)
                holes -= 1
                continue

            # Don't solve until we have enough holes to matter
            if holes < min_holes:
                continue

            test = self.clone()
            stats = SolverHumanStats.solveWithStats(
                test,
                raise_on_stuck=False,
                max_technique=max_technique
            )
            rated = SolverHuman.rateFromStats(stats)

            # condition de réussite
            if GrilleHuman.matches_target(stats, target):
                return stats

            # si on a dépassé la difficulté => on annule
            if target == Difficulte.FACILE and rated != Difficulte.FACILE:
                self.setCelluleValueCoord(r, c, val)
                holes -= 1
            elif target == Difficulte.MOYEN and rated == Difficulte.DIFFICILE:
                self.setCelluleValueCoord(r, c, val)
                holes -= 1
            elif target == Difficulte.DIFFICILE and rated in (Difficulte.EXTREME, Difficulte.GODMODE):
                self.setCelluleValueCoord(r, c, val)
                holes -= 1

        # a la fin, self contient la grille finale prête à résoudre
        final_test = self.clone()
        final_stats = SolverHumanStats.solveWithStats(final_test, raise_on_stuck=False)
        return final_stats
    
    def generateValuesDifficile(self, solution: Grille) -> dict:
        N = self.getSize() * self.getSize()

        min_holes = 46
        max_holes = 53
        max_attempts = 120
        max_restarts = 20

        best_snapshot = None
        best_stats = None

        for restart in range(max_restarts):
            # repartir d'une grille complète neuve à chaque restart
            for i in range(N):
                for j in range(N):
                    self.setCelluleValueCoord(i, j, solution.getCelluleValueCoord(i, j))

            holes = 0
            attempts = 0

            print(f"\n------- Restart {restart + 1}/{max_restarts} -----")

            while attempts < max_attempts and holes < max_holes:
                attempts += 1

                val, r, c = self._removeValue()
                if val == -1:
                    break

                holes += 1

                if holes < min_holes:
                    continue

                test = self.clone()
                stats = SolverHumanStats.solveWithStats(
                    test,
                    raise_on_stuck=False,
                    max_technique=Technique.PAIR_CACHEE
                )

                counts = stats["counts"]
                pair_count = counts[Technique.PAIR_NU] + counts[Technique.PAIR_CACHEE]
                max_tech = stats["maxTechnique"]

                # cible atteinte pour DIFFICILE
                if (
                    stats["solved"]
                    and not stats["stuck"]
                    and max_tech in (Technique.PAIR_NU, Technique.PAIR_CACHEE)
                    and pair_count >= 1
                    and counts[Technique.CANDIDAT_ENFERME] == 0
                ):
                    return stats

                # trop dur -> revert et continuer
                if stats["stuck"] or counts[Technique.CANDIDAT_ENFERME] > 0:
                    print(
                        f"  TROP DUR à holes={holes}, "
                        f"maxTech={max_tech}, "
                        f"candidatEnferme={counts[Technique.CANDIDAT_ENFERME]}"
                    )
                    self.setCelluleValueCoord(r, c, val)
                    holes -= 1
                    continue

                # encore trop facile mais valide -> garder le meilleur snapshot global
                if stats["solved"] and not stats["stuck"]:
                    print(f"  holes={holes}, maxTech={max_tech}, pairs={pair_count}")

                    best_snapshot = [
                        [self.getCelluleValueCoord(i, j) for j in range(N)]
                        for i in range(N)
                    ]
                    best_stats = stats

        # après TOUS les restarts seulement
        if best_stats is not None and best_snapshot is not None:
            for i in range(N):
                for j in range(N):
                    self.setCelluleValueCoord(i, j, best_snapshot[i][j])
            return best_stats

        # sinon, on analyse la grille actuelle une seule fois à la fin
        final_test = self.clone()
        return SolverHumanStats.solveWithStats(final_test, raise_on_stuck=False)