from collections import defaultdict
from config import DETECT_COLINEAR

class ConflictObject(object):
    def __init__(self, placed):
        self.rows = defaultdict(int)
        self.cols = defaultdict(int)
        self.ldiags = defaultdict(int)
        self.rdiags = defaultdict(int)
        for piece in placed:
            self.rows[piece[0]] += 1
            self.cols[piece[1]] += 1

            d1 = piece[0] - piece[1]
            d2 = piece[0] + piece[1]
            self.ldiags[d1] += 1
            self.rdiags[d2] += 1

    def get_danger(self, piece):
        d1 = piece[0] - piece[1]
        d2 = piece[0] + piece[1]
        danger = 0

        danger += self.rows[piece[0]]
        danger += self.cols[piece[1]]
        danger += self.ldiags[d1]
        danger += self.rdiags[d2]

        return danger

    def add(self, piece):
        self.rows[piece[0]] += 1
        self.cols[piece[1]] += 1

        d1 = piece[0] - piece[1]
        d2 = piece[0] + piece[1]
        self.ldiags[d1] += 1
        self.rdiags[d2] += 1

    def remove(self, piece):
        self.rows[piece[0]] -= 1
        self.cols[piece[1]] -= 1

        d1 = piece[0] - piece[1]
        d2 = piece[0] + piece[1]
        self.ldiags[d1] -= 1
        self.rdiags[d2] -= 1

class Board(object):
    def __init__(self, size=8):
        self.__size = size

    def check_board(self):
        # Look at all the placements and make sure they are valid
        placed = list(self._placed)
        for i, pos in enumerate(placed):
            for j in xrange(i + 1, len(placed)):
                # makes sure that these pieces aren't attacking?

                if self.check_pieces_in_danger(placed[i], placed[j]):
                    return False

        return True

    def check_board_colinearity(self):
        for piece in self._placed:
            if self.check_colinearity(piece):
                return False

        return True


    def check_pieces_in_danger(self, data_i, data_j):
        if data_i[0] == data_j[0] or data_i[1] == data_j[1]:
            return True

        dia_i = (data_i[0] - data_i[1], data_i[0] + data_i[1])
        dia_j = (data_j[0] - data_j[1], data_j[0] + data_j[1])

        if dia_i[0] == dia_j[0] or dia_i[1] == dia_j[1]:
            return True


    def print_board(self):
        board = self.get_board()
        print '\n'.join(["".join(x) for x in board])


    def check_colinearity(self, piece):
        slopes = defaultdict(int)
        conflicts = 0

        for placed in self._placed:
            if placed == piece:
                continue

            if piece[0] == placed[0] or piece[1] == placed[1]:
                continue

            slope = float(piece[0] - placed[0]) / float(piece[1] - placed[1])

            slopes[slope] += 1

        for slope in slopes:
            if slopes[slope] > 1:
                conflicts += 1

        return conflicts

    def get_conflict_count(self, piece):
        c = ConflictObject(self._placed)
        danger = c.get_danger(piece) - 4
        if DETECT_COLINEAR:
            danger += self.check_colinearity(piece)
        return danger

    # gets pieces in conflict
    def get_conflict_counts(self):
        dangers = {}
        c = ConflictObject(self._placed)

        for i, piece in enumerate(self._placed):
            danger = c.get_danger(piece) - 4

            if DETECT_COLINEAR:
                if danger == 0:
                    danger += self.check_colinearity(piece)

            if danger:
                dangers[piece] = danger

        return dangers



    def get_board(self):
        board = []
        for i in xrange(self.__size):
            board.append(["-"] * self.__size)

        for i, piece in enumerate(self._placed):
            board[piece[0]][piece[1]] = 'Q'

        return board

    def print_compact_board(self):
        print ",".join(map(str, self.get_compact_board()))

    def get_compact_board(self):
        locations = [0] * self.__size
        for piece in self._placed:
            locations[piece[0]] = piece[1] + 1
        return locations

    def print_solution(self):
        sol = self.get_compact_board()
        print len(sol)
        print sol
