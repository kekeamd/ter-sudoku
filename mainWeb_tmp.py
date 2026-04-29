import InterfaceWeb
import sys
import os

# Fichier qui fait la gestion Serveur, utile uniquement dans le cas d'un jeu SERVEUR
# Lancer à partir de main.py EVITER DE LANCER DIRECTEMENT CE FICHIER
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    print("Je me suis lancé :)")
    print("NON IMPLEMENTER")


### Gestion de lancement du fichier
if __name__=="__main__":
    print("Ne dois pas être lancé !")
    print("-F pour forcer le lancement (DEV UNIQUEMENT)")
    if len(sys.argv) == 1:
        exit() # AUCUN ARGUMENT
    elif (sys.argv[1]=="-F") or (sys.argv[1]=="-f"):
        main()
    else:
        print(f"ARGUMENT MAL SAISI ! {sys.argv[1]}")
        exit()
