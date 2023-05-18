#!/usr/bin/python
# -*- coding: utf-8 -*-

# goal: produce test formulas for LTLf satisfiability

#####################
########## procedures
#####################

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
	for i in [3,10,20]:
		name = 'e' + str(i) + '.txt'
		out_file = open(name,'w')
		en(i,out_file)
		out_file.close()

def el_gen():
	for i in [3,10,20]:
		for j in [5,10,15]:
			name = 'el' + str(i) + '-' + str(j) + '.txt'
			out_file = open(name,'w')
			eln(i,j,out_file)
			out_file.close()

def s_gen():
	for i in [3,10,20]:
		name = 's' + str(i) + '.txt'
		out_file = open(name,'w')
		sn(i,out_file)
		out_file.close()


#####################
########## main
#####################

e_gen()
el_gen()
s_gen()
