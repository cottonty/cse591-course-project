# encoding=utf-8
import jieba
import codecs
import re
from pprint import pprint
import math
import sys
from decimal import *
import time

#seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
#print("Default Mode: " + "/ ".join(seg_list))  # 精确模式

#jieba.load_userdict(file_name) # file_name 为文件类对象或自定义词典的路径
#* 词典格式和 `dict.txt` 一样，一个词占一行；每一行分三部分：词语、词频（可省略）、词性（可省略），用空格隔开，顺序不可颠倒。`file_name`

def train(infile):
	try:
		f = codecs.open(infile, "r", "utf-8")
	except IOError:
		print ("IOError: Can't Open File '%s'") % infile
		quit()

	freq = {}
	#countall = 0
	for line in f:
		tokens = re.split(r"[\s"+u'\u3000'+"]",line)
		for t in tokens:
			try:
				freq[t] += 1
			except KeyError:
				freq[t] = 1
			#countall += 1

	f.close()

	try:
		outf = codecs.open("dict.txt", "w", "utf-8")
	except IOError:
		print ("IOError: Can't Open File '%s'") % infile
		quit()

	
	for fq in freq:
		outf.write("%s %d\n" % (fq,freq[fq]))
	#outf.write("\n")
	outf.close()


def test(infile):
	try:
		f = codecs.open(infile, "r", "utf-8")
	except IOError:
		print ("IOError: Can't Open File '%s'") % infile
		quit()

	try:
		outf = codecs.open(infile+".plus", "w", "utf-8")
	except IOError:
		print ("IOError: Can't Open File '%s'") % infile
		quit()

	for line in f:
		seg_list = jieba.cut(line, cut_all=False)
		for w in seg_list:
			outf.write("%s " % w)
		#outf.write("\n")
    	
	f.close()
	outf.close()

def testnoHMM(infile):
	try:
		f = codecs.open(infile, "r", "utf-8")
	except IOError:
		print ("IOError: Can't Open File '%s'") % infile
		quit()

	try:
		outf = codecs.open(infile+".no", "w", "utf-8")
	except IOError:
		print ("IOError: Can't Open File '%s'") % infile
		quit()

	for line in f:
		seg_list = jieba.cut(line, cut_all=False, HMM=False)
		for w in seg_list:
			outf.write("%s " % w)
		#outf.write("\n")
    	
	f.close()
	outf.close()





if __name__ == "__main__":
	if len(sys.argv) != 3:
		print ("Usage: python DictplusHMM.py [train|test|noHMM] <inputfile>")
		quit()
	else:
		mode = sys.argv[1]
		if mode == "train":
			train(sys.argv[2])
		elif mode == "test":
			startime = time.time() * 1000
			test(sys.argv[2])
			stoptime = time.time() * 1000
			print "Time Elasp: " + str(stoptime - startime) + " milliseconds."
		elif mode == "noHMM":
			startime = time.time() * 1000
			testnoHMM(sys.argv[2])
			stoptime = time.time() * 1000
			print "Time Elasp: " + str(stoptime - startime) + " milliseconds."
		else:
			print ("Usage: python DictplusHMM.py [train|test] <inputfile>")
			quit()
