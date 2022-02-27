% lits.pl
% Jolyon Bloomfield February 2022
% https://blog.dodgyfysix.com, https://github.com/jolyonb/blog_puzzles
% Inputs:
% Regions:
% region(col, row, regionnum).
% Shapes:
% Define all available shapes, including all rotations and reflections.
% Each shape will be defined as a series of cells (X, Y), where (0, 0) is the "anchor" cell,
% which must be included in the shape.
% shape(name, orientation, x, y).

% Indices
% Region indices
regions(N) :- region(X, Y, N).
% Cell indices
cell(X, Y) :- region(X, Y, N).
% Shape indices
shape(S, O) :- shape(S, O, X, Y).
% Shape sizes
shape_size(S, C) :- shape(S, O), C = #count{Sx, Sy : shape(S, O, Sx, Sy)}.

% Solving
% Possible shape placements
% For each X, Y in each region N, try placing each shape S in orientation O at anchor point (X, Y).
% Count the number of cells that can be placed in the region; if it equals the cell count for the shape,
% it's a valid possibility.
% valid_anchor_loc(shape, orientation, regionnum, anchorx, anchory).
valid_anchor_loc(S,O,N,X,Y) :- region(X,Y,N), shape(S,O), shape_size(S,C1),
                               C2=#count{Rx,Ry : region(Rx,Ry,N), shape(S,O,Dx,Dy), Rx=X+Dx, Ry=Y+Dy},
                               C1=C2.

% For each region, choose a single shape/orientation/anchor
% region_piece(regionnum, shape, orientation, anchorx, anchory)
{region_piece(N, S, O, X, Y) : valid_anchor_loc(S, O, N, X, Y)} = 1 :- regions(N).

% Given the selected region_piece entries, label filled cells as black.
% We have two versions here, one that includes shape and region information, and one that doesn't.
% black(x, y, shape, regionnum).
% black(x, y).
black(Xabs, Yabs, S, N) :- region_piece(N, S, O, X, Y), region(Rx, Ry, N), shape(S, O, Dx, Dy), Xabs=X+Dx, Yabs=Y+Dy.
black(X,Y) :- black(X,Y,S,N).

% Adjacent black cells in different regions must have different shapes
% We set up adjacency atoms because we will need them for reachability later
adjacent(X,Y,X+1,Y) :- cell(X,Y), cell(X+1,Y).
adjacent(X,Y,X,Y+1) :- cell(X,Y), cell(X,Y+1).
adjacent(X2,Y2,X1,Y1) :- adjacent(X1,Y1,X2,Y2).
:- black(X1, Y1, S1, N1), black(X2, Y2, S2, N2), N1!=N2, adjacent(X1,Y1,X2,Y2), S1=S2.

% No 2x2 black pools
:- black(X,Y), black(X+1,Y), black(X,Y+1), black(X+1,Y+1).

% Reachability constraint
% Find the first black square (top row containing black, then first column in that row)
minrow(R) :- R = #min{Y : black(X,Y), cell(X,Y)}.
mincol(C) :- C = #min{X : black(X,Y), cell(X,Y), minrow(Y)}.
% Assert that the first black square can reach itself
reachable(X,Y) :- mincol(X), minrow(Y).
% Propagate reachability through adjacent black squares
reachable(X2,Y2) :- reachable(X1,Y1), adjacent(X1,Y1,X2,Y2), black(X2,Y2).
% We need all black squares to be reachable from the first black square
:- cell(X,Y), black(X,Y), not reachable(X,Y).

% White cells (for output purposes)
white(X,Y) :- not black(X,Y), cell(X,Y).

#show black/4.
#show white/2.
