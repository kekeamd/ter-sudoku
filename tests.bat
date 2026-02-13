@echo off

cls
echo Lancement des tests du projet !
pip check pytest
pause

cls
echo test Parser.py
pytest ./TestParser.py
pause

cls
echo test FileInteraction.py
pytest ./TestFileInteraction.py
pause

cls
echo test Cellule.py
pytest ./TestCellule.py
pause

cls
echo test Zone.py
pytest ./TestZone.py
pause

cls
echo test Grille.py
pytest ./TestGrille.py
pause

cls
echo FIN TESTS
pause
cls


