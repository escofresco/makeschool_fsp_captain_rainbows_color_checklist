from copy import deepcopy
from driver import *
import unittest
from unittest import mock



class TestSuite(unittest.TestCase):

    STRIKETHROUGH = '\u0336'
    VALID_CHECKLIST_ITEM = 'Drive the wheels'
    VALID_INCOMPLETE_CHECKLIST_ITEM = 'Clean the paper towels'
    VALID_COMPLETE_CHECKLIST_ITEM = (STRIKETHROUGH.join('Walk the leash')+
                                      STRIKETHROUGH)
    STATIC_CHECKLIST = [{
        'content': VALID_INCOMPLETE_CHECKLIST_ITEM,
        'is_complete': False,
    }, {
        'content': VALID_COMPLETE_CHECKLIST_ITEM,
        'is_complete': True,
    }]
    editable_checklist = deepcopy(STATIC_CHECKLIST)

    def reset_checklist(self):
        self.editable_checklist = deepcopy(self.STATIC_CHECKLIST)

    @mock.patch('builtins.input',
                mock.MagicMock(return_value=VALID_CHECKLIST_ITEM))
    def test_valid_add(self):
        self.reset_checklist()
        add(self.editable_checklist)
        self.assertEqual(len(self.editable_checklist), 3)
        self.assertEqual(self.editable_checklist[-1]['content'],
                         self.VALID_CHECKLIST_ITEM)

    @mock.patch('builtins.input', mock.MagicMock(return_value=''))
    def test_invalid_add(self):
        with self.assertRaises(ValueError):
            add(self.editable_checklist)

    @mock.patch('builtins.input', mock.MagicMock(return_value='0'))
    def test_valid_update(self):
        pass


    def test_invalid_update(self):
        pass

    @mock.patch('builtins.input', mock.MagicMock(return_value='0'))
    def test_valid_remove(self):
        self.reset_checklist()
        remove(self.editable_checklist)
        self.assertEqual(len(self.editable_checklist), 1)

    @mock.patch('builtins.input', mock.MagicMock(return_value='0'))
    def test_invalid_index_remove(self):
        with self.assertRaises(IndexError):
            remove([])

    @mock.patch('builtins.input', mock.MagicMock(return_value='$'))
    def test_invalid_character_remove(self):
        self.reset_checklist()
        with self.assertRaises(ValueError):
            remove(self.editable_checklist)

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

if __name__ == '__main__':
    unittest.main()
