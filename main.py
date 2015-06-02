
import sys
SIZE=9
if len(sys.argv) > 1:
  SIZE = int(sys.argv[1])

def main():
  from arrange import Board 
  b = Board(SIZE)
  b.solve()
  print ""
  print "PLACED ARE", b.placed()
  print ""
  b.print_board()
  print ""
  print "BOARD IS ALRIGHT?", b.check_board()

if __name__ == "__main__":
  main()
