import numpy
import pprint
import random
import datetime

__author__ = 'Alex Pinkney'


DIRS = {
    'UP',
    'RIGHT',
    'LEFT',
    'DOWN',
}

VERTICAL = {'UP', 'DOWN'}
HORIZONTAL = {'LEFT', 'RIGHT'}
REVERSED = {'DOWN', 'RIGHT'}

pp = pprint.PrettyPrinter(indent=4)


class Board:
    def __init__(self, size_x=4, size_y=4, start_nums=2):
        self.board = numpy.array([0] * (size_x * size_y)).reshape((size_x, size_y))
        self.prob_2 = 0.9
        self.score = 0

        for _ in xrange(start_nums):
            self._insert_random()

    def __str__(self):
        return pp.pformat(self.board)

    def get_legal_moves(self):
        return filter(lambda d: self._get_legality(d), DIRS)

    def _get_legality(self, direction):
        """
         A move is said to be legal if at least one of the following applies:
         - at least one column/row (dependent on direction) has adjacent similar nonzero values
             - ie numbers can be collapsed
         - there is at least one zero value separated from the far edge by a nonzero value
             - ie numbers can slide
        """

        if direction not in DIRS:
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
            if val and val == last_seen:
                return True
            if val:
                last_seen = val
        return False

    def _can_slide(self, direction):
        size_x, size_y = self.board.shape

        if direction in HORIZONTAL:
            indices = xrange(size_x)
        else:
            indices = xrange(size_y)

        for i in indices:
            if self._can_slide_row_left(self._get_list(direction, i)):
                return True
        return False

    def _can_collapse(self, direction):
        size_x, size_y = self.board.shape

        if direction in HORIZONTAL:
            indices = xrange(size_x)
        else:
            indices = xrange(size_y)

        for i in indices:
            if self._can_collapse_row(self._get_list(direction, i)):
                return True
        return False

    def _get_list(self, direction, index):
        if direction in HORIZONTAL:
            ls = self.board[index, :].tolist()
        else:
            ls = self.board[:, index].tolist()

        if direction in REVERSED:
            ls.reverse()

        return ls

    def _get_empty_cells(self):
        size_x, size_y = self.board.shape
        empties = []

        for x in xrange(size_x):
            for y in xrange(size_y):
                if not self.board[x][y]:
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
        points, new_row = self._get_collapsed_left_row(self._get_list(direction, index))
        self.score += points

        if direction in REVERSED:
            new_row.reverse()

        # Write it back to the board
        # TODO: Find out if narrays support sliced assignment
        for i, val in enumerate(new_row):
            if direction in HORIZONTAL:
                self.board[index][i] = val
            else:
                self.board[i][index] = val

    @staticmethod
    def _get_collapsed_left_row(row):

        points = 0

        new_row = filter(None, row)

        runs = []

        v = 0
        c = 1

        for val in new_row:
            if val == v:
                c += 1
            elif v:
                runs.append((v, c))
                c = 1
            v = val

        if v:
            runs.append((v, c))

        new_row = []

        for v, c in runs:
            new_row.extend([v * 2] * (c // 2))
            points += (v * 2) * (c // 2)

            if c % 2 == 1:
                new_row.append(v)

        if len(new_row) < len(row):
            new_row.extend([0] * (len(row) - len(new_row)))

        return points, new_row

    def move(self, direction):
        if not self._get_legality(direction):
            return False

        size_x, size_y = self.board.shape

        if direction in HORIZONTAL:
            indices = xrange(size_x)
        else:
            indices = xrange(size_y)

        for i in indices:
            self._collapse_row(direction, i)

        self._insert_random()

        return True


def main():
    board = Board(size_x=8, size_y=8)

    print str(board)

    nmoves = 0

    start_time = datetime.datetime.now()

    while True:
        moves = board.get_legal_moves()
        if not moves:
            break

        board.move(random.choice(moves))
        nmoves += 1

        if nmoves % 10000 == 0:
            print "After %s moves and %s:" % (nmoves, datetime.datetime.now() - start_time)
            print str(board)
            print board.score

    print "Game over! Score was %s from %s moves" % (board.score, nmoves)
    print str(board)
    print "Took %s" % (datetime.datetime.now() - start_time,)

if __name__ == '__main__':
    main()
