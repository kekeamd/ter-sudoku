# self = this in java
# __init__ = constructeur

from random import randint
from BanqueGrilles import BanqueGrilles
from Except.SolverError import SolverError
from Grille import Grille
from GrilleHuman import GrilleHuman
from Interface import Interface  # import le classe parent (Interface)
from Difficulte import Difficulte # askDifficulte()
from Parser import Parser # playSudoku()
from SolverBacktrack import SolverBacktrack # playMove()
from GrilleBacktrack import GrilleBacktrack
from SolverHuman import SolverHuman # gameLoop()
from SolverHumanStats import SolverHumanStats # gameLoop()
from SudokuScraping import getDifficultyFromGrille # playSudoku() pour afficher la difficulté estimée de la grille générée


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


    def askDifficulty(self) -> Difficulte:  # demande la difficulté
        difficulte_map = {
            '1': Difficulte.FACILE,
            '2': Difficulte.MOYEN,
            '3': Difficulte.DIFFICILE,
            '4': Difficulte.EXTREME,
            '5': Difficulte.GODMODE
        }

        while True:
            print("\nChoisissez une difficulté:")
            print("1. Facile")
            print("2. Moyen")
            print("3. Difficile")
            print("4. Extrême")
            print("5. God Mode")

            choix = input("Votre choix: ")

            if choix in difficulte_map:
                return difficulte_map[choix]

            print("\nChoix invalide. Réessayez.")

    def playSudoku(self): # prends la difficulté, la grille complete, fait la grille prete à resoudre et appele gameLoop
        self.errorCount = 0  # Réinitialiser le compteur d'erreurs
        difficulty = self.askDifficulty()

        #grilleVide = GrilleBacktrack()
        #self.grilleComplete = grilleVide.generateEntireGrille()

        #if self.grilleComplete is None:
         #   print("Erreur lors de la génération de la grille complète.")
         #   return

        #self.grilleDeJeu = GrilleHuman()
        #stats = self.grilleDeJeu.generateValuesHumanRated(difficulty, self.grilleComplete.clone())

        entree = BanqueGrilles.charger_grille_aleatoire(difficulty)

        self.grilleDeJeu = entree["grille"]
        self.grilleComplete = entree["solution"]
        self.stats = entree["stats"]

        if self.stats is None:
            print("Erreur: la génération n'a retourné aucune statistique.")
            return

        self.grilleDeJeu.adjustCandidates()  # Initialiser les candidats après génération

        rated = SolverHuman.rateFromStats(self.stats)

        print("\nGrille chargée depuis la banque :")
        print("Difficulté demandée :", difficulty.name)
        print("Difficulté estimée (méthodes humaines) :", rated.name)
        print("Steps :", self.stats["steps"])
        
        max_tech = self.stats["maxTechnique"]
        print("Max technique :", max_tech.name if max_tech else None)

       
        sudokuCoachRated = getDifficultyFromGrille(self.grilleDeJeu, headless=True)
        print(f"Difficulté estimée (sudoku.coach): {sudokuCoachRated  ['label']} (score: {sudokuCoachRated['score']})")

        #self.grilleDeJeu.generateValues(difficulty, self.grilleComplete.clone())

        self.grilleDeJeu.printGrille()
        
        # Message pour GODMODE
        if rated == Difficulte.GODMODE:
            print(
                "\nCette grille ne peut pas être résolue uniquement avec les techniques humaines "
                "actuellement implémentées dans ce projet "
                "(dernier nombre, singleton nu, singleton caché, paire nue, paire cachée, "
                "candidat enfermé, gratte-ciel).\n"
            )
    
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
                print("2. Afficher la grille des candidats")
                print("3. Résoudre automatiquement la grille (backtrack)")
                print("4. Résoudre automatiquement la grille (méthode humaine)")
                print("5. Quitter")

            choix = input("Votre choix: ")

            if choix == '1':
                if self.errorCount >= 3:
                    print("\nGame Over! Vous ne pouvez plus jouer.")
                else:
                    self.playMove()
            elif choix == '2':
                if self.errorCount >= 3:
                    print("\nGame Over! Vous ne pouvez plus jouer.")
                else:
                    self._printCandidatesGrid()

            elif choix == '3':
                print("\nLa grille résolue automatiquement (backtrack):\n")
                self.grilleComplete.printGrille()
                print("LE JEU EST TERMINÉ !\n")
                return  # sortir après résolution
            elif choix == '4':
                print("\nRésolution avec méthode humaine...")
                
                try:
                    #SolverHuman.solveGrille(self.grilleDeJeu)
                    res = SolverHumanStats.solveWithStats(self.grilleDeJeu)
                    print("\nRésolution humaine terminée.")
                    print("Solved:", res["solved"], "| Steps:", res["steps"], "| MaxTech:", res["maxTechnique"])
                    print("Counts:", {k.name: v for k, v in res["counts"].items()})
                    self.grilleDeJeu.printGrille()
                    # Afficher tous les étapes de résolution
                    print("\nVoulez-vous voir les étapes ?")
                    print("1. Oui")
                    print("2. Non")
                    choix_etapes = input("Votre choix: ")
                    if choix_etapes == '1':
                        for h in res["history"]:
                            tech = h["technique"].name
                            move = h["move"]
                            if move is not None:
                                print(f"Etape {h['step']} - {tech} : valeur {move['value']} en ligne {move['row']+1}, colonne {move['col']+1}")
                            else:
                                print(f"Etape {h['step']} - {tech} : aucun chiffre posé directement")

                except SolverError as e:
                    print("\n", e)
                    print("\nGrille partiellement résolue :")
                    self.grilleDeJeu.printGrille()
                    for h in res["history"]:
                        tech = h["technique"].name
                        move = h["move"]
                        if move is not None:
                            print(f"Etape {h['step']} - {tech} : valeur {move['value']} en ligne {move['row']+1}, colonne {move['col']+1}")
                        else:
                            print(f"Etape {h['step']} - {tech} : aucun chiffre posé directement")
                print("\nLE JEU EST TERMINÉ !\n")
                return  # terminer la boucle après affichage
            elif choix == '5':
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
        
        try:
            val = int(input("Valeur (1-9): "))
        except ValueError:
            print("\nEntrée invalide. Veuillez entrer un nombre entre 1 et 9.")
            return
        
        if SolverBacktrack.isValid(self.grilleDeJeu, row, col, val):
            self.grilleDeJeu.setCelluleValueCoord(row, col, val)
            self.grilleDeJeu.adjustCandidatesAfterAddingValueCoord(row, col)  # Mettre à jour les candidats
            if self.grilleDeJeu.getCelluleValueCoord(row, col) == self.grilleComplete.getCelluleValueCoord(row, col): # je compares avec la grille complète
                print("\nValeur insérée avec succès.\n")
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

    # affiche la grille avec tous le candidats
    def _printCandidatesGrid(self):
        print("\n=== Grille des candidats ===\n")
        for row in range(9):
            for col in range(9):
                val = self.grilleDeJeu.getCelluleValueCoord(row,col)
                
                if val != 0:
                    cell = f"{val}"
                else:
                    candidats = Grille.getCelluleCandidatesCoord(self.grilleDeJeu, row, col)
                    cell = "{" + ",".join(map(str, candidats)) + "}"
                print(f"{cell:12}", end="") # :12 cest le formatage de largeur car on peut avoir bcp de candidats, end="" pour ne pas passer à la ligne

                if (col + 1)  % 3 == 0 and col < 8:
                    print(" | ", end="")
            print()

            if (row + 1) % 3 == 0 and row < 8:
                print("-" * 120) # 120 au cas où on a bcp de candidats
        print("\n")