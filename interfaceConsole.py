from random import randint
import parser as p
from grilleUtils import *
from genererGrille import *

def demander_choix():
    print("\n=== SUDOKU CONSOLE ===")
    print("1. Générer une grille et jouer")
    #print("2. Résoudre une grille existante")
    print("2. Quitter")

    choix = input("Votre choix: ")
    return choix

def main():
    while True:
        choix = demander_choix()
        if choix == '1':
            jouer_sudoku()
        elif choix == '2':
            print("\nAu revoir!")
            break
        else:
            print("\nChoix invalide, veuillez réessayer.")

def demander_difficulte():
    print("\nChoisissez une difficulté:")
    print("1. Facile")
    print("2. Moyen")
    print("3. Difficile")
    print("4. Extrême")
    print("5. God Mode")
    choix = input("Votre choix: ")
    difficulte_map = {
        '1': "Facile",
        '2': "Moyen",
        '3': "Difficile",
        '4': "Extrême",
        '5': "God Mode"
        }
    return difficulte_map.get(choix, "Facile") # par défaut Facile

def grille_resolue():
    grille = grille_vide()
    p.grille_to_file(grille,"Generated_grille_empty")
    if solver(grille):
        p.grille_to_file(grille, "Generated_grille_completed")
        return grille

#completedGrille = grille_resolue()

def jouer_sudoku():
    difficulte = demander_difficulte()

    completedGrille = grille_resolue()
    if completedGrille is None:
        print("Erreur lors de la génération de la grille complète.")
        return
    
    print("\nGrille prête à résoudre:")
    # Retirer des valeurs selon la difficulte
    if difficulte == "Facile":
        nb_retraites = 40
    elif difficulte == "Moyen":
        nb_retraites = 50
    elif difficulte == "Difficile":
        nb_retraites = 60
    elif difficulte == "Extrême":
        nb_retraites = 65
    elif difficulte == "God Mode":
        nb_retraites = 70
    
    grille_copie = [row[:] for row in completedGrille] # copie pour ne pas modifier la grille complète
    grille_pour_resoudre = retirer_valeurs(grille_copie, nb_retraites)
    print_grille(grille_pour_resoudre)
    p.grille_to_file(grille_pour_resoudre,"Generated_grille_uncompleted")

    boucle_de_jeu(grille_pour_resoudre, completedGrille)


def boucle_de_jeu(grille, solution):
    while True:
        print("\nActions disponibles: ")
        print("1. Entrer un valeur")
        print("2. Résoudre automatiquement la grille")
        print("3. Quitter")

        choix = input("Votre choix: ")
        
        if choix == '1':
            joeur_coup(grille, solution)
        elif choix == '2':
            print("\nLa grille résolue automatiquement:")
            print_grille(solution)
            break
        elif choix == '3':
            break
        else:
            print("Choix invalide, veuillez réessayer.")


def joeur_coup(grille, solution):
    try:
        row = int(input("Ligne (1-9): ")) -1
        col = int(input("Colonne (1-9): ")) -1
        val = int(input("Valeur (1-9): "))
    except ValueError:
        print("\nEntrée invalide. Veuillez entrer des nombres entre 1 et 9.")
        return
    
    if not (0 <= row < 9 and 0 <= col < 9):
        print("\nLigne/colonne hors limites (1-9).")
        return
    
    if grille[row][col] != 0:
        print("\nCette case est déjà remplie.")
        return
    if is_valid(grille, row, col, val):
        grille[row][col] = val
        if grille[row][col] == solution[row][col]: # je compares avec la grille complète
            print("\nValeur insérée avec succès.")
            print_grille(grille)
        else:
            print("\nValeur invalide pour cette position.")
            grille[row][col] = 0
    else:
        print("\nValeur invalide pour cette position.")

if __name__ == "__main__":
    main()