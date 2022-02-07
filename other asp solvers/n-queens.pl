% Solve the n-queens problem
% Adapted from https://potassco.org/clingo/run/
#const n=8.
{ q(R, 1..n) } = 1 :- R = 1..n.  % Place one queen per row
{ q(1..n, C) } = 1 :- C = 1..n.  % Place one queen per column
:- { q(D-C, C) } >= 2, D = 2..2*n.  % Constraint: At most 1 queen per diagonal (first direction)
:- { q(D+C, C) } >= 2, D = 1-n..n-1.  % Constraint: At most 1 queen per diagonal (second direction)
