# Ce fichier doit contenir des test !
# Il est en work in progress pour le module parser.py
# Veuillez mettre seulement des fonction test à l'intérieur !

<<<<<<< HEAD
from genererGrille import GrilleGen,GrilleGenCompleted,solver
=======
from genererGrille import GrilleGen,GrilleGenCompleted,solver,comptePoss
>>>>>>> 04f7e796eeee121e5639e08b0e8419542a447d58
from grilleUtils import *
from parser import *
from interfaceConsole import main


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
 
def testFileToGrilleValid():
    clean()
    print("Generation d'une grille complète :")
    G = GrilleGenCompleted()
    print_grille(G)
    print("Grille générer dans :")
    print(grille_to_file(G,"test_Grille"))
    G1=[]
    print(G1)
    G1=file_to_grille("test_Grille")
    print_grille(G1)


# Erreur gérer mais arrêt du programme de toute manière !
def testFileToFrilleIncorrectData():
    # Intervention manuelle nécessaire !!!
    clean()
    print("Generation d'une grille complète :")
    G = GrilleGenCompleted()
    print_grille(G)
    print("Grille générer dans :")
    print(grille_to_file(G,"test_Grille"))
    print("<!>========================<!>")
    print("Veuillez modifier le fichier : ./sudoku_parser_out/test_Grille.txt")
    v=input("Avez-vous modifier le fichier afin de le rendre incorrect ?(Y/N)")
    print("<!>========================<!>")
    if v=='Y':
        G1=[]
        print(G1)
        try:
            G1=file_to_grille("test_Grille")
        except ParserError as err:
            print("Une erreur est survene, arrêt du programme !")
            print("Error :",err)
            exit()
        print(G1)
        print_grille(G1)
    else:
        print("Test annulé !")
        clean()

# Test de la fonction clone (parser)
def testCopy():
    # Ligne qui permet de générer la grille avec des trous
    G = GrilleGen(71)
    print("Grille générer")
    print_grille(G)
    print('\n')
    G1 = clone(G)
    print("Grille copié")
    print_grille(G1)
    print('\n')
    tmp=1
    while(not(solver(G1))):
        tmp+=1
    print("<!> ===",tmp,"essaies avant de faire la résolution === <!>")
    print("Grille Résolu !")
    print_grille(G1)
    print('\n')
    print("Grille de base")
    print_grille(G)

# Fonction de test du compteur de possiblité
def testcpt():
    # Nombre de trous dans la grille
    G=GrilleGen(40)
    print_grille(G)
    tmp=comptePoss(G)
    print("====================")
    print("On a",tmp,"solution existante !!")
    print("====================")
    print("\nPas de changement")
    print_grille(G)
    print("\nUne résolution")
    tmp=1
    while(not(solver(G))):
        tmp+=1
    print("<!> ===",tmp,"essaies avant de faire la résolution === <!>")
    print_grille(G)
