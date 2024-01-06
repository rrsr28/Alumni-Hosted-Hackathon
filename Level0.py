# Alumni Hosted Hackathon 2024
# Author - Sanjay Ram R R (21PD32)

# Import statements
# ----------------

import sys
import json
import numpy as np

output = []

def travelling_salesman(c):

    global cost

    adj_vertex = sys.maxsize
    min_val = sys.maxsize

    visited[c] = 1
    output.append(c+1)

    print((c + 1), end=" ")

    for k in range(21):
        if (graph[c][k] != 0) and (visited[k] == 0):
            if graph[c][k] < min_val:
                min_val = graph[c][k]
                adj_vertex = k

    if min_val != sys.maxsize:
        cost = cost + min_val

    if adj_vertex == sys.maxsize:
        adj_vertex = 0
        output.append(adj_vertex + 1)
        print((adj_vertex + 1), end=" ")
        cost = cost + graph[c][adj_vertex]
        return
    
    travelling_salesman(adj_vertex)


cost = 0
visited = np.zeros(21)
graph = []

json_file_path = 'Input data\level0.json'

with open(json_file_path, 'r') as file:
    data = json.load(file)

names = ['n0', 'n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'n7', 'n8', 'n9', 'n10', 'n11', 'n12', 'n13', 'n14', 'n15', 'n16', 'n17', 'n18', 'n19']
r = data['restaurants']['r0']['neighbourhood_distance']

for i in range(len(names)+1):
    graph.append([0])

for i in range(len(r)):
    graph[0].append(r[i])
for i in range(1, len(names)+1):
    d = data['neighbourhoods'][names[i-1]]['distances']
    for j in d:
        graph[i].append(j)
for i in range(1, 21):
    graph[i][0] = r[i-1]

graph = np.array(graph)

print("\nShortest Path : ")
travelling_salesman(0)
print("\nMinimum Cost : ", cost)


output_dict = {'v0': {'path': {}}}
mapping = {1: 'r0', 
           2: 'n0',
           3: 'n1',
           4: 'n2',
           5: 'n3',
           6: 'n4',
           7: 'n5',
           8: 'n6',
           9: 'n7',
           10: 'n8',
           11: 'n9',
           12: 'n10',
           13: 'n11',
           14: 'n12',
           15: 'n13',
           16: 'n14',
           17: 'n15',
           18: 'n16',
           19: 'n17',
           20: 'n18',
           21 : 'n19'}

path_list = []

for i in range(len(output)):
    path_list.append(mapping[output[i]])

output_dict['v0']['path'] = path_list

json_file_path = 'MyOutput\level0_output.json'

with open(json_file_path, 'w') as json_file:
    json.dump(output_dict, json_file, indent=2)
# ----------------------------------------------------------