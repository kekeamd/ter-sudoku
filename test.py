# Ce fichier doit contenir des test !
# Il est en work in progress pour le module parser.py
# Veuillez mettre seulement des fonction test à l'intérieur !

from genererGrille import GrilleGen,GrilleGenCompleted,solver
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

G = grille_vide()
for i in range (9):
    G[0][i]=i+1

print_grille(G)

grille_to_file(G,"test_Grille")

G1 = file_to_grille("test_Grille")
G2 = file_to_grille("test_Grille")
print("====================")
solver(G1)
solver(G2)
print_grille(G1)
print("====================")
print_grille(G2)
print("====================")
print_grille(G)