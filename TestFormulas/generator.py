#!/usr/bin/python
# -*- coding: utf-8 -*-

# goal: produce test formulas for LTLf satisfiability

#####################
########## procedures
#####################

import os,subprocess,shutil
n_values	= range(5,201,5)
fold		= "benchmarks/"
e_n 		= os.path.join(fold,"E_n")
s_n 		= os.path.join(fold,"S_n")
el_n_m 		= os.path.join(fold,"EL_n_m")

## produce the encoding of formula E(n)
def en (n,file):
	count = 3
	file.write('neg(1,p0).\nor(2,p0,1).\n')	
	for i in range(1,n+1):
		file.write('until(' + str(count) + ',2,p' + str(i) + ').\n')
		count += 1
	for i in range(3,count):
		file.write('next(' + str(count) + ',' + str(i) + ').\n')
		count += 1
	file.write('and(' + str(count) + ',3,4).\n')
	count += 1
	for i in range(5,n+3):
		file.write('and(' + str(count) + ',' + str(count-1) + ',' + str(i) + ').\n')
		count += 1
	file.write('isPhi(' + str(count-1) + ').\n')
	formula = count
	for i in range(1,n+1):
		file.write('neg(' + str(count) + ',p' + str(i) + ').\n')
		count += 1
	for i in range(2,formula):
		file.write('neg(' + str(count) + ',' + str(i) + ').\n')
		count += 1
	for i in range(n+1):
		file.write('sub(p' + str(i) + ').\n')
	for i in range(1,count):
		file.write('sub(' + str(i) + ').\n')


## produce the encoding of formula E(n) with long models
def eln (n,m,file):
	count = 3
	file.write('neg(1,p0).\nor(2,p0,1).\n')	
	for i in range(1,n+1):
		file.write('until(' + str(count) + ',2,p' + str(i) + ').\n')
		count += 1
	for i in range(3,count):
		file.write('next(' + str(count) + ',' + str(i) + ').\n')
		count += 1
	file.write('and(' + str(count) + ',3,4).\n')
	count += 1
	for i in range(5,n+3):
		file.write('and(' + str(count) + ',' + str(count-1) + ',' + str(i) + ').\n')
		count += 1
	formulae = count-1
	file.write('next(' + str(count) + ',p0).\n')
	count += 1
	for i in range(count,count+m-1):
		file.write('next(' + str(count) + ',' + str(count-1) + ').\n')
		count += 1
	file.write('and(' + str(count) + ',' + str(formulae) + ',' + str(count-1) + ').\n')
	file.write('isPhi(' + str(count) + ').\n')
	count += 1
	formula = count
	for i in range(1,n+1):
		file.write('neg(' + str(count) + ',p' + str(i) + ').\n')
		count += 1
	for i in range(2,formula):
		file.write('neg(' + str(count) + ',' + str(i) + ').\n')
		count += 1
	for i in range(n+1):
		file.write('sub(p' + str(i) + ').\n')
	for i in range(1,count):
		file.write('sub(' + str(i) + ').\n')



## produce the encoding of formula S(n)
def sn (n,file):
	count = 3
	file.write('neg(1,p0).\nor(2,p0,1).\n')	
	for i in range(1,n+1):
		file.write('neg(' + str(count) + ',p' + str(i) + ').\n')
		count += 1
	for i in range(3,count):
		file.write('until(' + str(count) + ',2,' + str(i) + ').\n')
		count += 1
	for i in range(n+3,count):
		file.write('next(' + str(count) + ',' + str(i) + ').\n')
		count += 1
	file.write('and(' + str(count) + ',' + str(n+3) + ',' + str(n+4) + ').\n')
	count += 1
	for i in range(n+5,2*n+3):
		file.write('and(' + str(count) + ',' + str(count-1) + ',' + str(i) + ').\n')
		count += 1
	file.write('isPhi(' + str(count-1) + ').\n')
	formula = count
	file.write('neg(' + str(count) + ',2).\n')
	count += 1
	for i in range(n+3,formula):
		file.write('neg(' + str(count) + ',' + str(i) + ').\n')
		count += 1
	for i in range(n+1):
		file.write('sub(p' + str(i) + ').\n')
	for i in range(1,count):
		file.write('sub(' + str(i) + ').\n')


#####################
########## generators
#####################

def e_gen():
	for i in n_values:
		name = 'e' + str(i) + '.txt'
		name = os.path.join(e_n,name)
		out_file = open(name,'w')
		en(i,out_file)
		out_file.close()
		subprocess.getoutput(f"bash ../build-inst-with-states.bash {name} {i} && mv inst.lp {name}")
	shutil.copyfile(os.path.join("..","encoding.prop.lp"),os.path.join(e_n,"encoding.asp"))
	shutil.copyfile(os.path.join("..","constraint.prop.lp"),os.path.join(e_n,"constraint.asp"))

def el_gen():
	for i in n_values:
		for j in [int(i/2),i+int(i/2)]:
			name = 'el' + str(i) + '-' + str(j) + '.txt'
			name = os.path.join(el_n_m,name)
			out_file = open(name,'w')
			eln(i,j,out_file)
			out_file.close()
			subprocess.getoutput(f"bash ../build-inst-with-states.bash {name} {j+1} && mv inst.lp {name}")
	shutil.copyfile(os.path.join("..","encoding.prop.lp"),os.path.join(el_n_m,"encoding.asp"))
	shutil.copyfile(os.path.join("..","constraint.prop.lp"),os.path.join(el_n_m,"constraint.asp"))
def s_gen():
	for i in n_values:
		name = 's' + str(i) + '.txt'
		name = os.path.join(s_n,name)
		out_file = open(name,'w')
		sn(i,out_file)
		out_file.close()
		subprocess.getoutput(f"bash ../build-inst-with-states.bash {name} {i} && mv inst.lp {name}")
	shutil.copyfile(os.path.join("..","encoding.prop.lp"),os.path.join(s_n,"encoding.asp"))
	shutil.copyfile(os.path.join("..","constraint.prop.lp"),os.path.join(s_n,"constraint.asp"))

#####################
########## main
#####################
for fold in [e_n,s_n,el_n_m]:
	if os.path.exists(fold):
		for file in os.listdir(fold):
			os.remove(os.path.join(fold,file))
	else:
		os.mkdir(fold)
		
e_gen()
el_gen()
s_gen()
