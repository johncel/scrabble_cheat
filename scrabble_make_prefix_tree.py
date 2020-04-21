import numpy as np
from itertools import combinations
import sys
import argparse
import os
import pickle


class Dictionary:
    def __init__(self):
        # self.words = open("/usr/share/dict/words").readlines()
        self.words = open("/usr/share/dict/words").read().splitlines()


class Node:
    def __init__(self):
        self.letter = None
        self.children = []
        self.words = []


def make_prefix_tree(words, root):
    print(f'making prefix tree')

    # insert the word into the tree
    for raw_word in words:
        raw_word = raw_word.lower()
        word = ''.join(sorted(list(raw_word))).lower()
        # we do not care about letter order, so we will sort this word by its letters
        node = root
        for i,letter in enumerate(word):
            last_letter = False
            if i == len(word) - 1:
                last_letter = True

            found = False
            for child in node.children:
                if letter == child.letter:
                    node = child
                    found = True
                    break
            if found == False:
                new_node = Node()
                new_node.letter = letter
                node.children.append(new_node)
                node = new_node

            if last_letter:
                print(f'adding word {raw_word} to prefix tree at key:{word}')
                node.words.append(raw_word)

    print(f'making prefix tree :: DONE')

def test_prefix_tree(words, root):
    print(f'testing prefix tree')
    print(f'testing prefix tree :: generating original words statstics')
    # get stats for original list
    letter_counts_orig = {}
    num_words_orig = len(words)
    for word in words:
        word = word.lower()
        for letter in word:
            if not letter in letter_counts_orig:
                letter_counts_orig[letter] = 1
            else:
                letter_counts_orig[letter] += 1

    print(f'testing prefix tree :: DONE')

    # walk the tree and get the same counts
    print(f'testing prefix tree :: generating tree words statstics')
    letter_counts_tree = {}
    num_words_tree = 0
    def _DFS(node):
        for word in node.words:
            nonlocal num_words_tree
            num_words_tree += 1
            for letter in word:
                if not letter in letter_counts_tree:
                    letter_counts_tree[letter] = 1
                else:
                    letter_counts_tree[letter] += 1
        for next_node in node.children:
            _DFS(next_node)        

    node = root
    _DFS(node)
    print(f'testing prefix tree :: DONE')

    print(f'num_words_orig: {num_words_orig}')
    print(f'num_words_tree: {num_words_tree}')
    print(f'letter_counts_orig: {letter_counts_orig}')
    print(f'letter_counts_tree: {letter_counts_tree}')

    if num_words_orig == num_words_tree and letter_counts_orig == letter_counts_tree:
        return True
    else:
        return False

d = Dictionary()
root = Node()
make_prefix_tree(d.words, root)

if test_prefix_tree(d.words, root):
    print(f'SUCCESS ... saving tree')
    with open('prefix_tree', 'wb') as f:
        pickle.dump(root, f)
