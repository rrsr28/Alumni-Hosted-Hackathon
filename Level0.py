# Alumni Hosted Hackathon 2024
# Author - Sanjay Ram R R (21PD32)

# Import statements
# ----------------

import sys
import json
import numpy as np


"""def read_input_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def calculate_shortest_path_and_cost(data):
    graph = [[0 for _ in range(20)] for _ in range(20)]
    for i in range(1, 20):
        graph[i] = data["neighbourhoods"]["n" + str(i)]["distances"]
    graph[0] = data["restaurants"]["r0"]["neighbourhood_distance"]

    visited = np.zeros(20)
    answer = np.array(graph)
    path = []
    cost = 0

    def travelling_salesman(src, flag):
        nonlocal cost
        nonlocal path
        nonlocal answer
        nonlocal visited

        adjV = sys.maxsize
        min_val = sys.maxsize

        visited[src] = 1
        
        
        if flag != 0:
            path.append((src + 1))
        flag = 1

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

        travelling_salesman(adjV, flag)

    travelling_salesman(0, 0)
    return path, cost

def generate_output_json(path):
    path_ = ['r0']
    path_ = []
    for i in path:
        path_.append('n'+str(i-1))
    path_.append('r0')
    dictionary = {"v0": {"path": path_}}
    json_object = json.dumps(dictionary, indent=4)
    with open("level0_output.json", "w") as outfile:
        outfile.write(json_object)

def main():
    file_path = 'Input data/level0.json'
    data = read_input_data(file_path)
    path, cost = calculate_shortest_path_and_cost(data)
    print("\nShortest Path : ", path)
    print("Minimum Cost : ", cost)
    generate_output_json(path)

if __name__ == "__main__":
    main()"""
# ----------------------------------------------------------

from typing import List
import math

def nearest_neighbor(cities, graph):
    unvisited = cities.copy()
    print(unvisited)
    current = cities[0]
    unvisited.remove(current)
    tour = [current]
    while unvisited:
        next_city = min(unvisited, key=lambda city: graph[cities.index(current)][cities.index(city)])
        tour.append(next_city)
        unvisited.remove(next_city)
        current = next_city
    return tour

file_path = 'Input data/level0.json'

with open(file_path, 'r') as file:
    data = json.load(file)

path = []
cost = 0

graph = [[0 for column in range(21)]
                      for row in range(21)]
for i in range(0, 20):
    graph[i+1] = data["neighbourhoods"]["n" + str(i)]["distances"]
graph[0] = data["restaurants"]["r0"]["neighbourhood_distance"]

cities = ["r0"] + ["n" + str(i) for i in range(20)]
print(cities)
path_ = nearest_neighbor(cities, graph)
print(path_)

for i in path:
    path_.append('n'+str(i-1))
path_.append('r0')
dictionary = {"v0": {"path": path_}}
json_object = json.dumps(dictionary, indent=4)
with open("level0_output.json", "w") as outfile:
    outfile.write(json_object)