"""
Task 1: Hangman Word Guessing Game (Console)
Author: Seebiraj V (Datheon Python Programming Internship)
Track: Python & AI Applications

Features:
- Random word selection from words.txt or fallback vocabulary.
- Visual ASCII gallows art evolving dynamically over 6 incorrect attempts.
- Masked word formatting with spaced underscores (e.g. '_ A _ H E O N').
- Tracking of all guessed letters with duplicate-guess penalty protection.
- Robust input sanitization (single alphabetic character enforcement).
- Clean terminal victory and defeat screens with game replay capability.
"""

import os
import random
import sys
from pathlib import Path
from typing import List, Set, Tuple

# 7 Visual ASCII Gallows Stages (0 incorrect guesses to 6 incorrect guesses)
STAGES: List[str] = [
    r"""
     +---+
     |   |
         |
         |
         |
         |
   =========
    """,
    r"""
     +---+
     |   |
     O   |
         |
         |
         |
   =========
    """,
    r"""
     +---+
     |   |
     O   |
     |   |
         |
         |
   =========
    """,
    r"""
     +---+
     |   |
     O   |
    /|   |
         |
         |
   =========
    """,
    r"""
     +---+
     |   |
     O   |
    /|\  |
         |
         |
   =========
    """,
    r"""
     +---+
     |   |
     O   |
    /|\  |
    /    |
         |
   =========
    """,
    r"""
     +---+
     |   |
     O   |
    /|\  |
    / \  |
         |
   =========
    """
]

VICTORY_ART = r"""
  ██████╗  ██████╗  ██████╗ ██████╗       ██╗██╗██╗
 ██╔════╝ ██╔═══██╗██╔═══██╗██╔══██╗      ██║██║██║
 ██║  ███╗██║   ██║██║   ██║██║  ██║█████╗██║██║██║
 ██║   ██║██║   ██║██║   ██║██║  ██║╚════╝╚═╝╚═╝╚═╝
 ╚██████╔╝╚██████╔╝╚██████╔╝██████╔╝      ██╗██╗██╗
  ╚═════╝  ╚═════╝  ╚═════╝ ╚═════╝       ╚═╝╚═╝╚═╝
         🎉 CONGRATULATIONS! YOU SAVED HIM! 🎉
"""

DEFEAT_ART = r"""
  ██████╗  █████╗ ███╗   ███╗███████╗     ██████╗ ██╗   ██╗███████╗██████╗ 
 ██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ██╔═══██╗██║   ██║██╔════╝██╔══██╗
 ██║  ███╗███████║██╔████╔██║█████╗      ██║   ██║██║   ██║█████╗  ██████╔╝
 ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝      ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗
 ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ╚██████╔╝ ╚████╔╝ ███████╗██║  ██║
  ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝     ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝
              💀 GAME OVER! THE GALLOWS WON! 💀
"""

FALLBACK_WORDS = [
    "PYTHON", "DATHEON", "ALGORITHM", "VARIABLE", "FUNCTION",
    "DATABASE", "SECURITY", "FRAMEWORK", "TERMINAL", "DEVELOPER"
]


def load_words(file_path: str = "words.txt") -> List[str]:
    """Loads English word vocabulary from file or returns fallback terms."""
    resolved_path = Path(__file__).resolve().parent / file_path
    if resolved_path.exists():
        with open(resolved_path, "r", encoding="utf-8") as f:
            words = [line.strip().upper() for line in f if line.strip()]
            if words:
                return words
    return FALLBACK_WORDS


class HangmanGame:
    """Core logic engine for the Hangman console game."""

    MAX_MISTAKES = 6

    def __init__(self, secret_word: str):
        self.secret_word: str = secret_word.upper().strip()
        self.guessed_letters: Set[str] = set()
        self.correct_letters: Set[str] = set()
        self.incorrect_letters: Set[str] = set()
        self.mistakes: int = 0

    @classmethod
    def from_random(cls, word_list: List[str] = None) -> "HangmanGame":
        """Instantiates a game selecting a random word from the vocabulary."""
        words = word_list or load_words()
        return cls(random.choice(words))

    def guess_letter(self, letter: str) -> Tuple[bool, str]:
        """
        Processes a single letter guess.
        Returns: (is_valid_new_guess, feedback_message)
        """
        if not letter or len(letter) != 1 or not letter.isalpha():
            return False, "⚠️ Invalid input! Please enter a single alphabetic letter (A-Z)."

        cleaned = letter.upper()

        if cleaned in self.guessed_letters:
            return False, f"⚠️ You already guessed '{cleaned}'! No penalty deducted."

        self.guessed_letters.add(cleaned)

        if cleaned in self.secret_word:
            self.correct_letters.add(cleaned)
            return True, f"✅ Splendid! '{cleaned}' is in the secret word."
        else:
            self.incorrect_letters.add(cleaned)
            self.mistakes += 1
            return True, f"❌ Oops! '{cleaned}' is NOT in the secret word."

    def get_masked_word(self) -> str:
        """Returns the masked word with revealed letters (e.g. '_ A _ H E O N')."""
        return " ".join([char if char in self.correct_letters else "_" for char in self.secret_word])

    def get_stage_art(self) -> str:
        """Returns current ASCII gallows art for current mistake count."""
        index = min(self.mistakes, len(STAGES) - 1)
        return STAGES[index]

    def is_won(self) -> bool:
        """Returns True if all letters of the secret word have been guessed."""
        return set(self.secret_word).issubset(self.correct_letters)

    def is_lost(self) -> bool:
        """Returns True if mistake limit of 6 has been reached."""
        return self.mistakes >= self.MAX_MISTAKES

    def is_game_over(self) -> bool:
        """Returns True if game ended via victory or defeat."""
        return self.is_won() or self.is_lost()

    def get_status_summary(self) -> dict:
        """Returns a snapshot of game status for UI or telemetry."""
        return {
            "masked_word": self.get_masked_word(),
            "mistakes": self.mistakes,
            "max_mistakes": self.MAX_MISTAKES,
            "attempts_remaining": self.MAX_MISTAKES - self.mistakes,
            "guessed_letters": sorted(list(self.guessed_letters)),
            "is_won": self.is_won(),
            "is_lost": self.is_lost()
        }


def play_game():
    """Interactive console game loop."""
    print("=" * 60)
    print("      🎮 WELCOME TO DATHEON HANGMAN CONSOLE CHALLENGE 🎮      ")
    print("=" * 60)
    print("Rule: Guess the hidden word letter by letter within 6 attempts.")
    print("Duplicate guesses will NOT penalize you.\n")

    words = load_words()

    while True:
        game = HangmanGame.from_random(words)
        last_message = "New game initiated. Good luck!"

        while not game.is_game_over():
            # Clear or separate screen
            print("\n" + "-" * 50)
            print(game.get_stage_art())
            print(f"Secret Word :  {game.get_masked_word()}")
            print(f"Attempts Left: {game.MAX_MISTAKES - game.mistakes} / {game.MAX_MISTAKES}")
            print(f"Guessed So Far: {', '.join(sorted(game.guessed_letters)) if game.guessed_letters else 'None'}")
            print(f"Status      :  {last_message}")
            print("-" * 50)

            user_input = input("Enter your letter guess [A-Z] (or 'QUIT' to exit): ").strip()
            if user_input.upper() == "QUIT":
                print("\n👋 Thanks for playing! Exiting game.")
                return

            _, last_message = game.guess_letter(user_input)

        # Game outcome screen
        print("\n" + "=" * 60)
        print(game.get_stage_art())
        if game.is_won():
            print(VICTORY_ART)
            print(f"✨ Brilliant Deduction! You revealed the word: '{game.secret_word}'")
            print(f"Total Mistakes: {game.mistakes} / {game.MAX_MISTAKES}")
        else:
            print(DEFEAT_ART)
            print(f"The secret word was: '{game.secret_word}'")
            print("Better luck next time!")
        print("=" * 60)

        replay = input("\nWould you like to play another round? (y/n): ").strip().lower()
        if replay not in ("y", "yes"):
            print("\nThank you for playing Datheon Hangman! Happy Coding!")
            break


if __name__ == "__main__":
    play_game()
