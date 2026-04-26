from Grille import Grille
from GrilleBacktrack import GrilleBacktrack
from SolverHuman import SolverHuman
from SolverHumanStats import SolverHumanStats
from Difficulte import Difficulte
from Technique import Technique

# Utilisé pendant le solve pour l'interrompre aussitôt qu'on sait que la grille est trop dure, sans finir de la résoudre
DIFFICULTY_MAX_TECHNIQUE = {
    Difficulte.FACILE:    Technique.SINGLETON_NU,     # arrêter si on dépasse "dernier nombre"
    Difficulte.MOYEN:     Technique.SINGLETON_CACHE,  # arrêter si on dépasse "singleton caché"
    Difficulte.DIFFICILE: Technique.CANDIDAT_ENFERME, # DIFFICILE tolère au maximum 1 candidat enfermé
    Difficulte.EXTREME:   Technique.GRATTE_CIEL,      # arrêter si on dépasse "gratte ciel"
    Difficulte.GODMODE:   None,                       # pas de plafond, grille insolvable par nos techniques
}

GEN_PARAMS = {
    Difficulte.FACILE: {
        "min_holes": 26,
        "max_holes": 34,
        "max_attempts": 120,
        "max_restarts": 10,
        "max_technique": Technique.SINGLETON_NU,
        "test_every": 1,
    },
    Difficulte.MOYEN: {
        "min_holes": 28,
        "max_holes": 40,
        "max_attempts": 140,
        "max_restarts": 30,
        "max_technique": Technique.SINGLETON_CACHE,
        "test_every": 1,
    },
    Difficulte.DIFFICILE: {
        "min_holes": 42,
        "max_holes": 54,
        "max_attempts": 160,
        "max_restarts": 15,
        "max_technique": Technique.CANDIDAT_ENFERME,
        "test_every": 1,
    },
    Difficulte.EXTREME: {
        "min_holes": 46,
        "max_holes": 60,
        "max_attempts": 120,
        "max_restarts": 15,
        "max_technique": Technique.GRATTE_CIEL,
        "test_every": 1,
    },
    Difficulte.GODMODE: {
        "min_holes": 54,
        "max_holes": 64,
        "max_attempts": 80,
        "max_restarts": 15,
        "max_technique": None,
        "test_every": 2,
    },
}

class GrilleHuman(GrilleBacktrack):
    @staticmethod
    def matches_target(stats: dict, target: Difficulte) -> bool:
        counts = stats["counts"]
        max_tech = stats["maxTechnique"]

        if target == Difficulte.GODMODE:
            return stats["stuck"] and not stats["solved"]

        # IMPORTANT :
        # Pour toutes les autres difficultés, la grille doit être complètement résolue par le solveur humain
        if not stats["solved"] or stats["stuck"]:
            return False

        if target == Difficulte.FACILE:
            return max_tech in (None, Technique.DERNIER_NOMBRE, Technique.SINGLETON_NU)

        if target == Difficulte.MOYEN:
            return (
                max_tech in (Technique.SINGLETON_NU, Technique.SINGLETON_CACHE)
                and counts[Technique.SINGLETON_CACHE] > 0
                and counts[Technique.PAIR_NU] == 0
                and counts[Technique.PAIR_CACHEE] == 0
                and counts[Technique.CANDIDAT_ENFERME] == 0
                and counts[Technique.GRATTE_CIEL] == 0
            )

        if target == Difficulte.DIFFICILE:
            return (
                max_tech in (
                    Technique.PAIR_NU,
                    Technique.PAIR_CACHEE,
                    Technique.CANDIDAT_ENFERME
                )
                and (
                    counts[Technique.PAIR_NU] > 0
                    or counts[Technique.PAIR_CACHEE] > 0
                )
                and counts[Technique.CANDIDAT_ENFERME] <= 1
                and counts[Technique.GRATTE_CIEL] == 0
            )

        if target == Difficulte.EXTREME:
            return (
                (
                    max_tech == Technique.GRATTE_CIEL
                    and counts[Technique.GRATTE_CIEL] > 0
                )
                or (
                    max_tech == Technique.CANDIDAT_ENFERME
                    and counts[Technique.CANDIDAT_ENFERME] >= 2
                )
            )

        return False
 
 
    def _removeValueAvoiding(self, banned_positions: set, max_tries: int = 30):
        for _ in range(max_tries):
            val, r, c = self._removeValue()

            if val == -1:
                return val, r, c

            if (r, c) not in banned_positions:
                return val, r, c

            # Cette position a déjà rendu la grille trop dure,
            # donc on annule immédiatement et on réessaie ailleurs
            self.setCelluleValueCoord(r, c, val)

        return -1, -1, -1

    # L'idee cest que on ne choisit plus la difficulte par nombre de cases enlevees, mais par les techniques
    # humaines necessaires pour resoudre la grille
    # Ici on modifie directement la grille de jeu via self, et on retourne les stats de la meilleure grille 
    # qu'on a pu generer pour la difficulte cible
    def generateValuesHumanRated(self, target: Difficulte, solution: Grille) -> dict:
        N = self.getSize() * self.getSize()
        params = GEN_PARAMS[target]

        for restart in range(params["max_restarts"]):
            for i in range(N):
                for j in range(N):
                    self.setCelluleValueCoord(i, j, solution.getCelluleValueCoord(i, j))

            holes = 0
            attempts = 0

            # Positions à éviter pendant ce restart
            # Ça empeche de retester toujours la meme case qui rend la grille trop dure
            banned_positions = set()
            too_hard_count = 0
            max_too_hard = 12

            print(f"\n------- Restart {target.name} {restart + 1}/{params['max_restarts']} -----")

            while attempts < params["max_attempts"] and holes < params["max_holes"]:
                attempts += 1

                val, r, c = self._removeValueAvoiding(banned_positions)

                if val == -1:
                    # Si on ne peut plus retirer de valeur, on teste quand meme la grille actuelle.
                    test = self.clone()
                    stats = SolverHumanStats.solveWithStats(
                        test,
                        raise_on_stuck=False,
                        max_technique=params["max_technique"]
                    )

                    if GrilleHuman.matches_target(stats, target):
                        return stats

                    break

                holes += 1

                if holes < params["min_holes"]:
                    continue

                if holes % params["test_every"] != 0:
                    continue

                test = self.clone()
                stats = SolverHumanStats.solveWithStats(
                    test,
                    raise_on_stuck=False,
                    max_technique=params["max_technique"]
                )

                # Condition de réussite
                if GrilleHuman.matches_target(stats, target):
                    return stats

                # Pour GODMODE, on ne rollback jamais une grille résoluble
                # On continue à enlever des cases pour chercher un blocage
                if target == Difficulte.GODMODE:
                    continue

                # Pour les autres niveaux, si le solver bloque,
                # c'est que la grille est devenue trop dure
                if stats["stuck"]:
                    print(
                        f" TROP DUR à holes={holes}, "
                        f"maxTech={params['max_technique']}, "
                        f"case=({r},{c})"
                    )

                    self.setCelluleValueCoord(r, c, val)
                    holes -= 1

                    # On interdit cette position pour éviter de refaire le même échec
                    banned_positions.add((r, c))
                    too_hard_count += 1

                    # Si ce restart bloque trop souvent, on passe au restart suivant
                    if too_hard_count >= max_too_hard:
                        print(" Trop de blocages dans ce restart, restart suivant.")
                        break

                    continue

            # test final du restart
            test = self.clone()
            stats = SolverHumanStats.solveWithStats(
                test,
                raise_on_stuck=False,
                max_technique=params["max_technique"]
            )

            if GrilleHuman.matches_target(stats, target):
                return stats

        return None