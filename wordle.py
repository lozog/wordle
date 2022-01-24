from enum import Enum
from pprint import pprint
import random


class LetterResult(Enum):
    INCORRECT = 0
    INCORRECT_POSITION = 1
    CORRECT_POSITION = 2
    UNUSED = 3


class GameResult(Enum):
    LOSS = 0
    WIN = 1


DEBUG_MODE = False
def print_debug(string):
    if DEBUG_MODE:
        print(string)


def pprint_debug(string):
    if DEBUG_MODE:
        pprint(string)


def get_input(guess_count, word_length):
    while True:
        print(f"Enter guess #{guess_count+1}: ", end="")
        guess = input()

        if len(guess) == word_length:
            break

        print(f"Your guess must be {word_length} letters long.")

    return guess.lower()


def analyze_guess(guess, word, letter_results):
    unguessed_letters = list(word)
    guess_result = []
    for letter_pair in zip(guess, word):
        letter = letter_pair[0]
        letter_result = LetterResult.INCORRECT
        if letter == letter_pair[1]:
            unguessed_letters.remove(letter)
            letter_result = LetterResult.CORRECT_POSITION
        elif letter in unguessed_letters:
            unguessed_letters.remove(letter)
            letter_result = LetterResult.INCORRECT_POSITION

        guess_result.append(letter_result)
        letter_results[letter] = letter_result
        print(f"{letter}: {letter_result}")

    return guess_result


WORD_LENGTH = 5
MAX_GUESS_COUNT = 6
input_file = open(f"word_list_{WORD_LENGTH}", 'r')
WORD_LIST = input_file.read().splitlines()
ALPHABET = "abcdefghijklmnopqrstuvwxyz"

while True:
    word_choice = random.randint(0, len(WORD_LIST) - 1)
    word = WORD_LIST[word_choice].lower()
    print_debug(word)
    game_result = GameResult.LOSS
    letter_results = {letter:LetterResult.UNUSED for letter in ALPHABET}

    for guess_count in range(MAX_GUESS_COUNT):
        guess = get_input(guess_count, WORD_LENGTH)
        res = analyze_guess(guess, word, letter_results)
        pprint_debug(letter_results)
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
