#include <unordered_map>
#include <cmath>
#include <algorithm>
#include <ctime>

#include <ext/pb_ds/assoc_container.hpp>
using namespace __gnu_pbds;

class ConflictCounter:
    int N
    vector<int> rows
    vector<int> cols
    vector<int> ldiags
    vector<int> rdiags
    public:
    ConflictCounter(vector<int> &board):
        self.N = board.size()
        self.rows.resize(2*N)
        self.cols.resize(2*N)
        self.ldiags.resize(2*N)
        self.rdiags.resize(2*N)
        for i = 0; i < N; i++:
            self.rows[i]++
            self.cols[board[i]]++
            d1 = i - board[i] + self.N
            d2 = i + board[i]
            self.ldiags[d1]++
            self.rdiags[d2]++

    def get_danger(int px, py):
        d1 = px - py + self.N
        d2 = px + py
        danger = 0

        danger += self.rows[px]
        danger += self.cols[py]
        danger += self.ldiags[d1]
        danger += self.rdiags[d2]

        return danger

    def add_piece(int px, py):
        self.rows[px] += 1
        self.cols[py] += 1

        d1 = px - py + self.N
        d2 = px + py
        self.ldiags[d1] += 1
        self.rdiags[d2] += 1

    def remove_piece(int px, py):
        self.rows[px] -= 1
        self.cols[py] -= 1

        d1 = px - py + self.N
        d2 = px + py
        self.ldiags[d1] -= 1
        self.rdiags[d2] -= 1

DETECT_COLINEAR=true
DEBUG=true

gp_hash_table<float, int> slopes;
def check_colinearity(auto &board, int px, py):
    slopes.clear()

    for i = 0; i < len(board); i++:
        ix = i
        iy = board[i]

        if ix == px || py == iy:
            continue

        slope = float(px - ix) / float(py - iy)
        slopes[slope] += 1

    conflicts = 0
    for auto slope : slopes:
        if slope.second > 1:
            conflicts += 1

    return conflicts * 2

def count_basic_conflicts(auto &board, int px, py):
    pleft = px - py
    pright = px + py

    N = board.size()
    danger = 0
    for i = 0; i < len(board); i++:
        if i == px: // skip the piece we are on
            continue

        if board[i] == py:
            danger++

        d1 = i - board[i]
        d2 = i + board[i]

        if d1 == pleft:
            danger++
        if d2 == pright:
            danger++

    return danger


def count_conflicts(auto &board, int px, py, min_seen):
    danger = count_basic_conflicts(board, px, py)
    if DETECT_COLINEAR:
        danger += check_colinearity(board, px, py)

    return danger

def board_is_good(auto &board):
    for i = 0; i < len(board); i++:
        if count_conflicts(board, i, board[i], 0) > 0:
            return false

    return true

def add_conflicted(auto &board, px, py, auto &conflicted):
    slopes.clear()

    for i = 0; i < len(board); i++:
        ix = i
        iy = board[i]

        if ix == px:
            continue

        if py == iy:
            continue

        slope = float(px - ix) / float(py - iy)

        slopes[slope] += 1

    for i = 0; i < len(board); i++:
        ix = i
        iy = board[i]

        if ix == px:
            continue

        if py == iy:
            conflicted[ix] = 1
            conflicted[px] = 1
            continue

        slope = float(px - ix) / float(py - iy)
        if slopes[slope] > 1:
            conflicted[i] = 1

inline bool update_position(auto &board, ConflictCounter &cc, int p):
    px = p
    py = board[p]

    cc.remove_piece(px, py)
    conflicts = cc.get_danger(px, py)
    if DETECT_COLINEAR:
        conflicts += check_colinearity(board, px, py)

    if conflicts == 0:
        cc.add_piece(px, py)
        return false

    orig_conflicts = conflicts

    best_move = py
    best_conflicts = conflicts
    vector<int> available

    for i = 0; i < len(board); i++:
        conflicts = cc.get_danger(px, i)
        if conflicts > best_conflicts:
            continue

        if DETECT_COLINEAR:
            conflicts += check_colinearity(board, px, i)

        if conflicts == best_conflicts:
            available.push_back(i)
            continue

        if conflicts < best_conflicts:
            best_conflicts = conflicts
            available.empty()
            available.push_back(i)


    if len(available) == 0:
        cc.add_piece(px, py)
        return true

    best_move = available[rand() % len(available)]

    if DEBUG:
        print "UPDATING PIECE", px, py, "TO", px, best_move, "C", orig_conflicts, "NC", best_conflicts
    board[px] = best_move
    cc.add_piece(px, best_move)

    return true

def print_board(auto &board):
    for i = 0; i < len(board); i++:
        for j = 0; j < len(board); j++:
            if board[i] == j:
                print 'Q',
            else:
                print '-',
        print

def solve(auto &board):
    N = len(board)
    rand_order = vector<int>(N)

    for i = 0; i < N; i++:
        rand_order[i] = i

    ConflictCounter cc(board)
    random_shuffle(rand_order.begin(), rand_order.end())
    gp_hash_table<float, int> conflicted;
    gp_hash_table<float, int> next_iter;
    for i = 0; i < N; i++:
        next_iter[i] = 1

    for iter = 0; iter < 20000; iter++:
        conflicted.clear()

        print "ITER", iter, next_iter.size(),
        if DEBUG:
            print ""
        made_move = 0
        for auto p : rand_order:
            if update_position(board, cc, p):
                made_move++
                conflicted[p] = 1

            add_conflicted(board, p, board[p], conflicted)

        next_iter = conflicted;

        print "MADE", made_move, "MOVES"

        if !made_move:
            if board_is_good(board):
                break

        if !made_move || iter % 50 == 0:
            for i = 0; i < N; i++:
                next_iter[i] = 1

        i = 0
        rand_order.resize(next_iter.size())
        for auto p : next_iter:
            rand_order[i] = p.first
            i++
        random_shuffle(rand_order.begin(), rand_order.end())


def main(int argc, char **argv):
    srand(time(NULL))

    N = 999
    vector<int> board(N);

    for i = 0; i < N; i++:
        board[i] = rand() % N

    solve(board)

    bad_board = false
    for i = 0; i < N; i++:
        if DETECT_COLINEAR:
            if check_colinearity(board, i, board[i]) > 0:
                print "BOARD HAS CO_LINEAR QUEENS"
                bad_board = true
                break

        if count_conflicts(board, i, board[i], 0) > 0:
            print "BOARD HAS CONFLICTS"
            bad_board = true
            break

    print_board(board)
    if !bad_board:
        print "BOARD IS GOOD!"

    print "[",
    for i = 0; i < N-1; i++:
        print board[i], ",",
    print board[N-1], "]"
