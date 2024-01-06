import json
from jsonfilereader import read_json_file

def create_orders_list(data):
    orders_list = []
    
    for i in range(data["n_neighbourhoods"]):
        neighborhood_key = "n" + str(i)
        order_quantity = data["neighbourhoods"][neighborhood_key]["order_quantity"]
        
        if order_quantity > 0:
            order = {
                "neighborhood": neighborhood_key,
                "quantity": order_quantity,
                "distance": sum(data["neighbourhoods"][neighborhood_key]["distances"])
            }
            orders_list.append(order)
    
    return orders_list

def find_delivery_slots(orders, scooter_capacity):
    orders.sort(key=lambda x: x['distance'])  # Sort orders by distance

    delivery_slots = []
    current_slot = {'orders': [], 'total_distance': 0, 'remaining_capacity': scooter_capacity}

    for order in orders:
        if order['quantity'] <= current_slot['remaining_capacity']:
            current_slot['orders'].append(order['neighborhood'])
            current_slot['total_distance'] += order['distance']
            current_slot['remaining_capacity'] -= order['quantity']
        else:
            delivery_slots.append(current_slot)
            current_slot = {'orders': [order['neighborhood']], 'total_distance': order['distance'], 'remaining_capacity': scooter_capacity - order['quantity']}

    if current_slot['orders']:
        delivery_slots.append(current_slot)

    return delivery_slots

file_path = r"C:\Users\TEMP.CS2K16.000\Downloads\Student Handout\Input data\level1a.json"
json_data = read_json_file(file_path)

orders_list = create_orders_list(json_data)

scooter_capacity = json_data['vehicles']['v0']['capacity']

delivery_slots = find_delivery_slots(orders_list, scooter_capacity)

output_data = {"v0": {}}
for i, slot in enumerate(delivery_slots):
    output_data["v0"]["path" + str(i + 1)] = ["r0"] + slot['orders'] + ["r0"]

print(json.dumps(output_data, indent=2))

output_file_path = "level1a_output.json"
with open(output_file_path, 'w') as output_file:
    json.dump(output_data, output_file, indent=2)

print(f"Result written to {output_file_path}")
