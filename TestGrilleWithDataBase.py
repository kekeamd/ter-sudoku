from GrilleWithDataBase import GrilleWithDataBase as GrilleData
from Except.GrilleError import GrilleError
import pytest
from Parser import Parser

@pytest.fixture
def StrBase():
    StrComplete : str= ""
    StrComplete+="000000000\n"
    StrComplete+="000000000\n"
    StrComplete+="000000000\n"
    StrComplete+="000000000\n"
    StrComplete+="000000000\n"
    StrComplete+="000000000\n"
    StrComplete+="000000000\n"
    StrComplete+="000000000\n"
    StrComplete+="000000000"
    return StrComplete

@pytest.fixture
def GrilleBase(StrBase) -> GrilleData:
    return Parser.stringToGrille(StrBase,1)

@pytest.fixture
def TabBase(StrBase) -> GrilleData:
    return Parser.stringToTab(StrBase)

# Test que la création de l'objet ne pose pas de soucis
def test_init():
    G = GrilleData()
    assert G.getSize()==3

# Test la fonction Rotate (Rota D 1,2,3)
def test_rotateD(GrilleBase : GrilleData):
    Gr1Att = GrilleBase.clone()
    Gr2Att = GrilleBase.clone()
    Gr3Att = GrilleBase.clone()
    for i in range (3):
        Gr1Att.setCelluleValueCoord(1,i+6,3-i)
        Gr2Att.setCelluleValueCoord(i+6,7,3-i)
        Gr3Att.setCelluleValueCoord(7,i,i+1)
        GrilleBase.setCelluleValueCoord(i,1,i+1)
    print("Gr1")
    Gr1 = GrilleBase.clone()
    Gr1.rotate('D',1)
    print("Gr2")
    Gr2 = GrilleBase.clone()
    Gr2.rotate('D',2)
    print("Gr3")
    Gr3 = GrilleBase.clone()
    Gr3.rotate('D',3)
    print("Grille de base :")
    GrilleBase.printGrille()
    print("Grille avec 1 rotation :")
    print("Attendu :")
    Gr1Att.printGrille()
    print("Résulat :")
    Gr1.printGrille()
    print("Grille avec 2 rotation :")
    print("Attendu :")
    Gr2Att.printGrille()
    print("Résulat :")
    Gr2.printGrille()
    print("Grille avec 3 rotation :")
    print("Attendu :")
    Gr3Att.printGrille()
    print("Résulat :")
    Gr3.printGrille()
    assert Parser.grilleToTab(Gr1Att)==Parser.grilleToTab(Gr1)
    assert Parser.grilleToTab(Gr2Att)==Parser.grilleToTab(Gr2)
    assert Parser.grilleToTab(Gr3Att)==Parser.grilleToTab(Gr3)

# Test la fonction Rotate (Rota G 1,2,3)
def test_rotateG(GrilleBase : GrilleData):
    Gr1Att = GrilleBase.clone()
    Gr2Att = GrilleBase.clone()
    Gr3Att = GrilleBase.clone()
    for i in range (3):
        Gr1Att.setCelluleValueCoord(7,i,i+1)
        Gr2Att.setCelluleValueCoord(i+6,7,3-i)
        Gr3Att.setCelluleValueCoord(1,i+6,3-i)
        GrilleBase.setCelluleValueCoord(i,1,i+1)
    print("Gr1")
    Gr1 = GrilleBase.clone()
    Gr1.rotate('G',1)
    print("Gr2")
    Gr2 = GrilleBase.clone()
    Gr2.rotate('G',2)
    print("Gr3")
    Gr3 = GrilleBase.clone()
    Gr3.rotate('G',3)
    print("Grille de base :")
    GrilleBase.printGrille()
    print("Grille avec 1 rotation :")
    print("Attendu :")
    Gr1Att.printGrille()
    print("Résulat :")
    Gr1.printGrille()
    print("Grille avec 2 rotation :")
    print("Attendu :")
    Gr2Att.printGrille()
    print("Résulat :")
    Gr2.printGrille()
    print("Grille avec 3 rotation :")
    print("Attendu :")
    Gr3Att.printGrille()
    print("Résulat :")
    Gr3.printGrille()
    assert Parser.grilleToTab(Gr1Att)==Parser.grilleToTab(Gr1)
    assert Parser.grilleToTab(Gr2Att)==Parser.grilleToTab(Gr2)
    assert Parser.grilleToTab(Gr3Att)==Parser.grilleToTab(Gr3)

# Test flip classic (verticale, horizontale)
def test_flipC(GrilleBase : GrilleData):
    GflipVertAtt = GrilleBase.clone()
    GflipHorizonAtt = GrilleBase.clone()
    GflipVert = GrilleBase.clone()
    GflipHorizon = GrilleBase.clone()
    for i in range (3):
        GflipVertAtt.setCelluleValueCoord(i*3,8,1)
        GflipVertAtt.setCelluleValueCoord(i*3+1,7,2)
        GflipVertAtt.setCelluleValueCoord(i*3+2,5,3)
        GflipVert.setCelluleValueCoord(i*3,0,1)
        GflipVert.setCelluleValueCoord(i*3+1,1,2)
        GflipVert.setCelluleValueCoord(i*3+2,3,3)
        GflipHorizonAtt.setCelluleValueCoord(8,i*3,1)
        GflipHorizonAtt.setCelluleValueCoord(7,i*3+1,2)
        GflipHorizonAtt.setCelluleValueCoord(5,i*3+2,3)
        GflipHorizon.setCelluleValueCoord(0,i*3,1)
        GflipHorizon.setCelluleValueCoord(1,i*3+1,2)
        GflipHorizon.setCelluleValueCoord(3,i*3+2,3)
    print("GrilleVerit :")
    print("Base :")
    GVertSave = GflipVert.clone()
    GflipVert.printGrille()
    GflipVert.flip(0)
    print("Attendu :")
    GflipVertAtt.printGrille()
    print("Résultat :")
    GflipVert.printGrille()
    assert Parser.grilleToTab(GflipVert)==Parser.grilleToTab(GflipVertAtt)
    GflipVert.flip(0)
    print("Double flip :")
    GflipVert.printGrille()
    assert Parser.grilleToTab(GVertSave)==Parser.grilleToTab(GflipVert)
    print("=================")
    print("Base :")
    GHorizonSave = GflipHorizon.clone()
    GflipHorizon.printGrille()
    GflipHorizon.flip(1)
    print("Attendu :")
    GflipHorizonAtt.printGrille()
    print("Résultat :")
    GflipHorizon.printGrille()
    assert Parser.grilleToTab(GflipHorizon)==Parser.grilleToTab(GflipHorizonAtt)
    GflipHorizon.flip(1)
    print("Double flip :")
    GflipHorizon.printGrille()
    assert Parser.grilleToTab(GHorizonSave)==Parser.grilleToTab(GflipHorizon)


# Test flip Advanced (diagonales)
def test_flipAdv():
    pass

# Grille de comparaison pour les tests de change number
# Nombre changer : 5/9
@pytest.fixture
def GForChangeNum() -> list[GrilleData]:
    G1s : str= ""
    G1s+="615379824\n"
    G1s+="729814365\n"
    G1s+="348652971\n"
    G1s+="576123489\n"
    G1s+="491785632\n"
    G1s+="832496157\n"
    G1s+="164237598\n"
    G1s+="253948716\n"
    G1s+="987561243"
    G2s : str= ""
    G2s+="619375824\n"
    G2s+="725814369\n"
    G2s+="348692571\n"
    G2s+="976123485\n"
    G2s+="451789632\n"
    G2s+="832456197\n"
    G2s+="164237958\n"
    G2s+="293548716\n"
    G2s+="587961243"
    return [Parser.stringToGrille(G1s,1),Parser.stringToGrille(G2s,1)]

# Test l'utilisation de change number avec les deux arguments rempli et sans problème
def test_changeNumberValid(GForChangeNum : list[GrilleData]):
    mG1=GForChangeNum[0]
    mG2=GForChangeNum[1]
    print("=========================")
    print("Grille 1 :")
    mG1.printGrille()
    print("=========================")
    print("Grille 2 :")
    mG2.printGrille()
    mG1C = mG1.clone()
    mG1.changeNumber(9,5)
    mG1C.changeNumber(5,9)
    assert (Parser.grilleToTab(mG1))==Parser.grilleToTab(mG2)
    assert (Parser.grilleToTab(mG1C))==Parser.grilleToTab(mG2)

# Test l'utilisation de change number avec une valeur trop grande
def test_changeNumberError(GForChangeNum : list[GrilleData]):
    with pytest.raises(GrilleError):
        GForChangeNum[0].changeNumber(10,5)