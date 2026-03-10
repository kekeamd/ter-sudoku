from enum import IntEnum

class Technique(IntEnum): # IntEnum car chaque methodes humaine doit avoir son propre nombre de difficulte
    DERNIER_NOMBRE = 1
    SINGLETON_NU = 2
    SINGLETON_CACHE = 3 # le plus le chiffre est grand, le plus dur est-il le methode
    PAIR_NU = 4
    # PAIR_CACHE ...
    # ...