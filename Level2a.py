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

def main():
    json_file_path = 'Input data\level1b.json'
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    name = ['n' + str(i) for i in range(50)]
    orders = [{'quantity': data['neighbourhoods'][name[i]]['order_quantity'], 'location': i} for i in range(len(name))]
    scooter_capacities = [250, 350, 350, 250, 300]

    all_optimized_paths = []
    all_total_distances = []
    all_slots = []

    for scooter_capacity in scooter_capacities:
        optimized_paths, total_distance, slots = optimize_delivery_slots(orders, scooter_capacity)
        all_optimized_paths.append(optimized_paths)
        all_total_distances.append(total_distance)
        all_slots.append(slots)

    tsp_g = [[0] + [data['restaurants']['r0']['neighbourhood_distance'][i] for i in range(50)]]
    for i in range(1, 51):
        d = data['neighbourhoods'][name[i-1]]['distances']
        tsp_g.append([data['restaurants']['r0']['neighbourhood_distance'][i-1]] + [d[j] for j in range(50)])

    slo = []
    for i in range(len(all_slots)):
        for j in all_optimized_paths[i]:
            temp = []
            for loc in range(len(j)):
                s = []
                for loc_1 in range(len(j)):
                    s.append(tsp_g[j[loc]+1][j[loc_1]+1])
                temp.append(s)
            slo.append(np.array(temp))

    min_slot_dis = []
    for i in range(len(slo)):
        permutation, distance = solve_tsp_dynamic_programming(slo[i])
        min_slot_dis.append([permutation, distance])

    m = {-1: 'r0', **{i: f'n{i}' for i in range(50)}}

    d = {}
    for i in range(len(min_slot_dis)):
        w = [m[all_optimized_paths[i][j]] for j in min_slot_dis[i][0]]
        w.append('r0')
        st = 'path' + str(i+1)
        d[f'v{i}'] = {st: w}

    json_file_path = 'MyOutput\level1b_output.json'
    with open(json_file_path, 'w') as json_file:
        json.dump(d, json_file, indent=2)

if __name__ == "__main__":
    main()