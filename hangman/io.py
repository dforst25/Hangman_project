from hangman.game import *


def prompt_guess() -> str:
    ch = input("Guess a letter: ").strip(' ')
    return ch


def print_status(state: dict) -> None:
    print(render_display(state))
    print(f"Your guessed letters are: {', '.join(state['guessed'])}")
    print(f'your remaindering guesses is: {state["max_tries"] - state["wrong_guesses"]}')


def print_result(state: dict) -> None:
    if is_won(state):
        print("You Won!!!")
    else:
        print("You Lost!!!")
    print(render_summary(state))
