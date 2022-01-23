from enum import Enum
from pprint import pprint


class LetterResult(Enum):
    INCORRECT = 0
    INCORRECT_POSITION = 1
    CORRECT_POSITION = 2


def analyze_guess(guess, word):
    unguessed_letters = list(word)
    guess_result = []
    for letter_pair in zip(guess, word):
        res = LetterResult.INCORRECT
        if letter_pair[0] == letter_pair[1]:
            unguessed_letters.remove(letter_pair[0])
            res = LetterResult.CORRECT_POSITION
        elif letter_pair[0] in unguessed_letters:
            unguessed_letters.remove(letter_pair[0])
            res = LetterResult.INCORRECT_POSITION

        print(f"{letter_pair[0]} {letter_pair[1]}: {res}")
        guess_result.append(res)

    return guess_result


WORD_LIST = ["crimp"]
MAX_GUESS_COUNT = 6

guess_count = 0

word = WORD_LIST[0]
print(f"Enter guess #{guess_count+1}: ", end="")
guess = input()
# TODO: ensure guess is 5 letters long

res = analyze_guess(guess, word)
if set(res) == set([LetterResult.CORRECT_POSITION]):
    print("you win!")
