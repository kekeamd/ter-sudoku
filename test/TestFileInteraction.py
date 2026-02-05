from FileInteraction import FileInteraction
from ParserError import ParserError
import os
import shutil
import pytest

# ICI seront réaliser les tests de la classe "FileInteraction"

def test_SetNamesWithoutParams():
    myInteraction=FileInteraction()
    assert myInteraction.getDirectory()=="./sudoku_parser_out/"
    assert myInteraction.getFile()=="file_out.txt"

def test_SetNamesDirectoryError():
    with pytest.raises(ParserError):
        myInteraction=FileInteraction("./_DoNotExists_")

def test_SetNames():
    myDir="./ForTests/"
    fileName = "MyFile.txt"
    os.makedirs(myDir)
    myInter = FileInteraction(myDir,fileName)
    assert myInter.getDirectory() == myDir
    assert myInter.getFile() == fileName
    os.removedirs(myDir)

def test_SetNamesBis():
    myDir = "./ForTests"
    fileName = "MyFile"
    os.makedirs(myDir)
    myInter = FileInteraction(myDir,fileName)
    assert myInter.getDirectory() == "./ForTests/"
    assert myInter.getFile() == "MyFile.txt"
    os.removedirs(myDir)

def test_WriteAndRead():
    myDir = "./ForTests/"
    fileName = "MyFile.txt"
    content="GoFaireDesTests :)"
    os.makedirs(myDir)
    myInter = FileInteraction(myDir,fileName)
    myInter.write(content)
    contentRead = myInter.read()
    assert len(contentRead) == 1
    assert contentRead[0] == content
    shutil.rmtree(myDir) 

def test_clearDir():
    myDir = "./ForTests/"
    fileName = "MyFile.txt"
    os.makedirs(myDir)
    myInter = FileInteraction(myDir,fileName)
    myInter.write("")
    assert os.path.exists(myDir+fileName) == True
    myInter.clearDirectory()
    assert os.path.exists(myDir+fileName) == False
    shutil.rmtree(myDir)

def test_clear():
    if os.path.exists("./ForTests/"):
        shutil.rmtree("./ForTests/")
    assert True