# n-Queens solver

min-conflicts / iterative repair solution to solve N queens problem. everything
is wired up inside main.py

this solver can also generate solution for non-colinear n queens problem
(change DETECT_COLINEAR in config.py), but is much much slower.  non-colinear
means that no 3 queens can be in a straight line.


## solvers

### python solver

run with `pypy py/main.py 50` to generate n queens board of size 50

without the co-linear constraint, a 999x999 solution can be generated in 5
seconds.  it originally took up to 2 hours to solve for non co-linear queens,
but now it takes 10 - 15 minutes to do 999x999 instead of 5 seconds.

PS. the colinear solver is not guaranteed to generate a solution


### okp / cpp solver

compile with `g++ -O3 okp/queens_repair.cpp -o qr` and run `qr`. changing N
requires re-compiling

i re-wrote the python solution in okp with the goal of solving 999x999 in under
5 minutes. it's now able to solve no co-linear queens for 999x999 in 2 - 5
minutes, but it's not guaranteed to find a solution.

## notes

### the algorithm

```
while board isn't valid:
    for queen on board:
        move queen to spot in her column that reduces conflicts the most
```

### optimizations

Initially, the solution could take 2 hours to run. Here are some things that
brought the runtime down:

1) (50 mins) the conflict counter is a data structure that gets updated when a queen is placed, instead of re-counting conflicts for each queen
2) (10 - 15 mins) we only check co-linearity if the current move would reduce conflicts to the best seen. this avoids many calls to check_colinearity
3) (2 - 5 mins) keep track of which queens were placed in danger on the last iteration and only check those
