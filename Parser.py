from FileInteraction import FileInteraction
from Grille import Grille
from Except.ParserError import ParserError
import GrilleWithDataBase as GDataBase
import GrilleBacktrack as GBacktrack
import GrilleHuman as GHuman

class Parser:
    
    def __init__(self, fileDescriptor : FileInteraction = FileInteraction()):
        self._fileInteraction=fileDescriptor
    
    #@classmethod
    def grilleToFile(self,g : Grille, directory : str = "", fileName : str = "") -> None:
        self._modifFileInteraction(directory,fileName,"grilleToFile")
        strG = ""
        for i in range ((g.getSize())**4):
            if i%(g.getSize()**2)==0 and i!=0:
                strG = strG + "\n"
            strG = strG + str(g.getCelluleValueIndex(i))
        self._fileInteraction.write(strG)
    
    # Permet de passer d'un fichier à une Grille de type Grille
    # Le type exact est défini par "typeGrille" :
    # 0 = GBacktrack
    # 1 = GWithData
    # 2 = GHuman
    #@classmethod
    def fileToGrille(self,directory : str = "", fileName : str = "", typeGrille : int = 0) -> Grille:
        self._modifFileInteraction(directory,fileName,"fileToGrille") # Modification de FileInteraction
        Gstr : str = self._fileInputFormat(self._fileInteraction.read()) # Formattage de l'entrée
        Gout : Grille = self._chooseTypeGrille(typeGrille,"fileToGrille") # Set du type de Grille
        i=0
        for s in Gstr:
            for c in s:
                Gout.setCelluleValueIndex(i,int(c))
                i+=1
        return Gout # Retourne une grille
    
    # Transforme un tableau en 2D en une Grille
    # Le type exact est défini par "typeGrille" :
    # 0 = GBacktrack
    # 1 = GWithData
    # 2 = GHuman
    @staticmethod
    def tabToGrille(tab : list[list[int]],typeGrille : int = 0): # -> Grille
        Gout : Grille = Parser._chooseTypeGrille(typeGrille,"tabToGrille")
        i=0
        for Stab in tab:
            for e in Stab:
                Gout.setCelluleValueIndex(i,e)
                i+=1
        return Gout
    
    # Transforme une Grille en tableau en 2D
    @staticmethod
    def grilleToTab(g : Grille) -> list[list[int]]:
        out = [[]]
        j = 0
        for i in range (g.getSize()**4):
            if i!=0 and i%(g.getSize()**2)==0:
                out.append([])
                j+=1
            out[j].append(g.getCelluleValueIndex(i))
        return out
    
    # Prends un fichier et le renvoie sous forme de tableau en 2D
    #@classmethod
    def fileToTab(self,directory : str = "", fileName : str = "") -> list[list[int]]:
        self._modifFileInteraction(directory,fileName,"fileToTab")
        out = []
        i=0
        for s in self._fileInputFormat(self._fileInteraction.read()):
            out.append([])
            for c in s:
                out[i].append(int(c))
            i+=1
        return out
    
    # Prends une chaine de char et la transforme en Grille
    # Ne prends pas en charge les candidats
    # typeGrille :
    # - 0 = GBacktrack
    # - 1 = GDataBase
    # - 2 = GHuman
    @staticmethod
    def stringToGrille(strG : str, typeGrille : int = 0): # -> Grille
        chffr = ["0","1","2","3","4","5","6","7","8","9"]
        Gout : Grille = Parser._chooseTypeGrille(typeGrille,"stringToGrille")
        #strG.split(",")
        i=0
        for e in strG:
            for c in e:
                if c in chffr:
                    Gout.setCelluleValueIndex(i,int(c))
                    i+=1
        return Gout # Retourne une grille
    
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
    
    # Transforme une Grille en String
    # AVEC LES CANDIDATS AFFICHIER
    @staticmethod
    def grilleToStringWithCandidates(g : Grille) -> str:
        size = g.getSize()**2
        numberOfCellule = size**2
        s = "[ "
        for i in range(numberOfCellule):
            s += g.getCelluleValueIndex(i)              # On mets la valeur de la cellule
            s += str(g.getCelluleCandidatesIndex(i))    # Suivi de ses candidats
            if (i!=size-1):
                s+= ", "
        s += " ]"
        return s # On retroune la Grille sous forme de String
    
    # Transforme une Grille en String
    # SANS LES CANDIDATS
    # g : La grille
    # Type : 
    # - 0 -> Une seule ligne avec toutes les lignes à la suite
    # - 1 -> Chaque ligne séparé par un \n
    # Output : String
    @staticmethod
    def grilleToStringWithoutCandidates(g: Grille, type : int = 0) -> str:
        size = g.getSize() ** 2
        numberOfCellule = size ** 2
        s = ""
        for i in range(numberOfCellule):
            s += str(g.getCelluleValueIndex(i))  # On mets la valeur de la cellule
            if (i+1)%size==0 and type==1 and i!=0 and i<(numberOfCellule-1):            # Cas où on veut des \n
                s += "\n"
        return s # On retroune la Grille sous forme de String
    
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
        return self._fileInteraction
    
    def setFileDescriptor(self,fileDescriptor : FileInteraction) -> None:
        self._fileInteraction=fileDescriptor
    
    # Fonction qui permet de formater un fichier en entrée
    # fileContent est le contenue d'un fichier lu (tab of str)
    # nombreAuth défini le tableau des nombres accepté
    # size défini la taille de notre tableau de sortie (size*size)
    # AutoComplet dit si jamais on veut compléter les cases vides avec des nombres trouver en dehors des bornes ou pas
    @staticmethod
    def _fileInputFormat(fileContent : list[str], nombreAuth : list[chr] = ['0','1','2','3','4','5','6','7','8','9'], size : int = 9, AutoComplet : bool = True) -> list[str]:
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
    
    # Fonction permettante de faire la modification sur l'attribut FileInteraction en sécurité
    def _modifFileInteraction(self, directory : str = "", fileName : str = "", who_ : str = ""):
        if who_=="":
            who="modifFileInteraction"
        else:
            who=who_
        if directory != "": # Utilisation du dossier de fileDescriptor
            try:
                self._fileInteraction.setDirectory(directory)
            except:
                Error="Parser : "+who+" -> Erreur lors de la modification du nom du directory !"
                raise(ParserError(Error))
        elif fileName != "": # Utilisation du fichier de fileDescriptor
            try:
                self._fileInteraction.setFile(fileName)
            except:
                Error="Parser : "+who+" -> Erreur lors de la modification du nom du fichier !"
                raise(ParserError(Error))
    
    # Fonction permettante de choisir un type de grille dépendant des paramètres en entrée
    @staticmethod
    def _chooseTypeGrille(type : int, who_ : str = "") -> Grille:
        if who_=="":
            who="chooseTypeGrille"
        else:
            who = who_
        match type:
            case 0:
                Gout = GBacktrack.GrilleBacktrack()
            case 1:
                Gout = GDataBase.GrilleWithDataBase()
            case 2:
                Gout = GHuman.GrilleHuman()
            case _:
                Error = who+" -> Paramètre typeGrille mal entré : "+str(type)
                raise(ParserError("Parser : "+Error))
        return Gout