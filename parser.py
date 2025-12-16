import shutil
import os

class ParserError(Exception):
    print(Exception)

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
