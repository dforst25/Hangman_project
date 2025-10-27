def init_state(secret: str, max_tries: int) -> dict:
    return {"secret": secret, "display": list('_' * len(secret)), "guessed": set(), "wrong_guesses": 0,
            "max": max_tries}


def validate_guess(ch: str, guessed: set[str]) -> tuple[bool, str]:
    if len(ch) != 1:
        return False, "Error: Input must be a single character."
    if ch.isdigit():
        return False, "Error: Input must not be a number."
    if ch in guessed:
        return False, "Error: Letter already guessed."
    return True, "Valid guess."


def update_display(state: dict, ch: str) -> None:
    secret = state["secret"]
    index = 0
    while ch in secret:
        index += state["secret"].find(ch)
        state["display"][index] = ch
        state["guessed"].add(ch)
        secret = secret[index + 1:]


def update_guessed(state: dict, ch: str) -> None:
    state["guessed"].add(ch)
    state["wrong_guesses"] += 1


def apply_guess(state: dict, ch: str) -> bool:
    if ch in state["secret"]:
        update_display(state, ch)
        return True
    else:
        update_guessed(state, ch)
        return False


def is_won(state: dict) -> bool:
    return '_' not in state["display"]


def is_lost(state: dict) -> bool:
    return state["wrong_guesses"] >= state["max"]


def render_display(state: dict) -> str:
    return ' '.join(state["display"])


def render_summary(state: dict) -> str:
    return f'''{'='*15}\nThe secret word is: {state["secret"]}
Your guessed words are: {' ,'.join(state["guessed"])}\n{'='*15}'''
