
import sys



import unittest
import getport


class test(unittest.TestCase):
    def test_get(self):
        self.assertTrue(type(getport.get()) == int, 'return should be a interger')


if __name__ == '__main__':
    unittest.main()