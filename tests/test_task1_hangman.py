"""
Unit tests for Task 1: Hangman Console Game.
"""

import sys
from pathlib import Path
import pytest

# Add task1_hangman directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "task1_hangman"))

from hangman import HangmanGame, load_words, STAGES


def test_game_initialization():
    game = HangmanGame("DATHEON")
    assert game.secret_word == "DATHEON"
    assert game.mistakes == 0
    assert game.MAX_MISTAKES == 6
    assert len(game.guessed_letters) == 0
    assert game.get_masked_word() == "_ _ _ _ _ _ _"
    assert not game.is_game_over()
    assert not game.is_won()
    assert not game.is_lost()


def test_correct_guesses_and_win():
    game = HangmanGame("CODE")
    valid, msg = game.guess_letter("c")
    assert valid is True
    assert "C" in game.correct_letters
    assert game.mistakes == 0
    assert game.get_masked_word() == "C _ _ _"

    game.guess_letter("O")
    game.guess_letter("D")
    game.guess_letter("E")
    assert game.is_won() is True
    assert game.is_game_over() is True
    assert game.get_masked_word() == "C O D E"


def test_incorrect_guesses_and_loss():
    game = HangmanGame("CAT")
    wrong_letters = ["Z", "Y", "X", "W", "V", "U"]
    for char in wrong_letters:
        valid, msg = game.guess_letter(char)
        assert valid is True

    assert game.mistakes == 6
    assert game.is_lost() is True
    assert game.is_won() is False
    assert game.is_game_over() is True


def test_duplicate_guess_protection():
    game = HangmanGame("PYTHON")
    game.guess_letter("P")
    valid_repeat, msg = game.guess_letter("P")
    assert valid_repeat is False
    assert "already guessed" in msg
    assert game.mistakes == 0

    game.guess_letter("Z")
    assert game.mistakes == 1
    valid_repeat_wrong, msg2 = game.guess_letter("Z")
    assert valid_repeat_wrong is False
    assert game.mistakes == 1  # Penalty was not deducted twice


def test_invalid_input_rejection():
    game = HangmanGame("TEST")
    valid, msg = game.guess_letter("123")
    assert valid is False
    assert "Invalid input" in msg

    valid, msg = game.guess_letter("!")
    assert valid is False


def test_stages_visual_art():
    assert len(STAGES) == 7
    game = HangmanGame("TEST")
    assert game.get_stage_art() == STAGES[0]
    game.guess_letter("Z")
    assert game.get_stage_art() == STAGES[1]


def test_load_words():
    words = load_words()
    assert isinstance(words, list)
    assert len(words) > 0
    assert all(w.isupper() for w in words)
