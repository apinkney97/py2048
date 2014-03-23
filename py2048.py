from numpy import np
from enum import Enum
import pprint
import random

__author__ = 'Alex Pinkney'


class Direction(Enum):
    UP = 1
    RIGHT = 2
    LEFT = 3
    DOWN = 4

VERTICAL = {Direction.UP, Direction.DOWN}
HORIZONTAL = {Direction.LEFT, Direction.RIGHT}
REVERSED = {Direction.UP, Direction.LEFT}

pp = pprint.PrettyPrinter(indent=4)


class Board:
    def __init__(self, size_x=4, size_y=4):
        self.board = np.zeros(size_x, size_y)
        self.prob_2 = 0.9

    def __str__(self):
        return pp.pformat(self.board)

    def get_legal_moves(self):
        return filter(lambda d: self._get_legality(d), Direction)

    def _get_legality(self, direction):
        """
         A move is said to be legal if at least one of the following applies:
         - at least one column/row (dependent on direction) has adjacent similar nonzero values
             - ie numbers can be collapsed
         - there is at least one zero value separated from the far edge by a nonzero value
             - ie numbers can slide
        """

        if direction not in Direction:
            raise Exception("Bad direction '%s'" % direction)

        if self._can_slide(direction):
            return True

        return self._can_collapse(direction)

    @staticmethod
    def _can_slide_row_left(row):
        seen_zero = False
        for val in row:
            if seen_zero and val:
                return True
            if not val:
                seen_zero = True
        return False

    @staticmethod
    def _can_collapse_row(row):
        last_seen = 0
        for val in row:
            if val == last_seen:
                return True
            if val:
                last_seen = val
        return False

    def _can_slide(self, direction):
        size_x, size_y = self.board.shape

        if direction in VERTICAL:
            indices = xrange(size_x)
        else:
            indices = xrange(size_y)

        for i in indices:
            if self._can_slide_row_left(self._get_list(direction, i)):
                return True
        return False

    def _can_collapse(self, direction):
        size_x, size_y = self.board.shape

        if direction in VERTICAL:
            indices = xrange(size_x)
        else:
            indices = xrange(size_y)

        for i in indices:
            if self._can_collapse_row(self._get_list(direction, i)):
                return True
        return False

    def _get_list(self, direction, index):
        if direction in VERTICAL:
            ls = self.board[:, index].tolist()
        else:
            ls = self.board[index, :].tolist()

        if direction in REVERSED:
            ls.reverse()

        return ls

    def _get_empty_cells(self):
        size_x, size_y = self.board.shape
        empties = []

        for x in xrange(size_x):
            for y in xrange(size_y):
                if self.board[x][y]:
                    empties.append((x, y))

        return empties

    def _insert_random(self):
        x, y = random.choice(self._get_empty_cells())
        if random.random() <= self.prob_2:
            num = 2
        else:
            num = 4
        self.board[x][y] = num

    def _collapse_row(self, direction, index):
        new_row = self._get_collapsed_left_row(self._get_list(direction, index))
        if new_row in REVERSED:
            new_row.reverse()

        # Write it back to the board
        # TODO: Find out if narrays support sliced assignment
        for i, val in enumerate(new_row):
            if direction in VERTICAL:
                self.board[index][i] = val
            else:
                self.board[i][index] = val

    @staticmethod
    def _get_collapsed_left_row(row):

        new_row = filter(None, row)

        runs = []

        v = 0
        c = 0

        for val in new_row:
            if val == v:
                c += 1
            elif v:
                runs.append((v, c))
                v = val
                c = 1

        if v:
            runs.append((v, c))

        new_row = []

        for v, c in runs:
            new_row.extend([v * 2] * (c // 2))
            if c % 2 == 1:
                new_row.append(v)

        if len(new_row) < len(row):
            new_row.extend([0] * (len(row) - len(new_row)))

        return new_row

    def move(self, direction):
        if not self._get_legality(direction):
            return False

        size_x, size_y = self.board.shape

        if direction in VERTICAL:
            indices = xrange(size_x)
        else:
            indices = xrange(size_y)

        for i in indices:
            self._collapse_row(direction, i)

        self._insert_random()

        return True


def main():
    pass

if __name__ == '__main__':
    main()
