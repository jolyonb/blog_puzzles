% slitherlink.pl
% Jolyon Bloomfield February 2022
% https://blog.dodgyfysix.com, https://github.com/jolyonb/blog_puzzles
% Inputs:
% #const rows=number of rows.
% #const cols=number of columns.
% Clue entries:
% clue(col, row, num).

% Set up indices for rows and columns
row(R) :- R=0..rows-1.
col(C) :- C=0..cols-1.

% Mark outside the grid as excluded
excluded(-1, R; cols+1, R) :- row(R).
excluded(C, -1; C, rows+1) :- col(C).

% Mark available cells, ignoring any exclusions
cell(C, R) :- col(C), row(R), not excluded(C, R).

% Available cells are either inside or outside the loop
{inside(C, R); outside(C, R)} = 1 :- cell(C, R).

% Detect edges between inside and outside
% Edges running horizontally
h_edge(C, R) :- inside(C, R-1), not inside(C, R).
h_edge(C, R) :- not inside(C, R-1), inside(C, R).
% Edges running vertically
v_edge(C, R) :- inside(C-1, R), not inside(C, R).
v_edge(C, R) :- not inside(C-1, R), inside(C, R).

% 4 edges cannot meet at a point
:- h_edge(C-1, R), h_edge(C, R), v_edge(C, R), v_edge(C, R-1).

% Edge counts must match clues
:- {v_edge(C, R); v_edge(C+1, R); h_edge(C, R); h_edge(C, R+1)} != N, clue(C, R, N).

% Create a list of vertices that are on the loop
% v_edge(C, R) connects vertices (C, R) and (C, R+1)
% h_edge(C, R) connects vertices (C, R) and (C+1, R)
vertex(C, R) :- v_edge(C, R).
vertex(C, R+1) :- v_edge(C, R).
vertex(C, R) :- h_edge(C, R).
vertex(C+1, R) :- h_edge(C, R).

% Specify which vertices a given vertex can reach by following the loop.
% Vertices can reach themselves
reachable(C, R, C, R) :- vertex(C, R).
% Vertices can move horizontally along an edge from a vertex they can already reach
reachable(C0, R0, C+1, R) :- reachable(C0, R0, C, R), h_edge(C, R).
reachable(C0, R0, C-1, R) :- reachable(C0, R0, C, R), h_edge(C-1, R).
% Vertices can move vertically along an edge from a vertex they can already reach
reachable(C0, R0, C, R+1) :- reachable(C0, R0, C, R), v_edge(C, R).
reachable(C0, R0, C, R-1) :- reachable(C0, R0, C, R), v_edge(C, R-1).

% Demand that all vertices on the loop can be reached from all other vertices.
:- vertex(C1, R1), vertex(C2, R2), not reachable(C1, R1, C2, R2).

#show inside/2.
