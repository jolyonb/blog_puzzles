% tent.pl
% Jolyon Bloomfield February 2022
% https://blog.dodgyfysix.com, https://github.com/jolyonb/blog_puzzles
% Inputs:
% #const r=number of rows.
% #const c=number of columns.
% Clue entries:
% row_clues(row, clue).
% col_clues(col, clue).
% tent(col, row).

% Initialization
% Define our indices
rows(0..r-1).  % Row entries, 0-indexed to align with python
cols(0..c-1).  % Column entries, 0-indexed to align with python

% Create an index for all cells we need to make decisions about
excluded(-100000,-100000).  % Just in case nothing else is excluded
cell(C, R) :- rows(R), cols(C), not excluded(C, R), not tree(C, R).

% Processing
% Rule 1: Cells either contain a tent or are empty.
{tent(C, R); empty(C, R)} = 1 :- cell(C, R).

% Rule 2: The number of tents in each column and row must match the clues
X = Y :- col_clues(C, X), Y = #count{R : tent(C, R)}.
X = Y :- row_clues(R, X), Y = #count{C : tent(C, R)}.

% Rule 3: Each tree is tied to a single orthogonally adjacent tent
orth(C1, R1, C2, R2) :- rows(R1), cols(C1), rows(R2), cols(C2), |R1-R2| + |C1-C2| = 1.
{tied(C, R, C2, R2) : orth(C, R, C2, R2), cell(C2, T2)} = 1 :- tree(C, R).
% When a tie is present, there must be a tent at the other end
tent(C, R) :- tied(_, _, C, R).

% Rule 4: Two trees cannot be tied to the same tent
C1 = C2 :- tied(C1, R1, C, R), tied(C2, R2, C, R).
R1 = R2 :- tied(C1, R1, C, R), tied(C2, R2, C, R).

% Rule 5: Tents cannot be adjacent (even diagonally)
% Horizontal/vertical
adj(Cadj, Radj, C, R) :- cell(C, R), cell(Cadj, Radj), |R-Radj| + |C-Cadj| = 1.
% Diagonal
adj(Cadj, Radj, C, R) :- cell(C, R), cell(Cadj, Radj), |R-Radj| = 1, |C-Cadj| = 1.
:- tent(C1, R1), tent(C2, R2), adj(C1, R1, C2, R2).

#show tent/2.
#show empty/2.
