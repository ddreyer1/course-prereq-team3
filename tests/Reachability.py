from fastapi import FastAPI,HTTPException
from graph.prereq_graph import load_data, build_graph

import json
import networkx as nx

app = FastAPI()

data = load_data("data/sampledata.json")

graph = build_graph(data)



def check_Reachability(start: int, target: int):

    if start not in graph:

        raise ValueError(f"course {start} not found")

    if target not in graph:

        raise ValueError(f"course {target} not found")

    reachable = nx.has_path(graph, target, start)

    if reachable:

        path = nx.shortest_path(graph, target, start)

    else:

        path = []       

    reachable_path = []

    for node in path:

        if graph.nodes[node].get("node_type") == "course":

            course_name = graph.nodes[node]["label"]
            reachable_path.append(course_name)

        else:

            reachable_path.append(node)

    return {

        "start_course": graph.nodes[start]["label"],
        "target_course":  graph.nodes[target]["label"],
        "reachable": reachable,
        "path": reachable_path

    }

result = check_Reachability(3, 2) #testing purposes
print(result) #testing purposes