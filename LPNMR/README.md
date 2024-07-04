This folder contains benchmarks and ASP-based encoding used in the paper "Automata-based LTL_f Satisfiability Checking via ASP"

The benchmarks folder contains 7 sub-folders, one for each considered benchmarks.
Each benchmark folder contains all the tested instances 

The ASP-based approach discussed in the paper, can be tested with the "asp-based.py" script.
This requires ltl2dfa python package to be installed.

For all other tools we refer to https://github.com/lijwen2748/aaltaf, and https://github.com/black-sat/black


Usage example for ASP-based approach

We run an instance of AR benchmarks with an initial number of state to 1 and with an exponential growth for the number of state

python3 asp-based.py benchmarks/AR/AlternateR5.ltl ltl_encoding.asp 1 0 

