from SolveHuman import SolveHuman

class HumanSolverStats(SolveHuman):
    def __init__(self, grille):
        super().__init__(grille)
        self.stats = {}
