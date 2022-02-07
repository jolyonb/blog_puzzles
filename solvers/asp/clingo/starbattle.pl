% starbattle.pl
% Jolyon Bloomfield February 2022
% https://blog.dodgyfysix.com, https://github.com/jolyonb/blog_puzzles
% Inputs:
% #const size=Number of rows/columns/regions.
% #const starcount=Number of stars per row/column/region.
% Region assignments:
% region(col, row, regionnum).

% Initialization
% Define a generic index for counting.
% We always have the same number of rows, columns and regions.
nums(N) :- N=0..size-1.

% Processing
% Rule 1: Place starcount stars on each row, column and region
{ star(C, R) : nums(C) } = starcount :- nums(R).     % Per row
{ star(C, R) : nums(R) } = starcount :- nums(C).     % Per column
{ star(C, R) : r(C, R, N) } = starcount :- nums(N).  % Per region

% Rule 2: Stars cannot be touching (including diagonally)
:- star(C1, R1), star(C2, R2), D=1..2, |R2-R1|**2 + |C2-C1|**2 = D.

% Rule 3: Squares without a star are empty
% This isn't needed for solving, but helps python take the intersection of multiple solutions
empty(C, R) :- nums(R), nums(C), not star(C, R).

#show star/2.
#show empty/2.
