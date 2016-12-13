import sys
import codecs
import re
from pprint import pprint
import math
from decimal import *
import time

minusInfnite = float("-inf")


def train(infile):
	
	countpi = {}
	countpitotal = 0
	countp = {}
	countptotal = {}
	countq = {}
	countqtotal = {}

	try:
		f = codecs.open(infile, "r", "utf-8")
	except IOError:
		print ("IOError: Can't Open File '%s'") % infile
		quit()
	#try:
	#	outf = codecs.open(outfile, "w", "utf-8")
	#except IOError:
	#	print ("IOError: Can't Open File '%s'") % infile
	#	quit()
	

	pre = ""

	for line in f:
		tokens = re.split(r"[\s"+u'\u3000'+"]",line)
		for t in tokens:
			l = len(t)
			for i in range(l):
				if i == 0:
					if l != 1:
						cur = 'B'						
					else:
						cur = 'S'
				elif i == l-1:
					cur = 'E'

				else:
					cur = 'M'

				try:
					countpi[cur] += 1
				except KeyError:
					countpi[cur] = 1
				countpitotal += 1

				try:
					countq[t[i],cur] += 1
				except KeyError:
					countq[t[i],cur] = 1

				try:
					countqtotal[cur] += 1
				except KeyError:
					countqtotal[cur] = 1

				if pre != "":
					try:
						countp[pre,cur] += 1
					except KeyError:
						countp[pre,cur] = 1
						
					try:
						countptotal[pre] += 1
					except KeyError:
						countptotal[pre] = 1

				pre = cur
	
	f.close()

	try:
		outf = codecs.open(infile+".para_pi", "w", "utf-8")
	except IOError:
		print ("IOError: Can't Open File '%s'") % infile
		quit()
	
	for pi in countpi:
		#countpi[pi] = math.log(countpi[pi]/countpitotal)
		countpi[pi] = Decimal(countpi[pi])/Decimal(countpitotal)
		outf.write("%s\t%.31f\n" % (pi,countpi[pi]))

	outf.close()

	try:
		outf = codecs.open(infile+".para_p", "w", "utf-8")
	except IOError:
		print ("IOError: Can't Open File '%s'") % infile
		quit()

	

	for pre,cur in countp:
		#countp[pre,cur] = math.log(countp[pre,cur]/countptotal[pre])
		countp[pre,cur] = Decimal(countp[pre,cur])/Decimal(countptotal[pre])
		outf.write("%s\t%s\t%.31f\n" % (pre,cur,countp[pre,cur]))
	
	outf.write("B\tB\t0.0\n")
	outf.write("B\tS\t0.0\n")
	outf.write("M\tB\t0.0\n")
	outf.write("M\tS\t0.0\n")
	outf.write("E\tM\t0.0\n")
	outf.write("E\tE\t0.0\n")
	outf.write("S\tM\t0.0\n")
	outf.write("S\tE\t0.0\n")
	
	outf.close()

	try:
		outf = codecs.open(infile+".para_q", "w", "utf-8")
	except IOError:
		print ("IOError: Can't Open File '%s'") % infile
		quit()

	for obs,cur in countq:
		#countq[obs,cur] = math.log(countq[obs,cur]/countqtotal[cur])
		countq[obs,cur] = Decimal(countq[obs,cur])/Decimal(countqtotal[cur])
		outf.write("%s\t%s\t%.31f\n" % (obs,cur,countq[obs,cur]))

	outf.close()

	#pprint(countpi)
	#pprint(countp)
	#pprint(countq)






def test(infile,paras):
	I = ['B','M','E','S']
	pi = {}
	p = {}
	q = {}

	try:
		fpi = codecs.open(paras+".para_pi", "r", "utf-8")
	except IOError:
		print ("IOError: Can't Open File '%s'") % infile
		quit()
	
	for line in fpi:
		para_pi = re.split(r'\t',line)
		pi[para_pi[0]] = Decimal(para_pi[1])

	fpi.close()


	try:
		fp = codecs.open(paras+".para_p", "r", "utf-8")
	except IOError:
		print ("IOError: Can't Open File '%s'") % infile
		quit()

	for line in fp:
		para_p = re.split(r'\t',line)
		p[para_p[0],para_p[1]] = Decimal(para_p[2])

	fp.close()


	try:
		fq = codecs.open(paras+".para_q", "r", "utf-8")
	except IOError:
		print ("IOError: Can't Open File '%s'") % infile
		quit()

	for line in fq:
		para_q = re.split(r'\t',line)
		q[para_q[0],para_q[1]] = Decimal(para_q[2])

	fq.close()

	#pprint(pi)
	#pprint(p)
	#pprint(q)

	try:
		f = codecs.open(infile, "r", "utf-8")
	except IOError:
		print ("IOError: Can't Open File '%s'") % infile
		quit()

	try:
		outf = codecs.open(infile+".HMM", "w", "utf-8")
	except IOError:
		print ("IOError: Can't Open File '%s'") % infile
		quit()

	for line in f:
		S = viterbi(line,I,pi,p,q)
		l = len(line)
		for i in range(l):
			outf.write(line[i])
			if (S[i] == 'E' or S[i] == 'S') and line[i] != '\n':
				outf.write('  ')
	f.close()
	outf.close()










def viterbi(O,I,pi,p,q):
	T = len(O)
	K = len(I)
	V = {}
	S = {}
	#print(T)
	
	count = {}
	counttotal = 0
	for t in O:
		counttotal += 1
		try:
			count[t] += 1
		except KeyError:
			count[t] = 1
	
	for c in count:
		#count[c] = math.log(count[c]/counttotal)
		count[c] = Decimal(count[c])/Decimal(counttotal)

	V[0,'B'] = pi['B']/(pi['B']+pi['S'])
	V[0,'S'] = pi['S']/(pi['B']+pi['S'])
	V[0,'M'] = Decimal(0)
	V[0,'E'] = Decimal(0)
			
	for t in range(1,T):		
		for k in I:
			maxvk = 0
			for i in I:
				tmp = p[i,k]*V[t-1,i]
				#if tmp < minusInfnite:
				#	tmp = minusInfnite
				if maxvk < tmp:
					maxvk = tmp
			try:
				V[t,k] = maxvk*(q[O[t],k]+count[O[t]])
			except KeyError:
				V[t,k] = maxvk*count[O[t]]

	maxst = 0
	for k in I:
		#print ("debug1",maxst,V[T-1,k])
		if maxst < V[T-1,k]:
			maxst = V[T-1,k]
			S[T-1] = k
			#print (S)
	for t in range(T-1,0,-1):

		maxst = 0
		#print ("debug2",maxst)
		for i in I:
			try:
				tmp = p[i,S[t]]*V[t-1,i]
			except KeyError:
				try:
					print ("p", p[i,S[t]])
				except KeyError:
					print ("S", S[t])
					print ("V", V[t-1,i])
			#if tmp < 0:
			#	tmp = 0
			if maxst < tmp:
				maxst = tmp
				S[t-1] = i

	return S
	#pprint (S)



if __name__ == "__main__":
    if len(sys.argv) < 3:
        print ("Usage: python[3] HHMwordsep.py [train|test] <inputfile> [<trainfile>]")
        # in case of training: 4 inputs:
        # inputfile is the training data, outputfile is the trained intputfile.para_pi,intputfile.para_p,intputfile.para_q
        # in case of testing: 5 inputs:
        # inputfile is testing data, outputfile is inputfile.results, trainfile is the input part of the above 
        quit()
    else:
    	if sys.argv[1] == "test" and sys.argv == 3:
    		print ("Usage: python[3] HHMwordsep.py [train|test] <inputfile> [<trainfile>]")
    		quit()
    	mode = sys.argv[1]
    	if mode == "train":
    		train(sys.argv[2])
    	elif mode == "test":
    		startime = time.time() * 1000
    		test(sys.argv[2],sys.argv[3])
    		stoptime = time.time() * 1000
    		print ("Time Elasp: " + str(stoptime - startime) + " milliseconds.")
    	else:
    		print ("Usage: python[3] HHMwordsep.py [train|test] <inputfile> [<trainfile>]")
    		quit()
        
