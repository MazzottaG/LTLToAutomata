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



#####################################################
#### VARDI STYLE FORMULAS
#####################################################

def vRE(n,file,long=0):
	if long > 0:
		file.write('(')
	file.write('(F x) -> (F (')
	for i in range(1,n):
		file.write('y' + str(i) + ' | ')
	file.write('y' + str(n) + '))')
	if long > 0:
		file.write(') & ( ')
		for i in range(long):
			file.write('X ( ')
		file.write(' z )')
		for i in range(long):
			file.write(')')

def vR(n,file,long=0):
	if long > 0:
		file.write('(')
	file.write('G( x -> F (')
	for i in range(1,n):
		file.write('y' + str(i) + ' | ')
	file.write('y' + str(n) + '))')
	if long > 0:
		file.write(') & ( ')
		for i in range(long):
			file.write('X ( ')
		file.write(' z )')
		for i in range(long):
			file.write(')')

def vAR(n,file,long=0):
	if long > 0:
		file.write('(')
	file.write('G( x -> X ( (~x) U (')
	for i in range(1,n):
		file.write('y' + str(i) + ' | ')
	file.write('y' + str(n) + ')))')
	if long > 0:
		file.write(') & ( ')
		for i in range(long):
			file.write('X ( ')
		file.write(' z )')
		for i in range(long):
			file.write(')')

def vCR(n,file,long=0):
	if long > 0:
		file.write('(')
	file.write('G( x -> X (')
	for i in range(1,n):
		file.write('y' + str(i) + ' | ')
	file.write('y' + str(n) + '))')
	if long > 0:
		file.write(') & ( ')
		for i in range(long):
			file.write('X ( ')
		file.write(' z )')
		for i in range(long):
			file.write(')')

def ve(n,file):
	file.write('(')
	for i in range(1,n):
		file.write(' F ( y' + str(i) + ' ) & ')
	file.write(' F ( y' + str(i) + ' ))')

def vel(n,m,file):
	file.write('(')
	for i in range(1,n):
		file.write(' F ( y' + str(i) + ' ) & ')
	file.write(' F ( y' + str(i) + ' )) & (')
	for i in range(m):
		file.write(' X (')
	file.write(' x )')
	for i in range(m):
		file.write(')')

def vs(n,file):
	file.write('( ')
	for i in range(1,n):
		file.write(' G ( y' + str(i) + ' ) & ')
	file.write(' G ( y' + str(i) + ' ))')

#####################
########## generators
#####################

def RE_gen():
	if vardi:
		prefix = 'v'
	else:
		prefix = ''
	for i in lengths:
		name = prefix + 'RExistence' + str(i) + '.txt'
		out_file = open(name,'w')
		if vardi:
			vRE(i,out_file)
		else:
			RE(i,out_file)
		out_file.close()

def R_gen():
	if vardi:
		prefix = 'v'
	else:
		prefix = ''
	for i in lengths:
		name = prefix + 'Response' + str(i) + '.txt'
		out_file = open(name,'w')
		if vardi:
			vR(i,out_file)
		else:
			R(i,out_file)
		out_file.close()

def AR_gen():
	if vardi:
		prefix = 'v'
	else:
		prefix = ''
	for i in lengths:
		name = prefix + 'AlternateR' + str(i) + '.txt'
		out_file = open(name,'w')
		if vardi:
			vAR(i,out_file)
		else:
			AR(i,out_file)
		out_file.close()

def CR_gen():
	if vardi:
		prefix = 'v'
	else:
		prefix = ''
	for i in lengths:
		name = prefix + 'ChainR' + str(i) + '.txt'
		out_file = open(name,'w')
		if vardi:
			vCR(i,out_file)
		else:
			CR(i,out_file)
		out_file.close()


#####################
########## main
#####################

vardi=False
#vardi=True
lengths = [] #[5,10,20,50,100]
RE_gen()
R_gen()
AR_gen()
CR_gen()

out = open('test.txt','w')
vel(4,5,out)
out.close()
