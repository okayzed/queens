// okp/queens_repair.cpy
#include <iostream>
#include <vector>
#define len(x) (int)(x).size()
using namespace std;

#include <unordered_map>
#include <cmath>
#include <algorithm>
#include <ctime>

#include <ext/pb_ds/assoc_container.hpp>
using namespace __gnu_pbds;

class ConflictCounter {
    int N;
    vector<int> rows;
    vector<int> cols;
    vector<int> ldiags;
    vector<int> rdiags;
    public:
    ConflictCounter(vector<int> &board) {
        this->N = board.size();
        this->rows.resize(2*N);
        this->cols.resize(2*N);
        this->ldiags.resize(2*N);
        this->rdiags.resize(2*N);
        for (auto i = 0; i < N; i++) {
            this->rows[i]++;
            this->cols[board[i]]++;
            auto d1 = i - board[i] + this->N;
            auto d2 = i + board[i];
            this->ldiags[d1]++;
            this->rdiags[d2]++; } }

    auto get_danger(int px, int py) {
        auto d1 = px - py + this->N;
        auto d2 = px + py;
        auto danger = 0;

        danger += this->rows[px];
        danger += this->cols[py];
        danger += this->ldiags[d1];
        danger += this->rdiags[d2];

        return danger; }

    auto add_piece(int px, int py) {
        this->rows[px] += 1;
        this->cols[py] += 1;

        auto d1 = px - py + this->N;
        auto d2 = px + py;
        this->ldiags[d1] += 1;
        this->rdiags[d2] += 1; }

    auto remove_piece(int px, int py) {
        this->rows[px] -= 1;
        this->cols[py] -= 1;

        auto d1 = px - py + this->N;
        auto d2 = px + py;
        this->ldiags[d1] -= 1;
        this->rdiags[d2] -= 1; } };

auto DETECT_COLINEAR = true;
auto DEBUG = true;

gp_hash_table<float, int> slopes;
auto check_colinearity(auto &board, int px, int py) {
    slopes.clear();

    for (auto i = 0; i < len(board); i++) {
        auto ix = i;
        auto iy = board[i];

        if (ix == px || py == iy) {
            continue; }

        auto slope = float(px - ix) / float(py - iy);
        slopes[slope] += 1; }

    auto conflicts = 0;
    for (auto slope : slopes) {
        if (slope.second > 1) {
            conflicts += 1; } }

    return conflicts * 2; };

auto count_basic_conflicts(auto &board, int px, int py) {
    auto pleft = px - py;
    auto pright = px + py;

    auto N = board.size();
    auto danger = 0;
    for (auto i = 0; i < len(board); i++) {
        if (i == px) {
            continue; }

        if (board[i] == py) {
            danger++; }

        auto d1 = i - board[i];
        auto d2 = i + board[i];

        if (d1 == pleft) {
            danger++; }
        if (d2 == pright) {
            danger++; } }

    return danger; };


auto count_conflicts(auto &board, int px, int py, int min_seen) {
    auto danger = count_basic_conflicts(board, px, py);
    if (DETECT_COLINEAR) {
        danger += check_colinearity(board, px, py); }

    return danger; };

auto board_is_good(auto &board) {
    for (auto i = 0; i < len(board); i++) {
        if (count_conflicts(board, i, board[i], 0) > 0) {
            return false; } }

    return true; };

auto add_conflicted(auto &board, auto px, auto py, auto &conflicted) {
    slopes.clear();

    for (auto i = 0; i < len(board); i++) {
        auto ix = i;
        auto iy = board[i];

        if (ix == px) {
            continue; }

        if (py == iy) {
            continue; }

        auto slope = float(px - ix) / float(py - iy);

        slopes[slope] += 1; }

    for (auto i = 0; i < len(board); i++) {
        auto ix = i;
        auto iy = board[i];

        if (ix == px) {
            continue; }

        if (py == iy) {
            conflicted[ix] = 1;
            conflicted[px] = 1;
            continue; }

        auto slope = float(px - ix) / float(py - iy);
        if (slopes[slope] > 1) {
            conflicted[i] = 1; } } };
inline bool update_position(auto &board, ConflictCounter &cc, int p) {
    auto px = p;
    auto py = board[p];

    cc.remove_piece(px, py);
    auto conflicts = cc.get_danger(px, py);
    if (DETECT_COLINEAR) {
        conflicts += check_colinearity(board, px, py); }

    if (conflicts == 0) {
        cc.add_piece(px, py);
        return false; }

    auto orig_conflicts = conflicts;

    auto best_move = py;
    auto best_conflicts = conflicts;
    vector<int> available;

    for (auto i = 0; i < len(board); i++) {
        conflicts = cc.get_danger(px, i);
        if (conflicts > best_conflicts) {
            continue; }

        if (DETECT_COLINEAR) {
            conflicts += check_colinearity(board, px, i); }

        if (conflicts == best_conflicts) {
            available.push_back(i);
            continue; }

        if (conflicts < best_conflicts) {
            best_conflicts = conflicts;
            available.empty();
            available.push_back(i); } }


    if (len(available) == 0) {
        cc.add_piece(px, py);
        return true; }

    best_move = available[rand() % len(available)];

    if (DEBUG) {
        cout << "UPDATING PIECE" << ' ' <<  px << ' ' <<  py << ' ' <<  "TO" << ' ' <<  px << ' ' <<  best_move << ' ' <<  "C" << ' ' <<  orig_conflicts << ' ' <<  "NC" << ' ' <<  best_conflicts << endl; }
    board[px] = best_move;
    cc.add_piece(px, best_move);

    return true; };

auto print_board(auto &board) {
    for (auto i = 0; i < len(board); i++) {
        for (auto j = 0; j < len(board); j++) {
            if (board[i] == j) {
                cout << 'Q' << ' '; }
            else {
                cout << '-' << ' '; } }
        cout << endl; } };

auto solve(auto &board) {
    auto N = len(board);
    auto rand_order = vector<int>(N);

    for (auto i = 0; i < N; i++) {
        rand_order[i] = i; }

    ConflictCounter cc(board);
    random_shuffle(rand_order.begin(), rand_order.end());
    gp_hash_table<float, int> conflicted;
    gp_hash_table<float, int> next_iter;
    for (auto i = 0; i < N; i++) {
        next_iter[i] = 1; }

    for (auto iter = 0; iter < 20000; iter++) {
        conflicted.clear();

        cout << "ITER" << ' ' <<  iter << ' ' <<  next_iter.size() << ' ';
        if (DEBUG) {
            cout << "" << endl; }
        auto made_move = 0;
        for (auto p : rand_order) {
            if (update_position(board, cc, p)) {
                made_move++;
                conflicted[p] = 1; }

            add_conflicted(board, p, board[p], conflicted); }

        next_iter = conflicted;

        cout << "MADE" << ' ' <<  made_move << ' ' <<  "MOVES" << endl;

        if (!made_move) {
            if (board_is_good(board)) {
                break; } }

        if (!made_move || iter % 50 == 0) {
            for (auto i = 0; i < N; i++) {
                next_iter[i] = 1; } }

        rand_order.resize(next_iter.size());
        auto i = 0;
        for (auto p : next_iter) {
            rand_order[i] = p.first;
            i++; }
        random_shuffle(rand_order.begin(), rand_order.end()); } };


int main(int argc, char **argv) {
    srand(time(NULL));

    auto N = 999;
    vector<int> board(N);

    for (auto i = 0; i < N; i++) {
        board[i] = rand() % N; }

    solve(board);

    auto bad_board = false;
    for (auto i = 0; i < N; i++) {
        if (DETECT_COLINEAR) {
            if (check_colinearity(board, i, board[i]) > 0) {
                cout << "BOARD HAS CO_LINEAR QUEENS" << endl;
                bad_board = true;
                break; } }

        if (count_conflicts(board, i, board[i], 0) > 0) {
            cout << "BOARD HAS CONFLICTS" << endl;
            bad_board = true;
            break; } }

    print_board(board);
    if (!bad_board) {
        cout << "BOARD IS GOOD!" << endl; }

    cout << "[" << ' ';
    for (auto i = 0; i < N-1; i++) {
        cout << board[i] << ' ' <<  "," << ' '; }
    cout << board[N-1] << ' ' <<  "]" << endl; };


