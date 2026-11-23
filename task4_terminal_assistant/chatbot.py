"""
Task 4: Rule-Based Interactive Terminal Assistant / Chatbot
Author: Seebiraj V (Datheon Python Programming Internship)
Track: Python & AI Applications

Features:
- Regex-powered multi-intent classification and keyword weighting.
- Conversational dialogue state management (GREETING -> IDENTIFICATION -> RESOLUTION -> EXIT).
- Dynamic FAQ loading from 'faq_dataset.json' with business hours, product offerings, support, and internship queries.
- Robust input normalization (lowercasing, punctuation stripping, whitespace trimming).
- Intelligent fallback suggestions when query confidence is low.
- Clean exit handling for words like 'bye', 'exit', 'quit', 'goodbye'.
"""

import json
import random
import re
import string
import sys
from enum import Enum, auto
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class DialogueState(Enum):
    INIT = auto()
    AWAITING_QUERY = auto()
    RESOLVED = auto()
    FALLBACK = auto()
    EXIT = auto()


class RuleBasedChatbot:
    """Conversational rule-based terminal assistant with multi-intent recognition."""

    def __init__(self, dataset_path: str = "faq_dataset.json"):
        self.resolved_path = Path(__file__).resolve().parent / dataset_path
        self.data = self._load_dataset()
        self.bot_name: str = self.data.get("bot_name", "Datheon Nova")
        self.intents: List[dict] = self.data.get("intents", [])
        self.fallbacks: List[str] = self.data.get("fallbacks", ["I'm sorry, I didn't understand that."])
        self.state: DialogueState = DialogueState.INIT
        self.history: List[Tuple[str, str, str]] = []  # (role, text, intent)

        # Precompile regular expressions for high throughput
        self._compiled_intents = []
        for item in self.intents:
            compiled_patterns = [re.compile(pat, re.IGNORECASE) for pat in item.get("patterns", [])]
            self._compiled_intents.append({
                "tag": item["tag"],
                "patterns": compiled_patterns,
                "responses": item.get("responses", [])
            })

    def _load_dataset(self) -> dict:
        """Loads intents and responses from JSON file."""
        if self.resolved_path.exists():
            with open(self.resolved_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"bot_name": "Datheon Nova", "intents": [], "fallbacks": []}

    def normalize_input(self, text: str) -> str:
        """Cleans and normalizes user input text."""
        if not text:
            return ""
        # Lowercase and strip whitespace
        normalized = text.lower().strip()
        # Remove excess punctuation while keeping words intact
        normalized = re.sub(r"[^\w\s]", " ", normalized)
        normalized = re.sub(r"\s+", " ", normalized).strip()
        return normalized

    def match_intent(self, user_text: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Evaluates input text against intent patterns using regex matching.
        Returns: (intent_tag, selected_response)
        """
        normalized = self.normalize_input(user_text)
        if not normalized:
            return "empty", "Please type a question or request so I can assist you!"

        # Check clean exit commands first
        if re.search(r"\b(bye|exit|quit|goodbye|see you|close)\b", normalized):
            for item in self._compiled_intents:
                if item["tag"] == "goodbye":
                    self.state = DialogueState.EXIT
                    return "goodbye", random.choice(item["responses"])

        # Check all registered intents
        best_intent = None
        best_score = 0
        best_response = None

        for item in self._compiled_intents:
            matches_count = 0
            for pattern in item["patterns"]:
                found = pattern.findall(normalized)
                matches_count += len(found)

            if matches_count > best_score:
                best_score = matches_count
                best_intent = item["tag"]
                best_response = random.choice(item["responses"])

        if best_score > 0 and best_intent:
            self.state = DialogueState.RESOLVED
            return best_intent, best_response

        # Fallback state when no pattern matches
        self.state = DialogueState.FALLBACK
        fallback_msg = random.choice(self.fallbacks)
        return "fallback", fallback_msg

    def reply(self, user_input: str) -> str:
        """Processes user input and returns conversational bot response."""
        tag, response = self.match_intent(user_input)
        self.history.append(("USER", user_input, tag or "none"))
        self.history.append(("BOT", response, tag or "none"))
        return response

    def is_session_active(self) -> bool:
        """Returns True if the chatbot conversation is active."""
        return self.state != DialogueState.EXIT


def launch_terminal_chat():
    """Interactive CLI terminal session."""
    bot = RuleBasedChatbot()
    print("=" * 65)
    print(f"       🤖 WELCOME TO {bot.bot_name.upper()} TERMINAL ASSISTANT 🤖       ")
    print("=" * 65)
    print("Ask about: operating hours, services, pricing, refund, internship,")
    print("support, or type 'topics' for options. Type 'quit' or 'bye' to exit.\n")

    # Initial greeting
    print(f"{bot.bot_name}: Hello! I'm here to assist you. What can I do for you today?")

    while bot.is_session_active():
        try:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue

            bot_response = bot.reply(user_input)
            print(f"\n{bot.bot_name}:\n{bot_response}")

            if bot.state == DialogueState.EXIT:
                print("\n[Session ended]")
                break

        except (KeyboardInterrupt, EOFError):
            print(f"\n\n{bot.bot_name}: Session interrupted. Goodbye!")
            break


if __name__ == "__main__":
    launch_terminal_chat()
