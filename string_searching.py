import sys


#In computer science, the Knuth–Morris–Pratt string-searching algorithm
# (or KMP algorithm) searches for occurrences of a "word" W within a
# main "text string" S by employing the observation that when a mismatch occurs,
# the word itself embodies sufficient information to determine where the next
# match could begin, thus bypassing re-examination of previously matched characters.

class KMP:
	def __init__(self, text, search_pattern) -> None:
		self.text =text
		self.pattern= search_pattern
		self.patternTable = [0]*(len(search_pattern)+1)
		self.patternTable[0] = -1
		self.calculatePatternTable()

	def calculatePatternTable(self):
		prefixLen = 0
		i = 1
		while i<len(self.pattern):
			if self.pattern[i]==self.pattern[prefixLen]:
				prefixLen+=1
				i+=1
				self.patternTable[i] =prefixLen
			elif prefixLen>0:
				prefixLen = self.patternTable[prefixLen]
			else:
				i+=1
	def search(self):
		curText, curPattern = 0, 0
		matches = []
		while curText<len(self.text):
			if self.pattern[curPattern]==self.text[curText]:
				curText+=1
				curPattern+=1
				if curPattern==len(self.pattern):
					matches.append(curText-curPattern)
					curPattern = self.patternTable[curPattern]
			else:
				curPattern = self.patternTable[curPattern]
				if curPattern<0:
					curText+=1
					curPattern+=1
		return matches




class RabinKarp:
	pass
class bcolors:
		HEADER = '\033[95m'
		OKBLUE = '\033[94m'
		OKCYAN = '\033[96m'
		OKGREEN = '\033[92m'
		WARNING = '\033[93m'
		FAIL = '\033[91m'
		ENDC = '\033[0m'
		BOLD = '\033[1m'
		UNDERLINE = '\033[4m'

tests = [
	{
		"input": ["abcaaaaaaaabc", "abc"],
		"answer": [0, 10]
	},
 	{
		"input": ["mississippi", "issipi"],
		"answer": []
	},
	{
		"input": ["sadbutsad","sad"],
		"answer": [0, 6]
	},
	{
		"input": ["hello", "ll"],
		"answer": [2]
	},
	{
		"input": ["aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "a"],
		"answer": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]
	},
 	{
		"input": ["AABAACAADAABAABA", "AABA"],
		"answer": [0, 9, 12]
	},

]

def plot(text, pattern, matches):
	first, second = [" "]*len(text),[" "]*len(text)
	for i in matches:
		first[i] = "↓"
		second[i+len(pattern)-1] ="↑"
	print("START: ", bcolors.FAIL, "".join(first), bcolors.ENDC)
	print("TEXT:  ",bcolors.BOLD,  text, bcolors.ENDC)
	print("END:   ",bcolors.OKGREEN, "".join(second), bcolors.ENDC)

if __name__=="__main__":
	print(bcolors.HEADER,"INFO:\n python3 -algo_name --plot \n\n -algo_name:[KMP, RabinKarp]\n --plot: Add this flag for plotting the results", bcolors.ENDC)
	algo_name = "graham_scan"
	is_plot = False
	while len(sys.argv)>1:
		s = sys.argv.pop()
		if s[:2]=="--":
			is_plot = s[2:]=="plot"
		elif s[:1]=='-':
			algo_name = s[1:]
	for ind, i in enumerate(tests):
		if algo_name=="KMP":
			gr = KMP(*i['input'])
		elif algo_name=="RabinKarp":
			gr = RabinKarp(i['input'])
		else: break
		ans = gr.search()
		print(ans)
		if sorted(ans)==sorted(i['answer']):
			print(bcolors.OKGREEN, " Test {} Passed".format(ind+1), bcolors.ENDC)
			if is_plot:
				print(bcolors.OKBLUE, "Text: {text}\n Seach Pattern: {pattern} ".format(pattern= i["input"][1],text=i["input"][0]),  bcolors.ENDC)
				plot(*i["input"], ans)
		else:
			print(bcolors.FAIL, " Test {} Failed".format(ind+1), bcolors.ENDC)
			print(bcolors.BOLD,"Your answer: {}\n Expected: {}".format(sorted(ans), sorted(i['answer'])), bcolors.ENDC)
			if is_plot:
				print(bcolors.OKBLUE, "Text: {text}\n Seach Pattern: {pattern} ".format(pattern= i["input"][1],text=i["input"][0]),  bcolors.ENDC)
				print("Your answer:")
				plot(*i["input"], ans)
				print("Actual Answer:")
				plot(*i["input"], i['answer'])
