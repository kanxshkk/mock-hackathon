
def nearest_neighbor(distances_matrix, start_point):
    n_neighbourhoods = len(distances_matrix)
    
    # Initialize lists to track visited and unvisited neighborhoods
    unvisited = set(range(1, n_neighbourhoods))
    visited = [0]  # Start with the restaurant

    current_node = 0  # Start from the restaurant
    total_distance = 0

    while unvisited:
        nearest_neighbor = min(unvisited, key=lambda x: distances_matrix[current_node][x])
        total_distance += distances_matrix[current_node][nearest_neighbor]
        current_node = nearest_neighbor
        visited.append(nearest_neighbor)
        unvisited.remove(nearest_neighbor)

    # Return to the starting point (restaurant)
    total_distance += distances_matrix[current_node][0]
    visited.append(0)

    # Create the path with the node names ("r0", "n0", "n1", ..., "r0")
    path = [start_point] + ["n" + str(node) for node in visited] + [start_point]

    return {"path": path, "total_distance": total_distance}