from Solver import Solver
from Grille import Grille
from GrilleUtils import *
from Except.GrilleError import GrilleError
from Except.SolverError import SolverError


class SolverHuman(Solver):
    @staticmethod
    def solveGrille(grille : Grille) -> bool:
        while not SolverHuman.isCompleted(grille):      #on boucle tant que la grille n'est pas complètement résolue
            if SolverHuman.singletonNu(grille):         #on essaye les techniques de la moins couteuse à la plus couteuse
                continue                                #on retourne au départ de la boucle si jamais une des techniques fonctionne
            if SolverHuman.dernierNombre(grille):
                continue
            if SolverHuman.singletonCache(grille):
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
                grille.setCelluleValueIndex(candidates[0])
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
                columnCandidates = listUnion(columnCandidates, grille.getCelluleCandidatesIndex(columnIndex*size + cell))
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
            if resList==1:
                if not SolverHuman.isValid(grille, rowIndexFromCelluleIndex(cell, sizeCote), columnIndexFromCelluleIndex(cell , sizeCote), resList[0]):    #failsafe au cas où la solution proposée n'est pas valide
                    raise(SolverError("SolverHuman: la technique de résolution singletonCache propose une valeur rendant la grille invalide!"))
                grille.setCelluleValueIndex(cell, resList[0])
                return True
            resList = SolverHuman._singletonCacheRow(grille, cell) #vérifie si on trouve une valeur adéquate à partir de la ligne
            if resList==1:
                if not SolverHuman.isValid(grille, rowIndexFromCelluleIndex(cell, sizeCote), columnIndexFromCelluleIndex(cell , sizeCote), resList[0]):    #failsafe au cas où la solution proposée n'est pas valide
                    raise(SolverError("SolverHuman: la technique de résolution singletonCache propose une valeur rendant la grille invalide!"))
                grille.setCelluleValueIndex(cell, resList[0])
                return True
            resList = SolverHuman._singletonCacheColumn(grille, cell) #vérifie si on trouve une valeur adéquate à partir de la colonne
            if resList==1:
                if not SolverHuman.isValid(grille, rowIndexFromCelluleIndex(cell, sizeCote), columnIndexFromCelluleIndex(cell , sizeCote), resList[0]):    #failsafe au cas où la solution proposée n'est pas valide
                    raise(SolverError("SolverHuman: la technique de résolution singletonCache propose une valeur rendant la grille invalide!"))
                grille.setCelluleValueIndex(cell, resList[0])
                return True
        return False            #renvoie faux car on a pas trouvé de valeur adéquate


    #applique la méthode dernier nombre afin de trouver une valeur dans la grille, renvoie True si une valeur a été trouvée et False sinon
    @staticmethod
    def dernierNombre(grille: Grille) -> bool:  #il est peut-être possible d'optimiser le nombre de ligne de code
        sizeCote = grille.getSize()
        size = sizeCote**2
        celluleCount = size**2          #on calcule le nombre de cellules
        for cell in range(celluleCount):            #on itère sur chaque cellule
            value = grille.getCelluleValueIndex(cell)
            if value==0:        #si la cellule est vide alors on regarde si il y en a une autre dans sa zone/ligne/colonne
                rowIndex = rowIndexFromCelluleIndex(cell, sizeCote)
                relatifIndexRow = relatifIndexFromAbsoluteIndex(cell, sizeCote, "row")
                columnIndex = columnIndexFromCelluleIndex(cell, sizeCote)
                relatifIndexColumn = relatifIndexFromAbsoluteIndex(cell, sizeCote, "column")
                zoneIndex = zoneIndexFromCoord(rowIndex, columnIndex, sizeCote)
                relatifIndexZone = relatifIndexFromAbsoluteIndex(cell, sizeCote, "zone")
                isTheOnlyZero = True
                for c in range(size):                    #-------------------- on teste la ligne
                    valueC = grille.getCelluleValueCoord(rowIndex, c)
                    if c!=relatifIndexRow and valueC==0:  #si il y a un deuxième zero alors on passe au type de région suivant
                        isTheOnlyZero = False
                        break
                if isTheOnlyZero:                       #si il n'y a qu'un seul zero alors on remplie la case
                    values= grille.getRow(rowIndex)     #on récupère les valeurs de la région pour déterminer la valeur de la case
                    for v in range(1, size):
                        if v not in values:
                            if not SolverHuman.isValid(grille, rowIndexFromCelluleIndex(cell, sizeCote), columnIndexFromCelluleIndex(cell , sizeCote), v):    #failsafe au cas où la solution proposée n'est pas valide
                                raise(SolverError("SolverHuman: la technique de résolution dernierNombre propose une valeur rendant la grille invalide!"))
                            grille.setCelluleValueIndex(cell, v)
                            return True
                else:
                    isTheOnlyZero=True
                for c in range(size):                    #-------------------- on teste la colonne
                    valueC = grille.getCelluleValueCoord(c, columnIndex)
                    if c!=relatifIndexColumn and valueC==0:  #si il y a un deuxième zero alors on passe au type de région suivant
                        isTheOnlyZero = False
                        break
                if isTheOnlyZero:                       #si il n'y a qu'un seul zero alors on remplie la case
                    values= grille.getColumn(columnIndex)   #on récupère les valeurs de la région pour déterminer la valeur de la case
                    for v in range(1, size):
                        if v not in values:
                            if not SolverHuman.isValid(grille, rowIndexFromCelluleIndex(cell, sizeCote), columnIndexFromCelluleIndex(cell , sizeCote), v):    #failsafe au cas où la solution proposée n'est pas valide
                                raise(SolverError("SolverHuman: la technique de résolution dernierNombre propose une valeur rendant la grille invalide!"))
                            grille.setCelluleValueIndex(cell, v)
                            return True
                else:
                    isTheOnlyZero=True
                for c in range(size):                    #-------------------- on teste la zone
                    valueC = grille.getCelluleValueZoneIndex(zoneIndex, c)
                    if c!=relatifIndexZone and valueC==0:  #si il y a un deuxième zero alors on passe au type de région suivant
                        isTheOnlyZero = False
                        break
                if isTheOnlyZero:                       #si il n'y a qu'un seul zero alors on remplie la case
                    values= grille.getZone(zoneIndex)   #on récupère les valeurs de la région pour déterminer la valeur de la case
                    for v in range(1, size):
                        if v not in values:
                            if not SolverHuman.isValid(grille, rowIndexFromCelluleIndex(cell, sizeCote), columnIndexFromCelluleIndex(cell , sizeCote), v):    #failsafe au cas où la solution proposée n'est pas valide
                                raise(SolverError("SolverHuman: la technique de résolution dernierNombre propose une valeur rendant la grille invalide!"))
                            grille.setCelluleValueIndex(cell, v)
                            return True
        return False        #on renvoie False si on a parcouru toute les cellules sans trouver une cellule vide unique