# self = this in java
# __init__ = constructeur

from random import randint
from Except.SolverError import SolverError
from Grille import Grille
from Interface import Interface  # import le classe parent (Interface)
from Difficulte import Difficulte # askDifficulte()
from Parser import Parser # playSudoku()
from SolverBacktrack import SolverBacktrack # playMove()
from GrilleBacktrack import GrilleBacktrack
from SolverHuman import SolverHuman # gameLoop()
from SolverHumanStats import SolverHumanStats # gameLoop()


class InterfaceConsole(Interface): # extends Interface

    def __init__(self): # constructeur InterfaceConsole()
        super().__init__()
        self.errorCount = 0  # compteur d'erreurs pour la partie en cours

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


    def askDifficulty(self) -> str: # demande la difficulté à propos de nbr de retraites
        print("\nChoisissez une difficulté:")
        print("1. Facile")
        print("2. Moyen")
        print("3. Difficile")
        print("4. Extrême")
        print("5. God Mode")
        choix = input("Votre choix: ")

        difficulte_map = {
            '1': Difficulte.FACILE,
            '2': Difficulte.MOYEN,
            '3': Difficulte.DIFFICILE,
            '4': Difficulte.EXTREME,
            '5': Difficulte.GODMODE
        }

        if choix in difficulte_map:
            return difficulte_map[choix]

        print("Choix invalide. Réessayez.")

    def playSudoku(self): # prends la difficulté, la grille complete, fait la grille prete à resoudre et appele gameLoop
        self.errorCount = 0  # Réinitialiser le compteur d'erreurs
        difficulty = self.askDifficulty()

        grilleVide = GrilleBacktrack()
        self.grilleComplete = grilleVide.generateEntireGrille()

        self.grilleDeJeu = GrilleBacktrack()
        stats = self.grilleDeJeu.generateValuesHumanRated(difficulty, self.grilleComplete.clone())
        self.grilleDeJeu.adjustCandidates()  # Initialiser les candidats après génération

        rated = SolverHuman.rateFromStats(stats)
        print("\nDifficulté estimée (méthodes humaines):", rated)
        print("Steps:", stats["steps"])
        print("Max technique:", stats["maxTechnique"].name if stats["maxTechnique"] else None)

        #self.grilleDeJeu.generateValues(difficulty, self.grilleComplete.clone())

        if self.grilleComplete is None:
            print("Erreur lors de la génération de la grille complète.")
            return
        
        self.grilleDeJeu.printGrille()
    
        self.gameLoop()

    def gameLoop(self): # soit entrer une valeur(appelle playMove()), soit donner la grille complete, soit quitter
        finish = False
        while True:
            if finish or self.errorCount >= 3:
                if self.errorCount >= 3:
                    print("\nGAME OVER - 3 erreurs atteintes!")
                print("\nVeuillez appuyer sur une touche pour quitter.")
                print("2. Résoudre automatiquement la grille (backtrack)")
                print("3. Résoudre automatiquement la grille (méthode humaine)")
                print("4. Quitter")
            else:
                print(f"Erreurs: {self.errorCount}/3")
                print("\nActions disponibles: ")
                print("1. Entrer une valeur")
                print("2. Résoudre automatiquement la grille (backtrack)")
                print("3. Résoudre automatiquement la grille (méthode humaine)")
                print("4. Quitter")

            choix = input("Votre choix: ")

            if choix == '1':
                if self.errorCount >= 3:
                    print("\nGame Over! Vous ne pouvez plus jouer.")
                else:
                    self.playMove()
            elif choix == '2':
                print("\nLa grille résolue automatiquement (backtrack):")
                self.grilleComplete.printGrille()
                print("\nLE JEU EST TERMINÉ !\n")
                return  # sortir après résolution
            elif choix == '3':
                print("\nRésolution avec méthode humaine...")
                
                try:
                    #SolverHuman.solveGrille(self.grilleDeJeu)
                    res = SolverHumanStats.solveWithStats(self.grilleDeJeu)
                    print("\nRésolution humaine terminée.")
                    print("Solved:", res["solved"], "| Steps:", res["steps"], "| MaxTech:", res["maxTechnique"])
                    print("Counts:", {k.name: v for k, v in res["counts"].items()})
                    self.grilleDeJeu.printGrille()

                except SolverError as e:
                    print("\n", e)
                    print("\nGrille partiellement résolue :")
                    self.grilleDeJeu.printGrille()
                print("\nLE JEU EST TERMINÉ !\n")
                return  # terminer la boucle après affichage
            elif choix == '4':
                return
            else:
                print("\nChoix invalide, veuillez réessayer.")

    def playMove(self): # entrer une certain valeur sur un certian ligne et colenne, verifie si cest bon en comparaison avec la grille complete
        try:
            row = int(input("Ligne (1-9): ")) -1
            col = int(input("Colonne (1-9): ")) -1
        except ValueError:
            print("\nEntrée invalide. Veuillez entrer des nombres entre 1 et 9.")
            return
        
        if not (0 <= row < 9 and 0 <= col < 9):
            print("\nLigne/colonne hors limites (1-9).")
            return
        
        if self.grilleDeJeu.getCelluleValueCoord(row, col) != 0:
            print("\nCette case est déjà remplie.")
            return
        
        candidats = Grille.getCelluleCandidatesCoord(self.grilleDeJeu, row, col)
        print("Candidats possibles pour la case avec row:", row+1, "col:", col+1, ":", candidats)
        
        try:
            val = int(input("Valeur (1-9): "))
        except ValueError:
            print("\nEntrée invalide. Veuillez entrer un nombre entre 1 et 9.")
            return
        
        if SolverBacktrack.isValid(self.grilleDeJeu, row, col, val):
            self.grilleDeJeu.setCelluleValueCoord(row, col, val)
            self.grilleDeJeu.adjustCandidatesAfterAddingValueCoord(row, col)  # Mettre à jour les candidats
            if self.grilleDeJeu.getCelluleValueCoord(row, col) == self.grilleComplete.getCelluleValueCoord(row, col): # je compares avec la grille complète
                print("\nValeur insérée avec succès.")
                self.grilleDeJeu.printGrille()

                # CHECK FIN DE JEU
                size = self.grilleDeJeu.getSize() ** 2
                hasZero = False
                for row in range(size):
                    for cell in self.grilleDeJeu.getRow(row):
                        if cell == 0:
                            hasZero = True
                            break
                    if hasZero:
                        break
                if not hasZero:
                    print("\nBravo ! Grille complétée !")
            else:
                print("\nValeur invalide pour cette position.")
                self.errorCount += 1
                print(f"Erreur ! \n")
                self.grilleDeJeu.setCelluleValueCoord(row, col, 0)
        else:
            print("\nValeur invalide pour cette position.")
            self.errorCount += 1
            print(f"Erreur ! \n")