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
    for i in range(G.getSize()**4):
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
baseType : Grille = None #la grille de base
grilleType : Grille = None
solutionType : Grille = None
sessionData = {'pseudo' : "", 'strict' : True, 'error' : 0, 'errorMax' : 5, 'finished' : False}
grilleData = {'base' : baseType, 'grille' : grilleType, 'solution' : solutionType, 'stats' : {}, 'difficulteHuman' : "", 'difficulteCoach' : ""}

@app.route('/')
def play():
    return render_template('index.html')


#Todo/idée: mettre tout ce qui concerne la grille dans InterfaceWeb d'une manière ou d'une autre?
@socketio.on('play')
def handle_play(data):
    difficulte= Difficulte.FACILE
    if data['difficulte']=="moyen":
        difficulte = Difficulte.MOYEN
    if data['difficulte']=="difficile":
        difficulte = Difficulte.DIFFICILE
    if data['difficulte']=="extreme":
        difficulte = Difficulte.EXTREME
    if data['difficulte']=="godmode":
        difficulte = Difficulte.GODMODE
    emit('info', {'data': "Génération d'une grille de difficulté "+str(data['difficulte'])})
    entree = BanqueGrilles.charger_grille_aleatoire(difficulte)
    grilleDeJeu : Grille= entree["grille"]
    grilleComplete : Grille = entree["solution"]
    stats = entree["stats"]
    if stats is None:
        emit('info', {'data': "Erreur: la génération n'a retourné aucune statistique."})
        return
    
    grilleDeJeu.adjustCandidates()  # Initialiser les candidats après génération
    rated = SolverHuman.rateFromStats(stats)
    if rated == Difficulte.GODMODE:
        emit('info', {'data': "Cette grille ne peut pas être résolue uniquement avec les techniques humaines actuellement implémentées dans ce projet (dernier nombre, singleton nu, singleton caché, paire nue, paire cachée, candidat enfermé, gratte-ciel)."})
    grille= Parser.grilleToStringWithoutCandidates(grilleDeJeu)
    solution= Parser.grilleToStringWithoutCandidates(grilleComplete)
    grilleData['base'] = grilleDeJeu.clone()
    grilleData['grille'] = grilleDeJeu
    grilleData['solution'] = grilleComplete
    sessionData['strict'] = data['strict']
    sessionData['error'] = 0
    sessionData['finished'] = False
    if data['strict']:
        sessionData['errorMax']= 5
    else:
        sessionData['errorMax']= -1
    grilleData['stats']= parseStats(stats)
    grilleData['difficulteHuman']= rated.name
    grilleData['difficulteCoach']= "WebScrapping WIP"
    #grilleData['difficulteCoach'] = getDifficultyFromGrille(grilleDeJeu, headless=True)

    removeAllCandidates(grilleData['grille'])
    emit('play', {'grille': grille, 'solution': solution, 'taille': grilleData['base'].getSize(), 'stats': grilleData['stats'], 'difficulteEstimee': [grilleData['difficulteHuman'], grilleData['difficulteCoach']], 'errorMax' : sessionData['errorMax']})
    return

@socketio.on('add')
def handle_add(data):
    finished= False
    value = data['value']   # Valeur de l'élément à placer
    pos = data['pos']       # Position de l'élément à Placer
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
                if sessionData['strict']:
                    if toSend['correct']:
                        grilleData['grille'].setCelluleValueIndex(pos,value)
                        if SolverHuman.isCompleted(grilleData['grille']) and Parser.grilleToStringWithoutCandidates(grilleData['grille'])==Parser.grilleToStringWithoutCandidates(grilleData['solution']):
                            finished= True
                    else:
                        toSend['done'] = False
                        if sessionData['error']>=sessionData['errorMax']:
                            sessionData['finished']= True
                            emit('finish', {'reason' : "lost"})
                        else:
                            sessionData['error'] += 1
                else:
                    grilleData['grille'].setCelluleValueIndex(pos,value)
                    if SolverHuman.isCompleted(grilleData['grille']) and Parser.grilleToStringWithoutCandidates(grilleData['grille'])==Parser.grilleToStringWithoutCandidates(grilleData['solution']):
                            finished= True
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
    print("==========\n")
    emit('add',toSend)   # Envoie des datas au client
    if finished:
        sessionData['finished']= True
        emit('finish', {'reason' : "won"})
    
@socketio.on('remove')
def handle_remove(data):
    # {'pos': pos, 'type': "candidate" or "value", 'value': candidate}
    value : int = None # Set initial car INUTILE en cas de VALEUR
    done = False
    pos = data["pos"]
    print(data)
    if data["type"] == "candidate":     # Si on veut supprimer un candidat on doit savoir qui ? 
        value = data["value"]
    if data["type"] == "candidate":
        grilleData['grille'].removeCandidateIndex(pos,value)
        done = True
    elif data["type"] == "value":
        grilleData['grille'].removeCelluleValueIndex(pos)
        done = True
    if done:
        emit("remove",data)
    else:
        emit('info',{'data' : "Erreur : Suppression d'un élément de type invalide dans une case !"})

@socketio.on('solve')
def handle_solve():
    emit('solve',{'solution': Parser.grilleToStringWithoutCandidates(grilleData['solution'])})
    sessionData['finished']= True
    emit('finish', {'reason': "solved"})

@socketio.on('reload')
def handle_reload():
    if (grilleData['base']!=None):
        base = Parser.grilleToStringWithoutCandidates(grilleData['base'])
        grille = Parser.grilleToStringWithoutCandidates(grilleData['grille'])
        solution = Parser.grilleToStringWithoutCandidates(grilleData['solution']) # initialisation de la grille
        emit('play', {'grille': base, 'solution': solution, 'taille': grilleData['base'].getSize(), 'stats': grilleData['stats'], 'difficulteEstimee': [grilleData['difficulteHuman'], grilleData['difficulteCoach']], 'errorMax' : sessionData['errorMax']})

        for i in range(len(grille)): #ajout des valeurs ajoutées par le joueur
            if base[i]!=grille[i]:
                emit('add', {'done' : True, 'correct' : True, 'entryData' : {'pos': i, 'type': "value", 'value': int(grille[i])}})
        
        emit('pseudo', {'pseudo' : sessionData['pseudo']})
        #envoie des données de session manquantes
        emit('reload', {'error' : sessionData['error'], 'strict' : sessionData['strict'], 'finished' : sessionData['finished']})

@socketio.on('getCandidates')
def handle_getCandidates():
    removeAllCandidates(grilleData['grille'])
    grilleData['grille'].adjustCandidates()
    listOfCands = []
    for i in range(grilleData['grille'].getSize()**4):
        listOfCands.append(grilleData['grille'].getCelluleCandidatesIndex(i))
    emit('getCandidates', {'cands' : listOfCands})

@socketio.on('login')
def handle_login(data):
    sessionData['pseudo'] = data['pseudo']
    emit('pseudo', {'pseudo' : sessionData['pseudo']})

@socketio.on('logout')
def handle_logout():
    sessionData['pseudo'] = ""
    emit('pseudo', {'pseudo' : sessionData['pseudo']})