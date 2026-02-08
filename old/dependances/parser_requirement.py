# Fichier contenant des fonctions nécessaire pour le parser

class ParserError(Exception):
    pass

#====================================================================================================
# PARSER PUR
#====================================================================================================

# Fonction qui parse un tableau de la forme : [["123456789"],["123456789"]...] (9x9)
def parseToRBF(T):
    codeVerif = verifTypeInput(T)
    if codeVerif==1:
        out=[]
        for r in range(len(T)):
            out.append([])
            for c in range(len(T[r])):
                if T[r][c]!='\n':
                    out[r].append(int(T[r][c]))
    else:
        raise ParserError("Format invalide !!! Attendu : 9x9 || CODE : "+codeVerif)
    return out

# Fonction qui parse un tableau de la forme : 
# - [["123456789..."]] (1x81)
# - [["1234567..."]] (1xX)
def parseLine(T):
    codeVerif = verifTypeInput(T)
    if codeVerif==2 or codeVerif==5:
        out=[]
        j=-1
        for i in range (81):
            if i%9==0:
                out.append([])
                j+=1
            if len(T[0])>i and T[0][i]!='\n':
                out[j].append(int(T[0][i]))
            else:
                out[j].append(0)
    else:
        raise ParserError("Format invalide !!! Attendu : 1x81 || CODE : "+codeVerif)
    return out
            
# Fonction qui parse un tableau de la forme : 
# - 9xX (tableau de 9 lignes avec des taille de ligne variable)
# - XxY (tableau de x ligne avec des taille de lignes variable)
def parseToR(T):
    codeVerif = verifTypeInput(T)
    if codeVerif==3 or codeVerif==4 or codeVerif==6:
        out=[]
        for i in range (9):
            out.append([])
            for j in range (9):
                if len(T)>i and len(T[i])>j and T[i][j]!='\n':
                    out[i].append(int(T[i][j]))
                else:
                    out[i].append(0)
    else:
        raise ParserError("Format invalide !!! Attendu : XxY ou 9xX ou XxY(avecLigneVide) || CODE : "+codeVerif)
    return out


#====================================================================================================
# FIN PARSER PUR
#====================================================================================================

# Fonction qui vérifie quel est le format de la donnée
# 1 : Bien formé -> 9 lignes avec 9 char (chiffre)
# 2 : Bien formé -> 1 ligne avec 81 char (chiffre)
# 3 : Problème -> 9 ligne avec des nombre de char variable
# 4 : Problème -> Nombre de ligne variable avec nombre de char variable par ligne 
# 5 : Problème -> 1 ligne avec un nombre de char variable
# 6 : Problème -> Nombre de ligne variable avec nombre de char variable par ligne et au moins 1 ligne avec 0 élément
# 0 : ERREUR
def verifTypeInput(T):
    out=0
    # Verification pour une grille bien formé en 9x9
    if len(T)==9:
        out=1
        for i in range (9):
            if len(T[i])!=9:
                out=3
    # Verification pour une grille bien formé en 1x81
    elif len(T)==1:
        if (len(T[0])) == 81:
            out=2
        elif len(T[0])>1:
            out=5
    # Verification que ce n'est pas une grille vide
    elif len(T)>1:
        out=4
        for i in range (len(T)):
            if len(T[i])==0:
                out=6
    # Cas particulier plusieurs lignes détécter mais seulement saut de ligne
    tmp=0
    for i in range (len(T)):
        if i==0:
            tmp=1
        elif not(T[i][0]=='\n'):
            tmp=0
    if tmp==1 and len(T)>0:
        if len(T[0])==81:
            out=1
        else:
            out=5
    # Verification de l'absence de char hors nombre
    for i in range (len(T)):
        for j in range (len(T[i])):
            if not(T[i][j] in ['\n','0','1','2','3','4','5','6','7','8','9']):
                raise ParserError("Char interdit détécté !!!")
    return out