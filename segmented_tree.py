

# Each element in input array is a left nodes of the SegmentedTree, so convert
# them into array and depending on your needes it can be array of integers, tuples, strings and etc
#join_func - is a joining function of the tree nodes and depends on tasks
#getValue - function to get a value from tree nodes
#check example
from typing import *
import math

class SegmentedTree:
	def __init__(self, input_array: List, join_func:Callable, getValue: Callable) -> None:
		self.n= len(input_array)
		self.func = join_func
		self.tree = [0]*(self.n)+input_array
		self.val = getValue
		for i in range(self.n-1, 0,-1):
			self.tree[i] =join_func(self.tree[i*2], self.tree[i*2+1])

	def update(self, index:int, node) -> None:
		index+=self.n
		self.tree[index] = node
		while index>1:
			index//=2
			newNode= self.func(self.tree[index*2], self.tree[index*2+1])
			if newNode==self.tree[index]: return
			self.tree[index]= newNode


	def find(self, index_from: int, index_to: int, find_func):
		l = index_from+self.n
		r = index_to+self.n
		result= None
		while l<r:
			if (l&1)==1:
				result = find_func(result, self.tree[l])
				l+=1
			if l!=r and (r&1)==0:
				result = find_func(result, self.tree[r])
				r-=1
			if l!=r:
				l=l//2
				r//=2
		result = find_func(result, self.tree[l])
		return result
	def __str__(self):
		ans= []
		start = self.n
		end= 2*self.n
		cnt= self.n
		while start<end:
			if cnt!=end-start:
				ans.append(self.tree[start:end]+[self.tree[end]])
			else:
				ans.append(self.tree[start:end])

			cnt=math.ceil(cnt/2)

			start=math.ceil(start/2)
			end=math.ceil(end/2)
		l = len(" ".join(map(str, map(self.val, ans[0]))))
		res = []
		space= 1
		for i in ans:
			i = list(map(str, map(self.val, i)))

			res.append(((space*" ").join(i)).center(l))
			space*=2
			space+=1
		return "\n".join(res[::-1])





class Node:
	def __init__(self,val) -> None:
		self.val = val

if __name__ == "__main__":
	array =[Node(i) for i in [6,10,5,2,7,1,0,9]]


	#Return element, not value here #Should be Node type here
	def _find(a,b):
		if b==None: return a
		if a==None: return b
		return max(a,b, key = lambda x: x.val)

	st = SegmentedTree(array, lambda x,y: Node(max(x.val, y.val)), lambda x: x.val)
	print(st.find(0,4, _find).val)
	st.update(4, Node(50))
	print(st.find(0,4, _find).val)
	print(st)

	array2 = [6,10,5]
	st2 = SegmentedTree(array2, lambda x,y: x+y, lambda x: x)
	print(st2)