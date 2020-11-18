import sys
import hashlib
import itertools
import time
import string

"""
This class will be used in order to create a proof-of-work string for a given message (in a file).

Input: nbits file

nbits = number of leading zero bits requested in the hash
file = contains the message to hash and put leading zeros in

Author: Chris Zachariah
"""

# number of bytes to read from file at a time
BUF_SIZE = 65536


def main():
    listOfAllCharacters = string.printable
    listOfAllCharacters = listOfAllCharacters.strip(' \t\n\r\x0b\x0c')
    listOfAllCharacters = listOfAllCharacters.replace('\'', '')
    listOfAllCharacters = listOfAllCharacters.replace('\"', '')

    print(listOfAllCharacters)

    r = 1
    while r <= (len(listOfAllCharacters)):
        combinations_object = itertools.combinations_with_replacement(listOfAllCharacters, r)       # get combos
        for combo in combinations_object:
            permutations_object = itertools.permutations(combo)                                     # get permutations
            for proof in permutations_object:
                i = 0
        r = r + 1

    #print( " HERE ")
    r = 1
    while r <= (len(listOfAllCharacters)):
        for p in itertools.product(listOfAllCharacters, repeat=r):
            i = 0
        r = r + 1


if __name__ == "__main__":
    main()
