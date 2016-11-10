# CSE591-Course-Project Proposal

Title: Chinese word segmentation with HMM

1. Basic Idea:

	Viterbi Algorithm
	Observed Sequence -> Status Sequence

--

HMM Setting
{
	StatusSet, 
	ObservedSet, 
	TransProbMatrix, 
	EmitProbMatrix, 
	InitStatus
}

--

StatusSet:
{
	B: appear at the begin of a word
	M: appear at middle of a word
	E: appear at the end of a word
	S: single char as a word
}

Some Constriction:
	B -> M|E
	M -> M|E
	E -> B|S
	S -> B|S

--

InitStatus:
	Prob, or log(prob)

--

TransProbMatrix: by statistical method
	P(Status[i]|Status[i-1]) 

--

EmitProbMatrix by statistical method
	P(Observed[i]|Status[j])



2. Dataset

	A large set of addresses in Chinese
	Can be used for building standarized address database and geocoding


3. How to obtain statistics of parameters

	THULAC
	http://nlp.csai.tsinghua.edu.cn/site2/index.php/en/the-news/238-thulac-thutag
	A well developed word seperation and tagging tool.


4. Variations:
	1).	Pure HMM
	2).	With Dictionary
	3). TBD


5. Comparation to other word seperation methods
	TBD


6. Reference:
	http://yanyiwu.com/work/2014/04/07/hmm-segment-xiangjie.html


