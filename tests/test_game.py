from hangman.words import *
from hangman.io import *
import builtins


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
    assert state["max_tries"] == 5


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
        "max_tries": 5,
    }
    assert is_won(state) is True


def test_is_won_false():
    state = {
        "secret": "hi",
        "display": ["h", "_"],
        "guessed": {"h"},
        "wrong_guesses": 0,
        "max_tries": 5,
    }
    assert is_won(state) is False


def test_is_lost_true():
    state = {
        "secret": "hi",
        "display": ["_", "_"],
        "guessed": {"a", "b"},
        "wrong_guesses": 5,
        "max_tries": 5,
    }
    assert is_lost(state) is True


def test_is_lost_false():
    state = {
        "secret": "hi",
        "display": ["_", "_"],
        "guessed": {"a"},
        "wrong_guesses": 3,
        "max_tries": 5,
    }
    assert is_lost(state) is False


def test_render_display_format():
    state = {
        "secret": "בננה",
        "display": ["_", "נ", "_", "ה"],
        "guessed": set(),
        "wrong_guesses": 0,
        "max_tries": 5,
    }
    display_str = render_display(state)
    assert isinstance(display_str, str)
    assert "_ נ _ ה" in display_str or "_ נ _ ה" == display_str.strip()



# ---------- tests for io.py ----------

def test_prompt_guess(monkeypatch):
    """Simulate user input for prompt_guess."""
    monkeypatch.setattr(builtins, "input", lambda _: "a")
    ch = prompt_guess()
    assert ch == "a"


def test_prompt_guess_strips_whitespace(monkeypatch):
    """Ensure whitespace is stripped from user input."""
    monkeypatch.setattr(builtins, "input", lambda _: "  b  ")
    ch = prompt_guess()
    assert ch == "b"


def test_print_status_output(capsys):
    """Check that print_status prints display, guessed, and remaining guesses."""
    state = {
        "secret": "apple",
        "display": ["a", "_", "p", "_", "e"],
        "guessed": {"a", "p", "x"},
        "wrong_guesses": 1,
        "max_tries": 5,
    }
    print_status(state)
    captured = capsys.readouterr().out

    assert render_display(state) in captured
    # guessed letters must appear comma-separated
    assert "a" in captured and "p" in captured and "x" in captured
    # remaining guesses should match (5 - 1 = 4)
    assert "4" in captured


def test_print_result_win(capsys):
    """Ensure print_result shows correct win message and summary."""
    state = {
        "secret": "apple",
        "display": list("apple"),
        "guessed": {"a", "p", "l", "e"},
        "wrong_guesses": 0,
        "max_tries": 5,
    }
    print_result(state)
    captured = capsys.readouterr().out
    assert "You Won" in captured
    assert "apple" in captured
    assert "a" in captured and "p" in captured and "l" in captured and "e" in captured
    assert "=" * 15 in captured  # from render_summary


def test_print_result_loss(capsys):
    """Ensure print_result shows correct loss message and summary."""
    state = {
        "secret": "apple",
        "display": ["a", "_", "_", "_", "_"],
        "guessed": {"a", "b", "c", "d", "e"},
        "wrong_guesses": 5,
        "max_tries": 5,
    }
    print_result(state)
    captured = capsys.readouterr().out
    assert "You Lost" in captured
    assert "apple" in captured
    assert "a" in captured and "b" in captured
    assert "=" * 15 in captured


def test_render_summary_basic():
    """Test render_summary output formatting."""
    state = {
        "secret": "banana",
        "guessed": {"b", "a", "x"},
    }
    result = render_summary(state)
    assert isinstance(result, str)
    assert "banana" in result
    assert "b" in result and "a" in result and "x" in result
    assert result.count("=") >= 2


def test_print_result_win(capsys):
    """Ensure print_result shows win message."""
    state = {
        "secret": "apple",
        "display": list("apple"),
        "guessed": {"a", "p", "l", "e"},
        "wrong_guesses": 1,
        "max_tries": 5,
    }
    print_result(state)
    captured = capsys.readouterr().out
    assert "won" in captured.lower() or "congrat" in captured.lower()
    assert "apple" in captured


def test_print_result_loss(capsys):
    """Ensure print_result shows loss message."""
    state = {
        "secret": "apple",
        "display": ["a", "_", "_", "_", "_"],
        "guessed": {"a", "b", "c", "d", "e"},
        "wrong_guesses": 5,
        "max_tries": 5,
    }
    print_result(state)
    captured = capsys.readouterr().out
    assert "lost" in captured.lower() or "game over" in captured.lower()
    assert "apple" in captured
