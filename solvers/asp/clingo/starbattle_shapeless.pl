% starbattle_shapeless.pl
% Jolyon Bloomfield February 2022
% https://blog.dodgyfysix.com, https://github.com/jolyonb/blog_puzzles
% Inputs:
% #const size=Number of rows/columns/regions.
% #const starcount=Number of stars per row/column/region.
% Exclusions:
% excluded(col, row).

% Initialization
% Define a generic index for counting.
% We always have the same number of rows and columns.
nums(N) :- N=0..size-1.

% Processing
% Rule 1: Place starcount stars on each row and column.
{ star(C, R) : nums(C) } = starcount :- nums(R).     % Per row
{ star(C, R) : nums(R) } = starcount :- nums(C).     % Per column

% Rule 2: Stars cannot be touching (including diagonally)
:- star(C1, R1), star(C2, R2), D=1..2, |R2-R1|**2 + |C2-C1|**2 = D.

% Rule 3: Excluded squares cannot contain a star
:- star(C, R), excluded(C, R).

% Rule 4: Mark empty squares
% This isn't needed for solving, but helps python take the intersection of multiple solutions
empty(C, R) :- nums(R), nums(C), not star(C, R), not excluded(C, R).

#show star/2.
#show empty/2.
