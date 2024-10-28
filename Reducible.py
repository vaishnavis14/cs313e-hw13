#  File: Reducible.py

#  Description: This returns the longest words from a hash table that are reducible.

#  Student Name: Vaishnavi Sathiyamoorthy

#  Student UT EID: vs25229

#  Partner Name: Saivachan Ponnapalli

#  Partner UT EID: sp48347

#  Course Name: CS 313E

#  Unique Number: 52530

#  Date Created: 10/19/2022

#  Date Last Modified: 10/20/2022

import time
import sys

# Input: takes as input a positive integer n
# Output: returns True if n is prime and False otherwise
def is_prime(n):
    if n == 1:
        return False

    limit = int(n ** 0.5) + 1
    div = 2
    while div < limit:
        if n % div == 0:
            return False
        div += 1
    return True


# Input: takes as input a string in lower case and the size
#        of the hash table
# Output: returns the index the string will hash into
def hash_word(s, size):
    hash_idx = 0
    for j in range(len(s)):
        letter = ord(s[j]) - 96
        hash_idx = (hash_idx * 26 + letter) % size
    return hash_idx


# Input: takes as input a string in lower case and the constant
#        for double hashing
# Output: returns the step size for that string
def step_size(s, const):
    hash_idx = 0
    for j in range(len(s)):
        letter = ord(s[j]) - 96
        hash_idx = (hash_idx * 26 + letter) % const
    return const - (hash_idx % const)


# Input: takes as input a string and a hash table
# Output: no output; the function enters the string in the hash table,
#         it resolves collisions by double hashing
def insert_word(s, hash_table):
    # calls hash_word to determine the index at the word should be inserted for the initial hash function
    idx = hash_word(s, len(hash_table))
    if len(hash_table[idx]) != 0:
        constant = 0
        hash_index = idx
        stepper = step_size(s, 11)
        # This loop keeps going with a different constant until an empty index is found
        while len(hash_table[hash_index]) != 0:
            constant += 1
            hash_index = (constant * stepper + idx) % len(hash_table)
        hash_table[hash_index] = s
    else:
        hash_table[idx] = s


# Input: takes as input a string and a hash table
# Output: returns True if the string is in the hash table
#         and False otherwise
def find_word(s, hash_table):
    # calls hash_word to determine the index at the word should be inserted for the initial hash function
    idx = hash_word(s, len(hash_table))
    # returns true if the word is in the hash table. This is without the step size
    if hash_table[idx] == s:
        return True
    else:
        constant = 0
        hash_index = idx
        if hash_table[hash_index] == s:
            return True
        else:
            # This uses the step size to determine if the word is in the hash table
            # returns true if it is, false otherwise
            stepper = step_size(s, 11)
            while len(hash_table[hash_index]) != 0:
                hash_index = (constant * stepper + idx) % len(hash_table)
                if hash_table[hash_index] == s:
                    return True
                else:
                    constant += 1
        return False


# Input: string s, a hash table, and a hash_memo
#        recursively finds if the string is reducible
# Output: if the string is reducible it enters it into the hash memo
#         and returns True and False otherwise
def is_reducible(s, hash_table, hash_memo):
    # The base case for which the function returns true if the word string is a i or o
    if len(s) == 1 and s.lower() in ['a', 'i', 'o']:
        return True
    # returns true if the word is in the hash memo
    elif find_word(s, hash_memo):
        return True
    # recursive loop where each letter is removed to see if it produces a viable string
    elif find_word(s, hash_table):
        for i in range(0, len(s)):
            reduced = s[0:i] + s[i + 1:len(s)]
            if is_reducible(reduced, hash_table, hash_memo):
                insert_word(s, hash_memo)
                return True
    return False


# Input: string_list a list of words
# Output: returns a list of words that have the maximum length
def get_longest_words(string_list):
    # sorts the list by the length of the string and returns the string with the maximum length
    overall = []
    string_list.sort(key=len)
    longest = string_list[len(string_list) - 1]
    return longest


def main():
    # create an empty word_list
    word_list = []
    # read words from words.txt and append to word_list
    for line in sys.stdin:
        word_list.append(line.strip())

    # find length of word_list
    # print(len(word_list))

    # determine prime number N that is greater than twice
    # the length of the word_list
    length = 2 * len(word_list)

    # create an empty hash_list
    hash_list = []

    # populate the hash_list with N blank strings
    for i in range(length):
        hash_list.append("")

    # hash each word in word_list into hash_list
    # for collisions use double hashing
    for i in range(len(word_list)):
        insert_word(word_list[i], hash_list)

    # create an empty hash_memo of size M
    # we do not know a priori how many words will be reducible
    # let us assume it is 10 percent (fairly safe) of the words
    # then M is a prime number that is slightly greater than
    # 0.2 * size of word_list
    hash_memo = []
    length = 0.2 * len(word_list)
    while not is_prime(length):
        length += 1

    # populate the hash_memo with M blank strings
    for i in range(len(word_list)):
        hash_memo.append("")

    # create an empty list reducible_words
    reducible_words = []
    # for each word in the word_list recursively determine
    # if it is reducible, if it is, add it to reducible_words
    # as you recursively remove one letter at a time check
    for i in word_list:
        if is_reducible(i, hash_list, hash_memo):
            reducible_words.append(i)

    # first if the sub-word exists in the hash_memo. if it does
    # then the word is reducible and you do not have to test
    # any further. add the word to the hash_memo.
    start = time.time()
    # find the largest reducible words in reducible_words
    longest = get_longest_words(reducible_words)
    end = time.time()
    # print the reducible words in alphabetical order
    print(longest)
    print(end - start)


# for each word in the word_list recursively determine
# if it is reducible, if it is, add it to reducible_words
# as you recursively remove one letter at a time check
# first if the sub-word exists in the hash_memo. if it does
# then the word is reducible and you do not have to test
# any further. add the word to the hash_memo.

# find the largest reducible words in reducible_words

# print the reducible words in alphabetical order
# one word per line

if __name__ == "__main__":
    # from time import perf_counter
    # t1_start = perf_counter()
    main()
# t1_stop = perf_counter()
# print (t1_stop - t1_start)