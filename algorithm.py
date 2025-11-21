import pandas as pd
from collections import deque
from ast import literal_eval


def neighbor_key(movie, inverted_dict):
    for key, value in inverted_dict.items():
        if key == movie:
            return value

    # df_temp = df_bfs[df_bfs["primaryTitle"].apply(lambda titles: movie in titles)]
    # numpy_array = df_temp["primaryName"].to_numpy()
    # return numpy_array.tolist()


# Define the BFS function
def bfs(tree, start, target):
    visited = set()  # List to keep track of visited nodes
    movies_visited = set()
    queue = deque([(start, [start])])  # Initialize the queue with the starting node
    parent_node = {start: None}

    if start == target:
        return [start]

    while queue:  # While there are still nodes to process
        node, path = queue.popleft()  # Dequeue a node from the front of the queue
        visited.add(node)

        # Enqueue all unvisited neighbors (children) of the current node
        for movie in tree[node]:
            if movie not in movies_visited:
                movies_visited.add(movie)
                neighbors = neighbor_key(movie, inverted_dict)

                for neighbor in neighbors:
                    if neighbor not in visited:
                        parent_node[neighbor] = node
                        if neighbor == target:
                            print("Returning...")
                            return path_constructor(parent_node, start, target)
                        queue.append((neighbor, path + [neighbor]))
                        visited.add(neighbor)
    return "No Path Found"


def path_constructor(parent, start, target):
    path = []
    current = target

    path.append(current)

    while current != start:
        prev = parent[current]
        path.append(prev)
        current = prev

    return path


############# MAIN #################
df_bfs = pd.read_csv("Filtered_Actor-Movie.csv")

df_bfs["primaryTitle"] = df_bfs["primaryTitle"].apply(literal_eval)

bfs_dict = pd.Series(
    df_bfs["primaryTitle"].values, index=df_bfs["primaryName"]
).to_dict()

inverted_dict = {}

for original_key, value_list in bfs_dict.items():
    for item_in_list in value_list:
        inverted_dict.setdefault(item_in_list, []).append(original_key)

# print(inverted_dict["Footloose"])

path = bfs(bfs_dict, "Kevin Bacon", "Marga Legal")

print(path)
