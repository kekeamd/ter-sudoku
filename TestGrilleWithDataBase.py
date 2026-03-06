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

def test_init():
    G = GrilleData()
    assert G.getSize()==3

