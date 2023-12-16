from pathlib import Path
from collections import namedtuple
DEFAULT_PATH = Path("C:\\Users\\feeli\\OneDrive\\Desktop\\ICS 32A\\wordle_words.txt")

Guaranteed = namedtuple("Guaranteed", ["index", "letter"])
Value = namedtuple("Value", ["count", "state"])

class FailedTest(Exception):
    pass

def setup_letter_count(dictionary: dict):
    """Sets up the letter count"""
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    for c in alphabet:
        dictionary[c] = Value(0, "min")
    
def setup_possible_words(some_list: list):
    """Appends all possible wordle words to given list"""
    file = DEFAULT_PATH.open("r")
    for word in file.readlines():
        if word[-1:] == "\n":
            some_list.append(word[:-1])
        else:
            some_list.append(word)

def increment_letter(dictionary: dict, letter: str):
    """Increments given letter in the dictionary, or add a new key and keyvalue if it doesn't already exist"""
    if letter in dictionary.keys():
        dictionary[letter] += 1
    else:
        dictionary[letter] = 1

def guarantee_match(guarantees: list[Value], word: str, match: bool):
    """Determines if the word has met the requirements of guarantees (whether or not they match)"""
    for guarantee in guarantees:
        if (word[guarantee.index: guarantee.index+1] == guarantee.letter) != match:
            raise FailedTest

def run():
    possible_words = []
    letter_count = {}
    setup_possible_words(possible_words)
    setup_letter_count(letter_count)

    # While there is more than 1 choice
    while len(possible_words) > 1:
        # Ask for input
        tried_word = input("What word did you input?\n")
        result = input("What was the result? (0 = Gray, 1 = Yellow, 2 = Green)\n")
        guaranteed = []
        blacklisted = []
        current_letter_count = {}
        # Search through response
        for i in range(0, 5):
            letter = tried_word[i: i+1]
            # If guaranteed, guarantee that the specific value is at that specific place, then increment letter count
            if result[i: i+1] == "2":
                guaranteed.append(Guaranteed(i, letter))
                increment_letter(current_letter_count, letter)
            # If included, guarantee that the specific value isn't at that specific place, then increment letter count
            elif result[i: i+1] == "1":
                blacklisted.append(Guaranteed(i, letter))
                increment_letter(current_letter_count, letter)
            # If not in word, set whatever is the count of that letter as the max (cannot get greater)
            elif result[i: i+1] == "0":
                letter_count[letter] = Value(letter_count[letter].count, "max")
        # Update the greatest count of each letter
        for letter in current_letter_count.keys():
            letter_count[letter] = Value(max(current_letter_count[letter], letter_count[letter].count), letter_count[letter].state)

        i = 0
        while i < len(possible_words):
            current_word = possible_words[i]
            try:
                # Discriminate words that doesn't have x at y
                guarantee_match(guaranteed, current_word, True)
                # Discriminate words that does have x at y
                guarantee_match(blacklisted, current_word, False)
                # Discriminate words that have less/more than letter_count
                for letter in letter_count.keys():
                    if letter_count[letter].count < current_word.count(letter) and letter_count[letter].state == "max":
                        raise FailedTest
                    elif letter_count[letter].count > current_word.count(letter) and letter_count[letter].state == "min":
                        raise FailedTest
            except FailedTest:
                possible_words.pop(i)
                i-=1
            finally:
                i+=1
        print(possible_words)
    print(f"The word is: {possible_words[0]}")

if __name__ == "__main__":
    run()