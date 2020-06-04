# Concordance
A hash map implementation of a concordance program. 
This hash map uses a hash table of buckets, each containing a linked list of hash links. 
Each hash link stores the key-value pair (string and integer in this case) and a pointer to the next link in the list. 
This hash map contains the following methods:  clear, get, resize_table, put, put_helper, remove, contains_key, empty_buckets, table_load methods.

The word_count file is the concordance program. 
Word_count.py takes an input document, computes the number of times each word was used in the document, and returns the top X words and associated counts.
Word_count.py stores each word in a hash table(functionality from hash map file) and keeps track of how many times the word appears.
