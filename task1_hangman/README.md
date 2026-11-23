# Task 1: Hangman Word Guessing Game (Console)

## Overview & Goal
Build an interactive, modular console game in Python implementing string manipulation, sets for deduplication, state machines, and control flow.

## Features
- **Visual ASCII Gallows Art**: 7 dynamic progression stages (from blank gallows to full hanging figure upon 6 mistakes).
- **Masked Word Formatting**: Displays revealed letters with spaced underscores (e.g. `_ A _ H E O N`).
- **Duplicate Penalty Deduction Prevention**: Warns players when a character has already been attempted without penalizing their mistake budget.
- **Robust Input Sanitization**: Rejects multi-character strings, numbers, and symbols while accepting lowercase/uppercase letters seamlessly.
- **Victory & Defeat Screens**: Clean ASCII celebration banners and revealing hidden words upon defeat.
- **Replay Loop**: Seamless round re-runs.

## File Manifest
- `hangman.py`: Main executable console game and `HangmanGame` logic engine.
- `words.txt`: Dataset of English technical vocabulary for random word selection.
- `demo_run.py`: Scripted validation harness for automated CI pipelines.

## How to Run
```bash
# Interactive game
python task1_hangman/hangman.py

# Automated test demo
python task1_hangman/demo_run.py
```
