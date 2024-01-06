import heapq
import json
import numpy as np
from python_tsp.exact import solve_tsp_dynamic_programming

def optimize_delivery_slots(orders, scooter_capacity):
    orders.sort(key=lambda x: x['quantity'], reverse=True)

    delivery_slots = []
    total_distance = 0
    path_locations = []

    for order in orders:
        quantity = order['quantity']
        location = order['location']

        if delivery_slots and delivery_slots[0][0] + quantity <= scooter_capacity:
            current_slot = heapq.heappop(delivery_slots)
            current_slot[0] += quantity
            current_slot[1].append(location)  # Append location to the path
            heapq.heappush(delivery_slots, current_slot)
        else:
            heapq.heappush(delivery_slots, [quantity, [location]])  # Start a new delivery slot

    # Extract locations from each path
    for slot in delivery_slots:
        path_locations.append(slot[1])


    return path_locations, total_distance, delivery_slots

# Example orders
json_file_path = 'Input data\level1b.json'
with open(json_file_path, 'r') as file:
    data = json.load(file)

name = ['n0', 'n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'n7', 'n8', 'n9', 'n10', 'n11', 'n12', 'n13', 'n14', 'n15', 'n16', 'n17', 'n18', 'n19', 'n20', 'n21',  'n22', 'n23', 'n24', 'n25', 'n26', 'n27', 'n28', 'n29', 'n30', 'n31', 'n32', 'n33', 'n34', 'n35', 'n36', 'n37', 'n38', 'n39', 'n40', 'n41', 'n42', 'n43', 'n44', 'n45', 'n46', 'n47', 'n48', 'n49']
orders = [{'quantity': data['neighbourhoods'][name[i]]['order_quantity'], 'location': i} for i in range(len(name))]


scooter_capacity = data['vehicles']['v0']['capacity']

optimized_paths, total_distance, slots = optimize_delivery_slots(orders, scooter_capacity)

for i in optimized_paths:
    i.insert(0, -1)

tsp_g = []

json_file_path = 'Input data\level1b.json'

# Read the JSON file
with open(json_file_path, 'r') as file:
    data = json.load(file)

r = data['restaurants']['r0']['neighbourhood_distance']

for i in range(len(name)+1):
    tsp_g.append([0])

for i in range(len(r)):
    tsp_g[0].append(r[i])

for i in range(1, len(name)+1):
    d = data['neighbourhoods'][name[i-1]]['distances']
    for j in d:
        tsp_g[i].append(j)

for i in range(1, 51):
    tsp_g[i][0] = r[i-1]

slo = []
for i in range(len(slots)):
    for j in optimized_paths:
        temp = []
        for loc in range(len(j)):
            s = []
            for loc_1 in range(len(j)):
                s.append(tsp_g[j[loc]+1][j[loc_1]+1])
            temp.append(s)
        slo.append(np.array(temp))
    break

min_slot_dis = []

for i in range(len(slo)):
    permutation, distance = solve_tsp_dynamic_programming(slo[i])
    min_slot_dis.append([permutation,distance])

d = {'v0': {}}

m = {-1: 'r0', 
     0: 'n0',
     1: 'n1',
     2: 'n2',
     3: 'n3',
     4: 'n4',
     5: 'n5',
     6: 'n6',
     7: 'n7',
     8: 'n8',
     9: 'n9',
     10: 'n10',
     11: 'n11',
     12: 'n12',
     13: 'n13',
     14: 'n14',
     15: 'n15',
     16: 'n16',
     17: 'n17',
     18: 'n18',
     19 : 'n19',
     20 : 'n20',
     21 : 'n21',
     22 : 'n22',
     23 : 'n23',
     24 : 'n24',
     25 : 'n25',
     26 : 'n26',
     27 : 'n27',
     28 : 'n28',
     29 : 'n29',
     30 : 'n30',
     31 : 'n31',
     32 : 'n32',
     33 : 'n33',
     34 : 'n34',
     35 : 'n35',
     36 : 'n36',
     37 : 'n37',
     38 : 'n38',
     39 : 'n39',
     40 : 'n40',
     41 : 'n41',
     42 : 'n42',
     43 : 'n43',
     44 : 'n44',
     45 : 'n45',
     46 : 'n46',
     47 : 'n47',
     48 : 'n48',
     49 : 'n49'}


for i in range(len(min_slot_dis)):
    w = []
    for j in min_slot_dis[i][0]:
        q = optimized_paths[i][j]
        w.append(m[q])
    w.append('r0')
    st = 'path'+str(i+1)        
    d['v0'][st] = w


json_file_path = 'MyOutput\level1b_output.json'

with open(json_file_path, 'w') as json_file:
    json.dump(d, json_file, indent=2)