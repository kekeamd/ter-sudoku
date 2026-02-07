def indexOfFirstZoneInRow(row : int, l : int) -> int:#row commence à 0    ;   l = nombre de zones par ligne
    return l*(row//l)


def indexOfFirstZoneInColumn(col : int, l : int) -> int:#col commence à 0    ;   l = nombre de zones par colonne
    return (col//l)


def indexOfZone(row : int, column : int, l : int) -> int: #l = nombre de zones/lignes/colonnes
        rowIndex = indexOfFirstZoneInRow(row, l)            #example: pour une grille 3x3, a pour valeur 0, 3, 6
        colIndex = indexOfFirstZoneInColumn(column, l)         #example: pour une grille 3x3, a pour valeur 0, 1, 2
        zoneIndex = rowIndex+colIndex             #example: pour une grille 3x3 avec row=3 et col=4, a pour valeur 3 + 1
        return zoneIndex


def indexRowOrColumnInZone(rowOrcol : int, l : int) -> int:#rowOrcol commence à 0    ;    l = nombre de lignes/colonnes par zone
    return rowOrcol%l


def indexOfRow(zoneI : int, index : int, l : int) -> int:#row commence à 0    ;   l = nombre de lignes
    globalRowIndex = zoneI//l
    localRowIndex = index//l
    rowIndex = l*globalRowIndex + localRowIndex
    return rowIndex


def indexOfColumn(zoneI : int, index : int, l : int) -> int:#col commence à 0    ;   l = nombre de colonnes
    globalColumnIndex = zoneI%l
    localColumnIndex = index%l
    columnIndex = l*globalColumnIndex + localColumnIndex
    return columnIndex


def valuesWithoutZero(values : list[int]) -> list[int]:
    newValues = []
    for i in range(len(values)):
        val = values[i]
        if (val!=0):
            newValues.append(val)

def listDifference(list1 : list[int], list2: list[int]) -> list[int]:
    newList = []
    for i in range(len(list1)):
        if (list1[i] not in list2):
            newList.append(list1[i])
    return newList