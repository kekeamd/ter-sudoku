from Interface import Interface
from InterfaceConsole import InterfaceConsole
from InterfaceWeb import InterfaceWeb
import os

if __name__ == "__main__":
    print("==============================")
    print("=========== Sudoku ===========")
    print("1 : Jeu dans la console")
    print("2 : Serveur web")
    print("3 : Tests haut niveau")
    print("4 : Sortir")
    print("==============================")
    TypeDeJeu : int = int(input("Faites votre choix : "))            # Choix pour la suite
    os.system('cls' if os.name == 'nt' else 'clear')            # Clear de la console
    if TypeDeJeu == 1:                                          # Jeu dans la console
        print("==============================")
        print("====== Bienvenue dans : ======")
        print("====== Sudoku Interface ======")
        print("==============================")
        interface : Interface = InterfaceConsole()
        interface.startPlaying()
        interface.askChoice()
        interface.askDifficulty()
        interface.gameLoop()
    elif TypeDeJeu == 2:                                        # Jeu sur serveur Web
        print("==============================")
        print("====== Bienvenue dans : ======")
        print("==== Sudoku : Serveur Web ====")
        print("==============================")
        interface : Interface = InterfaceWeb()
        answer : chr = input("Voulez-vous lancer le serveur ? (O/N) ")
        if answer == 'O':
            interface.startPlaying()
    elif TypeDeJeu == 3:                                        # Tests Haut niveaux
        print("==============================")
        print("====== Bienvenue dans : ======")
        print("====== Test haut niveau ======")
        print("==============================")
        print("/!\\ PAS ENCORE IMPLEMENTER /!\\")
        input("Voulez-vous continuer ? ")
    # Fermeture
    os.system('cls' if os.name == 'nt' else 'clear')            # Clear de la console
    print("==============================")
    print("=== Fermeture du Programme ===")
    print("==============================")
    exit(0)