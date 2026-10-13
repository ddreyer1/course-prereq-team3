from fastapi import FastAPI,HTTPException

import networkx as nx

app = FastAPI()

graph = nx.DiGraph()

#test code


graph.add_edges_from([

("CMCS 341","CMCS 203"),("CMCS 203","CMCS 202"),("CMCS 202","CMCS 201"),("CMCS 341","CMCS 331"),("CMCS 331","CMCS 201"),


])




def check_Reachability(start: str, target: str):

    if start not in graph:

        raise ValueError(f"course {start} not found")

    if target not in graph:

        raise ValueError(f"course {target} not found")

    reachable = nx.has_path(graph, target, start)

    if reachable:

        path = nx.shortest_path(graph, target, start)

    else:

        path = []       


    return {

        "start_course": start,
        "target_course": target,
        "reachable": reachable,
        "path": path

    }

result = check_Reachability("CMCS 201", "CMCS 341") #testing purposes
print(result) #testing purposes