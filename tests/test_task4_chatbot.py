"""
Unit tests for Task 4: Rule-Based Interactive Terminal Assistant.
"""

import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "task4_terminal_assistant"))

from chatbot import RuleBasedChatbot, DialogueState


def test_input_normalization():
    bot = RuleBasedChatbot()
    assert bot.normalize_input("  HELLO, WORLD!  ") == "hello world"
    assert bot.normalize_input("What is your price???") == "what is your price"


def test_intent_matching():
    bot = RuleBasedChatbot()

    tag, _ = bot.match_intent("Hi there, good morning")
    assert tag == "greeting"

    tag, _ = bot.match_intent("What are your business operating hours?")
    assert tag == "business_hours"

    tag, _ = bot.match_intent("How much does the program cost and is it free?")
    assert tag == "pricing_discounts"

    tag, _ = bot.match_intent("What is your refund policy?")
    assert tag == "refund_returns"

    tag, _ = bot.match_intent("My code has a bug and syntax error")
    assert tag == "technical_support"

    tag, _ = bot.match_intent("Tell me about the Datheon python internship certificate")
    assert tag == "datheon_internship"


def test_fallback_state():
    bot = RuleBasedChatbot()
    tag, resp = bot.match_intent("xyzqwerty123 totally random gibberish")
    assert tag == "fallback"
    assert bot.state == DialogueState.FALLBACK
    assert len(resp) > 0


def test_exit_trigger():
    bot = RuleBasedChatbot()
    tag, resp = bot.match_intent("Okay, thank you, bye!")
    assert tag == "goodbye"
    assert bot.state == DialogueState.EXIT
    assert not bot.is_session_active()


def test_conversation_history_recording():
    bot = RuleBasedChatbot()
    bot.reply("Hello")
    bot.reply("What hours are you open?")
    assert len(bot.history) == 4  # 2 user queries + 2 bot responses
