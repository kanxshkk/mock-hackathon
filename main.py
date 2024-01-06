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