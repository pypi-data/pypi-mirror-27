try:
    from .code import PearsonDictionary
except ImportError:
    from code import PearsonDictionary

import unittest


COMMON_TEST_WORD = 'dog'
COMMON_TEST_WORD_NOUN = 'noun'

class FullTest(unittest.TestCase):

    def test_1(self):
        pd = PearsonDictionary()

        result = pd.get_definitions(COMMON_TEST_WORD)
        self.assertTrue(COMMON_TEST_WORD in result, msg='Low level api request with common word 2')
        len_short = len(result)
        self.assertTrue(len_short > 0)

        result = pd.get_definitions(COMMON_TEST_WORD, load_all_items=True)
        self.assertTrue(COMMON_TEST_WORD in result, msg='Low level api with recursive requests')
        len_full = len(result)
        self.assertTrue(len_full > 0)

        self.assertTrue(len_full > len_short, msg='Full answer vs short answer')

        result = pd.get_definitions(COMMON_TEST_WORD, pos=COMMON_TEST_WORD_NOUN)
        self.assertTrue(COMMON_TEST_WORD in result, msg='Low level api request with common word and pos = noun')


if __name__ == '__main__':
    unittest.main()

