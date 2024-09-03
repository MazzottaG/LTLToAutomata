found_last:-last(N).
:-not found_last.

hasNext(N):-type(N,F),next(F,F1).
last(N):-state(N),not hasNext(N).
valid_state(N):-state(N),last(NP), NP >= N.

neg(X,F):-neg(F,X).
:-isPhi(F),not type(1,F).

type(N,F) :-state(N), sub(F), neg(F,F1), not type(N,F1).
type(N,F1) :-state(N), sub(F), neg(F,F1), not type(N,F).

%%%%%% AND operator %%%%%
:-and(F,X,Y), type(N,F),not type(N,X), valid_state(N).
:-and(F,X,Y), type(N,F),not type(N,Y), valid_state(N).

:-and(F,X,Y),type(N,X),type(N,Y),not type(N,F), valid_state(N).

%%%%%% OR operator %%%%%
:-or(F,X,Y),type(N,F),not type(N,X),not type(N,Y), valid_state(N).

:-or(F,X,Y),type(N,X),not type(N,F), valid_state(N).
:-or(F,X,Y),type(N,Y),not type(N,F), valid_state(N).

%%%% UNTIL operator
holds_until(N,F,X,Y):-until(F,X,Y), type(N,Y).
holds_until(N,F,X,Y):-until(F,X,Y),type(N,X),next(F1,F),type(N,F1).
:-until(F,X,Y),type(N,F),not holds_until(N,F,X,Y), valid_state(N).
:-not type(N,F),holds_until(N,F,X,Y), valid_state(N).


%%%%% if at type N holds NEXT F1 then at N+1 it must hold F1
:-next(F,F1),type(N,F),N1=N+1,state(N1),not type(N1,F1), valid_state(N).

%%%%% if at type N+1 it holds F then at N it must hold (NEXT F)
:-state(N), not type(N,F), next(F,F1),N1=N+1,type(N1,F1), valid_state(N).



%%%%% if at type N holds (NOT (NEXT F)) then at N+1 it must hold (NOT F)
:-neg(F,F1),next(F1,F2),neg(F3,F2),type(N,F),N1=N+1,state(N1), not type(N1,F3), valid_state(N).

%%%%% if at type N+1 it holds (NOT F) then at N it must hold (NOT NEXT F)
:-state(N), N1=N+1, type(N1,F), neg(F,F1),next(F3,F1),neg(F2,F3),not type(N,F2), valid_state(N).
