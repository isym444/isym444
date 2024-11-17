import random
from copy import deepcopy

# Take user input
def get_user_input():
    return input("Please enter a single word/text without numbers, punctuation or spaces: ")

# Check that input is valid -> for the purpose of this program, I have decided this means that the input must not have spaces or punctuation
def check_input_validity(user_input):
    checker = True
    for character in user_input:
        if character.isalpha() == False:
            checker = False
    return checker

# Check that input can be anagrammed -> i.e. has more than one letter, has at least more than one different letter
def check_input_anagrammable(user_input):
    checker = False
    if len(user_input) == 1:
        return False
    initial_character = user_input[0]
    for character in user_input:
        if character != initial_character:
            checker = True
    return checker

# Generate anagram
def generate_anagram(user_input):
    anagram = list(user_input)
    for traverser in range(len(user_input)):
        anagram_factor = random.randint(0, len(user_input)-1)
        temp = deepcopy(anagram)
        anagram[anagram_factor] = temp[traverser]
        anagram[traverser] = temp[anagram_factor]
    anagram = "".join(anagram)
    return anagram

# Check that anagrammed output differs from user input
def check_anagram_difers_from_input(user_input, anagram):
    checker = True
    if anagram == user_input:
        checker = False
    return checker

def main():
    print("This program will generate an anagram of a word/text you input")
    user_input = "!"
    while check_input_validity(user_input) == False:
        user_input = get_user_input()
    while check_input_anagrammable(user_input) == False:
        print("This word/text cannot be anagrammed")
        user_input = get_user_input()
    anagram = user_input
    while check_anagram_difers_from_input(user_input, anagram) == False:
        anagram = generate_anagram(user_input)
    print(f"Here is an anagram of your input: {anagram}")

main()