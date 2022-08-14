from collections import defaultdict, deque
from typing import List


class BiBFS:
  def __init__(self, node1, node2, graph) -> None:
    self.graph =defaultdict(list)
    for a,b in graph:
      self.graph[a].append(b)
      self.graph[b].append(a)
    if node2 not in self.graph:
      print("No node2")
      return
    if node1 not in self.graph:
      print("No node1")
      return
    self.node1= node1
    self.node2= node2
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
              self.result.append(a+b)
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
    return self.result

  def update(self, node1, node2, graph):
    self.node1 =node1
    self.node2 = node2
    self.graph =defaultdict(list)
    for a,b in graph:
      self.graph[a].append(b)
      self.graph[b].append(a)
    self.visited1 = defaultdict(list)
    self.visited2 = defaultdict(list)
    self.q1 = deque([node1])
    self.visited1[node1] = []
    self.q2 = deque([node2])
    self.visited2[node2] = []
    self.result = []

if __name__ == "__main__":
  node1= 1
  node2 = 5
  # '1-0-3-4-5'
  # '1-0-2-6-5'
  connections = [[0,1], [0,2], [0,3], [3,4], [4,5],[2,6], [5,6]]
  bfs = BiBFS(node1, node2, connections)
  print(bfs.search())