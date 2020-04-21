# scrabble_cheat

This utility helps you cheat at scrabble.

## Features
* uses pre-loaded dictionary on linux/bsd/osx systems
* produce words longer than a minimum length
* specify the letters in your rack (TODO add blank tiles)
* constrain results to words with a specific letter in a specific position (0-based)
* constrain results to words that start with a specific letter
* constrain results to words that end with a specific letter
```
usage: scrabble.py [-h] [-m MINLENGTH] [-l LETTERS] [-p POS] [-q POSLETTER]
                   [-s STARTSWITH] [-e ENDSWITH]

optional arguments:
  -h, --help            show this help message and exit
  -m MINLENGTH, --minlength MINLENGTH
  -l LETTERS, --letters LETTERS
  -p POS, --pos POS
  -q POSLETTER, --posletter POSLETTER
  -s STARTSWITH, --startswith STARTSWITH
  -e ENDSWITH, --endswith ENDSWITH
```


## Requirements
* Python 3.6+
* numpy
* hmm, I really need a `requirements.txt`

## Bootstrap
You must generate the dictionary with:
```
python scrabble_make_prefix_tree.py
```
