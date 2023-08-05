import unittest
from shortnumbers import millify, parse_millify

class TestDefaultMillify(unittest.TestCase):

    def test_millify(self):
        self.assertEqual(millify(0), '0')
        self.assertEqual(millify(1), '1')
        self.assertEqual(millify('2'), '2')
        self.assertEqual(millify(999), '999')
        self.assertEqual(millify(1000), '1k')
        self.assertEqual(millify(1234), '1k')
        self.assertEqual(millify(5678000), '6M')
        self.assertEqual(millify(-2000), '-2k')
        self.assertEqual(millify(-30000000000.12), '-30B')
        self.assertEqual(millify(12345, precision=2), '12.35k')
        self.assertEqual(millify(12345, precision=2, suffix=" ", ending="B"), '12.35 kB')
        self.assertEqual(millify(12345, precision=2, prefix="$"), '$12.35k')

    def test_parse_millify(self):
        self.assertEqual(parse_millify("0"), 0.0)
        self.assertEqual(parse_millify("1"), 1.0)
        self.assertEqual(parse_millify(1), 1.0)
        self.assertEqual(parse_millify("1k"), 1000.0)
        self.assertEqual(parse_millify("-1.56k"), -1560.0)
        self.assertEqual(parse_millify("24.5MB"), 24500000.0)
        self.assertEqual(parse_millify("24.5B"), 24500000000.0)

if __name__ == '__main__':
    unittest.main()
