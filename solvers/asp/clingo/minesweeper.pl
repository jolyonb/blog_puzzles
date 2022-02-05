% minesweeper.pl
% Jolyon Bloomfield February 2022
% Inputs:
% #const r=number of rows.
% #const c=number of columns.
% Clue entries:
% number(col, row, num).

% Initialization
% Define our indices
rows(1..r).  % Row entries
cols(1..c).  % Column entries
nums(0..8).  % Allowed numbers in a cell

% Create an index for all cells we can manipulate
excluded(-100000,-100000).  % Just in case nothing else is excluded
cell(C, R) :- rows(R), cols(C), not excluded(C, R).

% Processing
% Rule 1: All cells must contain one of a mine or a number from 0 to 8
{number(C, R, Z) : nums(Z) ; mine(C, R)} = 1 :- cell(C, R).

% Rule 2: Cells containing a number must have that many mines adjacent to them
{mine(Cadj, Radj) : adj(Cadj, Radj, C, R)} = N :- number(C, R, N).

% Adjacency rule, specifying if (Cadj, Radj) is adjacent to (C, R)
adj(Cadj, Radj, C, R) :- cell(C, R), cell(Cadj, Radj), |R-Radj|**2 + |C-Cadj|**2 <= 2.

#show mine/2.
#show number/3.
