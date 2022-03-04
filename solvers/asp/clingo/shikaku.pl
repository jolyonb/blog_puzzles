% Specify the grid size
#const rows=5.
#const cols=5.

% Specify the problem
% number(col, row, num, regionnum).   % TODO: get rid of regionnum, use col+row as key instead
number(0,0,2,1).
number(1,0,2,2).
number(2,0,2,3).
number(3,0,2,4).
number(3,2,4,5).
number(4,2,5,6).
number(1,3,2,7).
number(3,3,2,8).
number(0,4,4,9).

% Set up indices for cells
cell(X,Y) :- X=0..cols-1, Y=0..rows-1.

% Each cell (X, Y) gets mapped to a single region (including only nearby possibilities)
{region(X,Y,R) : number(X0,Y0,N,R), |X-X0|*|Y-Y0| <= N} = 1 :- cell(X, Y).

% Number cells belong to their own region
region(X,Y,R) :- number(X,Y,N,R).

% Require connection from each cell to the region's number cell
adjacent(X,Y,X+1,Y) :- cell(X,Y), cell(X+1,Y).
adjacent(X,Y,X,Y+1) :- cell(X,Y), cell(X,Y+1).
adjacent(X2,Y2,X1,Y1) :- adjacent(X1,Y1,X2,Y2).
% Each number can reach itself in its own region
reachable(X,Y,R) :- number(X,Y,N,R).
% Propagate reachability through adjacent squares of the same region
reachable(X2,Y2,R) :- reachable(X1,Y1,R), adjacent(X1,Y1,X2,Y2), region(X2,Y2,R).
% All cells in a region must be reachable
:- region(X,Y,R), not reachable(X,Y,R).

% Rectangular constraint: if three corners of a 2x2 block are in a single region,
% then so must the 4th (4 copies of this constraint, one for each corner)
:- region(X,Y,R), region(X+1,Y,R), region(X,Y+1,R), not region(X+1,Y+1,R).
:- region(X,Y,R), region(X+1,Y,R), not region(X,Y+1,R), region(X+1,Y+1,R).
:- region(X,Y,R), not region(X+1,Y,R), region(X,Y+1,R), region(X+1,Y+1,R).
:- not region(X,Y,R), region(X+1,Y,R), region(X,Y+1,R), region(X+1,Y+1,R).

% Count of cells in a region must equal number for that region.
N1 = N2 :- number(X1,Y1,N1,R), N2 = #count{X2,Y2 : region(X2,Y2,R)}.

#show region/3.
