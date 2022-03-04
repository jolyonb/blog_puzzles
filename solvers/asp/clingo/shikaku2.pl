% Specify the grid size
#const rows=5.
#const cols=5.

% Specify the problem
% number(col, row, num).
number(0,0,2).
number(1,0,2).
number(2,0,2).
number(3,0,2).
number(3,2,4).
number(4,2,5).
number(1,3,2).
number(3,3,2).
number(0,4,4).

% Set up indices for cells
cell(X,Y) :- X=0..cols-1, Y=0..rows-1.

% Each cell (X, Y) gets mapped to a single number cell (including only nearby possibilities)
{region(X,Y,X0,Y0) : number(X0,Y0,N), |X-X0|*|Y-Y0| <= N} = 1 :- cell(X, Y).

% Number cells belong to their own region
region(X,Y,X,Y) :- number(X,Y,N).

% Require connection from each cell to the region's number cell
% Adjacency helper
adjacent(X,Y,X+1,Y) :- cell(X,Y), cell(X+1,Y).
adjacent(X,Y,X,Y+1) :- cell(X,Y), cell(X,Y+1).
adjacent(X2,Y2,X1,Y1) :- adjacent(X1,Y1,X2,Y2).
% Each number can reach itself in its own region
reachable(X,Y,X,Y) :- number(X,Y,N).
% Propagate reachability through adjacent squares of the same region
reachable(X2,Y2,X0,Y0) :- reachable(X1,Y1,X0,Y0), adjacent(X1,Y1,X2,Y2), region(X2,Y2,X0,Y0).
% All cells in a region must be reachable
:- region(X,Y,X0,Y0), not reachable(X,Y,X0,Y0).

% Rectangular constraint: if three corners of a 2x2 block are in a single region,
% then so must the 4th (4 copies of this constraint, one for each corner)
:- region(X,Y,X0,Y0), region(X+1,Y,X0,Y0), region(X,Y+1,X0,Y0), not region(X+1,Y+1,X0,Y0).
:- region(X,Y,X0,Y0), region(X+1,Y,X0,Y0), not region(X,Y+1,X0,Y0), region(X+1,Y+1,X0,Y0).
:- region(X,Y,X0,Y0), not region(X+1,Y,X0,Y0), region(X,Y+1,X0,Y0), region(X+1,Y+1,X0,Y0).
:- not region(X,Y,X0,Y0), region(X+1,Y,X0,Y0), region(X,Y+1,X0,Y0), region(X+1,Y+1,X0,Y0).

% Count of cells in a region must equal number for that region.
N1 = N2 :- number(X0,Y0,N1), N2 = #count{X1,Y1 : region(X1,Y1,X0,Y0)}.

#show region/4.
