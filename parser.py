# Note : Architechture à retravailler !!

import shutil
import os
from dependances.parser_requirement import *


# Transforme la grille prise en entrée (grille) en fichier qui aura le nom "file_name"
# localisation du fichier ./sudoku_parser_out
def grille_to_file(grille,file_name):
    size=len(grille)
    for i in range (len(grille)):
        if len(grille[i])!=size:
            raise ParserError("WrongSizeOfCol")
    fName="./sudoku_parser_out/"+file_name+".txt"
    f = open(fName,"w")
    for i in range (size):
        myLine=""
        for j in range (size):
            myLine = myLine+str(grille[i][j])
        f.write(myLine+"\n")
    f.close()
    return fName

def clean():
    if os.path.isdir("./sudoku_parser_out"):
        shutil.rmtree("./sudoku_parser_out")
    os.makedirs("./sudoku_parser_out")


# Fonction Générique de parse
# N'accepte pas les char autre :
# - 0-9
# - \n
def Parse(Tb):
    type=verifTypeInput(Tb)
    out=[]
    if type==1:
        out=parseToRBF(Tb)
    elif type==2 or type==5:
        out=parseLine(Tb)
    elif type==3 or type==4 or type==6:
        out=parseToR(Tb)
    else:
        raise ParserError("Le fichier d'input n'est pas correct !!")
    return out

# Première version du parser file to grille
def file_to_grille(file_name):
    fName=""
    # Verification de l'existance du fichier en admettant le plus de possibilité possible
    # Afin de rendre l'utilisation plus simple
    if os.path.isfile("./sudoku_parser_out/"+file_name+".txt"):
        fName="./sudoku_parser_out/"+file_name+".txt"
    elif os.path.isfile("./sudoku_parser_out/"+file_name):
        fName="./sudoku_parser_out/"+file_name
    elif os.path.isfile(file_name):
        fName=file_name
    elif os.path.isfile("./"+file_name+".txt"):
        fName="./"+file_name+".txt"
    elif os.path.isfile("./"+file_name):
        fName="./"+file_name
    else:
        raise ParserError("Fichier inexistant !!")
    # Ouverture du fichier et récupération du contenu
    File=open(fName)
    f=File.readlines()
    File.close()
    return Parse(f)