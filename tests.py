from driver import *
import unittest
from unittest.mock import patch

class TestSuite(unittest.TestCase):
    def setUp(self):
        self.checklist = list()

    def test_valid_key_sanitization(self):
        self.assertTrue(sanitize('k'))

    def test_invalid_key_sanitization(self):
        self.assertEquals(sanitize('!'), None)

    @patch('add', return_value='anything')
    def test_add_to_list(self):
        test = list()
        add(test)
        self.assertEquals(len(test), 1)
        self.assertEquals(test[0], 'anything')


if __name__ == '__main__':
    unittest.main()
