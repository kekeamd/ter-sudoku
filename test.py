from genererGrille import GrilleGen,GrilleGenCompleted
from grilleUtils import *
from parser import *

# Fonction de vérification de validité de grille
# grille : la grille de jeu
# t : la taille de la grille (default : 9)
def is_valid_debug(grille,t):
    tab_output=[] # Tableau des cases problématiques
    for r in range (t):
        for c in range (t):
            # e : la valeur de l'élément courant
            e = grille[r][c]
            # Verification de la ligne
            if e in grille[r]:
                tab_output.append((r,c,e,'row'))
            # Verification de la colonne
            for z in range(9):
                if z!=r and grille[z][c] == e:
                    tab_output.append(r,c,e,'col')
            # Verification Carré 3x3
            start_row = (e // 3) * 3 # premier indice du carré (row)
            start_col = (c // 3) * 3 # premier indice du carré (column)
            for i in range(start_row, start_row + 3):
                for j in range(start_col, start_col + 3):
                    if grille[i][j] == e:
                        tab_output.append(r,c,e,"sqr")
    return tab_output


def testValidParseToFile():
    clean()
    print("Generation d'une grille complète :")
    G = GrilleGenCompleted()
    print_grille(G)
    print("Grille générer dans :")
    print(grille_to_file(G,"test_Grille"))

def testErrorParseToFile():
    clean()
    print("Generation d'une grille complète :")
    G = GrilleGenCompleted()
    try:
        G[2].append(5)
    except ParserError as err:
        print (err)
    print_grille(G)
    print("Grille générer dans :")
    print(grille_to_file(G,"test_Grille"))

