# Alumni Hosted Hackathon 2024
# Author - Sanjay Ram R R (21PD32)

# Import statements
# ----------------

import json
import itertools

file_path = 'Input data\\level1a.json'
with open(file_path) as file:
    data = json.load(file)

neighbourhood = data['neighbourhoods']
ord_quantity = []
distance = []

for i in neighbourhood.keys():
    temp = list(neighbourhood[i].values())
    ord_quantity.append(temp[0])
    distance.append(temp[1])

res_dist = data['restaurants']['r0']['neighbourhood_distance']

print("Distance to neighbourhood from restaurant r0:", res_dist)
print("Order_quantity for each area:", ord_quantity)

max_cap = data['vehicles']['v0']['capacity']

print("Capacity of scooter:", max_cap)
print("Total quantity:", sum(ord_quantity))
print("Minimum number of slots:", round(sum(ord_quantity) / max_cap))


def find_optimized_slots(distances, res_dist, ord_quantities, max_cap):
    node_order = sorted(range(len(res_dist)), key=lambda x: res_dist[x])
    slots = []
    current_slot = []
    current_capacity = 0
    current_distance = 0

    for node in node_order:
        if current_capacity + ord_quantities[node] <= max_cap:
            current_slot.append(node)
            current_capacity += ord_quantities[node]

            if len(current_slot) > 1:
                current_distance += distances[current_slot[-2]][current_slot[-1]]
        else:
            slots.append((current_slot, current_distance))
            current_slot = [node]
            current_capacity = ord_quantities[node]
            current_distance = 0

    if current_slot:
        slots.append((current_slot, current_distance))

    optimized_slots = []

    for slot, _ in slots:
        possible_orders = itertools.permutations(slot)
        min_distance = float('inf')
        best_order = []

        for order in possible_orders:
            dist = sum(distances[order[i]][order[i + 1]] for i in range(len(order) - 1))
            if dist < min_distance:
                min_distance = dist
                best_order = order

        optimized_slots.append((best_order, min_distance))

    return optimized_slots


optimized_slots = find_optimized_slots(distance, res_dist, ord_quantity, max_cap)
final_lst = []

for i in optimized_slots:
    temp = ['r0']
    temp.extend(['n' + str(j) for j in i[0]])
    temp.append('r0')
    final_lst.append(temp)

final_slots = {"v0": {f"path{i + 1}": final_lst[i] for i in range(len(final_lst))}}
print(final_slots)

output_file_path = "MyOutput/level1a_output.json"
with open(output_file_path, "w") as save_file:
    json.dump(final_slots, save_file, indent=6)