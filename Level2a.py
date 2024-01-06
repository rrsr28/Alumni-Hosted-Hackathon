# Alumni Hosted Hackathon 2024
# Author - Sanjay Ram R R (21PD32)

# Import statements
# ----------------

import json
from ortools.linear_solver import pywraplp

def find_optimized_slots(distances, res_dist, ord_quantities, max_capacities, num_scooters):
    solver = pywraplp.Solver.CreateSolver('SCIP')
    num_nodes = len(res_dist)
    num_vehicles = len(max_capacities)

    x = {}
    for i in range(num_nodes):
        for j in range(num_nodes):
            x[i, j] = solver.BoolVar('x[%i,%i]' % (i, j))

    u = [solver.IntVar(0, num_nodes - 1, 'u[%i]' % i) for i in range(num_nodes)]

    for i in range(num_nodes):
        solver.Add(solver.Sum([x[i, j] for j in range(num_nodes)]) == 1)
        solver.Add(solver.Sum([x[j, i] for j in range(num_nodes)]) == 1)

    for i in range(1, num_nodes):
        for j in range(1, num_nodes):
            if i != j:
                solver.Add(u[i] - u[j] + num_nodes * x[i, j] <= num_nodes - 1)

    objective = solver.Objective()
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j:
                objective.SetCoefficient(x[i, j], distances[i][j])

    objective.SetMinimization()

    solver.Solve()

    slots = [[] for _ in range(num_vehicles)]
    vehicle_deliveries = [0] * num_vehicles  # Track the deliveries for each vehicle

    for i in range(num_nodes):
        for j in range(num_nodes):
            if x[i, j].solution_value() == 1:
                vehicle_index = i % num_vehicles
                if vehicle_deliveries[vehicle_index] < max_capacities[vehicle_index]:
                    slots[vehicle_index].append((i, j))
                    vehicle_deliveries[vehicle_index] += ord_quantities[j]

    return slots

# Load input data from level2a.json
with open('Input data/level2a.json') as file:
    data = json.load(file)

distance = []
neighbourhood = data['neighbourhoods']
ord_quantity = [list(neighbourhood[i].values())[0] for i in neighbourhood]
for i in neighbourhood.keys():
    temp = list(neighbourhood[i].values())
    ord_quantity.append(temp[0])
    distance.append(temp[1])
res_dist = data['restaurants']['r0']['neighbourhood_distance']
num_scooters = 5  # Define num_scooters here
max_capacities = [data['vehicles'][f'v{i}']['capacity'] for i in range(num_scooters)]

num_scooters = len(max_capacities)

optimized_slots = find_optimized_slots(distance, res_dist, ord_quantity, max_capacities, num_scooters)

final_lst = []
for i in optimized_slots:
    temp = ['r0']
    temp.extend(['n' + str(j[0]) for j in i])
    temp.append('r0')
    final_lst.append(temp)

final_slots = {"v" + str(i): {f"path{j + 1}": final_lst[j] for j in range(len(final_lst))} for i in range(num_scooters)}

output_file_path = "MyOutput/level2a_output.json"
with open(output_file_path, "w") as save_file:
    json.dump(final_slots, save_file, indent=6)