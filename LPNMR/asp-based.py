#!/usr/bin/python3
import argparse
import subprocess
import sys,os
from pathlib import Path
from ltlf2dfa.parser.ltlf import LTLfParser
import ltlf2dfa.ltlf
import random

class LTLF2ASP:
    __next_formula_index : int
    __formula_to_index : dict
    __facts : list
    __subs : list
    __propositional_terms : set
    __program : list
    def __init__(self):
        self.__next_formula_index = 1
        self.__formula_to_index = dict()
        self.__facts = []
        self.__subs = []
        self.__propositional_terms = set()
        self.__program = []
    
    def add_propositional_term(self, term : str):
        self.__propositional_terms.add(term)

    def get_representation_for_formula(self, f):
        try:
            return self.__formula_to_index[str(f)][0] if  not type(f) is ltlf2dfa.ltlf.LTLfAtomic else str(f)
        except:
            self.__formula_to_index[str(f)] = (self.__next_formula_index, False)
            self.__next_formula_index += 1
            return self.__next_formula_index -1
    
    def is_printed(self, f):
        try:
            return self.__formula_to_index[str(f)]
            
        except:
            self.__formula_to_index[str(f)] = (self.__next_formula_index, False)
            self.__next_formula_index += 1
            return (self.__next_formula_index -1, False)
        
    def add_formula(self, f, index, isPhi):
        self.__formula_to_index[str(f)] = (index, True)
        if not isPhi:
            self.__facts.append(f"neg({self.__next_formula_index},{index}).")
            self.__next_formula_index += 1   
    
    def next_formula_index(self):
        return self.__next_formula_index
    
    def get_formula_index(self, formula):
        if str(formula) in self.__formula_to_index:
            return self.__formula_to_index[formula]
    
    def print_facts(self):
        for fact in self.__facts:
            print(fact) 

    def print_subs(self):
        for sub in self.__subs:
            print(sub)
        for i in range(1, self.__next_formula_index):
            print(f"sub({i}).")

    def get_program(self):
        if len(self.__program) == 0:
            for fact in self.__facts:
                self.__program.append(fact)
            for sub in self.__subs:
                self.__program.append(sub)
            for i in range(1, self.__next_formula_index):
                self.__program.append(f"sub({i}).")
        return self.__program
    
    def rewrite(self, formula):
        if formula is None:
            return
        
        visit_order = []
        visit_order.append(formula)
        isPhi = True
        while len(visit_order) != 0:
            f = visit_order.pop()
            if type(f) is ltlf2dfa.ltlf.LTLfAtomic:
                if not f.s in self.__propositional_terms:
                    self.__subs.append(f"sub({f.s}).")
                    self.add_propositional_term(f.s)
            elif type(f) is ltlf2dfa.ltlf.LTLfOr:
                index, printed = self.is_printed(f)
                if not printed:
                    t1 = self.get_representation_for_formula(f.formulas[0])
                    t2 = self.get_representation_for_formula(f.formulas[1])
                    self.__facts.append(f"or({index},{t1},{t2}).")
                    self.add_formula(f, index, isPhi)
                    visit_order.append(f.formulas[0])
                    visit_order.append(f.formulas[1])
            elif type(f) is ltlf2dfa.ltlf.LTLfAnd:
                index, printed = self.is_printed(f)
                if not printed:
                    t1 = self.get_representation_for_formula(f.formulas[0])
                    t2 = self.get_representation_for_formula(f.formulas[1])
                    self.__facts.append(f"and({index},{t1},{t2}).")
                    self.add_formula(f, index, isPhi)
                    visit_order.append(f.formulas[0])
                    visit_order.append(f.formulas[1])
            elif type(f) is ltlf2dfa.ltlf.LTLfUntil:
                index, printed = self.is_printed(f)
                if not printed:
                    t1 = self.get_representation_for_formula(f.formulas[0])
                    t2 = self.get_representation_for_formula(f.formulas[1])
                    self.__facts.append(f"until({index},{t1},{t2}).")
                    self.__facts.append(f"next({self.__next_formula_index},{index}).")
                    self.__next_formula_index += 1
                    self.__facts.append(f"neg({self.__next_formula_index},{self.__next_formula_index -1}).")
                    self.__next_formula_index += 1
                    self.add_formula(f, index, isPhi)
                    visit_order.append(f.formulas[0])
                    visit_order.append(f.formulas[1])
            elif type(f) is ltlf2dfa.ltlf.LTLfNot:
                index, printed = self.is_printed(f)
                if not printed:
                    t1 = self.get_representation_for_formula(f.f)
                    self.__formula_to_index[str(f)] = (index, True)
                    self.__facts.append(f"neg({index},{t1}).")             
                    visit_order.append(f.f)
            elif type(f) is ltlf2dfa.ltlf.LTLfNext:
                index, printed = self.is_printed(f)
                if not printed:
                    t = self.get_representation_for_formula(f.f)
                    self.__facts.append(f"next({index},{t}).")
                    self.add_formula(f, index, isPhi)
                    visit_order.append(f.f)
            else:
                print("Not supported construct found")
            
            if isPhi:
                isPhi = False
                self.__facts.append(f"isPhi({self.get_representation_for_formula(f)}).")



def main():
    parser = argparse.ArgumentParser(prog = "LTLF2ASP-wrapper", description = "Converts an ltlf formula into a set of facts and the calls the solver several\
                                      times with an increasing number of states until the program becomes satisfiable or a threshold in the number of states is exceeded\n")
    parser.add_argument('path_to_ltlf_formula', help="a path to a file containing an ltlf formula\n")
    parser.add_argument('path_to_asp_encoding', help="a path to a file containing the asp encoding\n")
    parser.add_argument('min_states', type=int, help="defines the minimum number of states that will be given to the solver.\n")
    parser.add_argument('states_growth', type=int, choices=[0, 1], help="0 defines an exponential growth in the number of states, 1 tries to make the states grow slower.\n")
    parser.add_argument('executable', nargs='?', help="the solver that will be called when executing this wrapper\n", default = "clingo")
    parser.add_argument('-e', "--encoder-only", dest="encode", default=False, action='store_true',help="disable solver usage and print qcir on stdout")
    args = parser.parse_args()

    ltlf_file = Path(args.path_to_ltlf_formula)
    encoding_file = Path(args.path_to_asp_encoding)
    min_states = args.min_states
    growth = args.states_growth
    executable  = args.executable
    print(f"Searching ltlf formula at {ltlf_file}")
    print(f"Searching asp encoding at {encoding_file}")
    if not ltlf_file.is_file() or not encoding_file.is_file():
        print("The specified files do not exist or are folders")
        sys.exit()
    ltlf_stream = open(ltlf_file)
    ltlf_formula = ltlf_stream.read()
    ltlf_stream.close()

    parser = LTLfParser()
    formula = parser(ltlf_formula)

    rewriter : LTLF2ASP = LTLF2ASP()
    rewriter.rewrite(formula)
    working_file = os.path.basename(ltlf_file)+".asp"

    program = rewriter.get_program()
    temp_file = open(working_file, "w")
    for fact in program + [f"state({i})." for i in range(1, min_states +1)]:
        print(f"{fact}",file=temp_file)
    temp_file.close()

    if args.encode:
        sys.exit(0)
    
    max_states = 8193
    num_states = min_states
    num_states_previous = None
    while True:
        
        if not num_states_previous is None:
            temp_file = open(working_file, "a")
            #add states
            for i in range(num_states_previous+1, num_states +1):
                print(f"state({i}).",file=temp_file)

            temp_file.close()
        try:
            command = [executable, encoding_file, working_file]
            print(F"executing with {num_states} states")
            process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, text=True)
            process.wait()
            output : str = ""
            if process.returncode == 10 or process.returncode == 30:
                output = "SAT"
            elif process.returncode == 20:
                output = "USAT"
            else:
                output = "ERROR"

            print(f"{output} using {num_states} states")
            if output == "SAT":
                break

        except subprocess.CalledProcessError as e:
            print("output while executing clingo")
            sys.exit()

        #num_states = num_states + random.randint(1, min_states) if growth == 1 else num_states * 2
        num_states_previous = num_states
        num_states = num_states + random.randint(num_states_previous, num_states +2) // 2 if growth == 1 else num_states * 2 
        if num_states > max_states:
            print("Maximum number of states exceeded")
            break


if __name__ == "__main__":
    main()