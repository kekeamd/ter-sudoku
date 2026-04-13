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
            "history": []
        }

        # Fonction pour avoir une matrice 2D de la grille actuel
        def snapshot_values():
            size = grille.getSize() ** 2
            return [[grille.getCelluleValueCoord(r, c) for c in range(size)] for r in range(size)]
        
        # Fonction pour trouver la valeur inserée après une étape de résolution
        def find_inserted_value(before, after):
            size = len(before)
            for r in range(size):
                for c in range(size):
                    if before[r][c] == 0 and after[r][c] != 0:
                        return {
                            "row": r,
                            "col": c,
                            "value": after[r][c]
                        }
            return None
        
        # Fonction pour stocker les stats
        def record(tech : Technique, move = None):
            stats["steps"] += 1
            stats["counts"][tech] += 1
            
            if stats["maxTechnique"] is None or tech > stats["maxTechnique"]:
                stats["maxTechnique"] = tech  # la technique la plus dur devient la technique posee en parametre
            
            # Ajouter des stats dans history
            stats["history"].append({
                "step": stats["steps"],
                "technique": tech,
                "move": move
            })

            # Early exit: already harder than the target difficulty
            if max_technique is not None and stats["maxTechnique"] is not None:
                if stats["maxTechnique"] > max_technique:
                    stats["stuck"] = True
                    stats["solved"] = False
                    return stats

        def try_and_record(tech: Technique, func):
            before = snapshot_values()
            if func(grille):
                after = snapshot_values()
                move = find_inserted_value(before, after)
                record(tech, move)
                return True
            return False

        grille.adjustCandidates()

        while not SolverHuman.isCompleted(grille):
            if try_and_record(Technique.DERNIER_NOMBRE, SolverHuman.dernierNombre):
                if stats["stuck"]: 
                    return stats  # vérifier après chaque record
                continue

            if try_and_record(Technique.SINGLETON_NU, SolverHuman.singletonNu):
                if stats["stuck"]:
                    return stats
                continue

            if try_and_record(Technique.SINGLETON_CACHE, SolverHuman.singletonCache):
                if stats["stuck"]:
                    return stats
                continue

            if try_and_record(Technique.PAIR_NU, SolverHuman.paireNu):
                if stats["stuck"]:
                    return stats
                continue

            if try_and_record(Technique.PAIR_CACHEE, SolverHuman.paireCachee):
                if stats["stuck"]:
                    return stats
                continue

            if try_and_record(Technique.CANDIDAT_ENFERME, SolverHuman.candidatEnferme):
                if stats["stuck"]:
                    return stats
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