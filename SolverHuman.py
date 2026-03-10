from Difficulte import Difficulte
from Solver import Solver
from Grille import Grille
from GrilleUtils import *
from Except.GrilleError import GrilleError
from Except.SolverError import SolverError
from Technique import Technique
from SolverBacktrackStats import SolverBacktrackStats


class SolverHuman(Solver):
    @staticmethod
    def solveGrille(grille : Grille) -> bool:
        grille.adjustCandidates()
        while not SolverHuman.isCompleted(grille):      #on boucle tant que la grille n'est pas complètement résolue
            #---------------debug:
            #for c in range(grille.getSize()**4):
            #    print("c:", c, ", v=", grille.getCelluleValueIndex(c), ", ca=", grille.getCelluleCandidatesIndex(c))
            #---------------
            if SolverHuman.singletonNu(grille):         #on essaye les techniques de la moins couteuse à la plus couteuse
                continue                                #on retourne au départ de la boucle si jamais une des techniques fonctionne
            if SolverHuman.dernierNombre(grille):
                continue
            if SolverHuman.singletonCache(grille):
                continue
            if SolverHuman.paireNu(grille):
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
    

    #applique la méthode de singleton caché sur la zone de la cellule numéro 'index', renvoie une liste avec la valeur si elle a été trouvée et vide sinon
    @staticmethod
    def _singletonCacheZone(grille : Grille, index : int) -> list[int]:
        sizeCote = grille.getSize()
        size = sizeCote**2
        zoneIndex = zoneIndexFromCoord(rowIndexFromCelluleIndex(index, sizeCote), columnIndexFromCelluleIndex(index, sizeCote), sizeCote)   #index de la zone
        relatifIndex = relatifIndexFromAbsoluteIndex(index, sizeCote)   #index de la cellule relatif à la zone
        celluleCandidates = grille.getCelluleCandidatesZoneIndex(zoneIndex, relatifIndex)
        zoneCandidates = []
        for cell in range(size):        #on crée la liste de tout les candidats dans la zone sauf ceux de la cellule en question
            if cell!=relatifIndex:
                zoneCandidates = listUnion(zoneCandidates, grille.getCelluleCandidatesZoneIndex(zoneIndex, cell))
        candidatesOnlyInThisCellule = listDifference(celluleCandidates, zoneCandidates)     #on enlève les candidats de la cellule qui sont autre part dans la zone
        if len(candidatesOnlyInThisCellule)>1:
            raise(GrilleError("SolverHuman: Il y a deux solutions possible pour une cellule en utilisant le singleton caché (sur la zone)!"))
        return candidatesOnlyInThisCellule


    #applique la méthode de singleton caché sur la ligne de la cellule numéro 'index', renvoie une liste avec la valeur si elle a été trouvée et vide sinon
    @staticmethod
    def _singletonCacheRow(grille : Grille, index : int) -> list[int]:
        sizeCote = grille.getSize()
        size = sizeCote**2
        rowIndex = rowIndexFromCelluleIndex(index, sizeCote)   #index de la ligne
        relatifIndex = relatifIndexFromAbsoluteIndex(index, sizeCote, "row")   #index de la cellule relatif à la ligne
        celluleCandidates = grille.getCelluleCandidatesIndex(index)
        rowCandidates = []
        for cell in range(size):        #on crée la liste de tout les candidats dans la ligne sauf ceux de la cellule en question
            if cell!=relatifIndex:
                rowCandidates = listUnion(rowCandidates, grille.getCelluleCandidatesIndex(rowIndex*size + cell))
        candidatesOnlyInThisCellule = listDifference(celluleCandidates, rowCandidates)     #on enlève les candidats de la cellule qui sont autre part dans la ligne
        if len(candidatesOnlyInThisCellule)>1:
            raise(GrilleError("SolverHuman: Il y a deux solutions possible pour une cellule en utilisant le singleton caché (sur la ligne)!"))
        return candidatesOnlyInThisCellule
    

    #applique la méthode de singleton caché sur la colonne de la cellule numéro 'index', renvoie une liste avec la valeur si elle a été trouvée et vide sinon
    @staticmethod
    def _singletonCacheColumn(grille : Grille, index : int) -> list[int]:
        sizeCote = grille.getSize()
        size = sizeCote**2
        columnIndex = columnIndexFromCelluleIndex(index, sizeCote)   #index de la colonne
        relatifIndex = relatifIndexFromAbsoluteIndex(index, sizeCote, "column")   #index de la cellule relatif à la colonne
        celluleCandidates = grille.getCelluleCandidatesIndex(index)
        columnCandidates = []
        for cell in range(size):        #on crée la liste de tout les candidats dans la colonne sauf ceux de la cellule en question
            if cell!=relatifIndex:
                columnCandidates = listUnion(columnCandidates, grille.getCelluleCandidatesIndex(columnIndex + cell*size))
        candidatesOnlyInThisCellule = listDifference(celluleCandidates, columnCandidates)     #on enlève les candidats de la cellule qui sont autre part dans la colonne
        if len(candidatesOnlyInThisCellule)>1:
            raise(GrilleError("SolverHuman: Il y a deux solutions possible pour une cellule en utilisant le singleton caché (sur la colonne)!"))
        return candidatesOnlyInThisCellule


    #applique la méthode de singleton caché afin de trouver une valeur dans la grille, renvoie True si une valeur a été trouvée et False sinon
    @staticmethod
    def singletonCache(grille : Grille) -> bool:
        sizeCote = grille.getSize()
        size = sizeCote**2
        celluleCount = size**2          #on calcule le nombre de cellules
        for cell in range(celluleCount):            #on itère sur chaque cellule
            value = grille.getCelluleValueIndex(cell)
            if value!=0:            #si la cellule a une valeur alors on ne s'en occupe pas
                continue
            resList = SolverHuman._singletonCacheZone(grille, cell) #vérifie si on trouve une valeur adéquate à partir de la zone
            if len(resList) == 1:
                if not SolverHuman.isValid(grille, rowIndexFromCelluleIndex(cell, sizeCote), columnIndexFromCelluleIndex(cell , sizeCote), resList[0]):    #failsafe au cas où la solution proposée n'est pas valide
                    raise(SolverError("SolverHuman: la technique de résolution singletonCache propose une valeur rendant la grille invalide!"))
                grille.setCelluleValueIndex(cell, resList[0])
                grille.adjustCandidatesAfterAddingValueIndex(cell)
                return True
            resList = SolverHuman._singletonCacheRow(grille, cell) #vérifie si on trouve une valeur adéquate à partir de la ligne
            if len(resList) == 1:
                if not SolverHuman.isValid(grille, rowIndexFromCelluleIndex(cell, sizeCote), columnIndexFromCelluleIndex(cell , sizeCote), resList[0]):    #failsafe au cas où la solution proposée n'est pas valide
                    raise(SolverError("SolverHuman: la technique de résolution singletonCache propose une valeur rendant la grille invalide!"))
                grille.setCelluleValueIndex(cell, resList[0])
                grille.adjustCandidatesAfterAddingValueIndex(cell)
                return True
            resList = SolverHuman._singletonCacheColumn(grille, cell) #vérifie si on trouve une valeur adéquate à partir de la colonne
            if len(resList) == 1:
                if not SolverHuman.isValid(grille, rowIndexFromCelluleIndex(cell, sizeCote), columnIndexFromCelluleIndex(cell , sizeCote), resList[0]):    #failsafe au cas où la solution proposée n'est pas valide
                    raise(SolverError("SolverHuman: la technique de résolution singletonCache propose une valeur rendant la grille invalide!"))
                grille.setCelluleValueIndex(cell, resList[0])
                grille.adjustCandidatesAfterAddingValueIndex(cell)
                return True
        return False            #renvoie faux car on a pas trouvé de valeur adéquate


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
                    raise(SolverError("SolverHuman: la technique de résolution dernierNombre à trouvé une unique cellule vide dans une région qui ne contient pas seulement un candidat"))
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

    # J'ai decidé de choisir la difficulté à propos des methodes humaines, càd que je vois les stats et selon les 
    # stats je choisit la difficulté
    # Idée pour l'instant:
    # FACILE : resolue sans SINGLETON_CACHE (donc maxTechnique <= DERNIER_NOMBRE)
    # MOYEN : resolue avec SINGLETON_CACHE au moins une fois (ÉLARGI pour inclure plus de cas)
    # DIFFICILE : le solveur humain est bloqué (stuck = True) ou techniques > SINGLETON_CACHE
    # SI VOUS AVEZ D'AUTRES IDEE N'HESITEZ PAS
    def rateFromStats(stats: dict) -> Difficulte:
        if stats["stuck"]:
            return Difficulte.DIFFICILE
        maxTech = stats["maxTechnique"]
        if maxTech is None or maxTech <= Technique.DERNIER_NOMBRE:
            return Difficulte.FACILE
        if maxTech == Technique.SINGLETON_CACHE or maxTech == Technique.SINGLETON_NU: 
            return Difficulte.MOYEN
        if maxTech == Technique.PAIR_NU:
            return Difficulte.DIFFICILE
        return Difficulte.DIFFICILE
    
    # Car j'ai testé plein de fois et j'ai remarqué que MOYEN prends enormemnt temps pour se
    # generer, alors pour l'instant tq on n'a pas beacoup de techniques humaines jai fais que cest 
    # MOYEN quand il peut etre aussi SINGLETON_NU