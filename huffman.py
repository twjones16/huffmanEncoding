# Algo HW4: Huffman Encoding
# PARTNERS: Kira Murphy and Tim Jones

import sys
import math
from typing import Dict, List, Tuple
from myheap import heap

def load_file(fn: str) -> Dict[str, int]:
    """
    Creates a character frequency dictionary given a file
    :param fn: Path to file
    :return: Frequency dictionary
    """
    freq = dict()
    f = open(fn)
    for line in f:
        for ch in line:
            if ch not in freq:
                freq[ch] = 0
            freq[ch] += 1
    return freq


class Tree:
    # Simple binary tree class
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self

    def __repr__(self):
        return str(self.left)


def build_tree(myheap: heap) -> Tree:
    """
    Builds a huffman tree for a given heap
    :param myheap: A heap of tuples (freq, Tree)
    :return: A huffman tree
    """
    while myheap.__len__() > 1:
        left = myheap.delete_root()
        right = myheap.delete_root()
        new_tree = Tree(left[1], right[1])
        myheap.insert((left[0] + right[0], new_tree))
        myheap.siftup(myheap.__len__() - 1)

    return myheap.delete_root()[1]


def build_heap(freq) -> heap:
    """
    Builds a heap of frequencies with a tuple containing a frequency and the corresponding tree
    :param freq: The dictionary of frequencies
    :return: The heap with frequencies and trees
    """
    h = heap([(freq[k], Tree(k, None)) for k in freq])
    return h


def get_codes(tree: Tree, codes: List[Tuple[str, str]], code: str) -> List[Tuple[str, str]]:
    """
    :param tree: The huffman tree that is being traversed
    :param codes: The list of characters with their current huffman encoding
    :param code: The current huffman code
    :return: The list of characters with their updated huffman encoding
    """
    # Characters are only stored in left nodes so check if this is a character
    if type(tree.left) == str:
        codes.append((tree.left, code))
    # If the left tree is not a string and not None, then we want to traverse left and add a 0
    # to the code
    if type(tree.left) != str and tree.left != None:
        get_codes(tree.left, codes, code + '0')
    # If the right tree is not a string and not None, then we want to traverse right and add a 1
    # to the code
    if type(tree.right) != str and tree.right != None:
        get_codes(tree.right, codes, code + '1')

    return codes


def no_compression_size(freq: Dict) -> int:
    """
    Returns the size of the file (in bytes) when no compression is performed
    :param freq: The frequency dictionary
    :return: The size of the file in bytes
    """
    total = 0
    for k in freq:
        # Add the frequency of each character because each character is one byte
        total += freq[k]
    return total


def compression_size(freq: Dict, lst: List) -> int:
    """
    Returns the size of the file (in bytes) when compression is performed
    :param freq: The frequency dictionary
    :param lst: The list of huffman codes
    :return: The size of the file in bytes
    """
    total = 0
    for item in lst:
        # Get each frequency
        frequency = freq[item[0]]
        # Multiply the frequency by the size of the corresponding huffman encoding and add total
        total += frequency * len(item[1])
    # Divide by 8 because total is currently in bits and take the ceiling of this
    return math.ceil(total // 8)


if __name__ == "__main__":
    sysargs = sys.argv
    # Load the given file by getting the list of character frequencies
    freq = load_file(sysargs[1])
    # Create a heap
    myheap = build_heap(freq)
    # Create a huffman tree using the heap
    huffman_tree = build_tree(myheap)
    # Get the codes of the huffman tree
    huffman_codes = get_codes(huffman_tree, [], "")
    # Print out the size in bytes with no compression and with our compression algoirthm
    print("The size of the file without compression is ", no_compression_size(freq), " bytes.")
    print("The size of the file with compression is ", compression_size(freq, huffman_codes), " bytes.")
