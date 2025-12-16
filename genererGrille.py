# La difference de ce fichier avec le solveurSudoku.py est que ici on genere une grille vide et on la remplit aleatoirement
# puis on retire des valeurs pour obtenir une grille a resoudre
# Jai mis aussi la categorie de difficulte selon le nombre de backtracks observes pendant la resolution (regardez et me dite si ca vous va)
# Et aussi le nombre de valeurs quon retire peuvent dependre de la difficulte obtenue
# par exemple si la difficulte est facile on peut retirer moins de valeurs etc.


from random import randint

def print_grille(grille):
    for row in range(9):
        line = ""
        for column in range(9):
            val = grille[row][column]
            line += str(val) if val != 0 else "."
            if column % 3 == 2 and column != 8:
                line += " | "
            else:
                line += " "
        print(line)
        if row % 3 == 2 and row != 8:
            print("-" * 21)


def grille_vide():
    return [[0 for _ in range(9)] for _ in range(9)]

def find_empty_cell(grille):
    for row in range(9):
        for col in range(9):
            if grille[row][col] == 0:
                return row, col
    return None

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
        

if __name__ == "__main__":
    grille = grille_vide()
    print_grille(grille)

    stats = {'appelsRecursifs': 0, 'testsEffectues': 0, 'nbBacktracks': 0}

    if solve(grille):
        print("\nGrille résolue:")
        print_grille(grille)

        print("\n--- Statistiques ---")
        print("Une solution trouvée")
        print(f"Difficulté de la grille : {categorie_dificulte(stats['nbBacktracks'])}")
        print(f"Nombre d'appels récursifs : {stats['appelsRecursifs']}")
        print(f"Nombre de tests effectués : {stats['testsEffectues']}")
        print(f"Nombre de backtracks : {stats['nbBacktracks']}")
        print("\n---- Complexité ----")
        print("- k est le nombre des cases vides")
        print("- chaque case aurait jusqu’à 9 possibilités")
        print("Alors la complexité est O(9^k) dans le pire des cas.")
    else:
        print("Aucune solution trouvée.")

    print("\nGrille avec des valeurs retirées:")
    nb_retraites = 40  # Par exemple: retirer 40 valeurs
    grille_pour_resoudre = retirer_valeurs(grille, nb_retraites)
    print_grille(grille_pour_resoudre)

    