import os
def clear_console():
   os.system('cls' if os.name == 'nt' else 'clear')

#idée: transformer les Historiques en fichiers contenant les grilles??
global Historique
global Historique_Connu
Historique = [] #pile historique des étape de la grille
Historique_Connu = [] # pile historique avec en dernier historique la grille affichée

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

def ajoutHistorique(grille):
    Historique.append(grille)
    if len(Historique_Connu) == 0:
        Historique_Connu.append(grille)

def showGrilleInterface():
    clear_console()
    print_grille(Historique_Connu[len(Historique_Connu)-1])
    print("     grille n°", len(Historique_Connu)-1)

def navigationHistorique(startingPos = "actual"): #startingPos = first pour commencer à la première grille et startingPos = last pour commencer à la dernière grille
    if startingPos == "first":
        Historique_Connu.clear()
        Historique_Connu.append(Historique[0])
    elif startingPos == "last":
        for i in range(len(Historique_Connu), len(Historique)):
            Historique_Connu.append(Historique[i])
    showGrilleInterface()
    exit = False
    if len(Historique_Connu)>len(Historique): #cas d'erreur (une grille a été ajouté à l'historique connu sans être ajouté à l'historique)
        print("Erreur: L'historique connu est plus grand que l'historique!!!")
        exit = True
    while not(exit):
        command = input("navigation([p/precedent] or [s/suivant]): ")
        if command == "p" or command == "precedent" or command == "previous": #on va à la grille précédente
            if len(Historique_Connu)==1: #cas où on est déjà à la première grille de l'historique
                print("Pas de grille précedente!")
            else: #navigation vers la grille précédente
                Historique_Connu.pop()
                showGrilleInterface()
        elif command == "s" or command == "n" or command == "suivant" or command == "next": #on va à la grille suivante
            if len(Historique_Connu)==len(Historique): # cas où on est déjà à la dernière grille de l'historique
                print("Pas de grille suivante!")
            else: #navigation vers la grille suivante
                Historique_Connu.append(Historique[len(Historique_Connu)])
                showGrilleInterface()
        elif command == "e" or command == "exit": # sortie de navigation
            print("Sortie de navigation.")
            exit = True
        else: #manuel
            print("Usage:")
            print(" Grille précedente: [p/precedent/previous]")
            print(" Grille suivante: [s/suivant/n/next]")
            print(" Sortie de navigation: [e/exit]")


def grille_vide():
    return [[0 for _ in range(9)] for _ in range(9)]

def find_empty_cell(grille):
    for row in range(9):
        for col in range(9):
            if grille[row][col] == 0:
                return row, col
    return None


#Tests print_grille

"""ajoutHistorique([[1, 4, 3, 2, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9]])
ajoutHistorique([[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9]])
navigationHistorique()"""