import random
from collections import defaultdict

DO_DETECT = False

DEBUG=False

def debug(*args):
    if DEBUG:
        print " ".join(args)

class Board(object):
    def __init__(self, size=8):
        self.__size = size
        self.__placed = []
        self.__board = []
        self.__available_rows = {}
        self.__available_columns = {}
        self.__used_diags = {}
        self.__used_slashes = {}

        for i in xrange(self.__size):
            self.__available_rows[i] = True
            self.__available_columns[i] = True


        for i in xrange(-i * 2, i * 2):
            self.__used_diags[i] = False
            self.__used_slashes[i] = False



        for x in xrange(size):
            self.__board.append([])


    def add_piece(self, piece):
        x, y = piece

        if DO_DETECT:
            if not self.check_board():
                debug("Can not place piece", (x, y))
                return False


        self.__placed.append((x, y))

        if DO_DETECT:
            if not self.check_board():
                self.__placed.pop()
                return False

        self.__available_rows[x] = False
        self.__available_columns[y] = False

        d1 = piece[0] - piece[1]
        d2 = piece[0] + piece[1]


        self.__used_diags[d1] = True
        self.__used_slashes[d2] = True
        return True

    def remove_piece(self, piece):
        self.__placed.remove((piece))
        x, y = piece
        self.__available_rows[x] = True
        self.__available_columns[y] = True

        d1 = x - y
        d2 = x + y
        self.__used_diags[d1] = False
        self.__used_slashes[d2] = False
        


    def get_candidates(self):
        for j in self.__available_columns:
            if not self.__available_columns[j]:
                continue

            for i in self.__available_rows:
                if not self.__available_rows[i]:
                    continue
                d1 = i - j
                d2 = i + j
                if self.__used_diags[d1]:
                    continue
                if self.__used_slashes[d2]:
                    continue

                yield (i, j)

    def check_pieces_in_danger(self, data_i, data_j):
        if data_i[0] == data_j[0] or data_i[1] == data_j[1]:
            debug("LINES MATCH", data_i, data_j)
            return True

        dia_i = (data_i[0] - data_i[1], data_i[0] + data_i[1])
        dia_j = (data_j[0] - data_j[1], data_j[0] + data_j[1])

        if dia_i[0] == dia_j[0] or dia_i[1] == dia_j[1]:
            debug(dia_i, dia_j)
            debug("DIAGONALS MATCH")
            return True


        

    def check_board(self):
        # Look at all the placements and make sure they are valid
        for i, pos in enumerate(self.__placed):
            for j in xrange(i + 1, len(self.__placed)):
                # makes sure that these pieces aren't attacking?

                if self.check_pieces_in_danger(self.__placed[i], self.__placed[j]):
                    return False

    
        return True


    def placed(self):
        return self.__placed

    def solve(self, size=None):
        # print "SOLVING FOR SIZE", size
        if size is None:
            size = self.__size

        if size == 0:
            return True

        candidates = self.get_candidates()

        for candidate in candidates:
            if not self.add_piece(candidate):
                continue
            
            debug("CHECKING CANDIDATE", candidate)

            if self.solve(size-1):
                return True

            self.remove_piece(candidate)

        debug("RAN OUT OF CANDIDATES")
        if len(self.__placed) != self.__size:
            return False

        return True

    def print_board(self):
        board = []
        for i in xrange(self.__size):
            board.append(["-"] * self.__size)

        for piece in self.__placed:
            board[piece[0]][piece[1]] = 'Q'

        print '\n'.join(["".join(x) for x in board])
