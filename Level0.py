# Alumni Hosted Hackathon 2024
# Author - Sanjay Ram R R (21PD32)

# Import statements
# ----------------

import sys
import json
import numpy as np
from itertools import permutations

file_path = 'Input data/level0.json'

with open(file_path, 'r') as file:
    data = json.load(file)

# Old Code (Dijkstras)
# -------------------

"""class Graph():
 
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)]
                      for row in range(vertices)]
 
    def printSolution(self, dist):
        print("Vertex \tDistance from Source")
        for node in range(self.V):
            print(node, "\t", dist[node])
 
    def minDistance(self, dist, sptSet):
 
        min = sys.maxsize

        for u in range(self.V):
            if dist[u] < min and sptSet[u] == False:
                min = dist[u]
                min_index = u
 
        return min_index

    def dijkstra(self, src):
 
        dist = [sys.maxsize] * self.V
        dist[src] = 0
        sptSet = [False] * self.V
        #sptSet[src] = True
        flag = 0
        for cout in range(self.V):
            x = self.minDistance(dist, sptSet)

            if flag == 0:
                sptSet[src] = False
                flag = 1
            sptSet[x] = True
 
            for y in range(self.V):
                if self.graph[x][y] > 0 and sptSet[y] == False and \
                        dist[y] > dist[x] + self.graph[x][y]:
                    dist[y] = dist[x] + self.graph[x][y]
 
        self.printSolution(dist)

    def tsp(self):
        V = self.V
        vertex = [i for i in range(V)]
        vertex.remove(0)
        min_path = sys.maxsize
        next_permutation = permutations(vertex)
        for i in next_permutation:
            current_pathweight = 0
            k = 0
            for j in i:
                current_pathweight += self.graph[k][j]
                k = j
            current_pathweight += self.graph[k][0]
            min_path = min(min_path, current_pathweight)
        return min_path



g = Graph(20)"""

# ----------------------------------------------------------
# New and Working Code
# -------------------

path = []
cost = 0

graph = [[0 for column in range(20)]
                      for row in range(20)]
for i in range(1, 20):
    graph[i] = data["neighbourhoods"]["n" + str(i)]["distances"]
graph[0] = data["restaurants"]["r0"]["neighbourhood_distance"]

def travellingsalesman(src):
    
    adjV = sys.maxsize
    min_val = sys.maxsize

    visited[src] = 1
    path.append((src + 1))

    global cost

    for k in range(20):

        if (answer[src][k] != 0) and (visited[k] == 0) and answer[src][k] < min_val:
            min_val = answer[src][k]
            adjV = k

    if min_val != sys.maxsize:
        cost = cost + min_val

    if adjV == sys.maxsize:
        adjV = 0
        path.append(adjV + 1)
        cost = cost + answer[src][adjV]
        return
    
    travellingsalesman(adjV)

visited = np.zeros(20)
answer = np.array(graph)

travellingsalesman(0)
print("\nShortest Path : ", path)
print("Minimum Cost : ", cost)


path_ = ['r0']
for i in path:
    path_.append('n'+str(i-1))
path_.append('r0')
dictionary = {"v0": {"path": path_}}
print(dictionary)


json_object = json.dumps(dictionary, indent=4)
with open("level0_output.json", "w") as outfile:
    outfile.write(json_object)

# ----------------------------------------------------------
