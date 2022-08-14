from collections import defaultdict, deque
from typing import List

class BiBFS:
		def __init__(self, graph, node1, node2) -> None:
				if node2 not in graph:
					print("No node2")
					return
				if node1 not in graph:
					print("No node1")
					return
				self.node1= node1
				self.node2= node2
				self.graph =graph
				self.visited1 = defaultdict(list)
				self.visited2 = defaultdict(list)
				self.q1 = deque([node1])
				self.visited1[node1] = []
				self.q2 = deque([node2])
				self.visited2[node2] = []
				self.result = []

		def dfs(self, v, visited, path, paths)->List[List]:
				path.append(v)
				if not visited[v]:
					if visited is self.visited1:
						paths.append(path[::-1])
					else:
						paths.append(path[:])
				for u in visited[v]:
					self.dfs(u, visited, path, paths)
					path.pop()

		def bfs(self, q, visited1, visited2, frombegin):
				level_visited = defaultdict(list)
				for _ in range(len(q)):
					u = q.popleft()
					for v in self.graph[u]:
						if v in visited2:
							paths1 = []
							paths2 = []
							self.dfs(u, visited1, [], paths1)
							self.dfs(v, visited2, [], paths2)
							if not frombegin:
								paths1, paths2 = paths2, paths1
							for a in paths1:
								for b in paths2:
									self.ans.append(a+b)
						elif v not in visited1:
							if v not in level_visited:
								q.append(v)
							level_visited[v].append(u)
				visited1.update(level_visited)

		def search(self):
				while self.q1 and self.q2 and not self.result:
					if len(self.q1) <= len(self.q2):
							self.bfs(self.q1, self.visited1, self.visited2, True)
					else:
							self.bfs(self.q2, self.visited2, self.visited1, False)
				return self.ans

		def update(self, node1, node2, graph):
				self.node1 =node1
				self.node2 = node2
				self.graph = graph
				self.visited1 = defaultdict(list)
				self.visited2 = defaultdict(list)
				self.q1 = deque([node1])
				self.visited1[node1] = []
				self.q2 = deque([node2])
				self.visited2[node2] = []
				self.result = []