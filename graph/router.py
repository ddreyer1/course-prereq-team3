#this gets the code from other programs and libraries and databases in order to run correctly
from fastapi import HTTPException, APIRouter
from database.types import *
from graph.prereq_graph import fullPrereqGraph
import networkx as nx


router = APIRouter(prefix="/prereq-graph")

# Graph Data is returned in a format compatible with Cytoscape.js

@router.get("/")
def get_prereq_graph():
    try:
        return nx.cytoscape_data(fullPrereqGraph.graph)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{course_id}")
def get_course_prereq_graph(course_id: int):
    try:
        subgraph = fullPrereqGraph.subgraph(course_id=course_id)
        return nx.cytoscape_data(subgraph)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


