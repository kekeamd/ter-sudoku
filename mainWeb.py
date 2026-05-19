from flask import Flask, render_template, request, redirect #Importation de la blibliothèque Flask.
from flask_socketio import SocketIO, emit #Importation de la blibliothèque Flask_socketio.
from Difficulte import *
from BanqueGrilles import BanqueGrilles
from Grille import Grille
from SolverHuman import SolverHuman
from SudokuScraping import getDifficultyFromGrille
from Parser import Parser
from Technique import Technique


def removeAllCandidates(G : Grille):
    for i in range(81):
        for j in G.getCelluleCandidatesIndex(i):
            G.removeCandidateIndex(i,j)

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
grilleType : Grille = None
solutionType : Grille = None
grilleData = {'grille' : grilleType, 'solution' : solutionType}

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
    grilleData['grille'] = grilleDeJeu
    grilleData['solution'] = grilleComplete
    grilleStats= parseStats(stats)
    HumanRated= rated.name

    removeAllCandidates(grilleData['grille'])
    emit('play', {'grille': grille, 'solution': solution, 'taille': grilleDeJeu.getSize(), 'stats': grilleStats, 'difficulteEstimee': [HumanRated, sudokuCoachRated]})
    return

@socketio.on('add')
def handle_add(data): #placeholder pour tester si ça fonctionne
    value = data['value']   # Valeur de l'élément à placer
    pos = data['pos']       # Position de l'élément à Placer
    strict = None           # Set Inital à None, car INUTILE lors des candidats
    if data['type'] == "value":
        strict = data['strict'] # Paramètre selon lequel on accepte des données non correctes
    # done                 # J'ai pu effectuer le changement
    # correct               # Le coup est juste
    toSend = {'done' : True, 'correct' : False, 'entryData' : data}
    if data['type']=="value":                                       # On set ici une valeur dans une case
        if grilleData['grille'].getCelluleValueIndex(pos) == value:
            print("ETRANGE : On me demande d'ajouter quelque chose déjà là... (Value)")
            toSend['done'] = False
        else:
            try:
                if grilleData['solution'].getCelluleValueIndex(pos) == value:
                    toSend['correct'] = True
                if strict:
                    if toSend['correct']:
                        grilleData['grille'].setCelluleValueIndex(pos,value)
                    else:
                        toSend['done'] = False
                else:
                    grilleData['grille'].setCelluleValueIndex(pos,value)
            except e as e:
                print(f"Value not set : \n{e}")
                toSend['done'] = False
        emit('info', {'data': "Demande d'ajout de la valeur "+str(value)+" dans la cellule "+str(pos)})
    # INFO : Pour les candidats, STRICT et CORRECT sont DES DATAS INUTILES
    elif data['type']=="candidate":                              # On set ici un candidat
        toSend['correct'] = True                                 # Correct Vrai dans tout les cas, car INUTILE
        if value in grilleData['grille'].getCelluleCandidatesIndex(pos):
            print("ETRANGE : On me demande d'ajouter quelque chose déjà là... (Candidats)")
            toSend['done'] = False
        else:
            try:
                grilleData['grille'].addCelluleCandidatesIndex(pos,[value])
            except e as e:
                print(f"Candidate not added : \n{e}")
                toSend['done'] = False
        emit('info', {'data': "Demande d'ajout du candidat "+str(value)+" dans la cellule "+str(pos)})
    else:
        emit('info', {'data': "Erreur: Tentative d'ajouter autre-chose qu'une valeur on un candidat à une cellule!"})
    print("\n==========")
    print("DEBUG : ")
    print(f"Value : {grilleData['grille'].getCelluleValueIndex(pos)}\n && -> {value} | {pos}")
    print(f"Candidates : {grilleData['grille'].getCelluleCandidatesIndex(pos)}\n && -> {value} | {pos}")
    print(f"Datas send : {toSend}")
    grilleData['grille'].printGrille()
    grilleData['grille'].printCandidatesOfGrille()
    print("==========\n")
    emit('add',toSend)   # Envoie des datas au client