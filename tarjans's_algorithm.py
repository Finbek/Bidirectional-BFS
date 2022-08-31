#Tarjan's strongly connected components algorithm is an algorithm
# in graph theory for finding the strongly connected components
# (SCCs) of a directed graph. It runs in linear time, matching
# the time bound for alternative methods including Kosaraju's
# algorithm and the path-based strong component algorithm.
# The algorithm is named for its inventor, Robert Tarjan.
# https://en.wikipedia.org/wiki/Tarjan%27s_strongly_connected_components_algorithm

import collections
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import sys


class Tarjan:
	def __init__(self, graph, n) -> None:
		self.graph = graph
		self.sce= []
		self.low = [0]*n

		self.sccCount=  0
		self.rank = 1

		self.ids =[0]*n
		self.onStack = [False]*n
		self.stack =collections.deque([])
	def dfs(self, cur):
		self.stack.append(cur)
		self.onStack[cur] =True
		self.ids[cur]=self.low[cur]= self.rank
		self.rank+=1
		for neigh in self.graph[cur]:
			if self.ids[neigh]==0: self.dfs(neigh)
			if self.onStack[neigh]: self.low[cur] = min(self.low[cur], self.low[neigh])

		if(self.ids[cur]==self.low[cur]):
			while self.stack:
				node = self.stack.pop()
				self.onStack[node]= False
				self.low[node]= self.low[cur]
				if node==cur:
					break
			self.sccCount+=1
	def run(self):
		for ind in range(len(self.low)):
			if self.low[ind]==0:
				self.dfs(ind)
		for a in self.graph:
			for b in self.graph[a]:
				if self.low[a]!=self.low[b]: self.sce.append([a,b])




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
		"input": [4, [[0,1],[1,2],[2,0],[1,3]]],
		"answer":[[1,3]]
	},
	{
		"input": [2, [[0,1]]],
		"answer":[[0,1]]
	},
 	{
		"input": [15, [[0,1], [1,2], [2,3], [3,0],[2,6], [4,2], [6,4], [4,5],[5,7],[8,5],[7,8],[5,9],[8,9],[9,10],
                 	[10,12], [12,13], [13,14], [14,10],[14,11]]],
		"answer":[[4, 5], [5, 9], [8, 9], [9, 10], [14, 11]]
	},
  {
		"input": [8, [[0,1],[1,2],[2,0], [5,0], [5,6], [6,4],[4,5],[6,2], [7,3],[3,7],[7,5],[3,4]]],
		"answer":[[5,0], [6, 2], [3, 4], [7, 5]]
	},
]

def newColor(prev):
  c= (np.random.random(), np.random.random(), np.random.random())
  while c in prev:
    c= (np.random.random(), np.random.random(), np.random.random())
  prev.add(c)
  return c
def plot(connections, lows, scc):
  G = nx.DiGraph()
  node_cols = []
  colors = {}
  generated_colors= set()
  for a,b in connections:
    G.add_edge(a,b)
  for a in G.nodes:
    if lows[a] not in colors: colors[lows[a]]=newColor(generated_colors)
    node_cols.append(colors[lows[a]])
  e_colors = []
  for a,b in G.edges:
    if [a,b] in scc or [b,a] in scc: e_colors.append(newColor(generated_colors))
    else: e_colors.append("black")
  nx.draw(G, with_labels=True,node_color=node_cols, edge_color=e_colors)
  plt.show()


if __name__=="__main__":
		is_plot= False
		while len(sys.argv)>1:
			s = sys.argv.pop()
			if s[:2]=="--":
				is_plot = s[2:]=="plot"
		for ind, i in enumerate(tests):
			graph = collections.defaultdict(list)
			for a,b in i["input"][1]:
				graph[a].append(b)
			tarjan = Tarjan(graph, i["input"][0])
			tarjan.run()
			ans = tarjan.sce
			if is_plot: plot(i["input"][1], tarjan.low, ans)
			if sorted(ans)==sorted(i['answer']):
				print(bcolors.OKGREEN, " Test {} Passed".format(ind+1), bcolors.ENDC)
			else:
				print(bcolors.FAIL, " Test {} Failed".format(ind+1), bcolors.ENDC)
				print(bcolors.BOLD,"Your answer: {}\n Expected: {}".format(sorted(ans), sorted(i['answer'])), bcolors.ENDC)