#!/usr/bin/python3
import argparse
import subprocess
import sys,os
from pathlib import Path
from ltlf2dfa.parser.ltlf import LTLfParser
import ltlf2dfa.ltlf
import random,math

class LTLF2ASP:
    __next_formula_index : int
    __formula_to_index : dict
    __propositional_terms : set
    __program : list
    
    def __init__(self):
        self.__next_formula_index = 1
        self.__formula_to_index = dict()
        self.__propositional_terms = set()

    def getSymbolCount(self):
        return len(self.__propositional_terms)+self.__next_formula_index

    def register_formula(self,formula: str):
        if type(formula) is ltlf2dfa.ltlf.LTLfAtomic:
            return (formula,(formula.s,True))
        str_formula = str(formula)
        try:
            return self.__formula_to_index[str_formula]
        except:
            self.__formula_to_index[str_formula]=(self.__next_formula_index,False)
            self.__next_formula_index+=1
            return (self.__next_formula_index-1,False)

    def add_sub_formula(self,f):
        result = []
        formulas = [f,ltlf2dfa.ltlf.LTLfNot(f) if type(f) != ltlf2dfa.ltlf.LTLfNot else f.negate()]
        if type(f) == ltlf2dfa.ltlf.LTLfUntil:
            formulas.append(ltlf2dfa.ltlf.LTLfNext(f))
            formulas.append(ltlf2dfa.ltlf.LTLfNot(formulas[-1]))

        for formula in formulas:
            result.append((formula,self.register_formula(formula)))
        return result
    
    def rewrite(self, formula, file):
        if formula is None:
            return
        
        visit_order = []
        visit_order.append(formula)
        isPhi = True
        while len(visit_order) != 0:
            formula = visit_order.pop()
            data = self.add_sub_formula(formula)
            add_to_visit = True
            for f, (index, printed) in data:
                if type(f) is ltlf2dfa.ltlf.LTLfAtomic:
                    if not f.s in self.__propositional_terms:
                        self.__propositional_terms.add(str(f.s))
                        print(f"sub({str(f.s)}).",file=file)
                elif type(f) is ltlf2dfa.ltlf.LTLfOr:
                    t1,_ = self.register_formula(f.formulas[0])
                    t2,_ = self.register_formula(f.formulas[1])
                    if not printed:
                        print(f"or({index},{t1},{t2}).",file=file)

                    if add_to_visit:
                        visit_order.append(f.formulas[0])
                        visit_order.append(f.formulas[1])

                elif type(f) is ltlf2dfa.ltlf.LTLfAnd:
                    t1,_ = self.register_formula(f.formulas[0])
                    t2,_ = self.register_formula(f.formulas[1])
                    if not printed:
                        print(f"and({index},{t1},{t2}).",file=file)

                    if add_to_visit:
                        visit_order.append(f.formulas[0])
                        visit_order.append(f.formulas[1])


                elif type(f) is ltlf2dfa.ltlf.LTLfUntil:
                    t1,_ = self.register_formula(f.formulas[0])
                    t2,_ = self.register_formula(f.formulas[1])
                    if not printed:
                        print(f"until({index},{t1},{t2}).",file=file)
                    if add_to_visit:
                        visit_order.append(f.formulas[0])
                        visit_order.append(f.formulas[1])


                elif type(f) is ltlf2dfa.ltlf.LTLfNot:
                    t,_ = self.register_formula(f.f)
                    if not printed:
                        print(f"neg({index},{t}).",file=file)
                    if add_to_visit:
                        visit_order.append(f.f)

                elif type(f) is ltlf2dfa.ltlf.LTLfNext:
                    t,_ = self.register_formula(f.f)
                    if not printed:
                        print(f"next({index},{t}).",file=file)
                    if add_to_visit:
                        visit_order.append(f.f)
                else:
                    print("Not supported construct found")
                add_to_visit=False
                self.__formula_to_index[str(f)]=(index,True)

                if isPhi:
                    print(f"isPhi({index}).",file=file)
                    isPhi = False

        for i in range(1,self.__next_formula_index):
            print(f"sub({i}).",file=file)


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
    working_file = os.path.join(os.path.basename(ltlf_file)+".asp")

    temp_file = open(working_file, "w")
    rewriter.rewrite(formula,temp_file)
    for fact in [f"state({i})." for i in range(1, min_states +1)]:
        print(f"{fact}",file=temp_file)
    temp_file.close()

    if args.encode:
        sys.exit(0)
    
    max_states = math.pow(2,rewriter.getSymbolCount())
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