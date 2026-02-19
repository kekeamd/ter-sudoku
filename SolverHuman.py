from Solver import Solver
from Grille import Grille
from GrilleUtils import *
from Except.GrilleError import GrilleError


class SolverHuman(Solver): #transformation de la classe en classe static parce qu'on ne veut absolument pas instancier des solvers T-T
    @staticmethod
    def solveGrille(grille : Grille) -> bool:
        pass

    
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
                grille.setCelluleValueIndex(cell, resList[0])
                return True
            resList = SolverHuman._singletonCacheRow(grille, cell) #vérifie si on trouve une valeur adéquate à partir de la ligne
            if resList==1:
                grille.setCelluleValueIndex(cell, resList[0])
                return True
            resList = SolverHuman._singletonCacheColumn(grille, cell) #vérifie si on trouve une valeur adéquate à partir de la colonne
            if resList==1:
                grille.setCelluleValueIndex(cell, resList[0])
                return True
        return False            #renvoie faux car on a pas trouvé de valeur adéquate