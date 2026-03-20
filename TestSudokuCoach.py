from SudokuScraping import getDifficultyFromSudokuCoach, getDifficultyFromGrille

if __name__ == "__main__":
    test_puzzle = "204503910060008005000100034009000600003005200006300047070001089038490000002050070"
    result = getDifficultyFromSudokuCoach(test_puzzle, headless=False)
    print(f"Score : {result['score']} — {result['label']}")