#renvoie l'index de la première zone dans la ligne numéro 'row'
def indexOfFirstZoneInRow(row : int, l : int) -> int:#row commence à 0    ;   l = nombre de zones par ligne
    return l*(row//l)


#renvoie l'index de la première zone dans la colonne numéro 'col'
def indexOfFirstZoneInColumn(col : int, l : int) -> int:#col commence à 0    ;   l = nombre de zones par colonne
    return (col//l)


#renvoie l'index de la zone dans laquelle est la cellule de coordonnées ('row', 'column')
def zoneIndexFromCoord(row : int, column : int, l : int) -> int: #l = nombre de zones par ligne/colonne
        rowIndex = indexOfFirstZoneInRow(row, l)            #example: pour une grille 9x9, a pour valeur 0, 3, 6
        colIndex = indexOfFirstZoneInColumn(column, l)         #example: pour une grille 9x9, a pour valeur 0, 1, 2
        zoneIndex = rowIndex+colIndex             #example: pour une grille 9x9 avec row=3 et col=4, a pour valeur 3 + 1
        return zoneIndex


#renvoie l'index de la ligne/colonne relative à la zone à partir de l'index absolu de la ligne/colonne
def indexRowOrColumnInZone(rowOrcol : int, l : int) -> int:#rowOrcol commence à 0    ;    l = nombre de lignes/colonnes par zone
    return rowOrcol%l           #renvoie l'index relatif de la ligne ou colonne (par rapport à la zone dans laquel elle est située)


#renvoie l'index de la ligne relative à la zone d'index 'zoneI' à laquelle appartient la cellule d'index relatif 'index'
def indexOfRow(zoneI : int, index : int, l : int) -> int:#row commence à 0    ;   l = nombre de lignes par zone
    globalRowIndex = zoneI//l
    localRowIndex = index//l
    rowIndex = l*globalRowIndex + localRowIndex
    return rowIndex


#renvoie l'index de la colonne relative à la zone d'index 'zoneI' à laquelle appartient la cellule d'index relatif 'index'
def indexOfColumn(zoneI : int, index : int, l : int) -> int:#col commence à 0    ;   l = nombre de colonnes par zone
    globalColumnIndex = zoneI%l
    localColumnIndex = index%l
    columnIndex = l*globalColumnIndex + localColumnIndex
    return columnIndex


#renvoie l'index de la ligne à laquelle appartient la cellule de position 'index' dans la grille
def rowIndexFromCelluleIndex(index : int, l : int) -> int: #index commence à 0
    size = l**2
    return index//size


#renvoie l'index de la colonne à laquelle appartient la cellule de position 'index' dans la grille
def columnIndexFromCelluleIndex(index : int, l : int) -> int: #index commence à 0
    size = l**2
    return index%size


#renvoie la position relative à sa région d'une cellule à partir de la position de la cellule dans la grille
def relatifIndexFromAbsoluteIndex(index : int, l : int, regionType : str= "zone") -> int:#index commence à 0   ; regionType = "zone" pour zone, "row" pour ligne et "column" pour colonne
    rowIndex = rowIndexFromCelluleIndex(index, l)
    colIndex = columnIndexFromCelluleIndex(index, l)
    if regionType == "zone":
        relatifRowIndex = indexRowOrColumnInZone(rowIndex, l)
        relatifColIndex = indexRowOrColumnInZone(colIndex, l)
        return relatifRowIndex * l + relatifColIndex
    if regionType == "row":
        return colIndex
    if regionType == "column":
        return rowIndex


#renvoie la position d'une cellule dans la grille à partir de la position de sa région et de sa position relative à la région
def AbsoluteIndexFromRelatifIndex(regionIndex : int, index : int, l : int, regionType : str= "zone") -> int:#regionIndex et index commencent à 0   ; regionType = "zone" pour zone, "row" pour ligne et "column" pour colonne
    size = l**2
    if regionType == "zone":
        rowIndex = indexOfRow(regionIndex, index, l)
        columnIndex = indexOfColumn(regionIndex, index, l)
        return rowIndex*size+columnIndex
    if regionType == "row":
        return regionIndex*size + index
    if regionType == "column":
        return regionIndex +  index*size


#compare si les cellules d'index 'index1' et 'index2' sont dans la même région
def compareIndexRegion(index1 : int, index2 : int, l : int, regionType : str="zone") -> bool: # regionType = "zone" pour zone, "row" pour ligne et "column" pour colonne
    rowIndex1 = rowIndexFromCelluleIndex(index1, l)
    rowIndex2 = rowIndexFromCelluleIndex(index2, l)
    columnIndex1 = columnIndexFromCelluleIndex(index1, l)
    columnIndex2 = columnIndexFromCelluleIndex(index2, l)
    if regionType=="zone":
        return zoneIndexFromCoord(rowIndex1, columnIndex1, l)==zoneIndexFromCoord(rowIndex2, columnIndex2, l)
    if regionType=="row":
        return rowIndex1==rowIndex2
    if regionType=="column":
        return columnIndex1==columnIndex2


#renvoie 'values' sans 0 à l'intérieur
def valuesWithoutZero(values : list[int]) -> list[int]:
    newValues = []
    for i in range(len(values)):
        val = values[i]
        if (val!=0):
            newValues.append(val)
    return newValues


#renvoie l'union des listes 'list1' et list2'
def listUnion(list1 : list[int], list2: list[int]) -> list[int]:
    newList = list1
    for i in range(len(list2)):
        if (list2[i] not in newList):
            newList.append(list2[i])
    return newList


#renvoie 'list1' sans les éléments de 'list2'
def listDifference(list1 : list[int], list2: list[int]) -> list[int]:
    newList = []
    for i in range(len(list1)):
        if (list1[i] not in list2):
            newList.append(list1[i])
    return newList


#renvoie le nombre de digit dans 'value'
def digitCount(value : int):
    if value==0:    #failsafe si value est déjà égal à 0
        return 1
    digitCount = 0     #digitCount = le nombre de digit de value
    while value!= 0:   #on fait la division entière par 10 jusqu'à avoir 0 et le nombre de division = le nombre de digit de value
        value = value//10
        digitCount+=1
    return digitCount


#renvoie 'value' sous forme de string et parfaitement centré avec 'maxDigitCount' comme référence du nombre maximal de digit de value
def valueToString(value : int, maxDigitCount : int):
    if value==0:
        middle = "."
    else:
        middle = str(value)
    before = ""
    after = ""
    digCount = digitCount(value)
    spaceCount = maxDigitCount - digCount
    if spaceCount%2==0:
        for _ in range(spaceCount//2):
            before+=" "
            after+= " "
    else:
        for _ in range(spaceCount//2):
            before+=" "
            after+=" "
        before+= " "
    return before + middle + after