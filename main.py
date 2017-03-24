import sys
from config import DETECT_COLINEAR
SIZE=9
SEED=0
if len(sys.argv) > 1:
  SIZE = int(sys.argv[1])

else:
  print "USAGE: python", sys.argv[0], "<N> [<SEED>]"
  sys.exit(0)

if len(sys.argv) > 2:
  SEED = sys.argv[2]

def main():
  import arrange
  arrange.SEED = SEED

  from arrange import BruteForceBoard 
  from repair import RepairingBoard 
  b = RepairingBoard(SIZE)
  b.solve()
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
