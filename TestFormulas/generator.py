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


#####################
########## generator
#####################

out_file = open('test.txt','w')
en(4,out_file)
out_file.close()