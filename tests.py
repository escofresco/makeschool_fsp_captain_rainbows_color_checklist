from driver import *
import unittest
from unittest import mock

class TestSuite(unittest.TestCase):

    VALID_CHECKLIST_ITEM = 'Clean the paper towels'

    @mock.patch('builtins.input',
                mock.MagicMock(return_value=VALID_CHECKLIST_ITEM))
    def test_valid_add(self):
        test = list()
        add(test)
        self.assertEqual(len(test), 1)
        self.assertEqual(test[0], self.VALID_CHECKLIST_ITEM)

    @mock.patch('builtins.input', mock.MagicMock(return_value=''))
    def test_invalid_add(self):
        test = list()
        with self.assertRaises(ValueError):
            add(test)

    @mock.patch('builtins.input', mock.MagicMock(return_value='0'))
    def test_valid_update(self):
        pass


    def test_invalid_update(self):
        pass

    @mock.patch('builtins.input', mock.MagicMock(return_value='0'))
    def test_valid_remove(self):
        test = list([self.VALID_CHECKLIST_ITEM])
        remove(test)
        self.assertEqual(len(test), 0)

    @mock.patch('builtins.input', mock.MagicMock(return_value='0'))
    def test_invalid_index_remove(self):
        test = list()
        with self.assertRaises(IndexError):
            remove(test)

    @mock.patch('builtins.input', mock.MagicMock(return_value='$'))
    def test_invalid_character_remove(self):
        test = list()
        with self.assertRaises(ValueError):
            remove(test)

    def test_valid_sanitize(self):
        for char in ['a', 'r', 'u']:
            self.assertEqual(sanitize(char), char.upper())

    def test_invalid_sanitize(self):
        for char in ['%', '3', 'aa', 'rrr', 'uuuuu']:
            with self.assertRaises(ValueError):
                sanitize(char)

    def test_valid_index_input(self):
        checklist = [self.VALID_CHECKLIST_ITEM]
        self.assertEqual(index('0', checklist), 0)

    def test_invalid_index_input(self):
        checklist = [self.VALID_CHECKLIST_ITEM]
        for input in ['-1', '1']:
            with self.assertRaises(IndexError):
                index(input, checklist)

    def test_invalid_char_for_index_input(self):
        checklist = [self.VALID_CHECKLIST_ITEM]
        for input in ['`!', ')(())()']:
            with self.assertRaises(ValueError):
                index(input, checklist)

if __name__ == '__main__':
    unittest.main()
