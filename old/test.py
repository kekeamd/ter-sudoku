# Ce fichier doit contenir des test !
# Il est en work in progress pour le module parser.py
# Veuillez mettre seulement des fonction test à l'intérieur !

from genererGrille import *
from grilleUtils import *
from parser import *
from interfaceConsole import main
from solveUtils import *

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
    G = GrilleGenBase(71)
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
    G=GrilleGenBase(40)
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


def testHisto2Grille():
    ajoutHistorique([[1, 4, 3, 2, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9]])
    ajoutHistorique([[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9]])
    navigationHistorique()

def testStatsGrilleGenere():
    G=GrilleGenBase(50)
    print_grille(G)
    stats=solveStats(G)
    print("\n--- Statistiques ---")
    print(f"Nombre de solutions trouvées : {comptePoss(G)}")
    print(f"Nombre d'appels récursifs : {stats['appelsRecursifs']}")
    print(f"Nombre de tests effectués : {stats['testsEffectues']}")
    print(f"Nombre de backtracks : {stats['nbBacktracks']}")
    print("\n---- Complexité ----")
    print("- k est le nombre des cases vides")
    print("- chaque case aurait jusqu’à 9 possibilités")
    print("Alors la complexité est O(9^k) dans le pire des cas.")
    print("\n---- Résolu ----")
    print_grille(G)

def testStatsNewGrille():
    G=grille_vide()
    print_grille(G)
    stats=solveStats(G)
    print("\n--- Statistiques ---")
    print(f"Nombre de solutions trouvées : {comptePoss(G)}")
    print(f"Nombre d'appels récursifs : {stats['appelsRecursifs']}")
    print(f"Nombre de tests effectués : {stats['testsEffectues']}")
    print(f"Nombre de backtracks : {stats['nbBacktracks']}")
    print("\n---- Complexité ----")
    print("- k est le nombre des cases vides")
    print("- chaque case aurait jusqu’à 9 possibilités")
    print("Alors la complexité est O(9^k) dans le pire des cas.")
    print("\n---- Résolu ----")
    print_grille(G)

def testCompcptsol():
    limit=50
    G=GrilleGenBase(50)
    print("nbSol par Compte Sol :",comptePoss(clone(G)))
    print("nbSol par Compte Sol limited :",comptePoss_limite(clone(G),limit))

# Test l'affichage des stats
# n est le nombre de cases vide à viser
def testAffichageStats(n):
    myS=[]
    G=GrilleGenCompleted()
    for _ in range (n):
        G=retirer_valeurs(G,1)
        myS.append(solveStats(clone(G)))
    print("<!> ========== DATA BRUT ========== <!>")
    print(myS)
    print("<!> =============================== <!>")
    afficheStats(myS)

def testRetireValeur():
    G1=retirer_valeurs(GrilleGenCompleted(),10)
    G2=retirer_valeurs(GrilleGenCompleted(),50)
    nbPossG1=comptePoss(G1)
    nbPossG2=comptePoss(G2)
    print("===============")
    print("=== Grille1 ===")
    print("===============")
    print(nbPossG1,"possiblité de résolution pour G1.")
    print_grille(G1)
    print("===============")
    print("===============")
    print("=== Grille2 ===")
    print("===============")
    print(nbPossG2,"possibilité de résolution pour G2")
    print_grille(G2)
    print("===============")
    print("Résultat suppression 1 valeur supplémentaire G1")
    print(retirevaleur(G1))
    print("===============")
    print("Résultat suppression 1 valeur supplémentaire G2")
    print(retirevaleur(G2))
    print("===============")

# Test de la fonction GrilleGen
# n est le nombre d'élément à supprimer
def testGrilleGen(n):
    print("============================================================")
    print("Test de génération d'une grille Unique à",n,"trous")
    print("============================================================")
    try:
        G=GrilleGen(n)
    except GeneratorError as e:
        print(e)
        print("Erreur arrivé avec ",n,"trous")
        return None
    print("===============")
    print("== La Grille ==")
    print_grille(G)
    print("===============")
    print("Vérification des possibilités !!")
    print("Il y a",comptePoss(G),"solutions possible")
    print("===============")

G = GrilleGen(30)
Gcomp = clone(G)
solver(Gcomp)
grille_to_file(Gcomp,"Completed")
grille_to_file(G,"WithEmptyCases")