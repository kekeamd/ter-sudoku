from SolverBacktrack import SolverBacktrack
from Grille import Grille
from Cellule import Cellule
from Except.GrilleError import GrilleError

# Merci de garder les commentaire ci-dessous, ils pourront être copier coller dans d'autres fichiers tests

# Test de la classe SolverBacktrack
# Lors des tests on considère que les classes n'étant pas celle qu'on teste fonctionne
# Exemple : Je teste Parser et j'utilise FileInteraction dans mes tests, je considère que FileInteraction fonctionne comme il le devrais
# Si des erreurs provienne d'une classe qui n'est pas la nôtre : 
# - First step : Je vérifie que l'erreur ne vient pas de mon utilisation des méthodes 
# -> (Je vais donc regarder les informations des méthodes que j'utilise, commentaire et signature)
# - Second step : Si je n'ai commis aucune erreur, je mets un commentaire pour signaler que le problème vient d'autre part
# et je communique ma situation au gérant de la classe que j'utilise afin de mieux comprendre d'où vient le problème
# NE PAS OUBLIER LE DIAGRAMME 

# les fonctions doivent être nommée de cette manière :
# def test_leNomDeMonTest():
# Si besoin d'exemple consulter d'autres fichiers tests