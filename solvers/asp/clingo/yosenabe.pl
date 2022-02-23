% Copied from https://github.com/atreyasha/clingo-solvers/blob/main/src/yosenabe.lp

% number(X, Y, Value) defines numbers
% area(X, Y, Value) defines areas, Value is a unique area number

% create targets and traces
% Target = set of all possible start squares for number starting at X, Y, ending up at X', Y'. I is the area index, V is the number itself
{target(X,Y,X,Y',I,V): number(X,Y,V), area(X,Y',I)}.
{target(X,Y,X',Y,I,V): number(X,Y,V), area(X',Y,I)}.

% Make trace(X', Y', X, Y) for every square covered by target(X,Y,X,Y')
% I'm guessing that ranges only work X..Y when X < Y, which is why there's four of these
trace(X..X',Y..Y',X,Y) :- target(X,Y,X',Y',_,_).
trace(X'..X,Y..Y',X,Y) :- target(X,Y,X',Y',_,_).
trace(X..X',Y'..Y,X,Y) :- target(X,Y,X',Y',_,_).
trace(X'..X,Y'..Y,X,Y) :- target(X,Y,X',Y',_,_).


% These are ... interesting. Perhaps because they're sums they don't create many rules?
% But it's basically a way of saying "each number moves to a single location, and no numbers land in the same spot"
% simplest constraints here to remove duplicates and overlapping
:-#sum{1,X,Y:target(X,Y,_,_,_,_)} != N, N = #sum{1,A,B:number(A,B,_)}.   % Count of targets used = count of numbers
:-#sum{1,X',Y':target(_,_,X',Y',_,_)} != N, N = #sum{1,A,B:number(A,B,_)}.   % Count of targets hit = count of numbers
:-#sum{1,X,Y,X',Y':target(X,Y,X',Y',_,_)} != N, N = #sum{1,A,B:number(A,B,_)}.   % Count of paths used = count of numbers


% Count of all target areas is count of underlying areas)
% constraints to ensure all shaded areas are filled up
:-#sum{1,I:target(_,_,_,_,I,_)} != N, N = #sum{1,C:area(_,_,C)}.


% Check that there are no overlaps on cells used by the traces
% complex constraints to prevent crossing by traces
:- trace(X,Y,X',_), trace(X,Y,X'',_), X''!= X'.
:- trace(X,Y,_,Y'), trace(X,Y,_,Y''), Y''!= Y'.


% Sum of target numbers matches goal for that area
% constraints to ensure goal matching
:-#sum{V,I,X,Y:target(X,Y,_,_,I,V)} != G, G = #sum{V,I:goal(I,V)}, goal(I,_).



% Just list the first four entries (X, Y) moves to (X', Y')
% project and print
target(X,Y,X',Y') :- target(X,Y,X',Y',I,V).
#show target/4.
