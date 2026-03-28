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
            # L'ordre ici est tres important car il influence la trace et les stats, alors j'ai choisi de les 
            # faire de plus simple vers le plus dur
            if SolverHuman.dernierNombre(grille):
                record(Technique.DERNIER_NOMBRE)
                continue

            if SolverHuman.singletonNu(grille):
                record(Technique.SINGLETON_NU)
                continue

            if SolverHuman.singletonCache(grille):
                record(Technique.SINGLETON_CACHE)
                continue

            if SolverHuman.paireNu(grille):
                record(Technique.PAIR_NU)
                continue

            if SolverHuman.paireCachee(grille):
                record(Technique.PAIR_CACHEE)
                continue

            if SolverHuman.candidatEnferme(grille):
                record(Technique.CANDIDAT_ENFERME)
                continue

            # bloqué
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