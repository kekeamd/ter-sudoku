import Interface
import InterfaceConsole
import InterfaceWeb
import os
from mainWeb_tmp import main as WebMain
from requirement import verifyRequire

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    clear()
    verifyRequire()
    while True:
        print("==============================")
        print("=========== Sudoku ===========")
        print("1 : Jeu dans la console")
        print("2 : Serveur web")
        print("3 : Tests haut niveau")
        print("4 : Sortir")
        print("==============================")
        
        try:
            TypeDeJeu = input("Faites votre choix : ")
        except ValueError:
            clear()
            continue
        clear()

        if TypeDeJeu == '1':                                          # Jeu dans la console
            print("======================================")
            print("========== Bienvenue dans : ==========")
            print("====== Sudoku Interface Console ======")
            print("======================================")
            
            interface : Interface = InterfaceConsole.InterfaceConsole()
            interface.startPlaying()

        elif TypeDeJeu == '2':                                        # Jeu sur serveur Web
            print("==============================")
            print("====== Bienvenue dans : ======")
            print("==== Sudoku : Serveur Web ====")
            print("==============================")

            interface : Interface = InterfaceWeb.InterfaceWeb()
            answer : str = input("Voulez-vous lancer le serveur ? (O/N) ").upper() # pour o et O, n et N
            if answer == 'O':
                print("Lancement du serveur Web...")
                WebMain()
            else:
                print("Serveur non lancé.")
            
            print("Mode serveur activé !")
            print("CTRL + C pour sortir")
            while(True):
                pass
        
        elif TypeDeJeu == '3':                                        # Tests Haut niveaux
            print("==============================")
            print("====== Bienvenue dans : ======")
            print("====== Test haut niveau ======")
            print("==============================")
            print("/!\\ PAS ENCORE IMPLEMENTER /!\\")
            input("Voulez-vous continuer ? ")

        else:                                                       # Tout autre entrée en quitte !
            break
        clear()

    # Fermeture
    print("==============================")
    print("=== Fermeture du Programme ===")
    print("==============================")

