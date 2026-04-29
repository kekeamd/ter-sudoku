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
            if SolverHuman.gratteCiel(grille):
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
    # "These 2 cells are locked → others must change"
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
                        #print(f"PAIRE NUE TROUVEE : {cand1}")  # temporaire
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
                            print(f"PAIRE NUE APPLIQUEE : {cand1}")
                            return True
        return False
    

    # Quand deux cellules d’une même région contiennent les mêmes deux candidats et que ces candidats ne sont pas dans le reste de la région, renvoie True si ces cellules sont trouvées et False sinon
    # Une fonction qui détecte la paire cachée et qui débloque la fonction pairNu
    # "These 2 numbers are locked → these cells must change"
    # On va le faire plus strict:
    # - number a appears in exactly two cells in the region
    # - number b appears in exactly two cells in the region
    # - and those are the same two cells
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

                # nouvelles listes : où apparaît chaque candidat dans la région
                cells_ca1 = []
                cells_ca2 = []

                for cellule in region:
                    if cellule.getValue()!= 0:
                        continue
                    candidats = cellule.getCandidates()

                    # on mémorise séparément les cellules contenant chaque candidat
                    if paire[0] in candidats:
                        cells_ca1.append(cellule)
                    if paire[1] in candidats:
                        cells_ca2.append(cellule)

                    # on garde aussi la logique de base pour repérer 2 cellules contenant la paire complète
                    if paire[0] in candidats and paire[1] in candidats: #on vérifie si la cellule contient la paire dans ses candidats
                        if cell1 == None:
                            cell1 = cellule
                        elif cell2 == None:
                            cell2 = cellule
                        else:        #si on avait déjà deux cellules contenant la paire dans leurs candidats alors on passe à la prochaine paire
                            cell1 = None
                            cell2 = None
                            break
                    # Cette elif déclenche presque à chaque fois la fonction
                    # on ignore les cellules contenant un seul des deux candidats : elles ne font pas partie de la paire cachée
                    # et leur existence ne l'invalide pas
                    #elif paire[0] in candidats or paire[1] in candidats: #si la cellule ne contient qu'un seul des deux candidats de la paire alors il ne peux pas y avoir de paire cachée avec cette paire dans cette région
                    #    cell1 = None
                    #    cell2 = None
                    #    break
                if (
                    cell1 is not None and cell2 is not None
                    and len(cells_ca1) == 2
                    and len(cells_ca2) == 2
                    and set(cells_ca1) == set(cells_ca2)
                    and cell1 in cells_ca1 and cell2 in cells_ca1
                ):     #on a une paire cachée
                    #print(f"paire cachée détectée : {paire} dans cellules {cell1.getPosition()} et {cell2.getPosition()}")
                    #-------------conséquences de la paire cachée
                    # vérifier que la réduction change quelque chose
                    
                    changed = False

                    if sorted(cell1.getCandidates()) != sorted(paire):
                        cell1.setCandidates(paire.copy()) # on élimine les autres candidats des cellules de la paire cachée
                        changed = True
                    if sorted(cell2.getCandidates()) != sorted(paire):
                        cell2.setCandidates(paire.copy())
                        changed = True
                    #for region2 in regions:             # on élimine les candidats de la paire de candidats dans la deuxième région qui contient entièrement la paire cachée si jamais elle existe
                    #    if cell1 in region2 and cell2 in region2 and region2!=region:
                    #        for cellule2 in region2:
                    #            if cellule2==cell1 or cellule2==cell2:
                    #                continue
                    #            old = cellule2.getCandidates()
                    #            new = listDifference(old, paire)
                    #            if new != old:
                    #                cellule2.setCandidates(new)
                    #                changed = True
                    #        break

                    # IMPORTANT :
                    # on ne supprime pas la paire dans une autre région commune ici
                    # Une paire cachée agit uniquement dans la région où elle a été détectée
                    # Le reste sera fait naturellement par les autres techniques

                    if changed:
                        print(f"paire cachée appliquée : {paire} dans cellules {cell1.getPosition()} et {cell2.getPosition()}")
                        return True
                    # sinon continuer à chercher une autre paire cachée qui change quelque chose
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

                    changed = False # sert pour vraiment savoir si on a changé qqch avec cette technique

                    for cellule in region2:
                        if cellule.getValue()==0 and cellule not in cellList:
                            old = cellule.getCandidates()
                            new = listDifference(old, [ca])
                            if new != old:
                                cellule.setCandidates(new)
                                changed = True
                    if changed:
                        return True
        return False

    @staticmethod
    def gratteCiel(grille : Grille) -> bool:
        sizeCote = grille.getSize()
        size = sizeCote**2
        # ── Version sur les lignes ─────────────────────────────────────────
        # Pour chaque val, on cherche deux lignes ayant exactement 2 candidats
        # avec une colonne en commun (la base) → les deux sommets s'éliminent mutuellement
        # Collecte : pour chaque ligne, les colonnes où val est candidat
        for val in range(1,size+1):
            rows_candidates = {}
            for r in range(size):
                cols=[c for c in range(size) 
                    if grille.getCelluleValueCoord(r,c)==0
                    and val in grille.getCelluleCandidatesCoord(r,c)]
                if len(cols)==2:
                    rows_candidates[r]=cols # on garde seulement les lignes avec exactement 2 colonnes candidates
            # Cherche deux lignes avec une colonne en commun
            rows=list(rows_candidates.keys())
            for i in range(len(rows)):
                for j in range(i+1,len(rows)):
                    r1,r2=rows[i],rows[j]
                    c1,c2=rows_candidates[r1]  # les deux colonnes de la ligne r1
                    c3,c4=rows_candidates[r2]  # les deux colonnes de la ligne r2

                    # Cherche la colonne commune (base) et les deux sommets
                    if c1==c3:
                        sommet1,sommet2=(r1,c2),(r2,c4)  # les sommets sont c2 et c4
                    elif c1==c4:
                        sommet1,sommet2=(r1,c2),(r2,c3)
                    elif c2==c3:
                        sommet1,sommet2=(r1,c1),(r2,c4)
                    elif c2==c4:
                        sommet1,sommet2=(r1,c1),(r2,c3)
                    else:
                        continue  # pas de base commune
                    
                     # Élimine val de toutes les cellules qui voient les deux sommets
                    changed = SolverHuman.eliminationCandidatsGratteCiel(grille, val, sommet1, sommet2, sizeCote)
                    if changed:
                        return True
            # ── Version sur les colonnes(symetrique) ───────────────────────────────────────
        # Même logique mais en cherchant des colonnes avec 2 candidats et une ligne en commun
        for val in range(1,size+1):
            cols_candidates={}
            for c in range(size):
                rows=[r for r in range(size)
                      if grille.getCelluleValueCoord(r,c)==0
                      and val in grille.getCelluleCandidatesCoord(r,c)]
                if len(rows)==2:
                    cols_candidates[c]=rows
            cols=list(cols_candidates.keys())
            for i in range(len(cols)):
                for j in range(i+1,len(cols)):
                    c1,c2=cols[i],cols[j]
                    r1,r2=cols_candidates[c1]
                    r3,r4=cols_candidates[c2]

                    if r1==r3:
                        sommet1,sommet2=(r2,c1),(r4,c2)
                    elif r1==r4:
                        sommet1,sommet2=(r2,c1),(r3,c2)
                    elif r2==r4:
                        sommet1,sommet2=(r1,c1),(r3,c2)
                    elif r2==r3:
                        sommet1,sommet2=(r1,c1),(r4,c2)
                    else:
                        continue #pas de base de gratte-ciel

                    changed = SolverHuman.eliminationCandidatsGratteCiel(grille, val, sommet1, sommet2, sizeCote)
                    if changed:
                        print("gratte ciel appliqué\n")
                        return True

        return False
    # Élimine val de toutes les cellules qui voient les deux sommets simultanément.Deux cellules se "voient" si elles partagent la même ligne, colonne ou zone.
    @staticmethod
    def eliminationCandidatsGratteCiel(grille: Grille, val: int, sommet1: tuple, sommet2: tuple, sizeCote: int) -> bool: 
        size= sizeCote**2
        changed=False
        r1,c1=sommet1
        r2,c2=sommet2
        zone1=zoneIndexFromCoord(r1,c1,sizeCote)
        zone2=zoneIndexFromCoord(r2,c2,sizeCote)
        for r in range(size):
            for c in range(size):
                if (r,c)==sommet1 or (r,c)==sommet2:
                    continue
                if grille.getCelluleValueCoord(r,c)!=0:
                    continue
                if val not in grille.getCelluleCandidatesCoord(r,c):
                    continue
                zone=zoneIndexFromCoord(r,c,sizeCote)
                voit1=(r==r1 or c==c1 or zone==zone1)
                voit2=(r==r2 or c==c2 or zone==zone2)
                if voit1 and voit2:
                    old=grille.getCelluleCandidatesCoord(r,c)
                    new=listDifference(old,[val])
                    grille._getCelluleCoord(r,c).setCandidates(new)
                    changed=True
        return changed


    @staticmethod
    def x_WingLignes(grille:Grille) -> bool:
        sizeCote=grille.getSize()
        size=sizeCote**2
        changed=False
        for val in range(1,size+1):
            row_candidates={}
            for r in range(size):
                cols=[c for c in range(size) 
                    if grille.getCelluleValueCoord(r,c)==0
                    and val in grille.getCelluleCandidatesCoord(r,c)]
                if len(cols)==2:
                    row_candidates[r]=cols
            
            # On compare les lignes deux à deux pour trouver un X-Wing
            rows= list(row_candidates.keys())
            for i in range(len(rows)):
                r1=rows[i]
                cols1=row_candidates[r1]

                for j in range(i+1,len(rows)):
                    r2=rows[j]
                    cols2=row_candidates[r2]

                    # Condition du X-Wing : mêmes colonnes
                    if cols1==cols2: 
                        c1,c2=cols1 # les deux colonnes du X-Wing
                        changed = False
                        print(
                            f"X-WING LIGNES DETECTE "
                        )
                        
                        #Élimination dans les autres lignes
                        for r in range(size):
                            if r!= r1 and r!=r2:
                                #colonne 1
                                if grille.getCelluleValueCoord(r,c1)==0 and val in grille.getCelluleCandidatesCoord(r,c1):
                                    grille.removeCandidateCoord(r,c1,val)
                                    changed=True
                                #colonne 2
                                if grille.getCelluleValueCoord(r,c2)==0 and val in grille.getCelluleCandidatesCoord(r,c2):
                                    grille.removeCandidateCoord(r,c2,val)
                                    changed=True
                        if changed:
                            print(
                                    f"X-WING LIGNES APPLIQUE : "
                                    f"val={val}, lignes=({r1},{r2}), colonnes=({c1},{c2})"
                                )
                            return True
        return False
    # --------------- X-Wing version colonnes -> lignes ----------------
    @staticmethod
    def x_WingColonne(grille:Grille) -> bool:
        changed= False
        sizeCote=grille.getSize()
        size=sizeCote**2
        for val in range(1,size+1):
            cols_candidates={}
            #Trouve les colonnes avec exactement 2 candidats pour val
            for c in range(size):
                rows=[r for r in range(size) 
                    if grille.getCelluleValueCoord(r,c)==0
                    and val in grille.getCelluleCandidatesCoord(r,c)]
                if len(rows)==2:
                    cols_candidates[c]=rows
            
            #Compare les colonnes deux à deux    
            cols=list(cols_candidates.keys())
            for i in range(len(cols)):
                c1=cols[i]
                rows1=cols_candidates[c1]
                for j in range(i+1,len(cols)):
                    c2=cols[j]
                    rows2=cols_candidates[c2]

                    # Condition du X-Wing horizontal : mêmes lignes
                    if rows1==rows2:
                        r1,r2=rows1
                        print(
                            f"X-WING COLONNES DETECTE "
                            )
                        
                        #Élimination dans les autres colonnes
                        for c in range(size):
                            if c != c1 and c != c2:
                                # ligne r1
                                if grille.getCelluleValueCoord(r1, c) == 0 and val in grille.getCelluleCandidatesCoord(r1, c):
                                    grille.removeCandidateCoord(r1, c, val)
                                    changed = True

                                # ligne r2
                                if grille.getCelluleValueCoord(r2, c) == 0 and val in grille.getCelluleCandidatesCoord(r2, c):
                                    grille.removeCandidateCoord(r2, c, val)
                                    changed = True
                        if changed:
                            print(
                                    f"X-WING COLONNES APPLIQUE : "
                                    f"val={val}, colonnes=({c1},{c2}), lignes=({r1},{r2})"
                                )
                            return True
        return False


        
    # Fonction liée au Sudoku Coach avec le score pour chauqe technique
    @staticmethod
    def scoreFromStats(stats: dict) -> dict:
        """
        Retourne un score numérique "coach-like" inspiré du principe de Sudoku Coach /
        SukakuExplainer : la technique maximale compte le plus, puis le volume de travail
        affine légèrement le score.

        IMPORTANT : ce n'est pas le vrai score Sudoku Coach. C'est une approximation locale
        adaptée uniquement aux techniques implémentées dans ce projet.
        """
        if stats is None:
            raise ValueError("scoreFromStats: stats vaut None")

        if stats["stuck"]:
            return {
                "score": 6.0,
                "label": "God Mode",
                "reason": "bloquée avec les techniques implémentées"
            }

        counts = stats["counts"]
        maxTech = stats["maxTechnique"]

        base_scores = {
            None: 1.0,
            Technique.DERNIER_NOMBRE: 1.0,
            Technique.SINGLETON_NU: 1.2,
            Technique.SINGLETON_CACHE: 1.8,
            Technique.PAIR_NU: 2.8,
            Technique.PAIR_CACHEE: 3.2,
            Technique.CANDIDAT_ENFERME: 4.0,
            #Technique.X_WINGC: 4.5,
            #Technique.X_WINGL: 4.5,
            Technique.GRATTE_CIEL: 4.8,
        }

        score = base_scores.get(maxTech, 4.8)

        # petit raffinement par quantité de travail, sans changer radicalement la classe
        score += min(counts.get(Technique.DERNIER_NOMBRE, 0), 12) * 0.01
        score += min(counts.get(Technique.SINGLETON_NU, 0), 20) * 0.02
        score += min(counts.get(Technique.SINGLETON_CACHE, 0), 10) * 0.04
        score += min(counts.get(Technique.PAIR_NU, 0), 6) * 0.08
        score += min(counts.get(Technique.PAIR_CACHEE, 0), 6) * 0.10
        score += min(counts.get(Technique.CANDIDAT_ENFERME, 0), 6) * 0.12
        #score += min(counts.get(Technique.X_WINGL, 0), 6) * 0.15
        #score += min(counts.get(Technique.X_WINGC, 0), 6) * 0.15
        score += min(counts.get(Technique.GRATTE_CIEL, 0), 6) * 0.18

        score = round(score, 2)

        if score <= 1.6:
            label = "Easy"
        elif score <= 2.6:
            label = "Medium"
        elif score <= 4.2:
            label = "Hard"
        elif score <= 6.4:
            label = "Vicious"
        else:
            label = "Fiendish+"

        return {
            "score": score,
            "label": label,
            "reason": maxTech.name if maxTech is not None else "Aucune technique non triviale"
        }

    # J'ai decidé de choisir la difficulté à propos des methodes humaines, càd que je vois les stats et selon les 
    # stats je choisit la difficulté
    @staticmethod
    def rateFromStats(stats: dict) -> Difficulte:
        if stats is None:
            raise ValueError("rateFromStats: stats vaut None")

        coach_like = SolverHuman.scoreFromStats(stats)
        score = coach_like["score"]

        if stats["stuck"]:
            return Difficulte.GODMODE

        if score <= 1.6:
            return Difficulte.FACILE
        if score <= 2.6:
            return Difficulte.MOYEN
        if score <= 4.9:
            return Difficulte.DIFFICILE
        if score <= 6.4:
            return Difficulte.EXTREME
        return Difficulte.GODMODE