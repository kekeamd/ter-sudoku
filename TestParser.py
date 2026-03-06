from Parser import Parser
from Except.ParserError import ParserError
from FileInteraction import FileInteraction
import pytest
import os
import shutil
from GrilleBacktrack import GrilleBacktrack


global StrComplete

def test_start():
    os.mkdir("./ForTests/")

@pytest.fixture
def fdTest() -> FileInteraction:
    return FileInteraction("ForTests","Complete")

@pytest.fixture
def strComplete() -> str:
    StrComplete : str= ""
    StrComplete+="619375824\n"
    StrComplete+="725814369\n"
    StrComplete+="348692571\n"
    StrComplete+="976123485\n"
    StrComplete+="451789632\n"
    StrComplete+="832456197\n"
    StrComplete+="164237958\n"
    StrComplete+="293548716\n"
    StrComplete+="587961243"
    return StrComplete

@pytest.fixture
def tabWanted() -> list[list[int]]:
    TabWanted = [[] for _ in range (9)]
    i=0
    for c in "619375824":
        TabWanted[i].append(int(c))
    i+=1
    for c in "725814369":
        TabWanted[i].append(int(c))
    i+=1
    for c in "348692571":
        TabWanted[i].append(int(c))
    i+=1
    for c in "976123485":
        TabWanted[i].append(int(c))
    i+=1
    for c in "451789632":
        TabWanted[i].append(int(c))
    i+=1
    for c in "832456197":
        TabWanted[i].append(int(c))
    i+=1
    for c in "164237958":
        TabWanted[i].append(int(c))
    i+=1
    for c in "293548716":
        TabWanted[i].append(int(c))
    i+=1
    for c in "587961243":
        TabWanted[i].append(int(c))
    i+=1
    return TabWanted

def test_verifString(strComplete : str):
    assert strComplete == "619375824\n725814369\n348692571\n976123485\n451789632\n832456197\n164237958\n293548716\n587961243"

# test grilleToFile
def test_grilleToFile(strComplete : str,tabWanted : list[list[int]],fdTest : FileInteraction):
    fdTest.write(strComplete)
    i=0
    GWanted = GrilleBacktrack()
    for l in tabWanted:
        for c in l:
            GWanted.setCelluleValueIndex(i,c)
            i+=1
    p = Parser(FileInteraction("ForTests","GrilleToFile"))
    p.grilleToFile(GWanted)
    assert fdTest.read()==p.getFileDescriptor().read()

# test fileToGrille
def test_fileToGrille(strComplete : str, fdTest : FileInteraction,tabWanted : list[list[int]]):
    fdTest.write(strComplete)
    Tfin=[]
    TToComp=[]
    p = Parser(fdTest)
    g = p.fileToGrille()
    i=0
    for l in tabWanted:
        for c in l:
            Tfin.append(c)
            TToComp.append(g.getCelluleValueIndex(i))
            i+=1
    assert TToComp==Tfin


# test tabToGrille
def test_tabToGrille(tabWanted : list[list[int]]):
    GWanted = GrilleBacktrack()
    i=0
    for l in tabWanted:
        for c in l:
            GWanted.setCelluleValueIndex(i,c)
            i+=1
    g=Parser.tabToGrille(tabWanted)
    Twant=[]
    Tout=[]
    for i in range(GWanted.getSize()**4):
        Twant.append(GWanted.getCelluleValueIndex(i))
        Tout.append(g.getCelluleValueIndex(i))
    assert Twant==Tout

# test grilleToTab
def test_grilleToTab(tabWanted : list[list[int]]):
    g = GrilleBacktrack()
    i=0
    for l in tabWanted:
        for c in l:
            g.setCelluleValueIndex(i,c)
            i+=1
    assert tabWanted==Parser.grilleToTab(g)

# test fileToTab
def test_fileToTab(strComplete,fdTest,tabWanted : list[list[int]]):
    fdTest.write(strComplete)
    assert os.path.exists("./ForTests/Complete.txt")
    p=Parser(fdTest)
    assert p.fileToTab()==tabWanted

# test stringToGrille
def test_stringToGrille(strComplete,tabWanted):
    G = Parser.stringToGrille(strComplete,0)
    tabW=[]
    for l in tabWanted:
        for e in l:
            tabW.append(e)
    tab=[]
    for i in range(81):
        tab.append(G.getCelluleValueIndex(i))
    assert tabW==tab

# test grilleToString
def test_grilleToString():
    pass # Possiblité de changement de retour de la fonction testé donc pas de tests

# test stringToTab
def test_stringToTab(strComplete,tabWanted):
    tab=Parser.stringToTab(strComplete)
    print(strComplete)
    assert tabWanted==tab
    strTab=str(tab)
    print(strTab)
    assert tabWanted==Parser.stringToTab(strTab)

# test getFileDescriptor & setFileDescriptor
def test_fileDescriptors():
    fd = FileInteraction()
    fdB = FileInteraction()
    p = Parser(fd)
    assert p.getFileDescriptor().getDirectory() == "./sudoku_parser_out/" # Tests avec le FileDescriptor de base
    p.getFileDescriptor().setDirectory("./ForTests") # Modification du FileDescriptor
    assert p.getFileDescriptor().getDirectory() == "./ForTests/" # test avec le nouveau nom
    p.setFileDescriptor(fdB) # Set du Deuxième fd de base
    assert p.getFileDescriptor().getDirectory() == "./sudoku_parser_out/" # Verification du nom

# test de fileInputFormat avec une entrée bien formaté
def test_fileInputFormatValid(fdTest : FileInteraction, strComplete : str):
    fdTest.write(strComplete)
    formated = strComplete.split('\n')
    assert formated == Parser._fileInputFormat(fdTest.read())
    fdTest.clearDirectory()

# test de fileInputFormat avec une entrée mal formaté
def test_fileInputFormatBadEasy(fdTest : FileInteraction, strComplete : str):
    StrComplete : str= ""
    StrComplete+="619375824725814369348692571976123485\n"
    StrComplete+="\n"
    StrComplete+="\n"
    StrComplete+="\n"
    StrComplete+="451789632\n"
    StrComplete+="832456197\n"
    StrComplete+="164237958\n"
    StrComplete+="293548716\n"
    StrComplete+="587961243"
    fdTest.write(StrComplete)
    formated = strComplete.split('\n')
    assert formated == Parser._fileInputFormat(fdTest.read())
    fdTest.clearDirectory()

def test_fileInputFormatBadLine(fdTest : FileInteraction, strComplete : str):
    StrComplete : str= "619375824725814369348692571976123485451789632832456197164237958293548716587961243\n"
    fdTest.write(StrComplete)
    formated = strComplete.split('\n')
    assert formated == Parser._fileInputFormat(fdTest.read())
    fdTest.clearDirectory()

def test_stop():
    if os.path.exists("./ForTests/"):
        shutil.rmtree("./ForTests/")