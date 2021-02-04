from collections import Counter
from functools import reduce
from typing import List

import nltk
nltk.download('brown')


word_dict = nltk.corpus.brown.words()
COUNTS = Counter(word_dict)


def __pdist(counter):
    # "Make a probability distribution, given evidence from a Counter."
    n = sum(counter.values())
    return lambda x: counter[x] / n


P = __pdist(COUNTS)


def __pwords(words: List[str]) -> int:
    # "Probability of words, assuming each word is independent of others."
    return reduce((lambda x, y: x * y), [P(w) for w in words])


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
        segments = max(candidates, key=__pwords)
        if len(segments) == len(text):  # this will be the case if no match
            return [text]
        else:
            return segments
