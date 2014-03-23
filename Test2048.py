import unittest
from py2048 import Board

__author__ = 'Alex'


class Test2048(unittest.TestCase):
    def test_can_slide_row(self):

        f = Board._can_slide_row_left

        row = [2] * 5
        self.failIf(f(row))

        row.append(0)
        self.failIf(f(row))

        row[0] = 0
        self.failUnless(f(row))

        row = [2]
        self.failIf(f(row))

        row = [0]
        self.failIf(f(row))

    def test_can_collapse_row(self):

        f = Board._can_collapse_row

        row = [2] * 5
        self.failUnless(f(row))

        row = [0, 2] * 5
        self.failUnless(f(row))

        row = [2, 4] * 5
        self.failIf(f(row))

        row = [2]
        self.failIf(f(row))

        row = [0]
        self.failIf(f(row))

    def test_get_collapsed_left_row(self):

        f = Board._get_collapsed_left_row

        tests = [
            ([0, 0], [0, 0]),
            ([2, 0], [2, 0]),
            ([0, 2], [2, 0]),
            ([2, 2], [4, 0]),
            ([0, 2, 2], [4, 0, 0]),
            ([2, 2, 2], [4, 2, 0]),
            ([0, 2, 0, 2, 2, 4, 4, 8, 4, 4], [4, 2, 8, 8, 8, 0, 0, 0, 0, 0]),
        ]

        for row_in, expected in tests:
            self.failUnlessEqual(f(row_in), expected)


def main():
    unittest.main()

if __name__ == '__main__':
    main()