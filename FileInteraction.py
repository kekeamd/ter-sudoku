import shutil
import os
from Except.ParserError import ParserError

class FileInteraction:
    def __init__(self,directory : str = "./sudoku_parser_out/",file : str = "file_out.txt"):
        self.directory=""
        self.setDirectory(directory)
        self.file=""
        self.setFile(file)
    
    def getDirectory(self) -> str :
        return self.directory
    
    def setDirectory(self,directory : str) -> None:
        if os.path.isdir(directory):
            if directory[len(directory)-1]=='/' or directory[len(directory)-1]=='\\':
                self.directory=directory
            else:
                self.directory=directory+"/"
        else:
            if directory==directory=="./sudoku_parser_out/":
                os.makedirs(directory)
            else:
                raise(ParserError("FileInteraction : Erreur lors de la création de l'objet -> directory non existant"))
    
    def getFile(self) -> str:
        return self.file
    
    def setFile(self, file : str) -> None:
        if file.endswith(".txt"):
            self.file = file
        else:
            self.file = file+".txt"
    
    # Ecrit de manière brute le contenue passer en paramètre /!\ PAS DE FORMATTAGE /!\
    def write(self,content : str) -> None:
        f=open(self.directory+self.file,"w")
        f.write(content)
        f.flush()
        f.close()
    
    def read(self) -> list[list[str]]:
        f=open(self.directory+self.file,"r")
        content=f.readlines()
        f.close()
        return content
    
    # Ecrit de manière brute le contenue passer en paramètre /!\ PAS DE FORMATTAGE /!\
    def writeFile(self,content : str, file : str) -> None:
        self.setFile(file)
        self.write(content)
    
    def readFile(self,file : str) -> list[list[str]]:
        self.setFile(file)
        if os.path.isfile(self.directory+self.file):
            print("FileInteraction : /!\\ WARNING /!\\ [READ] Fichier non existant")
            return [[""]]
        else:
            return self.read()
    
    # Ecrit de manière brute le contenue passer en paramètre /!\ PAS DE FORMATTAGE /!\
    def writeFileDirectory(self,content : str, file : str, directory : str) -> None:
        self.setFile(file)
        self.setDirectory(directory)
        self.write(content)
    
    def readFileDirectory(self,file : str, directory : str) -> list[list[str]]:
        self.setFile(file)
        self.setDirectory(directory)
        if os.path.isfile(self.directory+self.file):
            print("FileInteraction : /!\\ WARNING /!\\ [READ] Fichier non existant")
            return [[""]]
        else:
            return self.read()
    
    def clearDirectory(self) -> None:
        shutil.rmtree(self.directory)
        os.makedirs(self.directory)