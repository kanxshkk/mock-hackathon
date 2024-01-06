#read json file and get 2dlist
from  jsonfilereader import *

file_path =  r"C:\Users\TEMP.CS2K16.000\Downloads\Student Handout\Input data\level0.json"

json_data = read_json_file(file_path)

distances_matrix = create_distances_matrix(json_data)



for row in distances_matrix:
    print(row)

#nearwest neighbhours o(n^2) where as tsm O(n!)
from near_n import *
result = nearest_neighbor(distances_matrix, "r0")
print(result)
output_data = {"v0": {"path": result}}

# Write the result to a JSON file
output_file_path = "level0_output.json"
with open(output_file_path, 'w') as output_file:
    json.dump(output_data, output_file, indent=2)

print(f"Result written to {output_file_path}")
