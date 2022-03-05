% statue_park.pl
% Jolyon Bloomfield February 2022
% https://blog.dodgyfysix.com, https://github.com/jolyonb/blog_puzzles
% Inputs:
% #const rows=number of rows.
% #const cols=number of columns.
% Black circles
% black_circ(col, row).
% White circles
% white_circ(col, row).
% Shapes:
% Define all available shapes, including all rotations and reflections.
% Each shape will be defined as a series of cells (X, Y), where (0, 0) is the "anchor" cell,
% which must be included in the shape.
% shape(name, orientation, x, y).
% Information on available shapes
% shape_entry(shape_num,shape_name).

% Indices
% Cell indices
cell(C, R) :- R=0..rows-1, C=0..cols-1.
% Shape indices
shape(S, O) :- shape(S, O, X, Y).
% Shape sizes
shape_size(S, C) :- shape(S, O), C = #count{Sx, Sy : shape(S, O, Sx, Sy)}.

% Solving
% Possible shape placements
% For each X, Y in the grid, try placing each shape S in orientation O at anchor point (X,Y).
% Count the number of cells that can be placed; if it equals the cell count for the shape,
% it's a valid possibility.
% valid_anchor_loc(shape, orientation, anchorx, anchory).
valid_anchor_loc(S,O,X,Y) :- cell(X,Y), shape(S,O), shape_size(S,C1),
                             C2=#count{Cx,Cy : cell(Cx,Cy), shape(S,O,Dx,Dy), Cx=X+Dx, Cy=Y+Dy, not white_circ(Cx,Cy)},
                             C1=C2.

% Place each shape entry at one position
% placement(shape_number, shape_name, orientation, anchorx, anchory)
{ placement(N,S,O,X,Y) : valid_anchor_loc(S,O,X,Y) } = 1 :- shape_entry(N,S).

% Given the selected placement entries, label filled cells as black.
% We have two versions here, one that includes shape information, and one that doesn't.
% black(x, y, shape_number, shape_name).
% black(x, y).
black(Xabs,Yabs,N,S) :- cell(X,Y), placement(N,S,O,X,Y), shape(S,O,Dx,Dy), Xabs=X+Dx, Yabs=Y+Dy.
black(X,Y) :- black(X,Y,N,S).
% Any cell that isn't black is white
white(X,Y) :- cell(X,Y), not black(X,Y).

% Adjacent black cells must come from the same shape entry
% We set up adjacency atoms because we will need them for reachability later
adjacent(X,Y,X+1,Y) :- cell(X,Y), cell(X+1,Y).
adjacent(X,Y,X,Y+1) :- cell(X,Y), cell(X,Y+1).
adjacent(X2,Y2,X1,Y1) :- adjacent(X1,Y1,X2,Y2).
N1 = N2 :- black(X1,Y1,N1,S1), black(X2,Y2,N2,S2), adjacent(X1,Y1,X2,Y2).

% Black circles cannot be white
:- black_circ(X,Y), white(X,Y).
% White circles cannot be black
:- white_circ(X,Y), black(X,Y).

% Reachability constraint
% Find the first white square (top row containing white, then first column in that row)
minrow(R) :- R = #min{Y : white(X,Y), cell(X,Y)}.
mincol(C) :- C = #min{X : white(X,Y), cell(X,Y), minrow(Y)}.
% Assert that the first white square can reach itself
reachable(X,Y) :- mincol(X), minrow(Y).
% Propagate reachability through adjacent white squares
reachable(X2,Y2) :- reachable(X1,Y1), adjacent(X1,Y1,X2,Y2), white(X2,Y2).
% We need all white squares to be reachable from the first white square
:- cell(X,Y), white(X,Y), not reachable(X,Y).

#show black/4.
#show white/2.
#show black/2.
