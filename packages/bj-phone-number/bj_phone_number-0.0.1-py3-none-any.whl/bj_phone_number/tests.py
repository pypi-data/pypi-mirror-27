import unittest
from __init__ import validate_number

class BjPhoneNumber(unittest.TestCase):

    def setUp(self):
        self.data = [
            ['66526416', True],
            ['78985622', False],
            ['123',      False]
        ]

    def test(self):
        for d in self.data:
            self.assertEqual(validate_number(d[0]), d[1])

unittest.main()
