class UnionFind:
	def __init__(self, n: int) -> None:
		self.unions = [-1]*n
		self.largestSet = 1
		self.setsNumber= n
		self.n= n
	def find(self, x):
		paths = []
		while self.unions[x]>=0:
			paths.append(x)
			x= self.unions[x]
		for i in paths: self.unions[i] =x
		return x
	def union(self, x,y):
		x_par = self.find(x)
		y_par = self.find(y)
		if x_par!=y_par:
			self.setsNumber-=1
			if self.unions[x_par]>self.unions[y_par]:
				self.unions[y_par]+=self.unions[x_par]
				self.unions[x_par]= y_par
				self.largestSet = max(self.largestSet, -self.unions[y_par])
				return y_par
			self.unions[x_par]+=self.unions[y_par]
			self.largestSet = max(self.largestSet, -self.unions[x_par])
			self.unions[y_par]= x_par
		return x_par
	def copy(self):
		uf = UnionFind(self.n)
		uf.largestSet= self.largestSet
		uf.unions= self.unions[:]
		uf.setsNumber = self.setsNumber
		return uf
	def __str__(self):
		return "[{}]".format(",".join(map(str, self.unions)))
	def max(self): return self.largestSet
	def count(self): return self.setsNumber
	def groupSize(self,x): return -self.unions[-self.find(x)]


#In computer science, a disjoint-set data structure,
# also called a union–find data structure or merge–find set,
# is a data structure that stores a collection of disjoint sets.
# Equivalently, it stores a partition of a set into disjoint subsets.
#
#Give the number of elements and id(index) of the elements to join or find the set
if __name__=="__main__":
	#[1,2,3,4,5,6]
	uf = UnionFind(6)
	uf.union(1,2)
	uf.find(1)
	print(uf)
