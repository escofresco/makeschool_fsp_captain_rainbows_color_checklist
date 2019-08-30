from driver import *
import unittest
from unittest import mock

# def decorator(arg):
#     def real_decorator(func):
#         def wrapper(*args, **kwargs):
#             mock.patch('builtins.input', mock.MagicMock(return_value=*args))()
#         return wrapper
#     return real_decorator

class TestSuite(unittest.TestCase):

    VALID_CHECKLIST_ITEM = 'Clean the paper towels'

    def test_valid_key_sanitization(self):
        self.assertTrue(sanitize('k'))

    def test_invalid_key_sanitization(self):
        self.assertEqual(sanitize('!'), None)

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

    # @mock.patch('builtins.input', mock.MagicMock(return_value='0'))
    # def test_valid_update(self):
    #     test = list(['Rainbows are a hoax'])
    #
    #     update(test)
    #     self.assertEqual(test[0], self.VALID_CHECKLIST_ITEM)

    def test_invalid_update(self):
        pass

    @mock.patch('builtins.input', mock.MagicMock(return_value='0'))
    def test_valid_remove(self):
        test = list([self.VALID_CHECKLIST_ITEM])
        remove(test)
        self.assertEqual(len(test), 0)

    @mock.patch('builtins.input', mock.MagicMock(return_value='0'))
    def test_invalid_remove(self):
        test = list()
        with self.assertRaises(IndexError):
            remove(test)

    def test_sanitize(self):
        pass

    def test_valid_numerical_input(self):
        checklist = [self.VALID_CHECKLIST_ITEM]
        self.assertEqual(index('0', checklist), 0)

    # def test_invalid_numerical_input(self):
    #     checklist = [1]
    #     self.assertFalse(numerical_input_is_valid('$', checklist))
    #     self.assertFalse(numerical_input_is_valid('d', checklist))

if __name__ == '__main__':
    unittest.main()
