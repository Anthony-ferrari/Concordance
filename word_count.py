# word_count.py
# ===================================================
# Implement a word counter that counts the number of
# occurrences of all the words in a file. The word
# counter will return the top X words, as indicated
# by the user.
# ===================================================

import re
from hashmap import HashMap

"""
This is the regular expression used to capture words. It could probably be endlessly
tweaked to catch more words, but this provides a standard we can test against, so don't
modify it for your assignment submission.
"""
rgx = re.compile("(\w[\w']*\w|\w)")


def hash_function_2(key):
    """
    This is a hash function that can be used for the hashmap.
    """

    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash


def top_words(source, number):
    """
    Takes a plain text file and counts the number of occurrences of case insensitive words.
    Returns the top `number` of words in a list of tuples of the form (word, count).

    Args:
        source: the file name containing the text
        number: the number of top results to return (e.g. 5 would return the 5 most common words)
    Returns:
        A list of tuples of the form (word, count), sorted by most common word. (e.g. [("a", 23), ("the", 20), ("it", 10)])
    """

    keys = set()

    ht = HashMap(2500, hash_function_2)

    # This block of code will read a file one word as a time and
    # put the word in `w`. It should be left as starter code.
    with open(source) as f:
        for line in f:
            words = rgx.findall(line)
            for w in words:
                # make the word lower case for case insensitivity
                lower_case = w.lower()
                # if hashmap contains the words then use put function to update value
                if ht.contains_key(lower_case):
                    ht.put(lower_case, ht.get(lower_case) + 1)
                    keys.add(lower_case)
                else:
                    # use put function to insert word
                    ht.put(lower_case, 1)
                    keys.add(lower_case)
    # create list
    tuple_list = []
    for i in keys:
        tuple_list.append((i, ht.get(i)))

    # sort the list in reverse by the value
    # the key used here is the value given by lambda function x: x[1]
    # x[1] will be value (no need to convert to int or float since already int)
    sorted_tuple_list = sorted(tuple_list, reverse=True, key=lambda x: x[1])
    return sorted_tuple_list[:number]

