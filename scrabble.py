import numpy as np
from itertools import combinations
import sys
import argparse
import os
import pickle
from functools import lru_cache


class Node:
    def __init__(self):
        self.letter = None
        self.children = []
        self.words = []


prefix_tree = None
@lru_cache(maxsize=99999999)
def WordsWithLettersLookupPrefixTree(prefix, d):
    global prefix_tree
    fname = 'prefix_tree'
    if prefix_tree == None and os.path.exists(fname):
        print(f'WordsWithLettersLookupPrefixTree loading prefix tree')
        with open(fname, 'rb') as f:
            prefix_tree = pickle.load(f)
        print(f'WordsWithLettersLookupPrefixTree loading prefix tree... done')

    if prefix_tree == None:
        print(f'WordsWithLettersLookupPrefixTree can not run, we do not have a prefix_tree, please run scrabble_make_prefix_tree.py')
        sys.exit(1)
    else:
        node = prefix_tree
        for letter in prefix:
            for child in node.children:
                if letter == child.letter:
                    node = child
                    break

        if node:
            return node.words
        else:
            return []


@lru_cache(maxsize=99999999)
def WordsWithLettersLookup(prefix, d):
    cache_dir = 'cache'
    path = os.path.join(cache_dir, prefix)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            words = pickle.load(f)
    else:
        n_letters = len(prefix)
        t_words = list(d.words)
#         for letter in prefix:
# HERE - we only want words containing exactly our letters, duplicates exactly right, containing other letters too is not ok...
            # t_words = [x for x in t_words if letter in x and len(x) <= n_letters]
        # t_words = [x for x in t_words if len(x) == n_letters and x[0] in prefix and sorted(x) == prefix]
        t_words = [x for x in t_words if len(x) == n_letters and x[0] in prefix and ''.join(sorted(x)) == prefix]
#        print(f'found words {t_words} for prefix:{prefix}')
        words = t_words
        os.makedirs(cache_dir, exist_ok=True)
        with open(path, 'wb') as f:
            pickle.dump(words, f)

    return words


class Dictionary:
    def __init__(self):
        # self.words = open("/usr/share/dict/words").readlines()
        self.words = open("/usr/share/dict/words").read().splitlines()

    def prefix_match(self, prefix):
        my_found_words = [x for x in self.words if x[0:len(prefix)] == prefix]
        return my_found_words

    def words_from_letters(self, letters, startsWith=None, endsWith=None, minLength=4):
        all_words = []
        for word_length in range(minLength, len(letters) + 1):
            # gather all combinations of letters of this length
            letter_combos = combinations(letters, word_length)
            for letter_combo in letter_combos:
                if startsWith and startsWith not in letter_combo:
                    continue
                if endsWith and endsWith not in letter_combo:
                    continue
                words = self.words_with_letters_exactly(letter_combo, startsWith=startsWith, endsWith=endsWith)
                # print(f'words_from_letters:: considering combo: {letter_combo}, got words {words}')
                all_words += words

        return all_words
            

    def words_with_letters_exactly(self, letters, startsWith=None, endsWith=None): # all words that contain exactly these letters
        lists = []
        n_letters = len(letters)
        t_words = list(self.words)
        prefix = ''.join(sorted(letters))
        t_words = WordsWithLettersLookupPrefixTree(prefix, self)
#        for letter in letters:
#            if startsWith and endsWith:
#                tt_words = [x for x in t_words if letter in x and len(x) <= n_letters and x[0] == startsWith and x[-1] == endsWith]
#            elif startsWith:
#                tt_words = [x for x in t_words if letter in x and len(x) <= n_letters and x[0] == startsWith]
#            elif endsWith:
#                tt_words = [x for x in t_words if letter in x and len(x) <= n_letters and x[-1] == endsWith]
#            else:
#                tt_words = [x for x in t_words if letter in x and len(x) <= n_letters]
        if startsWith and endsWith:
            tt_words = [x for x in t_words if len(x) <= n_letters and x[0] == startsWith and x[-1] == endsWith]
        elif startsWith:
            tt_words = [x for x in t_words if len(x) <= n_letters and x[0] == startsWith]
        elif endsWith:
            tt_words = [x for x in t_words if len(x) <= n_letters and x[-1] == endsWith]
        else:
            tt_words = [x for x in t_words if len(x) <= n_letters]
        t_words = tt_words

        # remove words with extra letters
        final_words = []
        for word in t_words:
            add_word = True
            for letter in word:
                if letter not in letters:
                    add_word = False
                    break
            if add_word:
                final_words.append(word)
                    

        return final_words
    
#        intersection_list = []
#        first = True
#        for next_list in lists:
#            if first:
#                intersection_list = next_list
#                first = False
#            else:
#                intersection_list = list(set(intersection_list) & set(next_list))
#                if len(intersection_list) == 0:
#                    return []
#        return intersection_list 


class Board:
    def __init__(self):
        board = np.zeros((15, 15))
        self.tw = [( 0, 3), ( 0,11), ( 3, 0), (3, 14),
                   (11, 0), (14, 3), (11,14), (14,11)]
        self.dw = [( 1, 5), ( 1, 9), ( 3, 7), (5, 1 ),
                   ( 5,13), ( 7, 3), ( 7,11), (9, 1 ),
                   ( 9,13), (11, 7), (13, 5), (13, 9)]
        self.tl = [( 0, 6), ( 0, 8), (3, 3 ), (3, 11),
                   ( 5, 5), ( 5, 9), (6, 0 ), (6, 14),
                   ( 8, 0), ( 8,14), (9, 5 ), (9, 9 ),
                   (11, 3), (11,11), (14, 6), (14, 8)]
        self.dl = [( 1, 2), ( 1,12), ( 2, 1), ( 2, 4),
                   ( 2,10), ( 2,13), ( 4, 1), ( 4, 6),
                   ( 4, 8), ( 4,12), ( 6, 4), ( 6,10),
                   ( 8, 4), ( 8,10), (12, 1), (12, 4),
                   (12,10), (12,13), (13, 2), (13,12)]

        self.bag = list('a' * 9 + 
                   'b' * 2 +
                   'c' * 2 +
                   'd' * 5 +
                   'e' * 13 +
                   'f' * 2 +
                   'g' * 3 +
                   'h' * 4 +
                   'i' * 8 +
                   'j' * 1 +
                   'k' * 1 +
                   'l' * 4 +
                   'm' * 2 +
                   'n' * 5 +
                   'o' * 8 +
                   'p' * 2 +
                   'q' * 1 +
                   'r' * 6 +
                   's' * 5 +
                   't' * 7 +
                   'u' * 4 +
                   'v' * 2 +
                   'w' * 2 +
                   'x' * 1 +
                   'y' * 2 +
                   'z' * 1 +
                   ' ' * 2)

        self.letter_values = dict([('a', 1), 
                              ('b', 4), 
                              ('c', 4),
                              ('d', 4),
                              ('e', 1),
                              ('f', 4),
                              ('g', 3),
                              ('h', 3),
                              ('i', 1),
                              ('j', 10),
                              ('k', 5),
                              ('l', 2),
                              ('m', 4),
                              ('n', 2),
                              ('o', 1),
                              ('p', 4),
                              ('q', 10),
                              ('r', 1),
                              ('s', 1),
                              ('t', 1),
                              ('u', 2),
                              ('v', 5),
                              ('w', 4),
                              ('x', 8),
                              ('y', 3),
                              ('z', 10)])

    def get_space_modifier(self, space):
        x, y = space
        if (x,y) in self.tw:
            return 'tw'
        elif (x,y) in self.dw:
            return 'dw'
        elif (x,y) in self.tl:
            return 'tl'
        elif (x,y) in self.dl:
            return 'dl'
        else:
            return None

    def get_word_value(self, space, orientation, word):
        x, y = space
        word_multiplier = 1
        word_value = 0
        for letter in word:
            letter_value = self.letter_values[letter]
            space_modifier = self.get_space_modifier((x, y))
            if space_modifier == 'tw':
                word_multiplier = 3
            elif space_modifier == 'dw' and word_multiplier == 1:
                word_multiplier = 2
            elif space_modifier == 'tl':
                letter_value *= 3 
            elif space_modifier == 'dl':
                letter_value *= 2 
            word_value += letter_value

            if orientation == 'right':
                x += 1
            elif orientation == 'down':
                y += 1

        word_value *= word_multiplier 

        return word_value

    def sort_by_value(self, words):
        x = {}
        for word in words:
            x[word] = self.get_word_value((7, 4), 'right', word)
            # print(f'added word {word} at value {x[word]}')
        out_words = []
        word_values = {k: v for k, v in sorted(x.items(), key=lambda item: item[1], reverse=True)}
        for key in word_values:
            out_words.append(key)

        return out_words

b = Board()
d = Dictionary()
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--minlength", type=int)
parser.add_argument("-l", "--letters", type=str)
parser.add_argument("-p", "--pos", type=int)
parser.add_argument("-q", "--posletter", type=str)
parser.add_argument("-s", "--startswith", type=str)
parser.add_argument("-e", "--endswith", type=str)
args = parser.parse_args()

min_length = args.minlength
letters = list(args.letters)
starts_with = args.startswith
ends_with = args.endswith
all_words = d.words_from_letters(letters, minLength=min_length, startsWith=starts_with, endsWith=ends_with)
all_words = b.sort_by_value(all_words)
print(f'words from letters {letters} are {all_words}')

pos = args.pos
pos_letter = args.posletter
if pos and pos_letter:
    words_position = [x for x in all_words if pos < len(x) and x[pos] == pos_letter]
    words_position = b.sort_by_value(words_position)
    print(f'words from letters {letters} where {pos_letter} is at index {pos} are {words_position}')

print(f'done...')
sys.exit(1)

for space in [(1,1), (2,2), (3,3), (0,3)]:
    mod = b.get_space_modifier(space)
    print(f'{space} has modifier {mod}')

for space_word in [((0,3), 'right', 'bizz')]:
    space, orientation, word = space_word
    word_value = b.get_word_value(space, orientation, word)
    print(f'{word} at {space} going {orientation} has value {word_value}')


for prefix in ['chai', 'pop', 'wa']:
    words = d.prefix_match(prefix)
    print(f'words with prefix {prefix} are {words}')

letters = ['v', 'i', 'e', 'e']
words = d.words_with_letters_exactly(letters)
print(f'words with exactly letters {letters} are {words}')

# sys.exit(0)

# for letters in [['a', 'e', 'b'], ['u', 'y', 'f', 'z', 's', 'e', 't', 'l', 'm', 'a']]:
for letters in [['v', 'k', 'i', 'e', 'g', 'e', 'r', 'b']]:
    words = d.words_with_letters_exactly(letters)
    print(f'words with exactly letters {letters} are {words}')

    all_words = d.words_from_letters(letters)
    print(f'words from letters {letters} are {all_words}')

    pos = 1
    pos_letter = 'b'
    words_position = [x for x in all_words if x[pos] == pos_letter]
    print(f'words from letters {letters} where {pos_letter} is at index {pos} are {words_position}')

    pos = 2
    pos_letter = 'b'
    words_position = [x for x in all_words if x[pos] == pos_letter]
    print(f'words from letters {letters} where {pos_letter} is at index {pos} are {words_position}')

    startsWith = 'm'
    endsWith = 'b'
    all_words = d.words_from_letters(letters, startsWith=startsWith)
    print(f'words from letters {letters} starting with {startsWith} are {all_words}')
    all_words = d.words_from_letters(letters, endsWith=endsWith)
    print(f'words from letters {letters} ending with {endsWith} are {all_words}')
    all_words = d.words_from_letters(letters, startsWith=startsWith, endsWith=endsWith)
    print(f'words from letters {letters} starting with {startsWith} and ending with {endsWith} are {all_words}')
