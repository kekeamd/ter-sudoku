def indexOfFirstZoneInRow(row : int, l : int) -> int:#row commence à 0    ;   l = nombre de zones par ligne
    return l*(row//l)


def indexOfFirstZoneInColumn(col : int, l : int) -> int:#col commence à 0    ;   l = nombre de zones par colonne
    return (col//l)


def zoneIndexFromCoord(row : int, column : int, l : int) -> int: #l = nombre de zones par ligne/colonne
        rowIndex = indexOfFirstZoneInRow(row, l)            #example: pour une grille 9x9, a pour valeur 0, 3, 6
        colIndex = indexOfFirstZoneInColumn(column, l)         #example: pour une grille 9x9, a pour valeur 0, 1, 2
        zoneIndex = rowIndex+colIndex             #example: pour une grille 9x9 avec row=3 et col=4, a pour valeur 3 + 1
        return zoneIndex


def indexRowOrColumnInZone(rowOrcol : int, l : int) -> int:#rowOrcol commence à 0    ;    l = nombre de lignes/colonnes par zone
    return rowOrcol%l           #renvoie l'index relatif de la ligne ou colonne (par rapport à la zone dans laquel elle est située)


def indexOfRow(zoneI : int, index : int, l : int) -> int:#row commence à 0    ;   l = nombre de lignes par zone
    globalRowIndex = zoneI//l
    localRowIndex = index//l
    rowIndex = l*globalRowIndex + localRowIndex
    return rowIndex


def indexOfColumn(zoneI : int, index : int, l : int) -> int:#col commence à 0    ;   l = nombre de colonnes par zone
    globalColumnIndex = zoneI%l
    localColumnIndex = index%l
    columnIndex = l*globalColumnIndex + localColumnIndex
    return columnIndex


def rowIndexFromCelluleIndex(index : int, l : int) -> int: #index commence à 0
    size = l**2
    return index//size

def columnIndexFromCelluleIndex(index : int, l : int) -> int: #index commence à 0
    size = l**2
    return index%size

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

def valuesWithoutZero(values : list[int]) -> list[int]:
    newValues = []
    for i in range(len(values)):
        val = values[i]
        if (val!=0):
            newValues.append(val)


def listUnion(list1 : list[int], list2: list[int]) -> list[int]:
    newList = list1
    for i in range(len(list2)):
        if (list2[i] not in newList):
            newList.append(list2[i])
    return newList


def listDifference(list1 : list[int], list2: list[int]) -> list[int]:
    newList = []
    for i in range(len(list1)):
        if (list1[i] not in list2):
            newList.append(list1[i])
    return newList


def valueNumCount(value : int):
    if value==0:    #failsafe si value est déjà égal à 0
        return 1
    numCount = 0     #numCount = le nombre de chiffres qui composent value
    while value!= 0:   #on fait la division entière par 10 jusqu'à avoir 0 et le nombre de division = le nombre de chiffres qui composent value
        value = value//10
        numCount+=1
    return numCount


def valueToString(value : int, maxNumCount : int):
    if value==0:
        middle = "."
    else:
        middle = str(value)
    before = ""
    after = ""
    valNumCount = valueNumCount(value)
    spaceCount = maxNumCount - valNumCount
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