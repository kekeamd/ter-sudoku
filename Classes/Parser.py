from FileInteraction import FileInteraction

class Parser:
    
    def __init__(self, fileDescriptor : FileInteraction = FileInteraction()):
        self.fileInteraction=fileDescriptor
    
    def grilleToFile(self,g, directory : str = "", fileName : str = "") -> None: # g : Grille
        if directory == "": # Utilisation du dossier de fileDescriptor
            pass
        elif fileName == "": ## Utilisation du fichier de fileDescriptor
            pass
        else: # Utilisation d'emplacement passé en paramètre
            pass
    
    def fileToGrille(self,directory : str = "", fileName : str = ""): # -> Grille
        if directory == "": # Utilisation du dossier de fileDescriptor
            pass
        elif fileName == "": ## Utilisation du fichier de fileDescriptor
            pass
        else: # Utilisation d'emplacement passé en paramètre
            pass
        return None # Retourne une grille
    
    def tabToGrille(tab : list[list[int]]): # -> Grille
        return None ## Retourne une grille
    
    def grilleToTab(g) -> list[list[int]]: # g : Grille
        return None
    
    def fileToTab(self,directory : str = "", fileName : str = "") -> list[list[int]]:
        if directory == "": # Utilisation du dossier de fileDescriptor
            pass
        elif fileName == "": ## Utilisation du fichier de fileDescriptor
            pass
        else: # Utilisation d'emplacement passé en paramètre
            pass
        return None
    
    def stringToGrille(strG : str): # -> Grille
        return None # Retourne une grille
    
    def grilleToString(g) -> str:
        return ""
    
    def stringToTab(strG : str) -> list[list[int]]:
        return None
    
    def tabToString(tab : list[list[int]]) -> str:
        return ""
    
    def getFileDescriptor(self) -> FileInteraction:
        return self.fileDescriptor
    
    def setFileDescriptor(self,fileDescriptor : FileInteraction) -> None:
        self.fileInteraction=fileDescriptor