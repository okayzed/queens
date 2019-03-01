# this file checks if a board is valid or not

import sys
from config import DETECT_COLINEAR
import random
SIZE=9
SEED=0


# REPLACE THIS WITH YOUR BOARD
board = [ 21 , 50 , 39 , 47 , 84 , 62 , 87 , 85 , 34 , 78 , 92 , 53 , 60 , 4 , 14 , 43 , 93 , 63 , 59 , 27 , 70 , 86 , 32 , 55 , 90 , 9 , 29 , 8 , 58 , 1 , 44 , 64 , 12 , 51 , 35 , 88 , 61 , 11 , 77 , 22 , 0 , 97 , 18 , 56 , 73 , 23 , 19 , 99 , 15 , 36 , 2 , 82 , 5 , 68 , 46 , 67 , 26 , 91 , 40 , 75 , 16 , 49 , 66 , 3 , 25 , 71 , 17 , 57 , 13 , 96 , 41 , 33 , 83 , 95 , 20 , 98 , 30 , 72 , 76 , 81 , 89 , 45 , 79 , 48 , 28 , 6 , 65 , 80 , 54 , 52 , 37 , 10 , 24 , 42 , 69 , 94 , 7 , 74 , 31 , 38 ]

def main():
  import arrange, repair


  from arrange import BruteForceBoard 
  from repair import RepairingBoard 
  SIZE = len(board)
  b = RepairingBoard(SIZE)
  b._placed = set()

  for i, line in enumerate(board):
    piece = (i, int(line))
    b.place_piece(piece)
  
   

  print ""
  print "PLACED ARE", b._placed
  print ""
  b.print_board()
  print ""

  is_good_board = b.check_board()
  is_colinear_board = b.check_board_colinearity()

  print "BOARD HAS QUEENS IN DANGER?", not is_good_board
  print "BOARD HAS COLINEAR QUEENS?", not is_colinear_board

  if not is_good_board or (DETECT_COLINEAR and not is_colinear_board):
    print "BOARD IS NO GOOD!"
  else:
    print "BOARD IS GOOD!"

  b.print_solution()

if __name__ == "__main__":
  main()
