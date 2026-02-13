@echo off

cls
echo Lancement des tests du projet !
python requirement.py
pause

cls
echo test Parser.py
pytest ./TestParser.py -v
pause

cls
echo test FileInteraction.py
pytest ./TestFileInteraction.py -v
pause

cls
echo test Cellule.py
pytest ./TestCellule.py -v
pause

cls
echo test Zone.py
pytest ./TestZone.py -v
pause

cls
echo test Grille.py
pytest ./TestGrille.py -v
pause

cls
echo test SolverBacktrack.py
pytest ./TestSolverBacktrack.py -v
pause

cls
echo FIN TESTS
pause
cls


