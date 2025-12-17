# La difference de ce fichier avec le solveurSudoku.py est que ici on genere une grille vide et on la remplit aleatoirement
# puis on retire des valeurs pour obtenir une grille a resoudre
# Jai mis aussi la categorie de difficulte selon le nombre de backtracks observes pendant la resolution (regardez et me dite si ca vous va)
# Et aussi le nombre de valeurs quon retire peuvent dependre de la difficulte obtenue
# par exemple si la difficulte est facile on peut retirer moins de valeurs etc.


from random import randint
import parser as p
from grilleUtils import *


def is_valid(grille,row, column, val):
    # Vérifier la ligne
    if val in grille[row]:
        return False
    # Vérifier la colonne
    for i in range(9):
        if grille[i][column] == val:
            return False
    # Vérifier le carré 3x3
    start_row = (row // 3) * 3 # premier indice du carré (row)
    start_col = (column // 3) * 3 # premier indice du carré (column)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if grille[i][j] == val:
                return False
    return True
#stats = {'appelsRecursifs': 0, 'testsEffectues': 0, 'nbBacktracks': 0}
def solve(grille):
    stats['appelsRecursifs'] += 1 # j'utilise un dictionnaire pour stocker les statistiques
    vide = find_empty_cell(grille)
    if not vide:
        return True # Résolu
    row, column = vide
    for _ in range(9):
        val = randint(1, 9)
        stats['testsEffectues'] += 1
        if is_valid(grille, row, column, val):
            grille[row][column] = val
            if solve(grille):
                return True
            grille[row][column] = 0 # backtrack
            stats['nbBacktracks'] += 1
    return False


# Fonction pour solve sans stats
def solver(grille):
    vide = find_empty_cell(grille)
    if not vide:
        return True # Résolu
    row, column = vide
    for _ in range(9):
        val = randint(1, 9)
        if is_valid(grille, row, column, val):
            grille[row][column] = val
            if solver(grille):
                return True
            grille[row][column] = 0 # backtrack
    return False


def categorie_dificulte(nb_backtracks):
    if nb_backtracks < 250:
        return "Facile"
    elif nb_backtracks < 1000:
        return "Moyen"
    elif nb_backtracks < 5000:
        return "Difficile"
    elif nb_backtracks < 20000:
        return "Extrême"
    elif nb_backtracks < 100000:
        return "God Mode"

def retirer_valeurs(grille, nb_retraites):
    count = 0
    while count < nb_retraites:
        row = randint(0, 8)
        col = randint(0, 8)
        if grille[row][col] != 0:
            grille[row][col] = 0
            count += 1
    return grille

# Fonction qui génère une grille complète
def GrilleGenCompleted():
    out=grille_vide()
    if solver(out):
        return out
    else:
        return [] 

# Fonction qui génère une grille avec n valeur en moins
def GrilleGen(n):
    return retirer_valeurs(GrilleGenCompleted(),n)

if __name__ == "__main__":
    print("Grille vide :")
    p.clean()
    grille = grille_vide()
    print_grille(grille)
    p.grille_to_file(grille,"Generated_grille_empty")
    
    stats = {'appelsRecursifs': 0, 'testsEffectues': 0, 'nbBacktracks': 0}

    if solve(grille):
        print("\nGrille résolue :")
        print_grille(grille)

        print("\n--- Statistiques ---")
        print("Une solution trouvée")
        difficulte = categorie_dificulte(stats['nbBacktracks'])
        print(f"Difficulté de la grille : {difficulte}")
        print(f"Nombre d'appels récursifs : {stats['appelsRecursifs']}")
        print(f"Nombre de tests effectués : {stats['testsEffectues']}")
        print(f"Nombre de backtracks : {stats['nbBacktracks']}")
        print("\n---- Complexité ----")
        print("- k est le nombre des cases vides")
        print("- chaque case aurait jusqu’à 9 possibilités")
        print("Alors la complexité est O(9^k) dans le pire des cas.")
    else:
        print("Aucune solution trouvée.")
    p.grille_to_file(grille,"Generated_grille_completed")

    print("\nGrille avec des valeurs retirées:")
    # Retirer des valeurs selon la difficulte
    if difficulte == "Facile":
        nb_retraites = 40
    elif difficulte == "Moyen":
        nb_retraites = 50
    elif difficulte == "Difficile":
        nb_retraites = 60
    elif difficulte == "Extrême":
        nb_retraites = 65
    else:  # God Mode
        nb_retraites = 70
    grille_pour_resoudre = retirer_valeurs(grille, nb_retraites)
    print_grille(grille_pour_resoudre)
    p.grille_to_file(grille,"Generated_grille_uncompleted")