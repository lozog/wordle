from enum import Enum
import getopt
from pprint import pprint
import random
import sys


class LetterResult(Enum):
    INCORRECT = 0           # letter not in word
    INCORRECT_POSITION = 1  # letter in word, but wrong position
    CORRECT_POSITION = 2    # letter in correct position
    UNUSED = 3              # letter not yet guessed


class GameResult(Enum):
    LOSS = 0
    WIN = 1


def print_debug(string):
    if DEBUG_MODE:
        print(string)


def pprint_debug(string):
    if DEBUG_MODE:
        pprint(string)


def print_usage():
    print("Usage: python wordle.py [flags]")
    print("Available flags: -h, --help; -d, --debug")


def get_input(guess_count, word, word_list, letter_results):
    def are_hard_mode_conditions_met(guess, word, letter_results):
        for i, letter_pair in enumerate(zip(guess, word)):
            if (
                letter_results[letter_pair[1]] == LetterResult.CORRECT_POSITION
                and letter_pair[0] != letter_pair[1]
            ):
                print(f"Letter at position {i+1} must be {letter_pair[1]}.")
                return False
        return True

    while True:
        print(f"Enter guess #{guess_count+1}: ", end="")
        guess = input()

        if len(guess) != len(word):
            print(f"Your guess must be {len(word)} letters long.")
            continue

        if guess not in word_list:
            print(f"{guess} isn't in the word list.")
            continue

        if HARD_MODE:
            if not are_hard_mode_conditions_met(guess, word, letter_results):
                continue

        break

    return guess.lower()


def analyze_guess(guess, word, letter_results):
    guess_result = [LetterResult.INCORRECT for letter in guess]
    remaining_guess = list(guess)
    unguessed_letters = list(word)

    # first, find all letters in the correct position
    for i, letter_pair in enumerate(zip(guess, word)):
        letter = letter_pair[0]
        if letter == letter_pair[1]:
            guess_result[i] = LetterResult.CORRECT_POSITION
            remaining_guess[i] = None
            unguessed_letters[i] = None

    # then find any remaining letters that are in incorrect positions
    for i, letter in enumerate(remaining_guess):
        if letter is not None and letter in unguessed_letters:
            guess_result[i] = LetterResult.INCORRECT_POSITION
            unguessed_letters.remove(letter)

    # copy the guess results into letter_results
    for result in zip(guess, guess_result):
        if (
            result[1] == LetterResult.CORRECT_POSITION
            or letter_results[result[0]] == LetterResult.UNUSED
            or letter_results[result[0]] == LetterResult.INCORRECT_POSITION
        ):
            print_debug(f"setting {result[0]} to {result[1]}")
            letter_results[result[0]] = result[1]

    return guess_result


DEBUG_MODE = False
WORD_LENGTH = 5
MAX_GUESS_COUNT = 6
ALPHABET = "abcdefghijklmnopqrstuvwxyz"
HARD_MODE = False


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hdx", ["--help", "--hard", "--debug"])
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_usage()
            sys.exit()
        elif opt in ("-d", "--debug"):
            global DEBUG_MODE
            DEBUG_MODE = True
        elif opt in ("-x", "--hard"):
            global HARD_MODE
            HARD_MODE = True

    input_file = open(f"word_list_{WORD_LENGTH}", 'r')
    WORD_LIST = [word.lower() for word in set(input_file.read().splitlines())]

    while True:
        word_choice = random.randint(0, len(WORD_LIST) - 1)
        word = WORD_LIST[word_choice].lower()
        print_debug(word)
        game_result = GameResult.LOSS
        letter_results = {letter:LetterResult.UNUSED for letter in ALPHABET}

        for guess_count in range(MAX_GUESS_COUNT):
            guess = get_input(guess_count, word, WORD_LIST, letter_results)
            guess_result = analyze_guess(guess, word, letter_results)
            pprint_debug(letter_results)
            if set(guess_result) == set([LetterResult.CORRECT_POSITION]):
                game_result = GameResult.WIN
                break

        if game_result == GameResult.WIN:
            print("You win!")
        else:
            print(f"You lose! The word was {word}.")

        print("Play again? (y/n): ", end="")
        if input() != "y":
            break

if __name__ == "__main__":
    main(sys.argv[1:])
