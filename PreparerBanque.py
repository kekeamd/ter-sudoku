from GrilleHuman import GrilleHuman
from Difficulte import Difficulte
from BanqueGrilles import BanqueGrilles


NB_GRILLES_PAR_DIFFICULTE = 8

difficultes = [
    Difficulte.FACILE,
    Difficulte.MOYEN,
    Difficulte.DIFFICILE,
    Difficulte.EXTREME,
    Difficulte.GODMODE
]


for difficulte in difficultes:
    print(f"\n========== Génération des grilles {difficulte.name} ==========")
    
    if difficulte == Difficulte.GODMODE: # pas besoin de plus de grilles extreme ou godmode car ca prend trop de temps
        NB_GRILLES_PAR_DIFFICULTE = 5
    elif difficulte == Difficulte.EXTREME:
        NB_GRILLES_PAR_DIFFICULTE = 5
    
    while BanqueGrilles.nombre_grilles(difficulte) < NB_GRILLES_PAR_DIFFICULTE:
        numero = BanqueGrilles.nombre_grilles(difficulte) + 1

        print(f"\nGrille {numero}/{NB_GRILLES_PAR_DIFFICULTE} pour {difficulte.name}")

        # 1. Générer une solution complète
        solution = GrilleHuman()
        solution.generateEntireGrille()

        # 2. Créer une grille de jeu à partir de cette solution
        grille_jeu = GrilleHuman()

        # 3. Enlever des valeurs jusqu'à obtenir la difficulté demandée
        stats = grille_jeu.generateValuesHumanRated(difficulte, solution)

        # 4. Si la grille correspond à la difficulté, on la sauvegarde
        if stats is not None:
            BanqueGrilles.ajouter_grille(
                difficulte,
                grille_jeu,
                solution,
                stats
            )
        else:
            print("Échec : aucune grille trouvée, nouvelle tentative...")

print("\nPréparation terminée.")
BanqueGrilles.afficher_resume()