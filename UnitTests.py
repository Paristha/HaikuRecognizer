import unittest

from HaikuRecognizer import haiku


class HaikuTestCases(unittest.TestCase):

    def test_empty_str(self):
        is_haiku = haiku("")
        self.assertEqual(is_haiku, False)

    def test_two_word_str(self):
        sentence = "Manysyllablesarequitenice forseeingifthisworkstherightway"
        self.assertEqual(len(sentence.split()), 2)
        is_haiku = haiku()
        self.assertEqual(is_haiku, False)

    def test_eighteen_word_str(self):
        sentence = "I know that it takes many syllables being quite nice to see if this works the right way"
        self.assertEqual(len(sentence.split()), 18)
        is_haiku = haiku(sentence)
        self.assertEqual(is_haiku, False)


if __name__ == '__main__':
    unittest.main()
