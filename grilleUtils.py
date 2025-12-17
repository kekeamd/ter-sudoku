#idée: transformer les Historiques en fichiers contenant les grilles??
global Historique
global Historique_Connu
Historique = [] #pile historique des étape de la grille
Historique_Connu = [] # pile historique avec en dernier historique la grille affichée

def ajoutHistorique(grille): #fonction d'ajout de grille dans l'historique afin d'aussi l'ajouter dans l'histo connu lors de l'initialisation, à modifier par la suite??
    if Historique_Connu == Historique:
        Historique.append(grille)
        Historique_Connu.append(grille)
    else:
        Historique.append(grille)
        Historique_Connu.clear()
        for g in Historique:
            Historique_Connu.append(g)

def print_grille(grille, AddToHist = False, JustToShow = False): #AddToHist = True si vous voulez rajouter la grille à l'historique avant de l'affichée, JustToShow = True si vous ne voulez pas d'histoire d'historique
    if AddToHist == False and not(grille in Historique) and JustToShow == False: #check pour verifier que la grille est bien dans l'historique
        print("Grille non historicisé, avez-vous pensez à rajouter la grille dans l'historique?(voir les arguments AddToHist et JustToShow)")
    else:
        if AddToHist == True and not(len(Historique)==0) and grille == Historique[len(Historique)-1]:
            print("Deux grilles identiques se suivent!!")
        else:
            if AddToHist == True: #ajout de la grille à l'historique et actualisation de l'historique connu
                ajoutHistorique(grille)
            else:
                for posG in range(len(Historique)-1, -1, -1): #on repositionne l'historique connu sur la dernière occurence de la grille si jamais on se trouve après celle-ci
                    if Historique[posG] == grille:
                        while posG < len(Historique_Connu)-1:
                            Historique_Connu.pop()
                        if posG == len(Historique_Connu)-1 and Historique_Connu[len(Historique_Connu)-1]!= grille:
                            print("Erreur: L'historique connu est à la position de la grille mais la grille ne s'y trouve pas(historique connu n'est pas inclu dans Historique)")

                        break
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
            #--------navigation----------
            if JustToShow == False:
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
                            exit = True
                            print_grille(Historique_Connu[len(Historique_Connu)-1])
                    elif command == "s" or command == "n" or command == "suivant" or command == "next": #on va à la grille suivante
                        if len(Historique_Connu)==len(Historique): # cas où on est déjà à la dernière grille de l'historique
                            print("Pas de grille suivante!")
                        else: #navigation vers la grille suivante
                            Historique_Connu.append(Historique[len(Historique_Connu)])
                            exit = True
                            print_grille(Historique_Connu[len(Historique_Connu)-1])
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
""""
ajoutHistorique([[1, 4, 3, 2, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9]])
ajoutHistorique([[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9]])
print_grille([[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9]])
"""