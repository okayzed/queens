class Board(object):
    def __init__(self, size=8):
        self.__size = size

    def check_board(self):
        # Look at all the placements and make sure they are valid
        for i, pos in enumerate(self._placed):
            for j in xrange(i + 1, len(self._placed)):
                # makes sure that these pieces aren't attacking?

                if self.check_pieces_in_danger(self._placed[i], self._placed[j]):
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


    def get_conflict_counts(self):
        dangers = {}
        for i, piece in enumerate(self._placed):
            danger = 0
            for other_piece in self._placed:
                if other_piece == piece:
                    continue

                if self.check_pieces_in_danger(piece, other_piece):
                    danger += 1

            dangers[piece] = danger

        return dangers



    def get_board(self):
        board = []
        for i in xrange(self.__size):
            board.append(["-"] * self.__size)

        for i, piece in enumerate(self._placed):
            board[piece[0]][piece[1]] = 'Q'

        return board
