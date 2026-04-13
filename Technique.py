from enum import IntEnum

class Technique(IntEnum): # IntEnum car chaque methodes humaine doit avoir son propre nombre de difficulte
    DERNIER_NOMBRE = 1
    SINGLETON_NU = 2
    SINGLETON_CACHE = 3 # plus le chiffre est grand, plus la méthode est dure
    PAIR_NU = 4
    PAIR_CACHEE = 5
    CANDIDAT_ENFERME = 6
    GRATTE_CIEL = 7
    # ...
    # ...