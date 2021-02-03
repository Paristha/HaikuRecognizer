# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re
import sys
from collections import Counter
from functools import reduce
from num2words import num2words
from typing import List
import nltk
from nltk.corpus import cmudict
from nltk.tokenize import SyllableTokenizer
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
        segments = max(candidates, key=pwords)
        if len(segments) == len(text):  # this will be the case if no match
            return [text]
        else:
            return segments

ssp = SyllableTokenizer()

def count_syllables(pronunciation: List[str]) -> int:
    # Example input: ['T', 'R', 'IH1', 'M', 'D'], the pronunciation for 'trimmed'
    # Each string in the pronunciation that contains a digit is a syllable
    syllables = len([syl for syl in pronunciation if any(char.isdigit() for char in list(syl))])
    # syllables is now the number of strings in pronunciation that contain any digits
    return syllables

def sanitizeWordList(words):
    i = 0
    while i < len(words):
        if words[i][0] == '#':
            segments = segment(words[i][1:])
            words.pop(i)
            words[i:i] = segments
        parts = [part for part in re.split(r'[^\'\w]+', words[i]) if len(part) > 0]
        words.pop(i)
        words[i:i] = parts
        if words[i].isdigit():
            number = words.pop(i)
            number_words = num2words(number)
            words[i:i] = [word for word in re.split(r'[^\w]+', number_words)]
        i += 1

def checkSyllables(line_length, line_syllables, words, max_syllables):
    while line_syllables < max_syllables:
        word = words.pop(0)
        line_length += 1
        if pro_dict.get(word, False) is not False:
            pronunciations = pro_dict[word]
            while len(pronunciations) > 1:
                haiku = checkSyllables(line_length, line_syllables + count_syllables(pronunciations[0]), words.copy(), max_syllables)
                if haiku[1] == max_syllables:
                    return haiku
                pronunciations.pop(0)
            line_syllables += count_syllables(pronunciations[0])
        else:
            line_syllables += len(ssp.tokenize(word))
    return [line_length, line_syllables]

def checkIfHaiku(words):
    # Can only potentially be a haiku if there are 3 or more words (1 per line) and 17 or fewer words (1 per syllable)
    if 17 >= len(words) >= 3:

        first_line = []
        first_line_syll = 0
        while first_line_syll < 5:
            word = words.pop(0)
            first_line.append(word)
            if pro_dict.get(word, False) is not False:
                first_line_syll += count_syllables(pro_dict[word][0])
            else:
                first_line_syll += len(ssp.tokenize(word))
        if first_line_syll != 5:
            return False
        second_line = []
        second_line_syll = 0
        while second_line_syll < 7:
            word = words.pop(0)
            second_line.append(word)
            if pro_dict.get(word, False) is not False:
                second_line_syll += count_syllables(pro_dict[word][0])
            else:
                second_line_syll += len(ssp.tokenize(word))
        if second_line_syll != 7:
            return False
        third_line = []
        third_line_syll = 0
        while third_line_syll < 5:
            word = words.pop(0)
            third_line.append(word)
            if pro_dict.get(word, False) is not False:
                third_line_syll += count_syllables(pro_dict[word][0])
            else:
                third_line_syll += len(ssp.tokenize(word))
        if third_line_syll != 5 or len(words) > 0:
            return False
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sentence = ' '.join(sys.argv[1:]).lower()

    url_pattern = re.compile("(?P<url>https?://[^\s]+)")
    links = re.findall(url_pattern, sentence)
    sentence = url_pattern.sub("link", sentence)
    words = sentence.split()

    sanitizeWordList(words)

    print(' '.join(words))

    # words = word_tokenize(sentence)
    # print(words)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
