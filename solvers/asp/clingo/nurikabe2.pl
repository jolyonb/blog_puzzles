% Specify the grid size
#const rows=5.
#const cols=5.

% Specify the problem
% number(col, row, num).
number(1, 0, 2).
number(4, 1, 3).
number(3, 2, 1).
number(4, 4, 5).

% Set up indices for the grid
grid(X,Y) :- X=0..cols-1, Y=0..rows-1.

% Set up indices for colors
color(b; w).

% Every cell is either white or black
{cell(X, Y, C) : color(C)} = 1 :- grid(X,Y).

% No 2x2 blocks of black
:- cell(X, Y, b), cell(X, Y+1, b), cell(X+1, Y, b), cell(X+1, Y+1, b).

% Numbered cells are white
cell(X, Y, w) :- number(X, Y, N).

% Adjacency helper: is (X1, Y1) adjacent to (X2, Y2)?
adjacent(X,Y,X+1,Y) :- grid(X,Y), grid(X+1,Y).
adjacent(X,Y,X,Y+1) :- grid(X,Y), grid(X,Y+1).
adjacent(X2,Y2,X1,Y1) :- adjacent(X1,Y1,X2,Y2).

% Find all white cells that are reachable from a number
% Each number can reach itself in its own region
% reachable(X,Y,NumberX,NumberY).
reachable(X,Y,X,Y) :- number(X,Y,N).
% Propagate reachability through adjacent white squares
reachable(X2,Y2,Xn,Yn) :- reachable(X1,Y1,Xn,Yn), adjacent(X1,Y1,X2,Y2), cell(X2,Y2,w).
% White cells must be able to reach a single number
:- cell(X,Y,w), {reachable(X,Y,Xn,Yn) : number(Xn,Yn,N)} != 1.
% Each island needs to have the correct number of white cells
:- number(Xn,Yn,N), {reachable(X,Y,Xn,Yn)} != N.

% Assert all black squares are connected
% Find the first black square (top row containing black, then first column in that row)
minrow(R) :- R = #min{Y : cell(X,Y,b), grid(X,Y)}.
mincol(C) :- C = #min{X : cell(X,Y,b), grid(X,Y), minrow(Y)}.
% Assert that the first black square can reach itself
reachable(X,Y) :- mincol(X), minrow(Y).
% Propagate reachability through adjacent black squares
reachable(X2,Y2) :- reachable(X1,Y1), adjacent(X1,Y1,X2,Y2), cell(X2,Y2,b).
% We need all black squares to be reachable from the first black square
:- cell(X,Y,b), not reachable(X,Y).

% For output
black(X, Y) :- cell(X, Y, b).
white(X, Y) :- cell(X, Y, w).
#show black/2.
#show white/2.
