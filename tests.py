from copy import deepcopy
from display import Display
from driver import *
import unittest
from unittest import mock


class TestSuite(unittest.TestCase):

    VALID_CHECKLIST_ITEM = 'Drive the wheels'

    def setUp(self):
        self.STRIKETHROUGH = '\u0336'
        self.VALID_INCOMPLETE_CHECKLIST_ITEM = 'Clean the paper towels'
        self.VALID_COMPLETE_CHECKLIST_ITEM = (self.STRIKETHROUGH.join('Walk the leash')+
                                              self.STRIKETHROUGH)
        self.STATIC_CHECKLIST = [{
            'content': self.VALID_INCOMPLETE_CHECKLIST_ITEM,
            'is_complete': False,
        }, {
            'content': self.VALID_COMPLETE_CHECKLIST_ITEM,
            'is_complete': True,
        }]
        self.INITIAL_MATRIX = [
            ['B', 'i', 'g', ' ', 'T', 'h', 'i', 'n', 'g', 's', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['B', 'i', 'g', ' ', 'R', 'i', 'n', 'g', 's', ' ', ' ', ' ']]
        self.editable_checklist = deepcopy(self.STATIC_CHECKLIST)


    def reset_checklist(self):
        self.editable_checklist = deepcopy(self.STATIC_CHECKLIST)

    @mock.patch('builtins.input',
                mock.MagicMock(return_value=VALID_CHECKLIST_ITEM))
    def test_valid_add(self):
        self.reset_checklist()
        create(self.editable_checklist)
        self.assertEqual(len(self.editable_checklist), 3)
        self.assertEqual(self.editable_checklist[-1]['content'],
                         self.VALID_CHECKLIST_ITEM)

    @mock.patch('builtins.input', mock.MagicMock(return_value=''))
    def test_invalid_add(self):
        with self.assertRaises(ValueError):
            create(self.editable_checklist)

    @mock.patch('builtins.input', mock.MagicMock(return_value='0'))
    def test_valid_update(self):
        pass


    def test_invalid_update(self):
        pass

    @mock.patch('builtins.input', mock.MagicMock(return_value='0'))
    def test_valid_remove(self):
        self.reset_checklist()
        destroy(self.editable_checklist)
        self.assertEqual(len(self.editable_checklist), 1)

    @mock.patch('builtins.input', mock.MagicMock(return_value='0'))
    def test_invalid_index_remove(self):
        with self.assertRaises(IndexError):
            destroy([])

    @mock.patch('builtins.input', mock.MagicMock(return_value='$'))
    def test_invalid_character_remove(self):
        self.reset_checklist()
        with self.assertRaises(ValueError):
            destroy(self.editable_checklist)

    def test_valid_sanitize(self):
        for char in ['a', 'r', 'u']:
            self.assertEqual(sanitize(char), char.upper())

    def test_invalid_sanitize(self):
        for char in ['%', '3', 'aa', 'rrr', 'uuuuu']:
            with self.assertRaises(ValueError):
                sanitize(char)

    def test_valid_index_input(self):
        self.reset_checklist()
        self.assertEqual(index('0', self.editable_checklist), 0)

    def test_invalid_index_input(self):
        self.reset_checklist()
        for input in ['-1', '2']: # Program doesn't handle indexing from the end
            with self.assertRaises(IndexError):
                index(input, self.editable_checklist)

    def test_invalid_char_for_index_input(self):
        self.reset_checklist()
        for input in ['`!', ')(())()']:
            with self.assertRaises(ValueError):
                index(input, self.editable_checklist)

    def test_matrix_reshape_big_to_small(self):
        smaller_mats = [
            ((0,0),[]),
            ((1,1),[['B']]),
            ((2,1),[['B', 'i']]),
            ((1,2),[['B'],['i']]),
            ((12, 1),[['B', 'i', 'g', ' ', 'T', 'h', 'i', 'n', 'g', 's', ' ', ' ']]),
            ((5,2),[['B', 'i', 'g', ' ', 'T'], ['h', 'i', 'n', 'g', 's']]),
        ]
        for i, ((width, height), mat) in enumerate(smaller_mats):
            with self.subTest(i=i):
                self.assertEqual(Display.reshape_matrix(self.INITIAL_MATRIX,
                                                        width,
                                                        height), mat)
    def test_matrix_reshape_small_to_big(self):
        bigger_mats = [
            ((14,3),[['B', 'i', 'g', ' ', 'T', 'h', 'i', 'n', 'g', 's', ' ', ' ', ' ', ' '],
                     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                     ['B', 'i', 'g', ' ', 'R', 'i', 'n', 'g', 's', ' ', ' ', ' ', ' ', ' ']]),
            ((14, 4),[['B', 'i', 'g', ' ', 'T', 'h', 'i', 'n', 'g', 's', ' ', ' ', ' ', ' '],
                      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                      ['B', 'i', 'g', ' ', 'R', 'i', 'n', 'g', 's', ' ', ' ', ' ', ' ', ' '],
                      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]),
        ]
        for i, ((width, height), mat) in enumerate(bigger_mats):
            with self.subTest(i=i):
                self.assertEqual(Display.reshape_matrix(self.INITIAL_MATRIX,
                                                        width,
                                                        height), mat)

if __name__ == '__main__':
    unittest.main()
