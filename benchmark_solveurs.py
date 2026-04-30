import time
import matplotlib.pyplot as plt

from GrilleBacktrack import GrilleBacktrack
from Difficulte import Difficulte
from SolverBacktrack import SolverBacktrack
from SolverHumanStats import SolverHumanStats
from SolverHuman import SolverHuman
from Solver import Solver


# ---------------------------------------------------------
# Génère une grille partiellement remplie selon la difficulté
# ---------------------------------------------------------
def generate_puzzle(difficulte: Difficulte) -> GrilleBacktrack:
    g = GrilleBacktrack(size=3)
    g.generateValues(difficulte)
    return g


# ---------------------------------------------------------
# OPTION A : Temps d'exécution
# ---------------------------------------------------------
def measure_time_backtrack(grille):
    g = grille.clone()
    start = time.time()
    SolverBacktrack.solveGrille(g)
    return time.time() - start


def measure_time_human(grille):
    g = grille.clone()
    start = time.time()
    SolverHuman.solveGrille(g)
    return time.time() - start


# ---------------------------------------------------------
# OPTION B : Nombre de backtracks
# ---------------------------------------------------------
class BacktrackCounter:
    calls = 0
    backs = 0


def solve_rec_instrumented(grille):
    BacktrackCounter.calls += 1
    size = grille.getSize() ** 2

    for r in range(size):
        for c in range(size):
            if grille.getCelluleValueCoord(r, c) == 0:
                for val in range(1, size + 1):
                    if Solver.isValid(grille, r, c, val):
                        grille.setCelluleValueCoord(r, c, val)
                        if solve_rec_instrumented(grille):
                            return True
                        BacktrackCounter.backs += 1
                        grille.setCelluleValueCoord(r, c, 0)
                return False
    return True


def measure_backtracks(grille):
    BacktrackCounter.calls = 0
    BacktrackCounter.backs = 0
    g = grille.clone()
    solve_rec_instrumented(g)
    return BacktrackCounter.calls, BacktrackCounter.backs


# ---------------------------------------------------------
# OPTION D : Comparaison solveurs
# ---------------------------------------------------------
def benchmark(n_tests=10, difficulte=Difficulte.MOYEN):
    times_backtrack = []
    times_human = []
    calls_list = []
    backs_list = []

    for _ in range(n_tests):
        g = generate_puzzle(difficulte)

        # Temps solveur backtracking
        times_backtrack.append(measure_time_backtrack(g))

        # Temps solveur humain
        times_human.append(measure_time_human(g))

        # Backtracks
        calls, backs = measure_backtracks(g)
        calls_list.append(calls)
        backs_list.append(backs)

    # ---------------- COURBES ----------------

    # Temps d'exécution
    plt.figure(figsize=(10, 5))
    plt.plot(times_backtrack, label="Backtracking")
    plt.plot(times_human, label="Solver Humain")
    plt.title("Temps d'exécution des solveurs")
    plt.xlabel("Test n°")
    plt.ylabel("Temps (s)")
    plt.legend()
    plt.grid(True)

    # Appels récursifs
    plt.figure(figsize=(10, 5))
    plt.plot(calls_list, label="Appels récursifs (Backtracking)")
    plt.title("Nombre d'appels récursifs")
    plt.xlabel("Test n°")
    plt.ylabel("Appels")
    plt.legend()
    plt.grid(True)

    # Backtracks
    plt.figure(figsize=(10, 5))
    plt.plot(backs_list, label="Backtracks (Backtracking)")
    plt.title("Nombre de backtracks")
    plt.xlabel("Test n°")
    plt.ylabel("Backtracks")
    plt.legend()
    plt.grid(True)

    plt.show()


if __name__ == "__main__":
    benchmark(n_tests=10, difficulte=Difficulte.MOYEN)
