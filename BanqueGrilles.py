import pickle      # permet de sauvegarder et recharger des objets Python dans un fichier
import random      # permet de choisir une grille au hasard
import os          # permet de verifier si le fichier existe déjà

from Difficulte import Difficulte


# nom du fichier dans lequel les grilles seront sauvegardées
FICHIER_BANQUE = "banque_grilles.pkl"


class BanqueGrilles:

    @staticmethod
    def creer_banque_vide():
        # créer une banque vide avec une liste pour chaque difficulté
        return {
            Difficulte.FACILE: [],
            Difficulte.MOYEN: [],
            Difficulte.DIFFICILE: [],
            Difficulte.EXTREME: [],
            Difficulte.GODMODE: []
        }

    @staticmethod
    def charger_banque():
        # si le fichier n'existe pas encore, on retourne une banque vide
        if not os.path.exists(FICHIER_BANQUE):
            return BanqueGrilles.creer_banque_vide()

        # Sinon, on charge la banque sauvegardée avec pickle
        with open(FICHIER_BANQUE, "rb") as fichier:
            return pickle.load(fichier)

    # sauvegarde toute la banque dans le fichier .pkl
    @staticmethod
    def sauvegarder_banque(banque):
        with open(FICHIER_BANQUE, "wb") as fichier:
            pickle.dump(banque, fichier)

    @staticmethod
    def ajouter_grille(difficulte, grille_jeu, grille_solution, stats):
        # charge la banque actuelle
        banque = BanqueGrilles.charger_banque()

        # preparer les informations à sauvegarder pour une grille
        entree = {
            "grille": grille_jeu.clone(),          # grille à résoudre
            "solution": grille_solution.clone(),   # grille complete solution
            "difficulte": difficulte,              # difficulté associée
            "stats": stats                         # stats du solveur humain
        }

        # ajouter la grille dans la liste correspondant à sa difficulté
        banque[difficulte].append(entree)

        # sauvegarde la banque mise à jour
        BanqueGrilles.sauvegarder_banque(banque)

        print(f"Grille sauvegardée en {difficulte.name}. Total = {len(banque[difficulte])}")

    # charge la banque depuis le fichier
    @staticmethod
    def charger_grille_aleatoire(difficulte):
        banque = BanqueGrilles.charger_banque()

        # récupèrer toutes les grilles correspondant à la difficulté demandée
        grilles = banque[difficulte]

        # vérifier qu'il existe au moins une grille pour cette difficulté
        if len(grilles) == 0:
            raise Exception(f"Aucune grille disponible pour {difficulte.name}")

        # retourne une grille choisie au hasard
        return random.choice(grilles)

    # retourner le nombre de grilles sauvegardées pour une difficulté donnée
    @staticmethod
    def nombre_grilles(difficulte):
        banque = BanqueGrilles.charger_banque()
        return len(banque[difficulte])

    # afficher le nombre de grilles disponibles pour chaque difficulté
    @staticmethod
    def afficher_resume():
        # afficher le nombre de grilles disponibles pour chaque difficulté
        banque = BanqueGrilles.charger_banque()

        print("\n===== BANQUE DE GRILLES =====")
        for difficulte in banque:
            print(f"{difficulte.name} : {len(banque[difficulte])} grille(s)")