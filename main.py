from colorama import Fore, Style
from hangman.words import *
from hangman.io import *


def play(words: list[str], max_tries: int = 6) -> None:
    secret = choose_secret_word(words)
    state = init_state(secret, max_tries)
    while not is_won(state) and not is_lost(state):
        print_status(state)

        guess = prompt_guess()
        valid, message = validate_guess(guess, state["guessed"])

        print(message)

        if not valid:
            continue

        if apply_guess(state, guess):
            print(Fore.GREEN + "Very nice!!!" + Style.RESET_ALL)
        else:
            print(Fore.RED + "Not yet! Maybe next time you'll guess correctly." + Style.RESET_ALL)

    print_result(state)


if __name__ == "__main__":

    play(words, 10)
