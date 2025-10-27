from random import randrange


def choose_secret_word(words: list[str]) -> str:
    return words[randrange(len(words))]
