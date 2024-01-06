# Alumni Hosted Hackathon 2024
# Author - Sanjay Ram R R (21PD32)

# Import statements
# ----------------

import sys
import json
from itertools import permutations

file_path = 'Input data/level0.json'

with open(file_path, 'r') as file:
    data = json.load(file)

"""def save_neighborhood_graph(input_file):
    with open(input_file, 'r') as file:
        data = json.load(file)
        neighborhoods = data["neighbourhoods"]
        graph = {}
        for key, value in neighborhoods.items():
            distances = value["distances"]
            graph[key] = {neighborhoods[i]: distances[i] for i in range(len(distances))}
    return graph"""


class Graph():
 
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)]
                      for row in range(vertices)]
 
    def printSolution(self, dist):
        print("Vertex \tDistance from Source")
        for node in range(self.V):
            print(node, "\t", dist[node])
 
    # A utility function to find the vertex with
    # minimum distance value, from the set of vertices
    # not yet included in shortest path tree
    def minDistance(self, dist, sptSet):
 
        # Initialize minimum distance for next node
        min = sys.maxsize
        first = 0
        # Search not nearest vertex not in the
        # shortest path tree
        for u in range(self.V):
            if dist[u] < min and sptSet[u] == False and u != self.V:
                min = dist[u]
                min_index = u
            first = 1
 
        return min_index
 
    # Function that implements Dijkstra's single source
    # shortest path algorithm for a graph represented
    # using adjacency matrix representation
    def dijkstra(self, src):
 
        dist = [sys.maxsize] * self.V
        dist[src] = 0
        sptSet = [False] * self.V
 
        for cout in range(self.V):
 
            # Pick the minimum distance vertex from
            # the set of vertices not yet processed.
            # x is always equal to src in first iteration
            x = self.minDistance(dist, sptSet)
 
            # Put the minimum distance vertex in the
            # shortest path tree
            sptSet[x] = True
 
            # Update dist value of the adjacent vertices
            # of the picked vertex only if the current
            # distance is greater than new distance and
            # the vertex in not in the shortest path tree
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



g = Graph(20)
	
for i in range(1, 20):
    g.graph[i] = data["neighbourhoods"]["n" + str(i)]["distances"]
    g.graph[i][i] = -1
g.graph[0] = data["restaurants"]["r0"]["neighbourhood_distance"]
g.graph[0][0] = -1

print(g.V)
g.dijkstra(0)