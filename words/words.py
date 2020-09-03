import os

with open(f'{os.path.dirname(os.path.realpath(__file__))}/dictionary.txt') as f:
    words = f.read().splitlines()

UPPER_WORDS = [word for word in words if word[0].isupper() and word.isalpha()]
LOWER_WORDS = [word for word in words if word[0].islower() and word.isalpha()]
NAME_WORDS = [word for word in UPPER_WORDS if not word.isupper() and word.isalpha()]
