def print_grille(grille):
    for row in range(9):
        line = ""
        for column in range(9):
            val = grille[row][column]
            line += str(val) if val != 0 else "."
            if column % 3 == 2 and column != 8:
                line += " | "
            else:
                line += " "
        print(line)
        if row % 3 == 2 and row != 8:
            print("-" * 21)


def grille_vide():
    return [[0 for _ in range(9)] for _ in range(9)]

def find_empty_cell(grille):
    for row in range(9):
        for col in range(9):
            if grille[row][col] == 0:
                return row, col
    return None


