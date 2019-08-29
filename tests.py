from driver import *
import unittest
from unittest import mock

class TestSuite(unittest.TestCase):

    def test_valid_key_sanitization(self):
        self.assertTrue(sanitize('k'))

    def test_invalid_key_sanitization(self):
        self.assertEqual(sanitize('!'), None)

    @mock.patch('driver.add', mock.MagicMock(return_value='anything'))
    def test_valid_add(self):
        test = list()
        # add(test)
        self.assertEqual(len(test), 1)
        self.assertEqual(test[0], 'anything')

    def test_invalid_add(self):
        pass

    def test_valid_update(self):
        pass

    def test_invalid_update(self):
        pass

    def test_valid_remove(self):
        pass

    def test_invalid_remove(self):
        pass

    def test_sanitize(self):
        pass

    def test_valid_numerical_input(self):
        checklist = [1]
        self.assertTrue(numerical_input_is_valid('0', checklist))

    def test_invalid_numerical_input(self):
        checklist = [1]
        self.assertFalse(numerical_input_is_valid('$', checklist))
        self.assertFalse(numerical_input_is_valid('d', checklist))

if __name__ == '__main__':
    unittest.main()
