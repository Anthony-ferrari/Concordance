# hash_map.py
# ===================================================
# Implement a hash map with chaining
# ===================================================

class SLNode:
    def __init__(self, key, value):
        self.next = None
        self.key = key
        self.value = value

    def __str__(self):
        return '(' + str(self.key) + ', ' + str(self.value) + ')'


class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def add_front(self, key, value):
        """Create a new node and inserts it at the front of the linked list
        Args:
            key: the key for the new node
            value: the value for the new node"""
        new_node = SLNode(key, value)
        new_node.next = self.head
        self.head = new_node
        self.size = self.size + 1

    def remove(self, key):
        """Removes node from linked list
        Args:
            key: key of the node to remove """
        if self.head is None:
            return False
        if self.head.key == key:
            self.head = self.head.next
            self.size = self.size - 1
            return True
        cur = self.head.next
        prev = self.head
        while cur is not None:
            if cur.key == key:
                prev.next = cur.next
                self.size = self.size - 1
                return True
            prev = cur
            cur = cur.next
        return False

    def contains(self, key):
        """Searches linked list for a node with a given key
        Args:
        	key: key of node
        Return:
        	node with matching key, otherwise None"""
        if self.head is not None:
            cur = self.head
            while cur is not None:
                if cur.key == key:
                    return cur
                cur = cur.next
        return None

    def __str__(self):
        out = '['
        if self.head != None:
            cur = self.head
            out = out + str(self.head)
            cur = cur.next
            while cur != None:
                out = out + ' -> ' + str(cur)
                cur = cur.next
        out = out + ']'
        return out


def hash_function_1(key):
    hash = 0
    for i in key:
        hash = hash + ord(i)
    return hash


def hash_function_2(key):
    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash


class HashMap:
    """
    Creates a new hash map with the specified number of buckets.
    Args:
        capacity: the total number of buckets to be created in the hash table
        function: the hash function to use for hashing values
    """

    def __init__(self, capacity, function):
        self._buckets = []
        for i in range(capacity):
            self._buckets.append(LinkedList())
        self.capacity = capacity
        self._hash_function = function
        self.size = 0

    def clear(self):  # works
        """
        Empties out the hash table deleting all links in the hash table.
        """
        self._buckets = []
        for i in range(self.capacity):
            self._buckets.append(LinkedList())
        self.size = 0

    def get(self, key):  # works
        """
        Returns the value with the given key.
        Args:
            key: the value of the key to look for
        Return:
            The value associated to the key. None if the link isn't found.
        """
        # use hash function and capacity to get index
        index = self._hash_function(key) % self.capacity
        # the linkedlist at the index in hash table
        linkedList = self._buckets[index]
        # if the hash table has the key then we use contains function to return the value of the key
        if self.contains_key(key):
            return linkedList.contains(key).value
        # we dont do anything and return None
        else:
            return None

    def resize_table(self, capacity):  # works with change to put
        """
        Resizes the hash table to have a number of buckets equal to the given
        capacity. All links need to be rehashed in this function after resizing
        Args:
            capacity: the new number of buckets.
        """
        # new hash:
        # updates capacity
        self.capacity = capacity
        # creates new hash table (list)
        new = []
        # fills hash table with empty linked lists
        for k in range(capacity):
            new.append(LinkedList())
        # fills the linked lists with the nodes in the linked lists from original buckets
        for i in self._buckets:
            # if i.head is not None:
            cur = i.head
            while cur is not None:
                key = cur.key
                value = cur.value
                self.put_helper(key, value, new)
                cur = cur.next
        # empties out self._buckets of any nodes
        self.clear()
        # transfer over nodes from new hash table to self._buckets
        for j in new:
            # if j.head is not None:
            cur = j.head
            while cur is not None:
                key = cur.key
                value = cur.value
                self.put_helper(key, value)
                cur = cur.next

    def put(self, key, value):  # works
        """
        Updates the given key-value pair in the hash table. If a link with the given
        key already exists, this will just update the value and skip traversing. Otherwise,
        it will create a new link with the given key and value and add it to the table
        bucket's linked list.

        Args:
            key: they key to use to has the entry
            value: the value associated with the entry
            hashtable: the hash table to use
        """
        self.put_helper(key, value)

    def put_helper(self, key, value, hashtable=None):
        # directions:
        # 1. put key through hash function and get index
        # 2. give key to contains function for LL and if none, then add to front of LL
        # 3. Otherwise update value
        # 4. increase size but not capacity

        # three situations: 1) LL is empty 2) has nodes and key not there 3) has nodes and key is there

        # getting the index to put the node at
        index = self._hash_function(key) % self.capacity
        # checks that we use the correct hash table
        if hashtable is None:
            linkedList = self._buckets[index]
        else:
            linkedList = hashtable[index]
        # when the linked list does not have the key-value pair
        if linkedList.contains(key) is None:
            # # 1
            # if linkedList.head is None:
            linkedList.add_front(key, value)
            self.size += 1
        # when the LL does have the key-value pair
        else:
            cur = linkedList.head
            while cur is not None:
                if cur.key == key:
                    cur.value = value
                cur = cur.next

    def remove(self, key):  # works
        """
        Removes and frees the link with the given key from the table. If no such link
        exists, this does nothing. Remember to search the entire linked list at the
        bucket.
        Args:
            key: they key to search for and remove along with its value
        """
        # directions:
        # 1. link exists and have to free it
        # 2. link does not exist and nothing to be done

        # gets index to reach LL to remove node from
        index = self._hash_function(key) % self.capacity
        linkedList = self._buckets[index]
        # check if key-value pair exists and then removes it. updates size
        if self.contains_key(key):
            # free it
            linkedList.remove(key)
            self.size -= 1

    def contains_key(self, key):  # works
        """
        Searches to see if a key exists within the hash table

        Returns:
            True if the key is found False otherwise

        """
        # gets index to reach LL to check if node exists
        index = self._hash_function(key) % self.capacity
        linkedList = self._buckets[index]
        cur = linkedList.head
        # traverse the linked list for key-value pair
        while cur is not None:
            if cur.key == key:
                return True
            cur = cur.next
        # key-value pair not in LL
        return False

    def empty_buckets(self):  # works
        """
        Returns:
            The number of empty buckets in the table
        """
        # set counter
        count = 0
        # traverse hash table
        for i in self._buckets:
            # if the head of LL is empty then there are no nodes there
            if i.head is None:
                # increase counter
                count += 1
        return count

    def table_load(self):  # works
        """
        Returns:
            the ratio of (number of links) / (number of buckets) in the table as a float.

        """
        # number of links (elements in LL per index)
        # set counter
        count = 0
        # traverse hash table
        for linkedList in self._buckets:
            # increases with the size of each linkedList
            count += linkedList.size
        # computes ratio using formula in docstring
        ratio = count / self.capacity
        return ratio

    def __str__(self):
        """
        Prints all the links in each of the buckets in the table.
        """

        out = ""
        index = 0
        for bucket in self._buckets:
            out = out + str(index) + ': ' + str(bucket) + '\n'
            index = index + 1
        return out
