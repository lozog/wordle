from enum import Enum
import getopt
from pprint import pprint
import random
import sys


class LetterResult(Enum):
    INCORRECT = 0
    INCORRECT_POSITION = 1
    CORRECT_POSITION = 2
    UNUSED = 3


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


def get_input(guess_count, word_length, word_list, letter_results):
    while True:
        print(f"Enter guess #{guess_count+1}: ", end="")
        guess = input()

        if len(guess) != word_length:
            print(f"Your guess must be {word_length} letters long.")
            continue

        if guess not in word_list:
            print(f"{guess} isn't in the word list.")
            continue

        if HARD_MODE:
            for letter, letter_result in letter_results.items():
                if (
                    (letter_result == LetterResult.INCORRECT_POSITION
                    or letter_result == LetterResult.CORRECT_POSITION)
                    and letter not in guess
                ):
                    print(f"Your guess must contain {letter}.")
                    continue

        break

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
            guess = get_input(guess_count, WORD_LENGTH, WORD_LIST, letter_results)
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
