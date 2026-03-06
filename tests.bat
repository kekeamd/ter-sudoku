@echo off

cls
echo Lancement des tests du projet !
python requirement.py
pause

cls
echo test Parser.py
python -m pytest ./TestParser.py -v
pause

cls
echo test FileInteraction.py
python -m pytest ./TestFileInteraction.py -v
pause

cls
echo test Cellule.py
python -m pytest ./TestCellule.py -v
pause

cls
echo test Zone.py
python -m pytest ./TestZone.py -v
pause

cls
echo test Grille.py
python -m pytest ./TestGrille.py -v
pause

cls
echo test SolverBacktrack.py
python -m pytest ./TestSolverBacktrack.py -v
pause

cls
echo test SolverHuman.py
python -m pytest ./TestSolverHuman.py -v
pause

cls
echo test GrilleWithDataBase.py
python -m pytest ./TestGrilleWithDataBase.py -v
pause

cls
echo FIN TESTS
pause
cls


