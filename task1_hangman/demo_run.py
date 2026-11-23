"""
Non-interactive demonstration runner for Task 1 (Hangman).
Used by CI pipelines and automated testing harnesses.
"""

from hangman import HangmanGame, VICTORY_ART, DEFEAT_ART


def run_win_demo():
    print("\n--- Running Hangman Simulation: Victory Flow ---")
    game = HangmanGame("DATHEON")
    print("Secret Word Chosen: DATHEON")
    guesses = ["D", "A", "T", "X", "H", "E", "O", "N"]
    for char in guesses:
        valid, msg = game.guess_letter(char)
        print(f"Guess '{char}': {msg} | Word: {game.get_masked_word()} | Mistakes: {game.mistakes}")
    assert game.is_won(), "Game should be won!"
    print(VICTORY_ART)
    print("Victory flow successfully validated.\n")


def run_loss_demo():
    print("\n--- Running Hangman Simulation: Loss Flow ---")
    game = HangmanGame("PYTHON")
    print("Secret Word Chosen: PYTHON")
    wrong_guesses = ["A", "B", "C", "D", "E", "F"]
    for char in wrong_guesses:
        valid, msg = game.guess_letter(char)
        print(f"Guess '{char}': {msg} | Mistakes: {game.mistakes} / {game.MAX_MISTAKES}")
    assert game.is_lost(), "Game should be lost!"
    print(DEFEAT_ART)
    print("Loss flow successfully validated.\n")


def run_duplicate_penalty_demo():
    print("\n--- Running Duplicate Guess Protection Check ---")
    game = HangmanGame("CODE")
    game.guess_letter("Z")
    mistakes_before = game.mistakes
    valid, msg = game.guess_letter("Z")
    assert not valid, "Duplicate guess should return False validity"
    assert game.mistakes == mistakes_before, "Duplicate guess must NOT increment mistakes"
    print(f"Duplicate protection verified: '{msg}'")


if __name__ == "__main__":
    run_duplicate_penalty_demo()
    run_win_demo()
    run_loss_demo()
    print("All Task 1 automated demo simulations passed with 100% success!")
