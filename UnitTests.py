import unittest

from HaikuRecognizer import haiku, count_syllables, sanitize_sentence


class HaikuTestCases(unittest.TestCase):

    def test_empty_str(self):
        is_haiku = haiku("")
        self.assertEqual(is_haiku, "")

    def test_two_word_str1(self):
        sentence = "Manysyllablesarequitenice forseeingifthisworkstherightway"
        self.assertEqual(len(sentence.split()), 2)
        syl_options = count_syllables(sentence.split())
        is_haiku = haiku(sentence)
        self.assertEqual(is_haiku, "")

    def test_two_word_str2(self):
        sentence = "#Manysyllablesarequitenice #forseeingifthisworkstherightway"
        self.assertEqual(len(sentence.split()), 2)
        # len("Many syllables are quite nice for seeing if this works the right way".split()) = 13
        self.assertEqual(len(sanitize_sentence(sentence).split()), 13)
        is_haiku = haiku(sentence)
        self.assertNotEqual(is_haiku, "")  # recognized as a haiku!

    def test_eighteen_word_str(self):
        sentence = "a b c d e f g h i j k l m n o p q r"
        self.assertEqual(len(sentence.split()), 18)
        is_haiku = haiku(sentence)
        self.assertEqual(is_haiku, "")

    def test_seventeen_word_str(self):
        sentence = "a b c d e f g h i j k l m n o p q"
        self.assertEqual(len(sentence.split()), 17)
        is_haiku = haiku(sentence)
        self.assertNotEqual(is_haiku, "")  # recognized as a haiku!

    def test_links1(self):
        sentence = "a b c d e f g h i j k l m n o p q https://example.org"
        self.assertEqual(len(sentence.split()), 18)
        # version of sentence without link will pass
        is_haiku = haiku(sentence)
        self.assertNotEqual(is_haiku, "")  # recognized as a haiku!
        self.assertEqual(is_haiku.split()[-1], 'q')

    def test_links2(self):
        sentence = "a b c d e f g h i j k l m n o p https://example.org"
        # version of sentence with link replaced with "link" will pass
        self.assertEqual(len(sentence.split()), 17)
        is_haiku = haiku(sentence)
        self.assertNotEqual(is_haiku, "")  # recognized as a haiku!
        self.assertEqual(is_haiku.split()[-1], 'link')

    def test_links3(self):
        sentence = "a b c d e f g h i j k l m n https://example.org"
        self.assertEqual(len(sentence.split()), 15)
        # version of sentence with link replaced with 'u r l' will pass
        is_haiku = haiku(sentence)
        self.assertNotEqual(is_haiku, "")  # recognized as a haiku!
        self.assertEqual(is_haiku.split()[-1], 'l')

    def test_hashtags1(self):
        sentence = "a b c d e f g h i j k l m n o p q #r"
        self.assertEqual(len(sentence.split()), 18)
        # version of sentence without hashtag will pass
        is_haiku = haiku(sentence)
        self.assertNotEqual(is_haiku, "")  # recognized as a haiku!
        self.assertEqual(is_haiku.split()[-1], 'q')

    def test_hashtags2(self):
        sentence = "a b c d e f g h i j k l m n o p #r"
        self.assertEqual(len(sentence.split()), 17)
        # version of sentence with hashtag will pass
        is_haiku = haiku(sentence)
        self.assertNotEqual(is_haiku, "")  # recognized as a haiku!
        self.assertEqual(is_haiku.split()[-1], 'r')

    def test_hashtags3(self):
        sentence = "a b c d e f g h i j k l m n o #splitthis"
        self.assertEqual(len(sentence.split()), 16)
        # version of sentence with hashtag split will pass
        is_haiku = haiku(sentence)
        self.assertNotEqual(is_haiku, "")  # recognized as a haiku!
        self.assertEqual(is_haiku.split()[-1], 'this')

    def test_numbers1(self):
        sentence = "a b c d e f g h i j k l m n o p 1"
        self.assertEqual(len(sentence.split()), 17)
        # last word will be one
        is_haiku = haiku(sentence)
        self.assertNotEqual(is_haiku, "")  # recognized as a haiku!
        self.assertEqual(is_haiku.split()[-1], 'one')

    def test_numbers2(self):
        sentence = "a b c d e f g h i j k l m n 21"
        self.assertEqual(len(sentence.split()), 15)
        # last word will still be one - 21 -> 'twenty one' 3 syllables
        is_haiku = haiku(sentence)
        self.assertNotEqual(is_haiku, "")  # recognized as a haiku!
        self.assertEqual(is_haiku.split()[-1], 'one')

    def test_numbers3(self):
        sentence = "a b c d e f g h i 10601"
        self.assertEqual(len(sentence.split()), 10)
        # last word will still be one - 10601 -> 'ten thousand six hundred and one' 8 syllables
        is_haiku = haiku(sentence)
        self.assertNotEqual(is_haiku, "")  # recognized as a haiku!
        self.assertEqual(is_haiku.split()[-1], 'one')

    def test_numberhashtags1(self):
        sentence = "a b c d e f g h i j k l m n o #thing1"
        self.assertEqual(len(sentence.split()), 16)
        # last word will be one
        is_haiku = haiku(sentence)
        self.assertNotEqual(is_haiku, "")  # recognized as a haiku!
        self.assertEqual(is_haiku.split()[-1], 'one')

    def test_linkhashtags1(self):
        sentence = "a b c d e f g h i j k l m n o http://example.org #word"
        self.assertEqual(len(sentence.split()), 17)
        # version with hashtag with 'link' will pass, last word 'word'
        is_haiku = haiku(sentence)
        self.assertNotEqual(is_haiku, "")  # recognized as a haiku!
        self.assertEqual(is_haiku.split()[-1], 'word')

    def test_linkhashtags2(self):
        sentence = "a b c d e f g h i j k l m n o p http://example.org #word"
        self.assertEqual(len(sentence.split()), 18)
        # version without hashtag with 'link' will pass, last word 'link'
        is_haiku = haiku(sentence)
        self.assertNotEqual(is_haiku, "")  # recognized as a haiku!
        self.assertEqual(is_haiku.split()[-1], 'link')

    def test_linkhashtags3(self):
        sentence = "a b c d e f g h i j k l m http://example.org #need4wordshere"
        self.assertEqual(len(sentence.split()), 15)
        # version with hashtag without 'link' will pass, last word 'word'
        is_haiku = haiku(sentence)
        self.assertNotEqual(is_haiku, "")  # recognized as a haiku!
        self.assertEqual(is_haiku.split()[-1], 'here')

    def test_linkhashtags4(self):
        sentence = "a b c d e f g h i j k l m o p q r http://example.org #word"
        self.assertEqual(len(sentence.split()), 19)
        # version without hashtag without 'link' will pass, last word 'r'
        is_haiku = haiku(sentence)
        self.assertNotEqual(is_haiku, "")  # recognized as a haiku!
        self.assertEqual(is_haiku.split()[-1], 'r')

if __name__ == '__main__':
    unittest.main()
