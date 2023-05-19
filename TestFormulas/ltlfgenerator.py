#!/usr/bin/python
# -*- coding: utf-8 -*-

# goal: produce test formulas for LTLf satisfiability

#####################
########## procedures
#####################

## produce the encoding of formula RespondedExistence(n)
def RE (n,file,long=0):
	count = 7
	file.write('neg(1,p0).\nor(2,p0,1).\nuntil(3,2,p0).\nnext(4,3).\nneg(5,3).\nor(6,p1,p2).\n')	
	for i in range(3,n+1):
		file.write('or(' + str(count) + ',' + str(count-1) + ',p' + str(i) + ').\n')
		count += 1
	file.write('until(' + str(count) + ',2,' + str(count-1) + ').\nnext(' + str(count+1) + ',' + str(count) + ').\n')
	file.write('or(' + str(count+2) + ',5,' + str(count) + ').\n')
	count += 3
	#### long models
	for i in range(long):
		if i == 0:
			file.write('next(' + str(count) + ',1).\n')
		else:
			file.write('next(' + str(count) + ',' + str(count-1) + ').\n')
		count += 1
	#### end long models
	file.write('isPhi(' + str(count-1) + ').\n')
	formula = count
	for i in range(1,n+1):
		file.write('neg(' + str(count) + ',p' + str(i) + ').\n')
		count += 1
	for i in range(2,formula):
		if i == 5:
			continue
		file.write('neg(' + str(count) + ',' + str(i) + ').\n')
		count += 1
	for i in range(n+1):
		file.write('sub(p' + str(i) + ').\n')
	for i in range(1,count):
		file.write('sub(' + str(i) + ').\n')



## produce the encoding of formula Response(n)
def R (n,file,long=0):
	count = 4
	file.write('neg(1,p0).\nor(2,p0,1).\nor(6,p1,p2).\n')	
	for i in range(3,n+1):
		file.write('or(' + str(count) + ',' + str(count-1) + ',p' + str(i) + ').\n')
		count += 1
	file.write('until(' + str(count) + ',2,' + str(count-1) + ').\nnext(' + str(count+1) + ',' + str(count) + ').\n')
	file.write('and(' + str(count+2) + ',p0,' + str(count) + ').\n')  
	count += 2
	file.write('until(' + str(count) + ',2,' + str(count-1) + ').\nnext(' + str(count+1) + ',' + str(count) + ').\n')
	file.write('neg(' + str(count+2) + ',' + str(count) + ').\n')
	count += 3
	#### long models
	for i in range(long):
		if i == 0:
			file.write('next(' + str(count) + ',1).\n')
		else:
			file.write('next(' + str(count) + ',' + str(count-1) + ').\n')
		count += 1
	#### end long models
	file.write('isPhi(' + str(count-1) + ').\n')
	formula = count
	for i in range(1,n+1):
		file.write('neg(' + str(count) + ',p' + str(i) + ').\n')
		count += 1
	for i in range(2,formula-1):
		file.write('neg(' + str(count) + ',' + str(i) + ').\n')
		count += 1
	for i in range(n+1):
		file.write('sub(p' + str(i) + ').\n')
	for i in range(1,count):
		file.write('sub(' + str(i) + ').\n')



## produce the encoding of formula AlternateResponse(n)
def AR (n,file,long=0):
	count = 4
	file.write('neg(1,p0).\nor(2,p0,1).\nor(6,p1,p2).\n')	
	for i in range(3,n+1):
		file.write('or(' + str(count) + ',' + str(count-1) + ',p' + str(i) + ').\n')
		count += 1
	file.write('until(' + str(count) + ',1,' + str(count-1) + ').\nnext(' + str(count+1) + ',' + str(count) + ').\n')
	file.write('or(' + str(count+2) + ',1,' + str(count+1) + ').\n')  
	count += 3
	file.write('until(' + str(count) + ',2,' + str(count-1) + ').\nnext(' + str(count+1) + ',' + str(count) + ').\n')
	file.write('neg(' + str(count+2) + ',' + str(count) + ').\n')
	count += 3
	#### long models
	for i in range(long):
		if i == 0:
			file.write('next(' + str(count) + ',1).\n')
		else:
			file.write('next(' + str(count) + ',' + str(count-1) + ').\n')
		count += 1
	#### end long models
	file.write('isPhi(' + str(count-1) + ').\n')
	formula = count
	for i in range(1,n+1):
		file.write('neg(' + str(count) + ',p' + str(i) + ').\n')
		count += 1
	for i in range(2,formula-1):
		file.write('neg(' + str(count) + ',' + str(i) + ').\n')
		count += 1
	for i in range(n+1):
		file.write('sub(p' + str(i) + ').\n')
	for i in range(1,count):
		file.write('sub(' + str(i) + ').\n')



## produce the encoding of formula ChainResponse(n)
def CR (n,file,long=0):
	count = 4
	file.write('neg(1,p0).\nor(2,p0,1).\nor(6,p1,p2).\n')	
	for i in range(3,n+1):
		file.write('or(' + str(count) + ',' + str(count-1) + ',p' + str(i) + ').\n')
		count += 1
	file.write('next(' + str(count) + ',' + str(count-1) + ').\n')
	file.write('or(' + str(count+1) + ',1,' + str(count) + ').\n')  
	count += 2
	file.write('until(' + str(count) + ',2,' + str(count-1) + ').\nnext(' + str(count+1) + ',' + str(count) + ').\n')
	file.write('neg(' + str(count+2) + ',' + str(count) + ').\n')
	count += 3
	#### long models
	for i in range(long):
		if i == 0:
			file.write('next(' + str(count) + ',1).\n')
		else:
			file.write('next(' + str(count) + ',' + str(count-1) + ').\n')
		count += 1
	#### end long models
	file.write('isPhi(' + str(count-1) + ').\n')
	formula = count
	for i in range(1,n+1):
		file.write('neg(' + str(count) + ',p' + str(i) + ').\n')
		count += 1
	for i in range(2,formula-1):
		file.write('neg(' + str(count) + ',' + str(i) + ').\n')
		count += 1
	for i in range(n+1):
		file.write('sub(p' + str(i) + ').\n')
	for i in range(1,count):
		file.write('sub(' + str(i) + ').\n')




#####################
########## generators
#####################

def RE_gen():
	for i in lengths:
		name = 'RExistence' + str(i) + '.txt'
		out_file = open(name,'w')
		RE(i,out_file)
		out_file.close()

def R_gen():
	for i in lengths:
		name = 'Response' + str(i) + '.txt'
		out_file = open(name,'w')
		R(i,out_file)
		out_file.close()

def AR_gen():
	for i in lengths:
		name = 'AlternateR' + str(i) + '.txt'
		out_file = open(name,'w')
		AR(i,out_file)
		out_file.close()

def CR_gen():
	for i in lengths:
		name = 'ChainR' + str(i) + '.txt'
		out_file = open(name,'w')
		CR(i,out_file)
		out_file.close()


#####################
########## main
#####################

lengths = [5,10,20,50,100]
RE_gen()
R_gen()
AR_gen()
CR_gen()