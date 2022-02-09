% See puzzle in numbersquare.png
% Aim is to fill in empty squares with numbers 1-16 (15 is already provided).

% Define letters and numbers for use
letters(a;b;c;d;e;f;g;h;i;j;k;l;m;n;o;p).
numbers(1..16).

% box(letter, number) must be between 1 and 16
{box(L, N) : numbers(N)} = 1 :- letters(L).

% box p = 15
box(p, 15).

% Numbers can only be used once
X = Y :- box(X, N), box(Y, N), numbers(N), letters(X; Y).

% Equations to satisfy
% Be careful with division; we only have integer division available!
% Horizontal equations
A+B-C*D = -113 :- box(a, A), box(b, B), box(c, C), box(d, D).
E+F+G-H = 33   :- box(e, E), box(f, F), box(g, G), box(h, H).
I+J*K-L = 1    :- box(i, I), box(j, J), box(k, K), box(l, L).
M*N-O-P = 24   :- box(m, M), box(n, N), box(o, O), box(p, P).
% Vertical equations
A+E+I*M = 52 :- box(a, A), box(e, E), box(i, I), box(m, M).
B+F-J-N = 15 :- box(b, B), box(f, F), box(j, J), box(n, N).
C-G*O/K = 3  :- box(c, C), box(g, G), box(k, K), box(o, O).  % Out of order due to integer divide
D+H-L+P = 25 :- box(d, D), box(h, H), box(l, L), box(p, P).

#show box/2.
