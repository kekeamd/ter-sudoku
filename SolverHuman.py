from Difficulte import Difficulte
from Solver import Solver
from Grille import Grille
from GrilleUtils import *
from Except.SolverError import SolverError
from Technique import Technique


class SolverHuman(Solver):
    @staticmethod
    def solveGrille(grille : Grille) -> bool:
        grille.adjustCandidates()
        while not SolverHuman.isCompleted(grille):      #on boucle tant que la grille n'est pas complètement résolue
            #---------------debug:
            #for c in range(grille.getSize()**4):
            #    print("c:", c, ", v=", grille.getCelluleValueIndex(c), ", ca=", grille.getCelluleCandidatesIndex(c))
            #---------------
            if SolverHuman.dernierNombre(grille):
                continue
            if SolverHuman.singletonNu(grille):         #on essaye les techniques de la moins couteuse à la plus couteuse
                continue                                #on retourne au départ de la boucle si jamais une des techniques fonctionne
            if SolverHuman.singletonCache(grille):
                continue
            if SolverHuman.paireNu(grille):
                continue
            if SolverHuman.paireCachee(grille):
                continue
            if SolverHuman.candidatEnferme(grille):
                continue
            raise(SolverError("SolverHuman: Impossible de résoudre la grille à partir des techniques actuellement implémentées."))      #si on a testé toutes les techniques et aucune fonctionne alors il nous manque des techniques


    #vérifie si la grille est complète ou pas (si il reste des cellule vide)
    @staticmethod
    def isCompleted(grille : Grille) -> bool:
        sizeCote = grille.getSize()
        size = sizeCote**2
        celluleCount = size**2
        for cell in range(celluleCount):
            if grille.getCelluleValueIndex(cell)==0:
                return False
        return True


    #------------------------------------TECHNIQUES D'ATTRIBUTION DE VALEUR--------------------------------------------


    #applique la méthode de singleton nu afin de trouver une valeur dans la grille, renvoie True si une valeur a été trouvée et False sinon
    @staticmethod
    def singletonNu(grille : Grille) -> bool:
        sizeCote = grille.getSize()
        size = sizeCote**2
        celluleCount = size**2          #on calcule le nombre de cellules
        for cell in range(celluleCount):            #on itère sur chaque cellule
            candidates = grille.getCelluleCandidatesIndex(cell)
            value =  grille.getCelluleValueIndex(cell)
            if value==0 and len(candidates)==1:     #si la cellule n'a pas encore de valeur et a seulement un candidat alors on lui attribut la valeur du candidat
                if not SolverHuman.isValid(grille, rowIndexFromCelluleIndex(cell, sizeCote), columnIndexFromCelluleIndex(cell , sizeCote), candidates[0]):    #failsafe au cas où la solution proposée n'est pas valide
                    raise(SolverError("SolverHuman: la technique de résolution singletonNu propose une valeur rendant la grille invalide!"))
                grille.setCelluleValueIndex(cell, candidates[0])
                grille.adjustCandidatesAfterAddingValueIndex(cell)
                return True             #pas besoin d'aller plus loin, on renvoie vrai
        return False    #si on a pas trouvé de valeur alors on renvoie faux


    #applique la méthode de singleton caché afin de trouver une valeur dans la grille, renvoie True si une valeur a été trouvée et False sinon
    @staticmethod
    def singletonCache(grille : Grille) -> bool:
        sizeCote = grille.getSize()
        size = sizeCote**2
        regions = grille.getRegions()
        for region in regions:  #on itère sur chaque zone/ligne/colonne
                for ca in range(1, size+1):  #on itère sur chaque candidat possible et on vérifie si il est dans les candidats d'exactement une cellule
                    cell = None
                    for cellule in region:
                        if cellule.getValue()!=0:   #si la cellule a une valeur on passe à la prochaine
                            continue
                        candidats = cellule.getCandidates()
                        if ca in candidats:
                            if cell!=None:  #si il est candidat dans plus d'une cellule alors on passe au prochain candidat
                                cell=None
                                break
                            cell = cellule
                    if cell!=None:  #singleton caché trouvé
                        pos = cell.getPosition()
                        if not SolverHuman.isValid(grille, rowIndexFromCelluleIndex(pos, sizeCote), columnIndexFromCelluleIndex(pos , sizeCote), ca):    #failsafe au cas où la solution proposée n'est pas valide
                            raise(SolverError("SolverHuman: la technique de résolution singletonCache propose une valeur rendant la grille invalide!"))
                        grille.setCelluleValueIndex(pos, ca)
                        grille.adjustCandidatesAfterAddingValueIndex(pos)
                        return True

        return False


    #applique la méthode dernier nombre afin de trouver une valeur dans la grille, renvoie True si une valeur a été trouvée et False sinon
    @staticmethod
    def dernierNombre(grille: Grille) -> bool:  #il est peut-être possible d'optimiser le nombre de ligne de code
        sizeCote = grille.getSize()
        regions = grille.getRegions()
        for region in regions:      #on itère sur toutes les lignes/colonnes/zones de la grille
            regionValues = [c.getValue() for c in region]   #on créer la liste contenant la valeur des cellules dans la région
            if regionValues.count(0)==1:  #on vérifie si la région contient une et une seule cellule vide
                c = regionValues.index(0)
                cellule = region[c] #on récupère la cellule vide
                if len(cellule.getCandidates())!=1:     #failsafe si jamais on ne cherche pas correctement la cellule vide
                    raise(SolverError("SolverHuman: la technique de résolution dernierNombre à trouvé une unique cellule vide dans sa région qui ne contient pas seulement un candidat"))
                value = cellule.getCandidates()[0]
                pos = cellule.getPosition()
                if not SolverHuman.isValid(grille, rowIndexFromCelluleIndex(pos, sizeCote), columnIndexFromCelluleIndex(pos , sizeCote), value):    #failsafe au cas où la solution proposée n'est pas valide
                    raise(SolverError("SolverHuman: la technique de résolution dernierNombre propose une valeur rendant la grille invalide!"))
                grille.setCelluleValueIndex(pos, value)
                grille.adjustCandidatesAfterAddingValueIndex(pos)
                return True
        return False        #on renvoie False si on a parcouru toute les cellules sans trouver une cellule vide unique


    #------------------------------------TECHNIQUES D'ELIMINATION DE CANDIDATS--------------------------------------------


    # Quand deux cellules d’une même région contiennent exactement les mêmes deux candidats, elle permet d’éliminer ces 
    # candidats ailleurs, ce qui débloque ensuite d’autres techniques comme singletonNu
    @staticmethod
    def paireNu(grille: Grille) -> bool:
        for region in grille.getRegions():   # chaque région = zone, ligne, colonne
            pairCells = []

            # 1) récupérer les cellules vides avec exactement 2 candidats
            for cellule in region:
                if cellule.getValue() == 0: # cellule vide
                    candidats = cellule.getCandidates()
                    if len(candidats) == 2: # si la cellule possede exactement 2 candidats
                        pairCells.append((cellule, sorted(candidats))) # on trie les candidats

            # 2) chercher deux cellules ayant exactement la même paire
            for i in range(len(pairCells)):
                for j in range(i + 1, len(pairCells)):
                    cellule1, cand1 = pairCells[i]
                    cellule2, cand2 = pairCells[j]

                    if cand1 == cand2:
                        paire = cand1 # la paire trouvée
                        changed = False

                        # 3) retirer ces deux candidats des autres cellules de la région
                        for cellule in region:
                            # on ignore les deux cellules de la paire
                            if cellule is cellule1 or cellule is cellule2:
                                continue
                            # on ignore les cellules deja remplies
                            if cellule.getValue() != 0:
                                continue

                            oldCandidates = cellule.getCandidates()
                            # on enleve les valeurs de la paire des candidats
                            newCandidates = listDifference(oldCandidates, paire)

                            if newCandidates != oldCandidates:
                                cellule.setCandidates(newCandidates)
                                changed = True
                        if changed:
                            return True
        return False
    

    # Quand deux cellules d’une même région contiennent les mêmes deux candidats et que ces candidats ne sont pas dans le reste de la région, renvoie True si ces cellules sont trouvées et False sinon
    @staticmethod
    def paireCachee(grille: Grille) -> bool:
        sizeCote = grille.getSize()
        size = sizeCote**2
        regions = grille.getRegions()

        paires = []
        for ca1 in range(1, size+1):    #on créer toutes les paires de candidats possibles
                for ca2 in range(ca1+1, size+1):
                    paires.append([ca1, ca2])

        for region in regions:   #on itère sur toutes les lignes/colonnes/zones de la grille
            #-----------------identification de la paire cachée
            for paire in paires:    #on itère sur toutes les paires de candidats possibles et on vérifie si il y a exactement deux cellules contenant la paire dans leurs candidats(c'est-à-dire si on trouve une paire cachée à partir de cette paire)
                cell1 = None
                cell2 = None
                for cellule in region:
                    if cellule.getValue()!=0:
                        continue
                    candidats = cellule.getCandidates()
                    if paire[0] in candidats and paire[1] in candidats: #on vérifie si la cellule contient la paire dans ses candidats
                        if cell1 == None:
                            cell1 = cellule
                        elif cell2 == None:
                            cell2 = cellule
                        else:        #si on avait déjà deux cellules contenant la paire dans leurs candidats alors on passe à la prochaine paire
                            cell1 = None
                            cell2 = None
                            break
                    elif paire[0] in candidats or paire[1] in candidats: #si la cellule ne contient qu'un seul des deux candidats de la paire alors il ne peux pas y avoir de paire cachée avec cette paire dans cette région
                        cell1 = None
                        cell2 = None
                        break
                if cell1!=None and cell2!=None:     #on a une paire cachée
                    #-------------conséquences de la paire cachée
                    cell1.setCandidates(paire)   #on élimine les autres candidats des cellules de la paire cachée
                    cell2.setCandidates(paire)
                    for region2 in regions:             #on élimine les candidats de la paire de candidats dans la deuxième région qui contient entièrement la paire cachée si jamais elle existe
                        if cell1 in region2 and cell2 in region2 and region2!=region:
                            for cellule2 in region2:
                                if cellule2==cell1 or cellule2==cell2:
                                    continue
                                cellule2.setCandidates(listDifference(cellule2.getCandidates(), paire))
                            break
                    return True
        return False
    

    # quand un candidat est dans des cellules strictement à l'intersection de deux régions, renvoie True si ce candidat est trouvé et False sinon
    @staticmethod
    def candidatEnferme(grille : Grille) -> bool:
        sizeCote = grille.getSize()
        size = sizeCote**2
        regions = grille.getRegions()   #liste des régions alternant entre zone,ligne,colonne,zone,ligne,etc...
        for r in range(len(regions)):
            region = regions[r]
            for ca in range(1, size+1):
                cellList= []   #liste des cellules contenants le candidat enfermé
                region2Type = "" #"zone"/"row"/"column"
                for c in range(len(region)):    #on cherche les cellules contenant le candidat
                    cellule = region[c]
                    if cellule.getValue()!=0:
                        continue
                    if ca in cellule.getCandidates():   #la cellule contient le candidat
                        if len(cellList)==0:    #si c'est la première alors juste on l'ajoute à la liste
                            pass
                        elif len(cellList)==1:  #si c'est la deuxième alors on l'ajoute à la liste, on peut aussi déterminer si la deuxième région sera une zone/ligne/colonne, on s'arrête si on ne peut pas car ça rend le candidat impossible a enfermer
                            #----------------identification des régions----------------------
                            if r%3==0:  #la première région est une zone
                                if compareIndexRegion(cellList[0].getPosition(), cellule.getPosition(), sizeCote, "row"):    #la deuxième région est une ligne
                                    region2Type= "row"
                                if compareIndexRegion(cellList[0].getPosition(), cellule.getPosition(), sizeCote, "column"): #la deuxième région est une colonne
                                    region2Type= "column"
                            else:       #la première région est une ligne/colonne
                                if compareIndexRegion(cellList[0].getPosition(), cellule.getPosition(), sizeCote, "zone"):   #la deuxième région est une zone
                                    region2Type= "zone"
                            #-----------------------------------------------------------------
                            if region2Type=="": #les deux cellules ne sont pas à l'intersection de deux régions et donc le candidat ne peut pas être enfermé
                                cellList=[]
                                break
                        else:                   #si c'est au dessus de la deuxième alors on l'ajoute à la liste sauf si elle n'appartient pas à la deuxième région
                            if not compareIndexRegion(cellList[0].getPosition(), cellule.getPosition(), sizeCote, region2Type):
                                cellList=[]
                                break
                        cellList.append(cellule)
                if len(cellList)>1: #---------on a trouvé un candidat enfermé---------
                    region2 = None
                    rowIndex = rowIndexFromCelluleIndex(cellList[0].getPosition(), sizeCote)
                    columnIndex = columnIndexFromCelluleIndex(cellList[0].getPosition(), sizeCote)
                    zoneIndex = zoneIndexFromCoord(rowIndex, columnIndex, sizeCote)
                    if region2Type=="zone":
                        region2= regions[zoneIndex*3]
                    if region2Type=="row":
                        region2= regions[rowIndex*3+1]
                    if region2Type=="column":
                        region2= regions[columnIndex*3+2]
                    for cellule in region2:
                        if cellule.getValue()==0 and cellule not in cellList:
                            cellule.setCandidates(listDifference(cellule.getCandidates(), [ca]))
                    return True
        return False

    # J'ai decidé de choisir la difficulté à propos des methodes humaines, càd que je vois les stats et selon les 
    # stats je choisit la difficulté
    @staticmethod
    def rateFromStats(stats: dict) -> Difficulte:
        if stats is None:
            raise ValueError("rateFromStats: stats vaut None")

        if stats["stuck"]:
            return Difficulte.GODMODE

        maxTech = stats["maxTechnique"]
        counts = stats["counts"]

        if maxTech is None or maxTech == Technique.DERNIER_NOMBRE:
            return Difficulte.FACILE

        # plus precis pour la difficulté MOYEN
        if maxTech == Technique.SINGLETON_NU:
            if counts.get(Technique.SINGLETON_NU, 0) > 10:
                return Difficulte.MOYEN
            return Difficulte.FACILE

        if maxTech == Technique.SINGLETON_CACHE:
            return Difficulte.MOYEN

        if maxTech in (Technique.PAIR_NU, Technique.PAIR_CACHEE):
            return Difficulte.DIFFICILE

        if maxTech == Technique.CANDIDAT_ENFERME:
            return Difficulte.EXTREME

        return Difficulte.EXTREME