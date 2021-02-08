from collections import Counter
from functools import reduce
from typing import List

import nltk
from nltk.util import ngrams
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
word_dict = nltk.corpus.brown.words()

word_fd = nltk.FreqDist(word_dict)
bigram_fd = nltk.FreqDist(nltk.bigrams(word_dict))

# nltk.download('brown')



COUNTS = Counter(word_dict)


def __pdist(counter):
    # "Make a probability distribution, given evidence from a Counter."
    n = sum(counter.values())
    return lambda x: counter[x] / n


P = __pdist(COUNTS)


def __pwords(words):
    # "Probability of words, assuming each word is independent of others."
    return __product(P(w) for w in words)


def __product(nums):
    # "Multiply the numbers together.  (Like `sum`, but with multiplication.)"
    result = 1
    for x in nums:
        result *= x
    return result

"""
def __pwords(words: List[str]) -> int:
    # "Probability of words, assuming each word is independent of others."
    return reduce((lambda x, y: x * y), [P(w) for w in words])
"""


def __splits(text, start=0, length=20):
    # "Return a list of all (first, rest) pairs; start <= len(first) <= L."
    length = min(len(text), length)
    return [(text[:i], text[i:]) for i in range(start, length + 1)]


def segment(text: str) -> List[str]:
    # "Return a list of words that is the most probable segmentation of text."
    if not text:
        return []
    else:
        candidates = ([first] + segment(rest)
                      for (first, rest) in __splits(text, 1))
        return max(candidates, key=__pwords)
