from enum import Enum


class LetterResult(Enum):
    INCORRECT = 0
    INCORRECT_POSITION = 1
    CORRECT_POSITION = 2


WORD_LIST = ["crimp"]
MAX_GUESS_COUNT = 6

guess_count = 0

word = WORD_LIST[0]
print(f"Enter guess #{guess_count+1}: ", end="")
guess = input()

unguessed_letters = list(word)
for letter_pair in zip(guess, word):
    # 0 -> incorrect, 1 -> incorrect position, 2 -> correct position
    res = LetterResult.INCORRECT
    if letter_pair[0] == letter_pair[1]:
        unguessed_letters.remove(letter_pair[0])
        res = LetterResult.CORRECT_POSITION
    elif letter_pair[0] in unguessed_letters:
        unguessed_letters.remove(letter_pair[0])
        res = LetterResult.INCORRECT_POSITION

    print(f"{letter_pair[0]} {letter_pair[1]}: {res}")
