import unittest

from HaikuRecognizer import haiku


class HaikuTestCases(unittest.TestCase):

    def test_empty_str(self):
        is_haiku = haiku("")
        self.assertEqual(is_haiku, False)

    def test_two_word_str(self):
        is_haiku = haiku("Manysyllablesarequitenice forseeingifthisworkstherightway")
        self.assertEqual(is_haiku, False)


if __name__ == '__main__':
    unittest.main()
