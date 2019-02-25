== n queens solver ==


iterative repair solution to solve N queens problem. everything is wired up inside main.py

run with `python main.py 50` to generate n queens board of size 50.


=== no colinear queens ===

solver can also generate solution for non-colinear n queens problem (change
DETECT_COLINEAR in config.py), but is much much slower (maybe takes 20+
minutes to do 999x999). non-colinear means that no 3 queens can be in a
straight line.

PS. the colinear solver is not guaranteed to generate a solution and has bad
success rates (maybe < 10%)


