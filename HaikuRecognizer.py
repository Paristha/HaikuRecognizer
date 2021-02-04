import re
from num2words import num2words
from typing import List, Any
import nltk
from nltk.corpus import cmudict
from nltk.tokenize import SyllableTokenizer
from WordSplitter import segment
nltk.download('cmudict')


pro_dict = cmudict.dict()
ssp = SyllableTokenizer()


def count_syllables(pronunciation: List[str]) -> int:
    # Example input: ['T', 'R', 'IH1', 'M', 'D'], the pronunciation for 'trimmed'
    # Each string in the pronunciation that contains a digit is a syllable
    syllables = len([syl for syl in pronunciation if any(char.isdigit() for char in list(syl))])
    # syllables is now the number of strings in pronunciation that contain any digits
    return syllables


def sanitize_words(words):
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


def check_syllables(line_length, line_syllables, words, max_syllables):
    while line_syllables < max_syllables:
        word = words.pop(0)
        line_length += 1
        if pro_dict.get(word, False) is not False:
            pronunciations = pro_dict[word]
            while len(pronunciations) > 1:
                _, pro_syll = check_syllables(line_length, line_syllables + count_syllables(pronunciations[0]), words.copy(), max_syllables)
                if pro_syll == max_syllables:
                    return _, pro_syll
                pronunciations.pop(0)
            line_syllables += count_syllables(pronunciations[0])
        else:
            line_syllables += len(ssp.tokenize(word))
    return line_length, line_syllables


def haiku(corpus: str) -> Any:
    sentence = ' '.join(corpus).lower()
    url_pattern = re.compile("(?P<url>https?://[^\s]+)")
    links = re.findall(url_pattern, sentence)
    sentence = url_pattern.sub("link", sentence)
    words = sentence.split()

    sanitize_words(words)
    # Can only potentially be a haiku if there are 3 or more words (1 per line)
    # and 17 or fewer words (1 per syllable)
    if 17 >= len(words) >= 3:
        first_line_len, first_line_syll = check_syllables(0, 0, words.copy(), 5)
        if first_line_syll != 5:
            return False
        first_line = [words.pop(0) for _ in range(0, first_line_len)]
        second_line_len, second_line_syll = check_syllables(0, 0, words.copy(), 7)
        if second_line_syll != 7:
            return False
        second_line = [words.pop(0) for _ in range(0, second_line_len)]
        third_line_len, third_line_syll = check_syllables(0, 0, words.copy(), 5)
        if third_line_syll != 5 or third_line_len != len(words):
            return False
        third_line = [words.pop(0) for _ in range(0, third_line_len)]
        full_haiku = ' '.join(first_line) + "\n" + ' '.join(second_line) + "\n" + ' '.join(third_line)
        return full_haiku
    return False
