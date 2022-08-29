# In geometry, the convex hull or convex envelope or
# convex closure of a shape is the smallest convex set that contains it.
# The convex hull may be defined either as the intersection of all
# convex sets containing a given subset of a Euclidean space, or
# equivalently as the set of all convex combinations of points in the subset.

#This algorithms helps to find the convex hull or the smallest set of points that make a
#polygon which contains all other points

#Area of two vector can be find with cross product of two vectors, and by right thumb rule
	#if the area is positive than the angle is counterclockwise, otherwise it's clockwise
	#To find the cross product use vector multiplication:
	#        | A_x  B_x|
	# AxB =  |         | = (A_x*B_y)-(A_y*B_x)
	#        | A_y  B_y|
	#in our case three points are given, where
	# A starts at x, ends at y  -
	# B starts at x, ends at z

import sys
from math import atan2
import math
import matplotlib.pyplot as plt

class MonotoneChain:
	def __init__(self, points) -> None:
		self.points= points[:]
		self.points.sort()
		self.start = self.points[0]

	def run(self):
		upHull = []
		downHull = []
		for point in self.points:
			while len(upHull) >= 2 and self.angleSign(upHull[-2], upHull[-1], point) > 0:
				upHull.pop()
			while len(downHull) >= 2 and self.angleSign(downHull[-2], downHull[-1], point) < 0:
				downHull.pop()
			upHull.append(point)
			downHull.append(point)
		l = len(upHull)-1
		while l>=0:
			if upHull[l] in downHull: upHull.pop(l)
			l-=1
		return downHull+upHull[::-1]


	def angleSign(self, a, b, c):
		return (b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])




class GrahamScan:
	def __init__(self, points) -> None:
		self.points = points[:]
		self.start= min(points)
		self.points.pop(self.points.index(self.start))
		self.points.sort(key=lambda p: (atan2(p[1]-self.start[1], p[0]-self.start[0]), -p[1], p[0]))
		self.points = self.change(self.points)

	def change(self, points):
		last = len(points) - 1
		while last > 0 and self.angleSign(self.start, points[-1], points[last - 1]) == 0:
			last -= 1
		points[last:] = sorted(points[last:], key = lambda p: (-p[0]))
		first =0
		while first+1<len(points) and self.angleSign(self.start, points[0], points[first+1])==0:
			first+=1
		points[:first+1] = sorted(points[:first+1])
		return points

	def angleSign(self,a, b, c):
		return (b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])

	def run(self):
		stack = [self.start]
		for p in self.points:
			stack.append(p)
			while len(stack) > 2 and self.angleSign(*stack[-3:]) < 0:
				stack.pop(-2)
		return stack

class JarvisMarch:
	def __init__(self, points) -> None:
		self.points= points[:]
		self.points.sort(key= lambda xy: (xy[1], xy[0]))
		self.start= self.points[0]

	def run(self):
		if len(self.points) <= 3:
			return self.points
		first_point, last_point = self.points[0], self.points[0]
		start = True
		ans = []
		vis = set()
		while start or last_point != first_point:
			start = False
			cur_point = None
			for p in self.points:
				if p == last_point or ",".join(map(str, p)) in vis:
					continue
				if not cur_point or self.angleSign(last_point, cur_point, p) > 0:
					cur_point = p
					colliner = [p]
				elif self.angleSign(last_point, cur_point, p) == 0:
					if math.dist(last_point, cur_point) < math.dist(last_point, p):
						cur_point = p
					colliner.append(p)
			for i in colliner: vis.add(",".join(map(str, i)))
			colliner.remove(cur_point)
			ans += colliner+[cur_point]
			last_point = cur_point
		return ans
	def angleSign(self,a, b, c):
		return (b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])


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
	 "input": [[1,1],[2,2],[2,0],[2,4],[3,3],[4,2]],
	 "answer": [[1,1],[2,0],[3,3],[2,4],[4,2]],
	},
	{
	 "input": [[1,2],[2,2],[4,2]],
	 "answer": [[4,2],[2,2],[1,2]],
	},
	{
	 "input": [[1,5]],
	 "answer": [[1,5]],
	},
	{
	 "input":[[0,2],[0,1],[0,0],[1,0],[2,0],[1,1]],
	 "answer":[[0,2],[0,1],[0,0],[1,0],[2,0],[1,1]],
	},
	{
	 "input":[[0,2],[0,4],[0,5],[0,9],[2,1],[2,2],[2,3],[2,5],[3,1],[3,2],[3,6],[3,9],[4,2],[4,5],[5,8],[5,9],[6,3],[7,9],[8,1],[8,2],[8,5],[8,7],[9,0],[9,1],[9,6]],
	 "answer":[[0,2],[0,5],[9,1],[5,9],[3,9],[0,9],[7,9],[9,0],[0,4],[2,1],[9,6]]
		},
	{
	 "input":[[0,0],[0,1],[0,2],[1,2],[2,2],[3,2],[3,1],[3,0],[2,0]],
	 "answer":[[0,2],[2,0],[0,0],[1,2],[3,1],[0,1],[3,2],[3,0],[2,2]],
	},
	{
	 "input": [[0,1],[1,0],[100,100],[99,100],[100,99]],
	 "answer": [[1,0],[99,100],[100,100],[0,1],[100,99]]
	},
	{
		"input": [[0,0],[1,1],[2,2],[1,2],[2,4]],
		"answer": [[0,0],[1,2],[2,2],[1,1],[2,4]]
	},
	{
		"input": [[3,3],[2,4],[2,2],[7,4],[3,4]],
	"answer": [[2,4],[2,2],[3,4],[7,4]]
	},
	{
		"input":[[1,2],[2,2],[4,2],[5,2],[6,2],[7,2]],
	"answer": [[4,2],[6,2],[2,2],[5,2],[1,2],[7,2]]
	}



	]

def plot(arr, joins):
	p1 = []
	p2 = []
	for a in arr:
		p1.append(a[0])
		p2.append(a[1])
	plt.plot(p1, p2, 'ro')
	joins.append(joins[0])
	for a,b in zip(joins, joins[1:]):
		plt.plot([a[0], b[0]], [a[1],b[1]], 'g-')
	plt.show()



if __name__=="__main__":
	print(bcolors.HEADER,"INFO:\n python3 -algo_name --plot \n\n -algo_name:[graham_scan,jarvis_march,monotone_chain]\n --plot: Add this flag for plotting the results", bcolors.ENDC)
	algo_name = "graham_scan"
	is_plot = False
	while len(sys.argv)>1:
		s = sys.argv.pop()
		if s[:2]=="--":
			is_plot = s[2:]=="plot"
		else:
			algo_name = s[1:]
	for ind, i in enumerate(tests):
		if algo_name=="graham_scan":
			gr = GrahamScan(i['input'])
		elif algo_name=="jarvis_march":
			gr = JarvisMarch(i['input'])
		elif algo_name=="monotone_chain":
			gr= MonotoneChain(i['input'])
		else: break
		ans = gr.run()
		if sorted(ans)==sorted(i['answer']):
			print(bcolors.OKGREEN, " Test {} Passed".format(ind+1), bcolors.ENDC)
		else:
			print(bcolors.FAIL, " Test {} Failed".format(ind+1), bcolors.ENDC)
			print(bcolors.BOLD,"Your answer: {}\n Expected: {}".format(sorted(ans), sorted(i['answer'])), bcolors.ENDC)
		if is_plot: plot(gr.points+[gr.start], ans)
