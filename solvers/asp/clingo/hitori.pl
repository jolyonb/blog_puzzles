% hitori.pl
% Jolyon Bloomfield February 2022
% https://blog.dodgyfysix.com, https://github.com/jolyonb/blog_puzzles
% Adapted from https://www.cs.uni-potsdam.de/~torsten/Lehre/ASP/Folien/asp-handout.pdf
% Inputs:
% Numbers:
% number(col, row, num).

% Set up adjacency mapping
adjacent(X,Y,X+1,Y) :- number(X,Y,_), number(X+1,Y,_).
adjacent(X,Y,X,Y+1) :- number(X,Y,_), number(X,Y+1,_).
adjacent(X2,Y2,X1,Y1) :- adjacent(X1,Y1,X2,Y2).

% Every square is either black or not
{ black(X,Y) } :- number(X,Y,_).

% Adjacent black squares can't be black
:- adjacent(X1,Y1,X2,Y2), black(X1,Y1), black(X2,Y2).

% The same number cannot appear twice or more in a row/column
:- number(X,Y,N), 2 { not black(X,Y2) : number(X,Y2,N) }.  % column - fixed X
:- number(X,Y,N), 2 { not black(X2,Y) : number(X2,Y,N) }.  % row - fixed Y

% Find the first white square (top row containing white, then first column in that row)
% Yes, this is overkill for vanilla hitori, where one of the first two squares will always be white,
% but it's cheap, and the general construct is useful!
minrow(R) :- R = #min{Y : not black(X,Y), number(X,Y,N)}.
mincol(C) :- C = #min{X : not black(X,Y), number(X,Y,N), minrow(Y)}.
firstwhite(X,Y) :- mincol(X), minrow(Y).

% Construct the reachability constraint
% Assert that the first white square can reach itself
reachable(X,Y) :- firstwhite(X,Y).
% Propagate reachability through adjacent white squares
reachable(X2,Y2) :- reachable(X,Y), adjacent(X,Y,X2,Y2), not black(X2,Y2).
% We need all white squares to be reachable from the first white square
:- number(X,Y,_), not black(X,Y), not reachable(X,Y).

#show black/2.
