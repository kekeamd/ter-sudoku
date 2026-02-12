# self = this in java
# __init__ = constructeur

from random import randint
from Interface import Interface  # import le classe parent (Interface)
from Difficulte import Difficulte # askDifficulte()
from Parser import Parser # playSudoku()
from Solver import Solver # playMove()
from GrilleBacktrack import GrilleBacktrack # playSudoku()


class InterfaceConsole(Interface): # extends Interface

    def __init__(self): # constructeur InterfaceConsole()
        super().__init__()

    def startPlaying(self): # demande le choix: si 1:  playSudoku; si 2: quitter
        while True:
            choix = self.askChoice()
            if choix == '1':
                self.playSudoku()
            elif choix == '2':
                print("\nAu revoir!")
                return
            else:
                print("\nChoix invalide, veuillez réessayer.")

    def askChoice(self) -> str: # soit generer une grille et jouer, soit quitter
        print("1. Génerer une grille et joeur")
        print("2. Quitter")

        choix = input("Votre choix: ")
        return choix


    def askDifficulty(self) -> Difficulte: # demande la difficulté à propos de nbr de retraites
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
        return difficulte_map.get(choix, "Facile")
    
    def nbretraites(self, difficulte : str) -> int:
        nb_retraites = 0
        if difficulte == "Facile":
            nb_retraites = 40
        elif difficulte == "Moyen":
            nb_retraites = 50
        elif difficulte == "Difficile":
            nb_retraites = 55
        elif difficulte == "Extrême":
            nb_retraites = 60
        elif difficulte == "God Mode":
            nb_retraites = 67
        return nb_retraites

    def playSudoku(self): # prends la difficulté, la grille complete, fait la grille prete à resoudre et appele gameLoop
        difficulty = self.askDifficulty()

        completedGrille = GrilleBacktrack.generateEntireGrille()
        if completedGrille is None:
            print("Erreur lors de la génération de la grille complète.")
            return
        print("\nGrille prête à résoudre:")
        
        # Retirer des valeurs selon la difficulte
        nb_retraites = self.nbRetraits(difficulty)
        
        grille_copie = [row[:] for row in completedGrille] # copie pour ne pas modifier la grille complète
        grille_pour_resoudre = self.retirer_valeurs(grille_copie, nb_retraites)

        print("\nGrille prête à résoudre:")
        self.print_grille(grille_pour_resoudre)

        Parser.grilleToFile(grille_pour_resoudre, "Directory", "Generated_grille_uncompleted")

        self.gameLoop(grille_pour_resoudre, completedGrille)

    def print_grille(self, grille):
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

    
    #reset character NOW!!!!!
    def retirer_valeurs(self, grille, nb_retraites : int):
        count = 0
        while count < nb_retraites:
            row = randint(0, 8)
            col = randint(0, 8)
            if grille[row][col] != 0:
                grille[row][col] = 0
                count += 1
        return grille

    def gameLoop(self, grille, solution): # soit entrer une valeur(appelle playMove()), soit donner la grille complete, soit quitter
        finish=False
        while True:
            if finish:
                print("\nVeuillez appuyer sur une touche pour quitter.")
            else:
                print("\nActions disponibles: ")
                print("1. Entrer un valeur")
                print("2. Résoudre automatiquement la grille")
                print("3. Quitter")

            choix = input("Votre choix: ")
            if finish:
                choix='3'

            if choix == '1':
                self.playMove(grille, solution)
            elif choix == '2':
                print("\nLa grille résolue automatiquement:")
                self.print_grille(solution)
                print("\nLE JEU EST TERMINÉ!")
                finish=True
            elif choix == '3':
                return
            else:
                print("\nChoix invalide, veuillez réessayer.")

    def playMove(self, grille, solution): # entrer une certain valeur sur un certian ligne et colenne, verifie si cest bon en comparaison avec la grille complete
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
        if Solver.isValid(grille, row, col, val):
            grille[row][col] = val              #??????????????? tu fait le job de la grille maintenant???????????
            if grille[row][col] == solution[row][col]: # je compares avec la grille complète
                print("\nValeur insérée avec succès.")
                self.print_grille(grille)
            else:
                print("\nValeur invalide pour cette position.")
                grille[row][col] = 0
        else:
            print("\nValeur invalide pour cette position.")


    def quit(self): # ou tout simplement break
        pass