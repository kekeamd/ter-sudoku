# La difference de ce fichier avec le solveurSudoku.py est que ici on genere une grille vide et on la remplit aleatoirement
# puis on retire des valeurs pour obtenir une grille a resoudre
# Jai mis aussi la categorie de difficulte selon le nombre de backtracks observes pendant la resolution (regardez et me dite si ca vous va)
# Et aussi le nombre de valeurs quon retire peuvent dependre de la difficulte obtenue
# par exemple si la difficulte est facile on peut retirer moins de valeurs etc.


from random import randint, shuffle
import parser as p
from grilleUtils import *
from solveUtils import *

class GeneratorError(Exception):
    pass

# Fonction qui retire une seule valeur de la grille
# Renvoie un tuple :
# [0] Vrai si la valeur à été retirer, Faux sinon
# [1] Un tuple (Ligne,Colonne)
# Il est essentiel d'avoir d'une grille 9x9 en entrée, pas de gestion des exception !
def retirevaleur(G):
    rows=[i for i in range (9)]
    cols=[i for i in range (9)]
    shuffle(rows)
    shuffle(cols)
    for r in rows:
        for c in cols:
            if G[r][c]!=0: # Je teste si la case est vide
                save=G[r][c] # Je sauvegarde la valeur de la case
                G[r][c]=0 # Mise à 0 de la case
                if (comptePoss_limite(clone(G),2))<2: # Je vérifie qu'il n'y ait qu'une seule possibilité de résolution
                    return [True,(r,c)]
                else: # Case où il y a plusieurs solution
                    G[r][c]=save # Je remets l'ancienne valeur
    return [False,(-1,-1)]

# Fonction qui génère une grille complète
def GrilleGenCompleted():
    out=grille_vide()
    if solver(out):
        return out
    else:
        return [] 

# Fonction qui génère une grille avec n valeur en moins
# <!> PAS DE VERIFICATION D'UNICITE DE SOLUTION <!>
def GrilleGenBase(n):
    return retirer_valeurs(GrilleGenCompleted(),n)

# Fonction qui génère une grille avec n valeurs en moins
# Attention au delà de 50 valeurs le temps de génération peut être long
def GrilleGen(n):
    if n>64:
        raise GeneratorError("Nombre d'élément à supprimer trop grand.")
    G=GrilleGenCompleted()
    Gc=clone(G)
    Hist=[]
    i=0
    maxsuppr=n # Nombre maximal de suppression accepté
    nbsuppr=0
    while(i<n) and (maxsuppr>=nbsuppr):
        suppr=retirevaleur(G) # Je tente de supprimer une valeur
        if suppr[0]: # Si elle est supprimé j'ajoute l'index à l'historique
            Hist.append(suppr[1])
        else: # Sinon on va remettre la dernière valeur supprimé
            if len(Hist)<1:
                raise GeneratorError("Impossible de supprimer des valeurs ! (Tableau Hist Vide)") # Plus de valeurs à remettre !
            else:
                reco=Hist.pop()
                G[reco[0]][reco[1]]=Gc[reco[0]][reco[1]]
                i-=1 # On diminue i de 1 car on à fait un retour en arrière dans le process de suppression
                nbsuppr+=1 # On augmente le nombre de suppression
        i+=1
    if nbsuppr>=maxsuppr:
        raise GeneratorError("Impossible de générer la grille avec le nombre de valeur demander.(ForceStop)")
    return G

# ====================
# Fonction de stats
# ====================
def categorie_dificulte(nb_backtracks):
    if nb_backtracks < 150:
        return "Facile"
    elif nb_backtracks < 350:
        return "Moyen"
    elif nb_backtracks < 1000:
        return "Difficile"
    elif nb_backtracks < 5000:
        return "Extrême"
    else:
        return "God Mode"
# ====================

# ========================================
# Fonction A SUPPRIMER
# ========================================
# Remplacer par solveStats (fichier solveUtils)
#stats = {'appelsRecursifs': 0, 'testsEffectues': 0, 'nbBacktracks': 0}
def solve(grille):
    stats['appelsRecursifs'] += 1 # j'utilise un dictionnaire pour stocker les statistiques
    vide = find_empty_cell(grille)
    if not vide:
        return True # Résolu
    row, column = vide
    nums = [i for i in range(1, 10)]
    shuffle(nums)
    for val in nums: 
        stats['testsEffectues'] += 1
        if is_valid(grille, row, column, val):
            grille[row][column] = val
            if solve(grille):
                return True
            grille[row][column] = 0 # backtrack
            stats['nbBacktracks'] += 1
    return False
# ========================================
# ========================================

# ================================================================================
# A modifier pour supprimer la fonction solve
# Si nécessaire faire plus de modification
# A déplacer dans le fichier test.py pour plus de propreté de code
# ================================================================================
if __name__ == "__main__":
    print("Grille vide :")
    p.clean()
    grille = grille_vide()
    print_grille(grille)
    p.grille_to_file(grille,"Generated_grille_empty")
    
    solution = GrilleGenCompleted()
    print("\nGrille résolue :")
    print_grille(solution)
    p.grille_to_file(solution, "Generated_grille_completed")

    nb_retraites = 45  # Nombre de valeurs à retirer pour créer une grille à résoudre
    grille_a_resoudre = retirer_valeurs(clone(solution), nb_retraites)
    print("\nGrille à résoudre:")
    print_grille(grille_a_resoudre)
    p.grille_to_file(grille_a_resoudre,"Generated_grille_uncompleted")

    stats = {'appelsRecursifs': 0, 'testsEffectues': 0, 'nbBacktracks': 0}

    grille_a_resoudre_Copie = clone(grille_a_resoudre)

    if solve(grille_a_resoudre_Copie):
        print("\n--- Statistiques ---")
        nb_solutions = comptePoss_limite(grille_a_resoudre, 2)  # pour compter les solutions
        print(f"Nombre de solutions trouvées : {nb_solutions}")  # mieux : sur le puzzle
        if nb_solutions == 1:
            print("La grille a une solution unique.")
        else:
            print("La grille a plusieurs solutions.")
        difficulte = categorie_dificulte(stats['nbBacktracks'])
        print(f"Difficulté de la grille : {difficulte}")
        print(f"Nombre d'appels récursifs : {stats['appelsRecursifs']}")
        print(f"Nombre de tests effectués : {stats['testsEffectues']}")
        print(f"Nombre de backtracks : {stats['nbBacktracks']}")
        print("La complexité est O(9^k) dans le pire des cas.")
    else:
        print("Erreur : La grille généré n'a pas de solution !")
    # Utilisation de la solveStats au lieu de solve
    G=grille_vide()
    stats=solveStats(G)
    print("\nGrille résolue BIS :")
    print_grille(G)
    print("\n--- Statistiques BIS ---")
    print(f"Nombre de solutions trouvées : {comptePoss(G)}")
    difficulte = categorie_dificulte(stats['nbBacktracks'])
    print(f"Difficulté de la grille : {difficulte}")
    print(f"Nombre d'appels récursifs : {stats['appelsRecursifs']}")
    print(f"Nombre de tests effectués : {stats['testsEffectues']}")
    print(f"Nombre de backtracks : {stats['nbBacktracks']}")
    print("\n---- Complexité ----")
    print("- k est le nombre des cases vides")
    print("- chaque case aurait jusqu’à 9 possibilités")
    print("Alors la complexité est O(9^k) dans le pire des cas.")
    p.grille_to_file(grille,"Generated_grille_completed")
    p.grille_to_file(grille,"Generated_grille_completedBIS")

# ================================================================================
# ================================================================================

# Que faire de ça ?
    # Retirer des valeurs selon la difficulte
    #if difficulte == "Facile":
    #    nb_retraites = 40
    #elif difficulte == "Moyen":
    #    nb_retraites = 50
    #elif difficulte == "Difficile":
    #    nb_retraites = 60
    #elif difficulte == "Extrême":
    #    nb_retraites = 65
    #elif difficulte == "God Mode":
    #    nb_retraites = 70
    #grille_pour_resoudre = retirer_valeurs(grille, nb_retraites)
    #print_grille(grille_pour_resoudre)
    #p.grille_to_file(grille,"Generated_grille_uncompleted")