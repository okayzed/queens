# trying out iterative repair...
# for every piece on the board, evaluate how many conflicts it currently has
# the, go through all other squares for the max conflict piece on its row (or col) and move it to the best one
import random
import sys

from collections import defaultdict
from board import Board, ConflictObject
from config import DETECT_COLINEAR
SEED = 11

class RepairingBoard(Board):
    def __init__(self, size=8):
        random.seed(SEED)
        print "SEED IS", SEED
        self._placed = set()

        vals = range(size)
        random.shuffle(vals)
        for i in xrange(size):
            self.place_piece((i, vals[i]))


        self.__size = size
        Board.__init__(self, size)

    def remove_piece(self, piece):
        self._placed.remove(piece)
    def place_piece(self, piece):
        self._placed.add(piece)

    def repair_board(self):
        conflict_counts = self.get_conflict_counts()
        keys = conflict_counts.keys()

        movements = []
        for piece in keys:
            conflicts = self.get_conflict_count(piece)
            if conflicts == 0:
                continue


            self.remove_piece(piece)
            repair_conflicts = self.get_repair_conflicts(piece)

            repair_keys = repair_conflicts.keys()
            random.shuffle(repair_keys)
            repair_keys.sort(key=lambda x: repair_conflicts[x])

            val = repair_keys[0]

            intended = repair_conflicts[val]
            if intended > conflicts:
                self.place_piece(piece)
                continue

            print "MOVING", piece, "TO", val

            self.place_piece(val)
            movements.append(val)

        return movements



    def get_repair_conflicts(self, max_piece):

        dangers = {}
        c = ConflictObject(self._placed)

        c.remove(max_piece)

        min_danger = sys.maxint
        for i in xrange(self.__size):
            this_piece = (max_piece[0], i)
            if this_piece in self._placed:
                continue

            if this_piece == max_piece:
                continue

            danger = c.get_danger(this_piece) + 1

            if DETECT_COLINEAR:
                if danger <= min_danger:
                    danger += self.check_colinearity(this_piece) * 2

            min_danger = min(danger, min_danger)

            dangers[this_piece] = danger

        return dangers

    def solve(self):
        def break_cluster():
            # now we go for a cluster buster and knock several queens into the
            # same row, because we think we hit a somewhat local minima
            cluster = []
            i = 0
            placed = list(self._placed)
            import math
            cluster_size = int(math.sqrt(self.__size / 2))
            for _ in xrange(cluster_size):
                i = random.randint(0, self.__size-1)
                piece = placed[i]
                if piece in self._placed:
                    cluster.append(piece)
                    self.remove_piece(piece)
                    np = (piece[0], 0)
                    self.place_piece(np)


            print "BREAKING CLUSTER", cluster
            movements = [0] * self.__size

        for i in xrange(1000):
            print "ITERATING", i
            moves = self.repair_board()
            if i % 100 == 0:
                movements = [0] * self.__size

            if not moves:
                print "NO MOVEMENTS LEFT"
                is_good_board = self.check_board()
                if is_good_board:
                    print "GOOD BOARD, BREAKING"
                    break

                print "NOT GOOD BOARD!"
                break_cluster()

            for m in moves:
                movements[m[0]] += 1
                if movements[m[0]] >= 20:
                    print "LOOP DETECTED ON ", m[0]
                    break_cluster()

if __name__ == "__main__":
    import sys
    size = 11
    if len(sys.argv) > 1:
        size = int(sys.argv[1])

    b = RepairingBoard(size)
    b.solve()

