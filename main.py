# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re
import sys
from collections import Counter
from functools import reduce
from typing import List
import nltk
from nltk.corpus import cmudict
from nltk.tokenize import word_tokenize
nltk.download('brown')
nltk.download('cmudict')
nltk.download('punkt')


pro_dict = cmudict.dict()

word_dict = nltk.corpus.brown.words()
COUNTS = Counter(word_dict)


def pdist(counter):
    # "Make a probability distribution, given evidence from a Counter."
    n = sum(counter.values())
    return lambda x: counter[x]/n


P = pdist(COUNTS)


def pwords(words: List[str]):
    # "Probability of words, assuming each word is independent of others."
    return reduce((lambda x, y: x*y), [P(w) for w in words])


def splits(text, start=0, l=20):
    # "Return a list of all (first, rest) pairs; start <= len(first) <= L."
    return [(text[:i], text[i:]) for i in range(start, min(len(text), l) + 1)]


def segment(text):
    # "Return a list of words that is the most probable segmentation of text."
    if not text:
        return []
    else:
        candidates = ([first] + segment(rest)
                      for (first, rest) in splits(text, 1))
        return max(candidates, key=pwords)


def count_syllables(self, pronunciation: List[str]) -> int:
    # Example input: ['T', 'R', 'IH1', 'M', 'D'], the pronunciation for 'trimmed'
    # Each string in the pronunciation that contains a digit is a syllable
    syllables = len([syl for syl in pronunciation if any(char.isdigit() for char in list(syl))])
    # syllables is now the number of strings in pronunciation that contain any digits
    return syllables


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sentence = ' '.join(sys.argv[1:])
    url_pattern = re.compile("(?P<url>https?://[^\s]+)")
    sentence = url_pattern.sub("link", sentence)
    words = sentence.split()

    i = 0
    while i < len(words):
        if words[i][0] == '#' or pro_dict.get(words[i], False) is False:
            words[i:i] = segment(words[i][1:])
        words[i:i] = [word for word in re.split(r'[^\'\w]+', words[i]) if len(word) > 0]
        i += 1

    print(' '.join(words))

    # words = word_tokenize(sentence)
    # print(words)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
