from enum import Enum
from pprint import pprint
import random


class LetterResult(Enum):
    INCORRECT = 0
    INCORRECT_POSITION = 1
    CORRECT_POSITION = 2


class GameResult(Enum):
    LOSS = 0
    WIN = 1


def get_input(guess_count, word_length):
    while True:
        print(f"Enter guess #{guess_count+1}: ", end="")
        guess = input()

        if len(guess) == word_length:
            break

        print(f"Your guess must be {word_length} letters long.")

    return guess


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


WORD_LENGTH = 5
MAX_GUESS_COUNT = 6
input_file = open(f"word_list_{WORD_LENGTH}", 'r')
WORD_LIST = input_file.read().splitlines()

while True:
    word_choice = random.randint(0, len(WORD_LIST) - 1)
    word = WORD_LIST[word_choice]
    game_result = GameResult.LOSS

    for guess_count in range(MAX_GUESS_COUNT):
        guess = get_input(guess_count, WORD_LENGTH)
        res = analyze_guess(guess, word)
        if set(res) == set([LetterResult.CORRECT_POSITION]):
            game_result = GameResult.WIN
            break


    if game_result == GameResult.WIN:
        print("You win!")
    else:
        print(f"You lose! The word was {word}.")

    print("Play again? (y/n): ", end="")
    if input() != "y":
        break
