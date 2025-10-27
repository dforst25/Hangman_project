import pytest
from hangman.game import *
from hangman.words import *


# ---------- tests for words.py ----------

def test_choose_secret_word_returns_string():
    words = ["apple", "banana", "cherry"]
    secret = choose_secret_word(words)
    assert isinstance(secret, str)
    assert secret in words


# ---------- tests for game.py ----------

def test_init_state_structure():
    state = init_state("apple", 5)
    assert isinstance(state, dict)
    assert state["secret"] == "apple"
    assert state["display"] == ["_"] * len("apple")
    assert state["guessed"] == set()
    assert state["wrong_guesses"] == 0
    assert state["max"] == 5


def test_validate_guess_single_valid():
    ok, msg = validate_guess("a", set())
    assert ok is True
    assert msg.lower().startswith("valid")


def test_validate_guess_multiple_chars():
    ok, msg = validate_guess("ab", set())
    assert ok is False
    assert "single" in msg.lower()


def test_validate_guess_digit():
    ok, msg = validate_guess("5", set())
    assert ok is False
    assert "number" in msg.lower()


def test_validate_guess_already_guessed():
    ok, msg = validate_guess("a", {"a"})
    assert ok is False
    assert "already" in msg.lower()


def test_apply_guess_correct_hit():
    state = init_state("apple", 5)
    result = apply_guess(state, "p")
    assert result is True  # False when we guessed correctly
    assert state["display"] == ["_", "p", "p", "_", "_"]
    assert "p" in state["guessed"]
    assert state["wrong_guesses"] == 0


def test_apply_guess_wrong_hit():
    state = init_state("apple", 5)
    result = apply_guess(state, "x")
    assert result is False  # True when wrong
    assert state["wrong_guesses"] == 1
    assert "x" in state["guessed"]


def test_is_won_true():
    state = {
        "secret": "hi",
        "display": ["h", "i"],
        "guessed": {"h", "i"},
        "wrong_guesses": 0,
        "max": 5,
    }
    assert is_won(state) is True


def test_is_won_false():
    state = {
        "secret": "hi",
        "display": ["h", "_"],
        "guessed": {"h"},
        "wrong_guesses": 0,
        "max": 5,
    }
    assert is_won(state) is False


def test_is_lost_true():
    state = {
        "secret": "hi",
        "display": ["_", "_"],
        "guessed": {"a", "b"},
        "wrong_guesses": 5,
        "max": 5,
    }
    assert is_lost(state) is True


def test_is_lost_false():
    state = {
        "secret": "hi",
        "display": ["_", "_"],
        "guessed": {"a"},
        "wrong_guesses": 3,
        "max": 5,
    }
    assert is_lost(state) is False


def test_render_display_format():
    state = {
        "secret": "בננה",
        "display": ["_", "נ", "_", "ה"],
        "guessed": set(),
        "wrong_guesses": 0,
        "max": 5,
    }
    display_str = render_display(state)
    assert isinstance(display_str, str)
    assert "_ נ _ ה" in display_str or "_ נ _ ה" == display_str.strip()
