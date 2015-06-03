import random
from collections import defaultdict
from board import Board

DO_DETECT=False # check the board  before and after every placement
DEBUG=False # print debugging statements, dont turn on unless you pipe to file


SHUFFLE=True
SEED=0

# TURN THIS TO TRUE TO FIND ONLY CO-LINEAR BOARD PLACEMENTS
DETECT_COLINEAR=False

MAX_ITERATIONS=100000
MAX_TRIES=100

def debug(*args):
    if DEBUG:
        print " ".join(args)

class MaxDepthError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
    
class BruteForceBoard(Board):
    def __init__(self, size=8):
        self.__size = size
        self.__reset__()

        Board.__init__(self, size)



    def __reset__(self):
        size = self.__size
        self._placed = []
        self.__board = []
        self.__available_rows = {}
        self.__available_columns = {}
        self.__used_diags = {}
        self.__used_slashes = {}

        self.__iterations = 0
        self.__close_calls = 0


        self.__rows = range(size)
        self.__cols = range(size)

        if SHUFFLE:
            random.seed(SEED)
            random.shuffle(self.__rows)
            random.shuffle(self.__cols)


        for i in xrange(self.__size):
            self.__available_rows[i] = True
            self.__available_columns[i] = True


        for i in xrange(-i * 3, i * 3):
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


        slopes = defaultdict(int)

        if DETECT_COLINEAR:
            for placed in self._placed:
                slope = float(piece[0] - placed[0]) / float(piece[1] - placed[1])
                slopes[slope] += 1

            for slope in slopes:
                if slopes[slope] > 1:

                    if len(self._placed) == self.__size - 2:
                        self.__close_calls += 1

                        if DEBUG:
                            board = self.get_board()
                            board[x][y] = '?'

                            candidates = list(self.get_candidates())
                            for c in candidates:
                                board[c[0]][c[1]] = 'c'

                            print '\n'.join(["".join(x) for x in board])
                            print "ADDING PIECE", piece
                            print "MULTIPLE SLOPES, INVALID POSITION"

                    return False
                
        self._placed.append((x, y))

        if DO_DETECT:
            if not self.check_board():
                self._placed.pop()
                return False


        self.__available_rows[x] = False
        self.__available_columns[y] = False

        d1 = piece[0] - piece[1]
        d2 = piece[0] + piece[1]


        self.__used_diags[d1] = True
        self.__used_slashes[d2] = True
        return True

    def remove_piece(self, piece):
        self._placed.remove((piece))
        x, y = piece
        self.__available_rows[x] = True
        self.__available_columns[y] = True

        d1 = x - y
        d2 = x + y
        self.__used_diags[d1] = False
        self.__used_slashes[d2] = False
        


    def get_candidates(self):
        for j in self.__cols:
            if not self.__available_columns[j]:
                continue

            for i in self.__rows:
                if not self.__available_rows[i]:
                    continue

                d1 = i - j
                d2 = i + j
                if self.__used_diags[d1]:
                    continue
                if self.__used_slashes[d2]:
                    continue

                yield (i, j)

        

    def solve(self):
        for i in xrange(MAX_TRIES):
            try:
                self._solve()
            except MaxDepthError, e:
                global SEED, SHUFFLE
                SHUFFLE=True
                SEED = random.random()
                self.__reset__()
                print "MAX ITERATIONS EXCEEDED", i
            except Exception, e:
                print 'EXCEPTION', e
                break

    def _solve(self, size=None):
        if size is None:
            size = self.__size

        if size == 0:
            return True

        candidates = self.get_candidates()

        self.__iterations += 1

        if self.__iterations >= MAX_ITERATIONS:
            raise MaxDepthError()

        for candidate in candidates:
            if not self.add_piece(candidate):
                continue
            
            debug("CHECKING CANDIDATE", candidate)

            if self._solve(size-1):
                return True

            self.remove_piece(candidate)

        debug("RAN OUT OF CANDIDATES")
        if len(self._placed) != self.__size:
            return False

        return True
