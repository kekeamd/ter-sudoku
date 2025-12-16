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


def find_empty(grille):
    for row in range(9):
        for column in range(9):
            if grille[row][column] == 0:
                return row, column
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
    vide = find_empty(grille)
    if not vide:
        return True # Résolu
    row, column = vide
    for val in range(1, 10):
        stats['testsEffectues'] += 1
        if is_valid(grille, row, column, val):
            grille[row][column] = val
            if solve(grille):
                return True
            grille[row][column] = 0 # backtrack
            stats['nbBacktracks'] += 1
    return False

if __name__ == "__main__":
    # Exemple simple (0 = vide)
    # Exemple vu en cours d'Algo 4
    grille = [
        [5,3,0, 0,7,0, 0,0,0],
        [6,0,0, 1,9,5, 0,0,0],
        [0,9,8, 0,0,0, 0,6,0],
        [8,0,0, 0,6,0, 0,0,3],
        [4,0,0, 8,0,3, 0,0,1],
        [7,0,0, 0,2,0, 0,0,6],
        [0,6,0, 0,0,0, 2,8,0],
        [0,0,0, 4,1,9, 0,0,5],
        [0,0,0, 0,8,0, 0,7,9]
    ]
    print("Grille initiale:")
    print_grille(grille)

    stats = {'appelsRecursifs': 0, 'testsEffectues': 0, 'nbBacktracks': 0}

    if solve(grille):
        print("\nGrille résolue:")
        print_grille(grille)
        print("\n--- Statistiques ---")
        print("Une solution trouvée")
        print(f"Nombre d'appels récursifs : {stats['appelsRecursifs']}")
        print(f"Nombre de tests effectués : {stats['testsEffectues']}")
        print(f"Nombre de backtracks : {stats['nbBacktracks']}")
        print("\n---- Complexité ----")
        print("- k est le nombre des cases vides")
        print("- chaque case aurait jusqu’à 9 possibilités")
        print("Alors la complexité est O(9^k) dans le pire des cas.")
    else:
        print("Aucune solution trouvée.")