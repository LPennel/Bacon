from dash import Dash, State, dcc, html, Input, Output,callback
from collections import deque
from ast import literal_eval
import pandas as pd

#################### DATA SETUP ###########################

df_bfs = pd.read_csv("Filtered_Actor-Movie.csv")

df_bfs["primaryTitle"] = df_bfs["primaryTitle"].apply(literal_eval)

bfs_dict = pd.Series(
    df_bfs["primaryTitle"].values, index=df_bfs["primaryName"]
).to_dict()

inverted_dict = {}

for original_key, value_list in bfs_dict.items():
    for item_in_list in value_list:
        inverted_dict.setdefault(item_in_list, []).append(original_key)

################# INTERFACE #####################################

app = Dash()

app.layout = html.Div([
    html.H1(children='6 Degrees of Kevin Bacon'),
    html.Hr(),
    dcc.Dropdown(value = 'Kevin Bacon', id='start-dropdown'),
    dcc.Dropdown(value = 'Hugh Jackman', id='target-dropdown'),
    html.Hr(),
    html.H1(id='dd-output-container')
    ])

@callback(
    Output('start-dropdown', 'options'),
    Input('start-dropdown', 'search_value'),
    State('start-dropdown', 'value')
)
def update_start_options(search, current_value):

    if not search or len(search) < 3:
        if current_value:
            return [{"label": current_value, "value": current_value}]
        return []
    
    matches = [key for key in bfs_dict.keys() if search in key and len(matches) <= 50]

    return [
        {"label": match, "value": match}
        for match in matches
    ]

@callback(
    Output('target-dropdown', 'options'),
    Input('target-dropdown', 'search_value'),
    State('target-dropdown', 'value')
)
def update_target_options(search, current_value):

    matches = []

    if not search or len(search) < 3:
        if current_value:
            return [{"label": current_value, "value": current_value}]
        return []

    matches = [key for key in bfs_dict.keys() if search in key and len(matches) <= 50]

    return [
        {"label": match, "value": match}
        for match in matches
    ]


@callback(
    Output('dd-output-container', 'children'),
    Input('start-dropdown', 'value'),
    Input('target-dropdown', 'value')
)
def update_output(start_input, target_input):
    return str(bfs(bfs_dict, inverted_dict, start_input, target_input))

#################### ALGORITHM ###############################

def neighbor_key(movie, inverted_dict):
    for key, value in inverted_dict.items():
        if key == movie:
            return value

def bfs(tree, inverted_tree, start, target):
    visited = set()
    movies_visited = set()
    queue = deque([(start, [start])])
    parent_node = {start: None}

    if start == target:
        return [start]

    while queue:
        node, path = queue.popleft()
        visited.add(node)

        for movie in tree[node]:
            if movie not in movies_visited:
                movies_visited.add(movie)
                neighbors = neighbor_key(movie, inverted_tree)

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

#############################################################

if __name__ == '__main__':
    app.run(debug=True)