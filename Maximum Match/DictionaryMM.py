from __future__ import division
# you need to install mmseg to excute this file
# python setup.py install


#import mmseg
from pymmseg import mmseg

import codecs
import re
from pprint import pprint
import math
import sys
from decimal import *
import time


reload(sys)  
sys.setdefaultencoding('utf8')

def train(infile):

	try:
		f = codecs.open(infile, "r", "utf-8")
	except IOError:
		print ("IOError: Can't Open File '%s'") % infile
		quit()

	freq = {}
	words = {}
	countall = 0
	for line in f:
		tokens = re.split(r"[\s"+u'\u3000'+"]",line)
		for t in tokens:
			#print t
			for c in t:
				try:
					freq[c] += 1
				except KeyError:
					freq[c] = 1
				countall += 1
			words[t] = len(t)
	f.close()


	for fq in freq:
		freq[fq] = Decimal(freq[fq])/Decimal(countall)

	try:
		outf = codecs.open(infile+".chars.dic", "w", "utf-8")
	except IOError:
		print ("IOError: Can't Open File '%s'") % infile
		quit()

	for fq in freq:
		outf.write("%.31f %s\n" % (freq[fq],fq))
	outf.write("\n")
	outf.close()

	try:
		outf = codecs.open(infile+".words.dic", "w", "utf-8")
	except IOError:
		print ("IOError: Can't Open File '%s'") % infile
		quit()

	for w in words:
		outf.write("%d %s\n" % (words[w],w))
	outf.write("\n")
	outf.close()

def test(infile,dictfile="default"):

	if dictfile == "default":
		mmseg.dict_load_defaults()
	else:
		mmseg.dict_load_words(dictfile+".words.dic")
		mmseg.dict_load_chars(dictfile+".chars.dic")

	try:
		f = codecs.open(infile, "r", "utf-8")
	except IOError:
		print ("IOError: Can't Open File '%s'") % infile
		quit()

	try:
		outf = codecs.open(infile+".mmseg", "w", "utf-8")
	except IOError:
		print ("IOError: Can't Open File '%s'") % infile
		quit()

	firstline = True
	for line in f:
		#print line
		if firstline == True:
			firstline = False
		else:
			outf.write("\n")

		algor = mmseg.Algorithm(codecs.encode(line,"utf-8"))
		for tok in algor:
			#print '%s [%d..%d]' % (tok.text, tok.start, tok.end)
			outf.write("%s " % tok.text)
    	
	f.close()
	outf.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print ("Usage: python DictionaryMM.py [train|test] <inputfile> [<trainfile>]")
        quit()
    else:
    	mode = sys.argv[1]
    	if mode == "train":
    		if len(sys.argv) != 3:
    			print ("Usage: python DictionaryMM.py [train|test] <inputfile> [<trainfile>]")
    			quit()
    		train(sys.argv[2])
    	elif mode == "test":
    		if len(sys.argv) == 3:
    			startime = time.time() * 1000
    			test(sys.argv[2])
    			stoptime = time.time() * 1000
    			print "Time Elasp: " + str(stoptime - startime) + " milliseconds."
    		elif len(sys.argv) == 4:
    			startime = time.time() * 1000
    			test(sys.argv[2],sys.argv[3])
    			stoptime = time.time() * 1000
    			print "Time Elasp: " + str(stoptime - startime) + " milliseconds."
    		else:
    			print ("Usage: python DictionaryMM.py [train|test] <inputfile> [<trainfile>]")
    			quit()
    	else:
    		print ("Usage: python DictionaryMM.py [train|test] <inputfile> [<trainfile>]")
    		quit()


