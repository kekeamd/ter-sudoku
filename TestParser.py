from Parser import Parser
from Except.ParserError import ParserError
from FileInteraction import FileInteraction
import pytest
import os
import shutil



global StrComplete
global fdTest

def test_start():
    os.mkdir("./ForTests/")
    fdTest = FileInteraction("ForTests","Complete")
    StrComplete = ""
    StrComplete+="619375824\n"
    StrComplete+="725814369\n"
    StrComplete+="348692571\n"
    StrComplete+="976123485\n"
    StrComplete+="451789632\n"
    StrComplete+="832456197\n"
    StrComplete+="164237958\n"
    StrComplete+="293548716\n"
    StrComplete+="587961243"

def test_verifString():
    assert StrComplete == "619375824\n725814369\n348692571\n976123485\n451789632\n832456197\n164237958\n293548716\n587961243"

# test grilleToFile
def test_grilleToFile():
    myP = Parser()
    

# test fileToGrille
def test_fileToGrille():
    myP = Parser()
    myP.getFileDescriptor()

# test tabToGrille
def test_tabToGrille():
    pass # test Impossible pour le moment (setCelluleValueIndex)

# test grilleToTab
def test_grilleToTab():
    pass # test Impossible pour le moment (setCelluleValueIndex)

# test fileToTab
def test_fileToTab():
    TabWanted = [[] for _ in range (9)]
    i=0
    for c in "619375824":
        TabWanted[i].append(ord(c))
    i+=1
    for c in "725814369":
        TabWanted[i].append(ord(c))
    i+=1
    for c in "348692571":
        TabWanted[i].append(ord(c))
    i+=1
    for c in "976123485":
        TabWanted[i].append(ord(c))
    i+=1
    for c in "451789632":
        TabWanted[i].append(ord(c))
    i+=1
    for c in "832456197":
        TabWanted[i].append(ord(c))
    i+=1
    for c in "164237958":
        TabWanted[i].append(ord(c))
    i+=1
    for c in "293548716":
        TabWanted[i].append(ord(c))
    i+=1
    for c in "587961243":
        TabWanted[i].append(ord(c))
    i+=1
    fdTest.write(StrComplete)
    p=Parser(fdTest)
    assert p.fileToTab()==TabWanted

# test stringToGrille
def test_stringToGrille():
    pass # test Impossible pour le moment (setCelluleValueIndex)

# test grilleToString
def test_grilleToString():
    pass # test Impossible pour le moment (setCelluleValueIndex)

# test stringToTab
def stringToTab():
    pass

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

def test_stop():
    if os.path.exists("./ForTests/"):
        shutil.rmtree("./ForTests/")