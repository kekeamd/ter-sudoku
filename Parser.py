from FileInteraction import FileInteraction
from Grille import Grille
from Except.ParserError import ParserError

class Parser:
    
    def __init__(self, fileDescriptor : FileInteraction = FileInteraction()):
        self.__fileInteraction=fileDescriptor
    
    #@classmethod
    def grilleToFile(self,g : Grille, directory : str = "", fileName : str = "") -> None:
        self.__modifFileInteraction(directory,fileName,"grilleToFile")
        strG = ""
        for i in range (g.getSize()*g.getSize):
            if i==g.getSize():
                strG = strG + "\n"
            # strG = strG + g.getCelluleValueIndex(None,i) || -> Utilisation de getCelluleValueIndex Impossible !
        self.__fileInteraction.write(strG)
    
    #@classmethod
    def fileToGrille(self,directory : str = "", fileName : str = ""): # -> Grille
        self.__modifFileInteraction(directory,fileName,"fileToGrille")
        Gstr = self.__fileInputFormat(self.__fileInteraction.read())
        Gout = Grille()
        w=0
        for s in Gstr:
            for c in s:
                # Gout.setCelluleValueIndex(None,i,c) || -> Utilisation de setCelluleValueIndex Impossible !
                i+=1
        return Gout # Retourne une grille
    
    @staticmethod
    def tabToGrille(tab : list[list[int]]): # -> Grille
        outG : Grille = Grille()
        i=0
        for Stab in tab:
            for e in Stab:
                # Grille.setCelluleValueIndex(None,i,e) || -> Utilisation de setCelluleValueIndex Impossible !
                i+=1
        return outG
    
    # Transforme une Grille en tableau en 2D
    @staticmethod
    def grilleToTab(g : Grille) -> list[list[int]]:
        out = []
        j = 0
        for i in range (g.getSize()*g.getSize):
            if g.getSize()==i:
                out.append([])
                j+=1
            # out[j].append(g.getCelluleValueIndex(None,i))  || -> Utilisation de getCelluleValueIndex Impossible !
        return out
    
    # Prends un fichier et le renvoie sous forme de tableau en 2D
    #@classmethod
    def fileToTab(self,directory : str = "", fileName : str = "") -> list[list[int]]:
        self.__modifFileInteraction(directory,fileName,"fileToTab")
        out = []
        i=0
        for s in self.__fileInputFormat(self.__fileInteraction.read()):
            out.append([])
            for c in s:
                out[i].append(int(c))
            i+=1
        return out
    
    # Prends une chaine de char et la transforme en Grille
    # Ne prends pas en charge les candidats
    # NON FONCTIONNEL !
    @staticmethod
    def stringToGrille(strG : str): # -> Grille
        chffr = [0,1,2,3,4,5,6,7,8,9]
        outG : Grille = Grille()
        strG.split(",")
        i=0
        for e in strG:
            for c in e:
                if abs(c) in chffr:
                    # Grille.setCelluleValueIndex(None,i,abs(c)) || -> Utilisation de setCelluleValueIndex Impossible !
                    pass
        return outG # Retourne une grille
    
    """ CELLULE IMPOSSIBLE A OBTENIR DONC PAS DE TOSTRING
    # Probablement remplacer par une manière d'afficher les candidats dans grilleToString
    @staticmethod
    def celluleToString(c) -> str:
        pass
    """
    
    """ ZONE IMPOSSIBLE A OBTENIR DONC PAS DE TOSTRING
    # Probablement supprimé
    @staticmethod
    def zoneToString(z) -> str:
        pass
    """
    
    @staticmethod
    def grilleToString(g) -> str: # ??
        size = g.getSize()**2
        s = "[ "
        for i in range(size):
            s +=g.getValueIndex(i)
            if (i!=size-1):
                s+= ", "
        s += " ]"
        return s
    
    
    # Transforme une chaine de char en tableau en 2D
    # /!\ ATTENTION /!\ char séparateur : "[]" ou "\n"
    @staticmethod
    def stringToTab(strG : str) -> list[list[int]]:
        chffr = ['0','1','2','3','4','5','6','7','8','9']
        out=[]
        i=-1
        saved = []
        j=0
        for c in strG:
            if c == '[' or c == '\n':
                if strG[j+1] != '[':
                    out.append([])
                    i+=1
                    while len(saved)>0:
                        out[i].append(saved.pop(0))
                if i==0 and c == '\n':
                    out.append([])
                    i+=1
            elif c in chffr:
                if i!=-1:
                    out[i].append(int(c))
                else:
                    saved.append(int(c))
            j+=1
        return out
    
    @staticmethod
    def tabToString(tab : list[list[int]]) -> str:
        s="["
        for i in len(tab):
            s = s + "["
            for j in len(i):
                s = s + str(tab[i][j])
                if j < len(i)-1:
                    s = s + ","
            s = s + "]"
        s = s + "]"
        return s
    
    def getFileDescriptor(self) -> FileInteraction:
        return self.__fileInteraction
    
    def setFileDescriptor(self,fileDescriptor : FileInteraction) -> None:
        self.__fileInteraction=fileDescriptor
    
    # Fonction qui permet de formater un fichier en entrée
    # fileContent est le contenue d'un fichier lu (tab of str)
    # nombreAuth défini le tableau des nombres accepté
    # size défini la taille de notre tableau de sortie (size*size)
    # AutoComplet dit si jamais on veut compléter les cases vides avec des nombres trouver en dehors des bornes ou pas
    @staticmethod
    def __fileInputFormat(fileContent : list[str], nombreAuth : list[chr] = ['0','1','2','3','4','5','6','7','8','9'], size : int = 9, AutoComplet : bool = True) -> list[str]:
        out = [] # Tableau de chaine de char (sortie)
        saved = [] # Items qui lors de la première lecture n'ont pas pu être placé
        nbItems = 0 # Nombre d'item qui respecte les conditions
        auth = nombreAuth # Lite d'entier qui défini les conditions
        i=0 # Itérateur qui permet de connaître le numéro de la ligne
        for s in fileContent:
            if i<size:
                out.append("")
            for c in s:
                if c in auth:
                    nbItems+=1
                    if i<size and len(out[i])<size: # On vérifie que l'élément fait partie du tableau de taille size*size
                        out[i]+=c
                    else:
                        saved.append(c)
            i+=1
        i=0
        while(len(out)<size):
            out.append("")
        if saved!=[]: # Si il y a des nombres qu'on a pas pu placer
            for s in out: # On itère sur les listes de out pour finir de les remplir
                while(len(s)<size): # Tant que la liste n'est pas à la taille requise
                    if AutoComplet and len(saved)>0: # Si l'autoComplet est activé et qu'il me reste des éléments à placer
                        s = s + saved.pop(0) # Je place le permier élément de saved
                    else: # Sinon
                        s= s + '0'
                out[i]=s
                i+=1
        return out
    
    def __modifFileInteraction(self, directory : str = "", fileName : str = "", who_ : str = ""):
        if who_=="":
            who="modifFileInteraction"
        else:
            who=who_
        if directory != "": # Utilisation du dossier de fileDescriptor
            try:
                self.__fileInteraction.setDirectory(directory)
            except:
                Error="Parser : "+who+" -> Erreur lors de la modification du nom du directory !"
                raise(ParserError(Error))
        elif fileName != "": # Utilisation du fichier de fileDescriptor
            try:
                self.__fileInteraction.setFile(fileName)
            except:
                Error="Parser : "+who+" -> Erreur lors de la modification du nom du fichier !"
                raise(ParserError(Error))