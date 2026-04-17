from Interface import Interface  # import le classe parent (Interface)
from Difficulte import Difficulte

from flask import Flask, render_template, request, redirect # Le framework pour Python
from flask_socketio import SocketIO, send, emit

# L'inteface web va faire les memes trucs comme InterfaceConsole : demande si on joue ou on quit, demande diffuculté,
# generer la grille, permet le user de jouer, verifie erreurs, mais avec l'aide des pages and buttons
# It should manage: home page, difficulty selection, new game creation, display sudoku game, validation/checking,
# restart/quit/new game, win/lose page
class InterfaceWeb(Interface): # extends Interface
    def __init__(self):
        super().__init__()
        self.app = Flask(__name__, static_folder='static', template_folder='web_data')

    # Méthodes obligatoires à définir
    # Commence le serveur Flask
    def startPlaying(self):
        try:
            self.app.run(debug=True)
        except:
            print("Erreur de démarrage serveur !")

    # Devient home page route
    @app.route()
    def askChoice(self) -> str:
        return render_template("./web_data/log.html") # par exemple

    # Devient difficulty page route
    def askDifficulty(self) -> Difficulte:
        pass

    # Devient game page route
    def playSudoku(self):
        pass

    # Méthodes suplémentaires