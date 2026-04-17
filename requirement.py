def verifyRequire(test : bool = True):
    notInstall = []
    # Vérification de matplotlib
    try:
        import matplotlib
    except:
        notInstall.append("matplotlib")
    # Vérification de random
    try:
        import random
    except:
        notInstall.append("random")
    # Vérification de shutil
    try:
        import shutil
    except:
        notInstall.append("shutil")
    # Vérification de selenium
    try:
        import selenium
    except:
        notInstall.append("selenium")
    # Vérification de webdriver_manager
    try:
        import webdriver_manager
    except:
        notInstall.append("webdriver_manager")
    # Vérification de flask
    try:
        import flask
    except:
        notInstall.append("flask")
    # Vérification de flask_socketio
    try:
        import flask_socketio
    except:
        notInstall.append("flask_socketio")
    
    if test:
        # Vérification de pytest
        try:
            import pytest
        except:
            notInstall.append("pytest")
    for e in notInstall:
        print("Le module :",e,"n'est pas installer !!")
        print("Essaie d'installation automatique")
    if len(notInstall)>0 :
        
        raise(Exception("Dépendance manquantes !"))

verifyRequire(True)
print("Toutes les dépendances sont installées :)")