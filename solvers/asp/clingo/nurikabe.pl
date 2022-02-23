% Specify the grid size
#const rows=5.
#const cols=5.

% Specify the problem
% number(col, row, num).
number(1, 0, 2).
number(4, 1, 3).
number(3, 2, 1).
number(4, 4, 5).

% Set up indices for rows and columns
row(Y) :- Y=0..rows-1.
col(X) :- X=0..cols-1.

% Set up indices for colors
color(b; w).

% Every cell is either white or black
{cell(X, Y, C) : color(C)} = 1 :- col(X), row(Y).

% No 2x2 blocks of black
:- cell(X, Y, b), cell(X, Y+1, b), cell(X+1, Y, b), cell(X+1, Y+1, b), col(X), row(Y).

% Numbered cells are white
cell(X, Y, w) :- number(X, Y, N).

% For a given cell, establish which cells of the same color it is connected to.
% Adjacency helper: is (X1, Y1) adjacent to (X2, Y2)?
adj(X1, Y1, X2, Y2) :- col(X1), col(X2), row(Y1), row(Y2), |X2-X1| + |Y2-Y1| = 1.
% Cells are connected to themselves
connected(C, X, Y, X, Y) :- cell(X, Y, C).
% If cell A is connected to cell B, and cell B is adjacent to cell C of the same color, cell A is connected to cell C
connected(C, X1, Y1, X3, Y3) :- connected(C, X1, Y1, X2, Y2), cell(X3, Y3, C), adj(X2, Y2, X3, Y3).

% White cells must be connected to a single number
:- cell(X, Y, w), {connected(w, X, Y, Xn, Yn) : number(Xn, Yn, N)} != 1.

% All black cells must be connected
:- cell(X1, Y1, b), cell(X2, Y2, b), not connected(b, X1, Y1, X2, Y2).

% Each island needs to have the correct number of white cells
:- number(Xn, Yn, N), {connected(w, Xn, Yn, X, Y) : row(Y), col(X)} != N.

% For output
black(X, Y) :- cell(X, Y, b).
white(X, Y) :- cell(X, Y, w).
#show black/2.
#show white/2.
