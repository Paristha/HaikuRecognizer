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


def count_syllables(words: List[str]) -> set:
    word_syl_dict = {word: [] for word in words}

    for word in words:
        syllable_nums = cmudict_syl(word)
        if syllable_nums is False:
            syllable_nums = [ssp_syl(word)]
        word_syl_dict[word] = syllable_nums

    total_syl_set = set()
    recur_count_syl(0, word_syl_dict, words.copy(), total_syl_set)

    return total_syl_set


def recur_count_syl(syl_count: int, word_syl_dict: dict, words: List[str], total_syl_set: set):
    while words:
        word = words.pop(0)
        pronunciations = word_syl_dict[word].copy()
        while len(pronunciations) > 1:
            recur_count_syl(syl_count + pronunciations.pop(), word_syl_dict, words.copy(), total_syl_set)
        syl_count += pronunciations.pop()
    total_syl_set.add(syl_count)


def cmudict_syl(word: str) -> List[int]:
    pronunciations = pro_dict.get(word, False)
    if pronunciations is False:
        return pronunciations
    syllable_list = []
    for pronunciation in pronunciations:
        # Example input: ['T', 'R', 'IH1', 'M', 'D'], the pronunciation for 'trimmed'
        # Each string in the pronunciation that contains a digit is a syllable
        syllable_num = len([syl for syl in pronunciation if any(char.isdigit() for char in list(syl))])
        # syllable_num is now the number of strings in pronunciation that contain any digits
        # which is the number of syllables in this pronunciation of the word
        syllable_list.append(syllable_num)
    return syllable_list


def ssp_syl(word):
    # nltk's Sonority Sequencing Principle (SSP) uses a default English sonority hiearchy
    # in order to split any word into syllables
    # see https://www.nltk.org/api/nltk.tokenize.html#module-nltk.tokenize.sonority_sequencing
    # this is algorithmically done, not a lookup, so less reliable than cmudict
    syllables = ssp.tokenize(word)
    return len(syllables)


def sanitize_sentence(sentence: str, hashtags: bool = True) -> str:
    if not sentence:
        return ""
    words = sentence.split()
    i = 0
    while i < len(words):
        if words[i][0] == '#':
            hashtag = words.pop(i)
            if hashtags:
                segments = segment(hashtag[1:])
                words[i:i] = segments
        parts = [part for part in re.split(r'[^\'\w]+', words[i]) if len(part) > 0]
        words.pop(i)
        words[i:i] = parts
        if words[i].isdigit():
            number = words.pop(i)
            number_words = num2words(number)
            words[i:i] = [word for word in re.split(r'[^\w]+', number_words)]
        i += 1
    return ' '.join(words)


def find_line(words: List[str], line_syllable_num: int) -> Any:
    curr_line = [words.pop()]
    curr_line_possible_total_syllables = count_syllables(curr_line)
    while words and line_syllable_num not in curr_line_possible_total_syllables and \
            min(curr_line_possible_total_syllables) < line_syllable_num:
        curr_line.append(words.pop(0))
        curr_line_possible_total_syllables = count_syllables(curr_line)
    if line_syllable_num not in curr_line_possible_total_syllables:
        curr_line = False
    return curr_line


def get_haiku(words: List[str]) -> Any:
    # Can only potentially be a haiku if there are 3 or more words (1 per line)
    # and 17 or fewer words (1 per syllable)
    if 17 >= len(words) >= 3:
        first_line = find_line(words, 5)
        if first_line is False:
            return False
        second_line = find_line(words, 7)
        if second_line is False:
            return False
        third_line = find_line(words, 5)
        if third_line is False or len(words) != 0:
            return False
        full_haiku = ' '.join(first_line) + "\n" + ' '.join(second_line) + "\n" + ' '.join(third_line)
        return full_haiku


def haiku(words: List[str]) -> Any:
    sentence = ' '.join(words).lower()
    url_pattern = re.compile("(?P<url>https?://[^\s]+)")
    links = re.findall(url_pattern, sentence)
    no_hashtag_sentence = sanitize_sentence(sentence, False)
    sentence = sanitize_sentence(sentence)
    possible_sentences = [url_pattern.sub("link", sentence), url_pattern.sub("u r l", sentence),
                          url_pattern.sub("link", no_hashtag_sentence),
                          url_pattern.sub("u r l", no_hashtag_sentence),
                          url_pattern.sub("", no_hashtag_sentence)]
    full_haiku = False
    while possible_sentences and full_haiku is False:
        sentence = possible_sentences.pop()
        words = sentence.split()
        full_haiku = get_haiku(words)

    return full_haiku
