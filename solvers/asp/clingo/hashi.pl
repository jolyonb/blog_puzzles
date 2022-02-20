% Define possible number of bridges
bridge(N) :- N=1..max_bridges.

% Define all possible connections in the form connection(col1, ro1, col2, row2, num_bridges)
{connection(C, R, C, R2, B) : island(C, R2, N2), R < R2, bridge(B)} :- island(C, R, N).
{connection(C, R, C2, R, B) : island(C2, R, N2), C < C2, bridge(B)} :- island(C, R, N).

% Only one connection object allowed between two islands
B1 = B2 :- connection(C, R, C2, R2, B1), connection(C, R, C2, R2, B2).

% Number of connections to an island must sum to the island number
S = N :- island(C, R, N), S = #sum{B, C2, R2 : connection(C, R, C2, R2, B); B, C2, R2 : connection(C2, R2, C, R, B)}.

% A connection cannot pass through an island
:- connection(C, R1, C, R2, B), island(C, R, N), R1 < R, R < R2.
:- connection(C1, R, C2, R, B), island(C, R, N), C1 < C, C < C2.

% Connections cannot cross
:- connection(C1, R1a, C1, R1b, B1), connection(C2a, R2, C2b, R2, B2), C2a < C1, C1 < C2b, R1a < R2, R2 < R1b.

% The global condition: All islands must be connected in a single connected group.
% Islands can reach themselves
reachable(C, R, C, R) :- island(C, R, N).
% If A -> B, then B -> A
reachable(C2, R2, C1, R1) :- reachable(C1, R1, C2, R2).
% Connections extend reach
reachable(C0, R0, C1, R1) :- reachable(C0, R0, C, R), connection(C, R, C1, R1, B).
reachable(C0, R0, C1, R1) :- reachable(C0, R0, C, R), connection(C1, R1, C, R, B).
% All islands must be able to be reached from all other islands.
:- island(C1, R1, N1), island(C2, R2, N2), not reachable(C1, R1, C2, R2).

#show connection/5.
