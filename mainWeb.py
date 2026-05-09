from flask import Flask, render_template, request, redirect #Importation de la blibliothèque Flask.
from flask_socketio import SocketIO, emit #Importation de la blibliothèque Flask_socketio.
from Difficulte import *
from BanqueGrilles import BanqueGrilles
from Grille import Grille
from SolverHuman import SolverHuman
from SudokuScraping import getDifficultyFromGrille
from Parser import Parser
from Technique import Technique

def parseStats(stats: dict) -> dict:
    grilleStats={}
    for k, v in stats.items():
        if k=='counts':
            grilleCounts= {}
            for kbis, vbis in v.items():
                grilleCounts[kbis.name]= vbis
            grilleStats[k]= grilleCounts
        elif k=='maxTechnique':
            grilleStats[k]= v.name
        elif k=='history':
            grilleHistory= []
            for move in v:
                moveDetails= {}
                for kbis, vbis in move.items():
                    if kbis=='technique':
                        moveDetails[kbis]=vbis.name
                    else:
                        moveDetails[kbis]= vbis
                grilleHistory.append(moveDetails)
            grilleStats[k]= grilleHistory
        else:
            grilleStats[k]= v
    return grilleStats


if __name__=="__main__":
    print("Ne dois pas être lancé !")
    exit()

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def play():
    return render_template('index.html')


#Todo/idée: mettre tout ce qui concerne la grille dans InterfaceWeb d'une manière ou d'une autre?
@socketio.on('play')
def handle_play(data):
    difficulte= Difficulte.FACILE
    if data=="moyen":
        difficulte = Difficulte.MOYEN
    if data=="difficile":
        difficulte = Difficulte.DIFFICILE
    if data=="extreme":
        difficulte = Difficulte.EXTREME
    if data=="godmode":
        difficulte = Difficulte.GODMODE
    emit('info', {'data': "Génération d'une grille de difficulté "+str(data)})
    entree = BanqueGrilles.charger_grille_aleatoire(difficulte)
    grilleDeJeu : Grille= entree["grille"]
    grilleComplete : Grille = entree["solution"]
    stats = entree["stats"]
    if stats is None:
        emit('info', {'data': "Erreur: la génération n'a retourné aucune statistique."})
        return
    
    grilleDeJeu.adjustCandidates()  # Initialiser les candidats après génération
    rated = SolverHuman.rateFromStats(stats)
    sudokuCoachRated= "WebScrapping WIP"
    #sudokuCoachRated = getDifficultyFromGrille(grilleDeJeu, headless=True)
    if rated == Difficulte.GODMODE:
        emit('info', {'data': "Cette grille ne peut pas être résolue uniquement avec les techniques humaines actuellement implémentées dans ce projet (dernier nombre, singleton nu, singleton caché, paire nue, paire cachée, candidat enfermé, gratte-ciel)."})
    grille= Parser.grilleToStringWithoutCandidates(grilleDeJeu)
    solution= Parser.grilleToStringWithoutCandidates(grilleComplete)
    grilleStats= parseStats(stats)
    HumanRated= rated.name

    emit('play', {'grille': grille, 'solution': solution, 'taille': grilleDeJeu.getSize(), 'stats': grilleStats, 'difficulteEstimee': [HumanRated, sudokuCoachRated]})
    return

@socketio.on('add')
def handle_add(data): #placeholder pour tester si ça fonctionne
    if data['type']=="value":
        emit('info', {'data': "ajout de la valeur "+str(data['value'])+" dans la cellule "+str(data['pos'])})
    elif data['type']=="candidate":
        emit('info', {'data': "ajout du candidat "+str(data['value'])+" dans la cellule "+str(data['pos'])})
    else:
        emit('info', {'data': "Erreur: Tentative d'ajouter autre-chose qu'une valeur on un candidat à une cellule!"})