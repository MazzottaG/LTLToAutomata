# Automata-based LTL_f Satisfiability Checking via ASP

This folder contains benchmarks and the ASP-based encoding used in the paper "Automata-based LTL_f Satisfiability Checking via ASP".

## Contents

- **benchmarks/**: Contains 7 sub-folders, one for each considered benchmark. Each benchmark folder contains all the tested instances.
- **asp-based.py**: The script to test the ASP-based approach discussed in the paper. Requires the `ltlf2dfa` Python package to be installed.

## Benchmarks

The benchmarks folder includes:

- **AR/**: Contains instances for Alternate Response.
- **CR/**: Contains instances for Chain Response.
- **R/**: Contains instances for Response.
- **RE/**: Contains instances for Responded Existence.
- **E_n/**: Contains instances for E(n) pattern.
- **S_n/**: Contains instances for S(n) pattern.
- **EL_n_m/**: Contains instances for EL(n,m) pattern.

## Requirements

- `ltlf2dfa` Python package

## Other Tools

For other tools, please refer to:
- [Aaltaf](https://github.com/lijwen2748/aaltaf)
- [Black](https://github.com/black-sat/black)

## Usage Example for ASP-based Approach

To run an instance of the AR benchmark with an initial number of states set to 1 and an exponential growth for the number of states:

```
python3 asp-based.py benchmarks/AR/AlternateR5.ltl ltl_encoding.asp 1 0
