# n-Queens solver

min-conflicts / iterative repair solution to solve N queens problem. everything
is wired up inside main.py


## solvers

### python solver

run with `pypy py/main.py 50` to generate n queens board of size 50

### cpp solver

compile with `g++ -O3 okp/queens_repair.cpp -o qr` and run `qr`, changing N
requires re-compiling

## notes

### the algorithm

```
while board isn't valid:
    for queen on board:
        move queen to spot in her column that reduces conflicts the most
```

### no-colinear queens

solver can also generate solution for non-colinear n queens problem (change
DETECT_COLINEAR in config.py), but is much much slower (takes 2 - 5 minutes to
do 999x999 instead of 1 - 2 seconds). non-colinear means that no 3 queens can
be in a straight line.

PS. the colinear solver is not guaranteed to generate a solution, current success
rate is ~80%


### optimizations

Initially, the solution could take 2 hours to run. Here are some things that
brought the runtime down:

1) (50 mins) the conflict counter is a data structure that gets updated when a queen is placed, instead of re-counting conflicts for each queen
2) (10 - 15 mins) we only check co-linearity if the current move would reduce conflicts to the best seen. this avoids many calls to check_colinearity
3) (2 - 5 mins) keep track of which queens were placed in danger on the last iteration and only check those
