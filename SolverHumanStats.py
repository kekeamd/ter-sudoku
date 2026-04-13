from Except import SolverError
from SolverHuman import SolverHuman
from Grille import Grille
from Technique import Technique

class SolverHumanStats(SolverHuman):
    # Cette fonction applique les methodes humaines jusqu'a resolution ou blocage; retourne des stats
    @staticmethod
    def solveWithStats(grille : Grille, raise_on_stuck : bool = False, max_technique: Technique = None) -> dict:
        stats = {
            "solved": False,
            "stuck": False,
            "steps": 0, # nombre de valeurs posees
            "counts": {
                Technique.SINGLETON_NU: 0,
                Technique.DERNIER_NOMBRE: 0,
                Technique.SINGLETON_CACHE: 0,
                Technique.PAIR_NU: 0,
                Technique.PAIR_CACHEE: 0,
                Technique.CANDIDAT_ENFERME: 0,
                Technique.GRATTE_CIEL: 0,
            },
            "maxTechnique": None, # Technique la plus dur
        }

        # Fonction pour stocker les stats
        def record(tech : Technique):
            stats["steps"] += 1
            stats["counts"][tech] += 1
            if stats["maxTechnique"] is None or tech > stats["maxTechnique"]:
                stats["maxTechnique"] = tech  # la technique la plus dur devient la technique posee en parametre
            
            # Early exit: already harder than the target difficulty
            if max_technique is not None and stats["maxTechnique"] is not None:
                if stats["maxTechnique"] > max_technique:
                    stats["stuck"] = True
                    stats["solved"] = False
                    return stats
        
        grille.adjustCandidates()
        while not SolverHuman.isCompleted(grille):
            if SolverHuman.dernierNombre(grille):
                record(Technique.DERNIER_NOMBRE)
                if stats["stuck"]: return stats  # vérifier après chaque record
                continue

            if SolverHuman.singletonNu(grille):
                record(Technique.SINGLETON_NU)
                if stats["stuck"]: return stats
                continue

            if SolverHuman.singletonCache(grille):
                record(Technique.SINGLETON_CACHE)
                if stats["stuck"]: return stats
                continue

            if SolverHuman.paireNu(grille):
                record(Technique.PAIR_NU)
                if stats["stuck"]: return stats
                continue

            if SolverHuman.paireCachee(grille):
                record(Technique.PAIR_CACHEE)
                if stats["stuck"]: return stats
                continue

            if SolverHuman.candidatEnferme(grille):
                record(Technique.CANDIDAT_ENFERME)
                if stats["stuck"]: return stats
                continue
            if SolverHuman.gratteCiel(grille):     
                record(Technique.GRATTE_CIEL)
                if stats["stuck"]: return stats
                continue

            stats["stuck"] = True
            stats["solved"] = False
            if raise_on_stuck:
                raise SolverError(
                    "SolverHuman: Impossible de résoudre la grille avec des techniques implémentées !",
                    stats
                )
            return stats

        stats["solved"] = True
        return stats