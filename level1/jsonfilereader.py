import json

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def create_distances_matrix(data):
    n_neighbourhoods = data["n_neighbourhoods"]
    distances_matrix = [[0] * n_neighbourhoods for _ in range(n_neighbourhoods)]

    for i in range(n_neighbourhoods):
        neighborhood_key = "n" + str(i)
        distances_matrix[i] = data["neighbourhoods"][neighborhood_key]["distances"]

    return distances_matrix