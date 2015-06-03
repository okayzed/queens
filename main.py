
import sys
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
  print "BOARD IS ALRIGHT?", b.check_board()

if __name__ == "__main__":
  main()
