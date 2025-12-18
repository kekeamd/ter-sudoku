# La difference de ce fichier avec le solveurSudoku.py est que ici on genere une grille vide et on la remplit aleatoirement
# puis on retire des valeurs pour obtenir une grille a resoudre
# Jai mis aussi la categorie de difficulte selon le nombre de backtracks observes pendant la resolution (regardez et me dite si ca vous va)
# Et aussi le nombre de valeurs quon retire peuvent dependre de la difficulte obtenue
# par exemple si la difficulte est facile on peut retirer moins de valeurs etc.


from random import randint, shuffle
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
    nums = [i for i in range(1, 10)]
    shuffle(nums)
    for val in nums: 
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
    
    nums = [i for i in range(1, 10)]
    shuffle(nums)
    for val in nums:  
      if is_valid(grille, row, column, val):
            grille[row][column] = val
            if solver(grille):
                return True
            grille[row][column] = 0 # backtrack
    return False

# Fonction qui compte le nombre de possibilité de résolution pour grille
def comptePoss_limite(grille, limite=2):
    vide = find_empty_cell(grille)
    if not vide:
        return 1 #solution trouvée

    r, c = vide
    total = 0

    for val in range(1, 10):
        if is_valid(grille, r, c, val):
            grille[r][c] = val
            total += comptePoss_limite(grille, limite)
            grille[r][c] = 0  # backtrack encore :(

            # si on a deja atteint la limite, on s'arrête
            if total >= limite:
                return total

    return total


def categorie_dificulte(nb_backtracks):
    if nb_backtracks < 150:
        return "Facile"
    elif nb_backtracks < 350:
        return "Moyen"
    elif nb_backtracks < 1000:
        return "Difficile"
    elif nb_backtracks < 5000:
        return "Extrême"
    else:
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
    
    solution = GrilleGenCompleted()
    print("\nGrille résolue :")
    print_grille(solution)
    p.grille_to_file(solution, "Generated_grille_completed")

    nb_retraites = 45  # Nombre de valeurs à retirer pour créer une grille à résoudre
    grille_a_resoudre = retirer_valeurs(clone(solution), nb_retraites)
    print("\nGrille à résoudre:")
    print_grille(grille_a_resoudre)
    p.grille_to_file(grille_a_resoudre,"Generated_grille_uncompleted")

    stats = {'appelsRecursifs': 0, 'testsEffectues': 0, 'nbBacktracks': 0}

    grille_a_resoudre_Copie = clone(grille_a_resoudre)

    if solve(grille_a_resoudre_Copie):
        print("\n--- Statistiques ---")
        nb_solutions = comptePoss_limite(grille_a_resoudre, 2)  # pour compter les solutions
        print(f"Nombre de solutions trouvées : {nb_solutions}")  # mieux : sur le puzzle
        if nb_solutions == 1:
            print("La grille a une solution unique.")
        else:
            print("La grille a plusieurs solutions.")
        difficulte = categorie_dificulte(stats['nbBacktracks'])
        print(f"Difficulté de la grille : {difficulte}")
        print(f"Nombre d'appels récursifs : {stats['appelsRecursifs']}")
        print(f"Nombre de tests effectués : {stats['testsEffectues']}")
        print(f"Nombre de backtracks : {stats['nbBacktracks']}")
        print("La complexité est O(9^k) dans le pire des cas.")
    else:
        print("Erreur : La grille généré n'a pas de solution !")

    
    # Retirer des valeurs selon la difficulte
    #if difficulte == "Facile":
    #    nb_retraites = 40
    #elif difficulte == "Moyen":
    #    nb_retraites = 50
    #elif difficulte == "Difficile":
    #    nb_retraites = 60
    #elif difficulte == "Extrême":
    #    nb_retraites = 65
    #elif difficulte == "God Mode":
    #    nb_retraites = 70
    #grille_pour_resoudre = retirer_valeurs(grille, nb_retraites)
    #print_grille(grille_pour_resoudre)
    #p.grille_to_file(grille,"Generated_grille_uncompleted")