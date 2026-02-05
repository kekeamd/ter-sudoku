class FileInteraction:
    def __init__(self,directory : str = "../sudoku_parser_out",file : str = "file_out.txt"):
        self.directory=directory
        self.file=file
    
    def getDirectory(self) -> str :
        return self.directory
    
    def setDirectory(self,directory : str) -> None:
        self.directory = directory
    
    def getFile(self) -> str:
        return self.file
    
    def setFile(self, file : str) -> None:
        self.file = file
    
    def write(self,content : str) -> None:
        pass
    
    def read() -> str:
        return ""
    
    def writeFile(content : str, file : str) -> None:
        pass
    
    def readFile(file : str) -> str:
        return ""
    
    def writeFileDirectory(content : str, file : str, directory : str) -> None:
        pass
    
    def readFileDirectory(file : str, directory : str) -> str:
        return ""