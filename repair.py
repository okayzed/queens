# trying out iterative repair...
# for every piece on the board, evaluate how many conflicts it currently has
# the, go through all other squares for the max conflict piece on its row (or col) and move it to the best one
import random
from collections import defaultdict
from board import Board
from config import DETECT_COLINEAR

class RepairingBoard(Board):
    def __init__(self, size=8):
        self._placed = set()

        vals = range(size)
        random.shuffle(vals)
        for i in xrange(size):
            self._placed.add((i, vals[i]))


        self.__size = size
        Board.__init__(self, size)


    def repair_board(self):
        conflict_counts = self.get_conflict_counts()
        keys = conflict_counts.keys()
        made_movement = False

        movements = []
        for piece in keys:
            if conflict_counts[piece] == 0:
                continue


            self._placed.remove(piece)
            repair_conflicts = self.get_repair_conflicts(piece)

            repair_keys = repair_conflicts.keys()
            random.shuffle(repair_keys)
            repair_keys.sort(key=lambda x: repair_conflicts[x])

            val = repair_keys[0]

            intended = repair_conflicts[val]
            if intended > conflict_counts[piece]:
                self._placed.add(piece)
                continue

            print "MOVING", piece, "TO", val
            made_movement = True

            self._placed.add(val)
            movements.append(val)
            conflict_counts = self.get_conflict_counts()

        return movements



    def get_repair_conflicts(self, max_piece):

        dangers = {}
        for i in xrange(self.__size):
            danger = 0
            this_piece = (max_piece[0], i)
            if this_piece in self._placed:
                continue

            if this_piece == max_piece:
                continue

            dangers[this_piece] = 0
            for other_piece in self._placed:
                if self.check_pieces_in_danger(this_piece, other_piece):
                    danger += 1

            if DETECT_COLINEAR:
                danger += self.check_colinearity(this_piece) * 2

            dangers[this_piece] = danger

        return dangers

    def solve(self):
        def break_cluster():
            # now we go for a cluster buster and knock several queens into the
            # same row, because we think we hit a somewhat local minima
            cluster = []
            i = 0
            placed = list(self._placed)
            for _ in xrange(5):
                i = random.randint(0, self.__size-1)
                piece = placed[i]
                if piece in self._placed:
                    cluster.append(piece)
                    self._placed.remove(piece)
                    np = (piece[0], 0)
                    self._placed.add(np)


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

