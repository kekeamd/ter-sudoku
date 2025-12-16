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


# Première version du parser file to grille
def file_to_grille(file_name):
    fName=""
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
    File=open(fName)
    f=File.readlines()
    File.close()
    out=[]
    for r in range(len(f)):
        out.append([])
        for c in range(len(f[r])):
            if f[r][c]!='\n':
                out[r].append(int(f[r][c]))
    size=len(out)
    for i in range(len(out)):
        if len(out[i])!=size:
            print("Size :",size,"Current size :",len(out[i]),"Line number :",i+1)
            raise ParserError("DataIncompatible")
    return out