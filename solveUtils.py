from grilleUtils import *


# Fonction qui vérifie si la grille est valide
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

# Fonction solve avec stats :
# info : [bool,stats]
# stats = {'appelsRecursifs': 0, 'testsEffectues': 0, 'nbBacktracks': 0}
def solveStats(grille):
    s = {'appelsRecursifs': 0, 'testsEffectues': 0, 'nbBacktracks': 0,'valid': False}
    return solveStatsUtils(grille,s)


def solveStatsUtils(g,stats):
    stats['appelsRecursifs'] += 1 # j'utilise un dictionnaire pour stocker les statistiques
    vide = find_empty_cell(g)
    if not vide:
        stats['valid']=True
        return stats # Résolu
    row, column = vide
    nums = [i for i in range(1, 10)]
    shuffle(nums)
    for val in nums:
        stats['testsEffectues'] += 1
        if is_valid(g, row, column, val):
            g[row][column] = val
            if solveStatsUtils(g,stats)['valid']:
                stats['valid']=True
                return stats
            g[row][column] = 0 # backtrack
            stats['nbBacktracks'] += 1
    stats['valid']=False
    return stats

# Fonction qui compte le nombre de possibilité de résolution pour grille
def comptePoss(grille):
    vide=find_empty_cell(grille)
    if not vide:
        return 1
    r,c=vide
    sum=0
    for i in range (1,10):
        if is_valid(grille, r, c, i):
            G=clone(grille)
            G[r][c] = i
            tmp=comptePoss(G)
            if tmp>0:
                sum=sum+tmp
    return sum