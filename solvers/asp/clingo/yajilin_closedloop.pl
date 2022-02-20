% yajilin_closedloop.pl
% Jolyon Bloomfield February 2022
% https://blog.dodgyfysix.com, https://github.com/jolyonb/blog_puzzles
% Inputs:
% #const r=number of rows.
% #const c=number of columns.
% Number entries, using n/s/e/w for directions:
% number(col, row, num, dir).
% Excluded entries:
% excluded(col, row).

% Row and column indices
row(0..rows-1).
col(0..cols-1).

% Loop segment indices
% Note that our grid has 0,0 in the top left hand corner, so S increases row and E increases col.
segment(ne; ns; nw; se; sw; ew).
north(ne; ns; nw).
south(ns; se; sw).
east(ne; se; ew).
west(nw; sw; ew).

% Which cells can we modify?
cell(C, R) :- row(R), col(C), not excluded(C, R), not number(C, R, _, _).

% Mark outside the grid as excluded
excluded(-1, R; cols+1, R) :- row(R).
excluded(C, -1; C, rows+1) :- col(C).

% Cells must be either black or a loop
{black(C, R); loop(C, R, S) : segment(S)} = 1 :- cell(C, R).

% Record the directions each cell is moving (helps decrease the number of rules needed later)
dir(C, R, n) :- loop(C, R, N), north(N).
dir(C, R, s) :- loop(C, R, S), south(S).
dir(C, R, e) :- loop(C, R, E), east(E).
dir(C, R, w) :- loop(C, R, W), west(W).

% Loop segments must connect
:- dir(C, R, s), not dir(C, R+1, n).
:- dir(C, R, n), not dir(C, R-1, s).
:- dir(C, R, w), not dir(C-1, R, e).
:- dir(C, R, e), not dir(C+1, R, w).

% Black squares can't be adjacent
:- black(C, R), black(C+1, R).
:- black(C, R), black(C, R+1).

% Cell wall crossings must satisfy number constraints
% This is the only block that is changed from standard yajilin
:- {dir(C, R2, n) : row(R2), R2 < R} != N, number(C, R, N, n).  % Count north movers only
:- {dir(C, R2, n) : row(R2), R2 > R} != N, number(C, R, N, s).  % Count north movers only
:- {dir(C2, R, e) : col(C2), C2 > C} != N, number(C, R, N, e).  % Count east movers only
:- {dir(C2, R, e) : col(C2), C2 < C} != N, number(C, R, N, w).  % Count east movers only

% Finally, the global single-loop constraint
% Create a list of vertices that are on the loop
vertex(C, R) :- dir(C, R, _).

% Specify which vertices a given vertex can reach by following the loop.
% Vertices can reach themselves
reachable(C, R, C, R) :- vertex(C, R).
% Vertices can move following the loop
reachable(C0, R0, C, R-1) :- reachable(C0, R0, C, R), dir(C, R, n).
reachable(C0, R0, C, R+1) :- reachable(C0, R0, C, R), dir(C, R, s).
reachable(C0, R0, C+1, R) :- reachable(C0, R0, C, R), dir(C, R, e).
reachable(C0, R0, C-1, R) :- reachable(C0, R0, C, R), dir(C, R, w).

% Demand that all vertices on the loop can be reached from all other vertices.
:- vertex(C1, R1), vertex(C2, R2), not reachable(C1, R1, C2, R2).

#show black/2.
#show loop/3.
