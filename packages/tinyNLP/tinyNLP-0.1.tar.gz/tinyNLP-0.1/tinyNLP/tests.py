import unittest
import doctest
import miniNLP

class TestSplitIntoSentences(unittest.TestCase):
    def test_basic_split_sentences(self):
        text = 'A b c. D e f. G h i.'
        s = miniNLP.text2sentences(text)
        self.assertEqual(s,['A b c.', 'D e f.', 'G h i.'])

        text = 'A b c! D e f! G h i!'
        s = miniNLP.text2sentences(text)
        self.assertEqual(s,['A b c!', 'D e f!', 'G h i!'])

        text = 'A b c? D e f? G h i?'
        s = miniNLP.text2sentences(text)
        self.assertEqual(s,['A b c?', 'D e f?', 'G h i?'])

        text = 'A b c. D e f? G h i!'
        s = miniNLP.text2sentences(text)
        self.assertEqual(s,['A b c.', 'D e f?', 'G h i!'])

    def test_split_with_parentheses(self):
        text = 'Abc def. Ghi jkl. Mno pqr.'
        s = miniNLP.text2sentences(text)
        self.assertEqual(s,['Abc def.', 'Ghi jkl.', 'Mno pqr.'])

        text = 'Abc def. (Ghi) jkl. Mno pqr.'
        s = miniNLP.text2sentences(text)
        self.assertEqual(s,['Abc def.', '(Ghi) jkl.', 'Mno pqr.'])

        text = 'Abc def. Ghi (jkl). Mno pqr.'
        s = miniNLP.text2sentences(text)
        self.assertEqual(s,['Abc def.', 'Ghi (jkl).', 'Mno pqr.'])

        text = 'Abc def. Ghi (jkl.) Mno pqr.'
        s = miniNLP.text2sentences(text)
        self.assertEqual(s,['Abc def.', 'Ghi (jkl.)', 'Mno pqr.'])

        text = 'Abc def. Ghi (jkl) mno. Pqr.'
        s = miniNLP.text2sentences(text)
        self.assertEqual(s,['Abc def.', 'Ghi (jkl) mno.', 'Pqr.'])

class TestSplitIntoWords(unittest.TestCase):
    def test_basic_split_words(self):
        text = 'A b c.'
        s = miniNLP.sentence2words(text)
        self.assertEqual(s,['A', 'b', 'c', '.'])

        text = 'A b c!'
        s = miniNLP.sentence2words(text)
        self.assertEqual(s,['A', 'b', 'c', '!'])

        text = 'A b c?'
        s = miniNLP.sentence2words(text)
        self.assertEqual(s,['A', 'b', 'c', '?'])

        text = 'Abc def ghi.'
        s = miniNLP.sentence2words(text)
        self.assertEqual(s,['Abc', 'def', 'ghi', '.'])

        text = 'Abc def ghi!'
        s = miniNLP.sentence2words(text)
        self.assertEqual(s,['Abc', 'def', 'ghi', '!'])

        text = 'Abc def ghi?'
        s = miniNLP.sentence2words(text)
        self.assertEqual(s,['Abc', 'def', 'ghi', '?'])

        text = 'Abc, def ghi.'
        s = miniNLP.sentence2words(text)
        self.assertEqual(s,['Abc', ',', 'def', 'ghi', '.'])

    def test_basic_split_with_parentheses(self):
        text = '(A b) c.'
        s = miniNLP.sentence2words(text)
        self.assertEqual(s,['(', 'A', 'b', ')', 'c', '.'])

        text = 'A (b) c.'
        s = miniNLP.sentence2words(text)
        self.assertEqual(s,['A', '(', 'b', ')', 'c', '.'])

        text = 'A (b c).'
        s = miniNLP.sentence2words(text)
        self.assertEqual(s,['A', '(', 'b', 'c', ')', '.'])

        text = 'A (b c.)'
        s = miniNLP.sentence2words(text)
        self.assertEqual(s,['A', '(', 'b', 'c', '.', ')'])



class TestSplitText(unittest.TestCase):
    def test_basic_split(self):
        text = 'A b c. D e f. G h i.'
        s = miniNLP.text2words(text)
        self.assertEqual(s,[['A', 'b', 'c', '.'], ['D', 'e', 'f', '.'], ['G', 'h', 'i', '.']])

        text = 'A b c! D e f! G h i!'
        s = miniNLP.text2words(text)
        self.assertEqual(s,[['A', 'b', 'c', '!'], ['D', 'e', 'f', '!'], ['G', 'h', 'i', '!']])

        text = 'A b c? D e f? G h i?'
        s = miniNLP.text2words(text)
        self.assertEqual(s,[['A', 'b', 'c', '?'], ['D', 'e', 'f', '?'], ['G', 'h', 'i', '?']])

        text = 'A b c. D e f! G h i?'
        s = miniNLP.text2words(text)
        self.assertEqual(s,[['A', 'b', 'c', '.'], ['D', 'e', 'f', '!'], ['G', 'h', 'i', '?']])

    def test_split_with_parentheses(self):
        text = 'A b c. (D e) f. G h i.'
        s = miniNLP.text2words(text)
        self.assertEqual(s,[['A', 'b', 'c', '.'],
                            ['(', 'D', 'e', ')', 'f', '.'],
                            ['G', 'h', 'i', '.']])

        text = 'A b c. D (e f.) G h i.'
        s = miniNLP.text2words(text)
        self.assertEqual(s,[['A', 'b', 'c', '.'],
                            ['D', '(', 'e', 'f', '.', ')'],
                            ['G', 'h', 'i', '.']])

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(miniNLP))
    return tests

if __name__ == '__main__':
    unittest.main()
