import json
from jsonfilereader import read_json_file

def create_distances_matrix(data):
    n_neighbourhoods = data.get("n_neighbourhoods", 0)  # Default to 0 if not found
    distances_matrix = {}

    for i in range(n_neighbourhoods):
        neighborhood_key = "n" + str(i)
        distances_matrix[i] = data["neighbourhoods"][neighborhood_key]["distances"]

    return distances_matrix

def held_karp(distances):
    n = len(distances)
    memo = {}

    def tsp(mask, pos):
        if mask == (1 << n) - 1:
            return distances[pos][0], [pos]

        if (mask, pos) in memo:
            return memo[(mask, pos)]

        optimal_cost = float('inf')
        optimal_path = None

        for next_pos in range(n):
            if mask & (1 << next_pos) == 0:
                new_mask = mask | (1 << next_pos)
                cost, path = tsp(new_mask, next_pos)
                total_cost = distances[pos][next_pos] + cost

                if total_cost < optimal_cost:
                    optimal_cost = total_cost
                    optimal_path = [pos] + path

        memo[(mask, pos)] = optimal_cost, optimal_path
        return optimal_cost, optimal_path

    _, optimal_path = tsp(1, 0)
    return optimal_path

def convert_output(output_data):
    converted_output = {}
    for vehicle, paths in output_data.items():
        converted_paths = {}
        for path, nodes in paths.items():
            converted_nodes = ["r0"] + [f"n{node}" if isinstance(node, int) else node for node in nodes[1:-1]] + ["r0"]
            converted_paths[path] = converted_nodes
        converted_output[vehicle] = converted_paths
    return converted_output

def create_orders_list(data):
    orders_list = []
    n_neighbourhoods = data.get("n_neighbourhoods", 0)  # Default to 0 if not found

    for i in range(n_neighbourhoods):
        neighborhood_key = "n" + str(i)
        order_quantity = data["neighbourhoods"][neighborhood_key]["order_quantity"]
        
        if order_quantity > 0:
            order = {
                "neighborhood": i,  # Convert key to integer
                "quantity": order_quantity,
                "distance": 0
            }
            for j in range(n_neighbourhoods):
                if i != j:  # Exclude the same neighborhood
                    order["distance"] += data["neighbourhoods"][neighborhood_key]["distances"][j]

            orders_list.append(order)
    
    return orders_list


def find_delivery_slots(orders, scooter_capacity, distances_matrix):
    orders.sort(key=lambda x: x['quantity'], reverse=True)  # Sort orders by quantity in descending order

    delivery_slots = []
    current_slot = {'orders': [], 'total_distance': 0, 'remaining_capacity': scooter_capacity}

    for order in orders:
        if order['quantity'] <= current_slot['remaining_capacity']:
            current_slot['orders'].append(order['neighborhood'])
            current_slot['total_distance'] += distances_matrix[order['neighborhood']][0]  # Distance to restaurant
            current_slot['remaining_capacity'] -= order['quantity']
        else:
            delivery_slots.append(current_slot)
            current_slot = {'orders': [order['neighborhood']], 'total_distance': distances_matrix[order['neighborhood']][0], 'remaining_capacity': scooter_capacity - order['quantity']}

    if current_slot['orders']:
        delivery_slots.append(current_slot)

    return delivery_slots

file_path = r"C:\Users\TEMP.CS2K16.000\Downloads\Student Handout\Input data\level1a.json"
json_data = read_json_file(file_path)

# Create orders list
orders_list = create_orders_list(json_data)

# Get scooter capacity
scooter_capacity = json_data['vehicles']['v0']['capacity']

# Get distances matrix
distances_matrix = create_distances_matrix(json_data)

# Use Held-Karp to find the optimal path
optimal_path = held_karp(distances_matrix)

# Find delivery slots using the optimal path
delivery_slots = find_delivery_slots(orders_list, scooter_capacity, distances_matrix)

# Prepare output data
output_data = {"v0": {}}
for i, slot in enumerate(delivery_slots):
    output_data["v0"]["path" + str(i + 1)] = ["r0"] + slot['orders'] + ["r0"]

# Convert and print the result
converted_output = convert_output(output_data)
print(json.dumps(converted_output, indent=2))

# Save the result to a file
output_file_path = "level1a_output.json"
with open(output_file_path, 'w') as output_file:
    json.dump(converted_output, output_file, indent=2)

print(f"Result written to {output_file_path}")
