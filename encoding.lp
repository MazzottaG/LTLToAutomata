found_last:-last(N).
:-not found_last.

hasNext(N):-type(N,F),next(F,F1).
last(N):-state(N),not hasNext(N).

type(1,F):-isPhi(F).
type(N,F):-sub(F),state(N),not nType(N,F).
nType(N,F):-sub(F),state(N),not type(N,F).

%%%%%% AND operator %%%%%
:-type(N,F),and(F,X,Y),not type(N,X), last(NP), NP >= N.
:-type(N,F),and(F,X,Y),not type(N,Y), last(NP), NP >= N.

:-type(N,X),type(N,Y),and(F,X,Y),not type(N,F), last(NP), NP >= N.

%%%%%% OR operator %%%%%
:-type(N,F),or(F,X,Y),not type(N,X),not type(N,Y), last(NP), NP >= N.

:-type(N,X),or(F,X,Y),not type(N,F), last(NP), NP >= N.
:-type(N,Y),or(F,X,Y),not type(N,F), last(NP), NP >= N.

%%%%% NOT operator
:- type(N,F), neg(F,X), type(N,X), last(NP), NP >= N. 
:- state(N), neg(F,X), not type(N,X),not type(N,F), last(NP), NP >= N. 

%%%% UNTIL operator
holds_until(N,F,X,Y):-until(F,X,Y), type(N,Y).
holds_until(N,F,X,Y):-until(F,X,Y), type(N,X), type(N,F1), next(F1,F).

:-type(N,F),until(F,X,Y),not holds_until(N,F,X,Y), last(NP), NP >= N.
:-not type(N,F),holds_until(N,F,X,Y), last(NP), NP >= N.

%%%%% Missing explanation
:-type(N,F),next(F,F1),N1=N+1,not type(N1,F1), last(NP), NP >= N.
:-type(N,F),neg(F,F1),next(F1,F2),neg(F3,F2),N1=N+1, not type(N1,F3), last(NP), NP >= N.

:-state(N),not type(N,F), next(F,F1),N1=N+1,type(N1,F1), last(NP), NP >= N.

:-neg(F,F1),N1=N+1,type(N1,F),neg(F2,F3),next(F3,F1),not type(N,F2), last(NP), NP >= N.

