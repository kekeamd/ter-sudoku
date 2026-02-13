from abc import ABC, abstractmethod
from Grille import Grille
from Zone import Zone
from GrilleUtils import indexOfZone

class Solver(ABC): #transformation de la classe en classe static parce qu'on ne veut absolument pas instancier des solvers T-T
    @staticmethod
    @abstractmethod
    def solveGrille(grille : Grille) -> bool:
        pass


    @staticmethod
    def isValid(grille : Grille, row : int, column : int, value : int) -> bool: 
        if grille.columnContainsValue(column, value) or grille.rowContainsValue(row, value):
                    return False
        zone_index = indexOfZone(row, column, grille.getSize())
        zone = grille.getZone(zone_index)
        if zone and zone.containsValue(value):
            return False
        return True
