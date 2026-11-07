#imprts and other connections to the database and the prereq graph
import json
import pytest
import networkx as nx

import matplotlib.pyplot as plt

from database.queries import get_graph_data

from graph.prereq_graph import build_graph, getCoursePrereqs, draw_graph


#define database data
@pytest.fixture(scope = "module")
def database_data():

    #gets data
    data = get_graph_data()

    #populates data
    assert data is not None

    #sets the data for each section
    assert "courses" in data
    assert "prerequisite_groups" in data
    assert "prerequisites" in data

    return data


#graph of data
@pytest.fixture(scope = "module")
def graph(database_data):

    #returns the built graph
    return build_graph(database_data)

#test to see if graph is built
def test_build_graph(graph, database_data):

    #assets that graph is in instance of nx graph
    assert isinstance(graph, nx.DiGraph)

    #for any course in database data that is cousre, check to see if it matches the database
    for course in database_data["courses"]:

        course_id = course.course_id

        assert course_id in graph

        assert graph.nodes[course_id]["node_type"] == "course"

        assert graph.nodes[course_id]["label"] == course.course_title

        assert graph.nodes[course_id]["course_identifier"] == course.course_identifier

    #checks to see id the group data in database is correct with eachother
    for group in database_data["prerequisite_groups"]:

        group_id = f"group_{group.prerequisite_group_id}"

        assert group_id in graph

        assert graph.nodes[group_id]["node_type"] == "group"

        assert graph.nodes[group_id]["operator"] == group.group_operator


#checks edge cases of the group
def test_build_graph_edge_group(graph, database_data):

    #checks to see if the group data in database match parent and itself
    for group in database_data["prerequisite_groups"]:

        group_id = f"group_{group.prerequisite_group_id}"

        parent_id = group.parent_group_id

        #if not check to see if it has edges
        if parent_id is None:

            assert graph.has_edge(group_id, group.course_id)

        #otherwise compare data
        else:

            parent_group_id = f"group_{parent_id}"

            assert graph.has_edge(group_id, parent_group_id)


#checks to build of prereq edge data
def test_build_prereq_edges(graph, database_data):

    #checks to see of data in prerequisit graph are the same as the given data
    for prerequisite in database_data["prerequisites"]:

        prereq_course = prerequisite.prerequisite_course_id

        group_id =  f"group_{prerequisite.prerequisite_group_id}"

        assert graph.has_edge(prereq_course, group_id)

        edge_data = graph.edges[prereq_course, group_id]

        assert edge_data["min_grade"] == prerequisite.min_grade

        assert edge_data["concurrent_allowed"] == prerequisite.concurrent_allowed

        assert edge_data["negative_prerequisite"] == prerequisite.negative_prerequisite


#checks getting data by course id
def test_getCoursePrereq_id(graph, database_data):

    course_id = database_data["courses"][0].course_id

    subgraph = getCoursePrereqs(graph, course_id=course_id)

    expected = nx.ancestors(graph, course_id)

    expected.add(course_id)

    assert set(subgraph.nodes()) == expected

    assert course_id in subgraph

    assert isinstance(subgraph, nx.DiGraph)

#test get course id by identifier (id anyways but wrote it anyways)
def test_getCourse_identifier(graph, database_data):

    course = database_data["courses"][0]

    course_id = course.course_id

    subgraph = getCoursePrereqs(graph, course_id= course_id)

    assert course_id in subgraph

#checks for invalid id
def test_getCoursePrereq_invalid_id(graph):

    with pytest.raises(ValueError):

        getCoursePrereqs(graph, course_id = -9999)


#checks for invalid identifier (again just id)
def test_getCoursePrereq_invalid_identifier(graph):

    with pytest.raises(ValueError):

        getCoursePrereqs(graph, course_id = -1)


#test drawing the graph
def test_draw_graph(graph, monkeypatch):

    #sets the attributes of the graph to defaults
    monkeypatch.setattr(plt, "show", lambda: None)

    #draws graph
    draw_graph(graph)

    #closes graph
    plt.close("all")


# Unit tests for the graph wrapper and its HTTP routes.
from types import SimpleNamespace
from unittest.mock import Mock

from fastapi import FastAPI
from fastapi.testclient import TestClient

from graph import prereq_graph as prereq_graph_module
from graph import router as graph_router


@pytest.fixture
def prerequisite_graph_data():
    return {
        "courses": [
            SimpleNamespace(
                course_id=course_id,
                course_identifier=identifier,
                course_title=title,
            )
            for course_id, identifier, title in [
                (1, "CMSC 201", "Introduction to Programming"),
                (2, "CMSC 202", "Computer Science II"),
                (3, "CMSC 341", "Data Structures"),
                (4, "MATH 151", "Calculus I"),
            ]
        ],
        "prerequisite_groups": [
            SimpleNamespace(
                prerequisite_group_id=group_id,
                course_id=course_id,
                group_operator=operator,
                parent_group_id=parent_id,
            )
            for group_id, course_id, operator, parent_id in [
                (10, 2, "AND", None),
                (20, 3, "OR", None),
                (21, 3, "AND", 20),
            ]
        ],
        "prerequisites": [
            SimpleNamespace(
                prerequisite_course_id=course_id,
                prerequisite_group_id=group_id,
                min_grade="C",
                concurrent_allowed=False,
                negative_prerequisite=False,
            )
            for course_id, group_id in [(1, 10), (2, 21), (1, 20)]
        ],
    }


@pytest.fixture
def prerequisite_graph(monkeypatch, prerequisite_graph_data):
    monkeypatch.setattr(
        prereq_graph_module, "get_graph_data", lambda: prerequisite_graph_data
    )
    return prereq_graph_module.PrerequisiteGraph()


@pytest.fixture
def graph_client(monkeypatch, prerequisite_graph):
    monkeypatch.setattr(graph_router, "fullPrereqGraph", prerequisite_graph)
    app = FastAPI()
    app.include_router(graph_router.router)
    with TestClient(app) as client:
        yield client


def test_prerequisite_graph_initializes_from_database(monkeypatch, prerequisite_graph_data):
    get_data = Mock(return_value=prerequisite_graph_data)
    monkeypatch.setattr(prereq_graph_module, "get_graph_data", get_data)

    prerequisite_graph = prereq_graph_module.PrerequisiteGraph()

    get_data.assert_called_once_with()
    assert isinstance(prerequisite_graph.graph, nx.DiGraph)
    assert set(prerequisite_graph.graph) == {1, 2, 3, 4, "group_10", "group_20", "group_21"}
    assert set(prerequisite_graph.graph.edges) == {
        (1, "group_10"), (1, "group_20"), ("group_10", 2),
        (2, "group_21"), ("group_21", "group_20"), ("group_20", 3),
    }
    assert prerequisite_graph.graph.nodes[3]["course_identifier"] == "CMSC 341"
    assert prerequisite_graph.graph.nodes["group_20"]["operator"] == "OR"
    assert prerequisite_graph.graph.edges[2, "group_21"] == {
        "min_grade": "C",
        "concurrent_allowed": False,
        "negative_prerequisite": False,
    }


def test_prerequisite_graph_rejects_existing_graph():
    with pytest.raises(NotImplementedError, match="Initializing with an existing graph"):
        prereq_graph_module.PrerequisiteGraph(graph=nx.DiGraph())


def test_prerequisite_graph_courses_excludes_groups(prerequisite_graph):
    assert prerequisite_graph.courses() == [
        (1, "CMSC 201", "Introduction to Programming"),
        (2, "CMSC 202", "Computer Science II"),
        (3, "CMSC 341", "Data Structures"),
        (4, "MATH 151", "Calculus I"),
    ]


def test_prerequisite_graph_empty_database(monkeypatch):
    monkeypatch.setattr(prereq_graph_module, "get_graph_data", lambda: {
        "courses": [], "prerequisite_groups": [], "prerequisites": [],
    })
    prerequisite_graph = prereq_graph_module.PrerequisiteGraph()

    assert len(prerequisite_graph.graph) == 0
    assert prerequisite_graph.courses() == []
    with pytest.raises(ValueError, match="not found in the graph"):
        prerequisite_graph.subgraph(course_id=1)


@pytest.mark.parametrize("course_id, expected_nodes, expected_edges", [
    (1, {1}, set()),
    (2, {1, 2, "group_10"}, {(1, "group_10"), ("group_10", 2)}),
    (3, {1, 2, 3, "group_10", "group_20", "group_21"}, {
        (1, "group_10"), (1, "group_20"), ("group_10", 2),
        (2, "group_21"), ("group_21", "group_20"), ("group_20", 3),
    }),
])
def test_prerequisite_graph_subgraph_by_id(
    prerequisite_graph, course_id, expected_nodes, expected_edges
):
    subgraph = prerequisite_graph.subgraph(course_id=course_id)

    assert isinstance(subgraph, nx.DiGraph)
    assert set(subgraph) == expected_nodes
    assert set(subgraph.edges) == expected_edges
    for node in subgraph:
        assert subgraph.nodes[node] == prerequisite_graph.graph.nodes[node]
    for source, target in subgraph.edges:
        assert subgraph.edges[source, target] == prerequisite_graph.graph.edges[source, target]


def test_prerequisite_graph_subgraph_is_independent(prerequisite_graph):
    subgraph = prerequisite_graph.subgraph(course_id=3)
    subgraph.nodes[3]["label"] = "Changed title"
    subgraph.edges[2, "group_21"]["min_grade"] = "A"
    subgraph.remove_node(1)

    assert prerequisite_graph.graph.nodes[3]["label"] == "Data Structures"
    assert prerequisite_graph.graph.edges[2, "group_21"]["min_grade"] == "C"
    assert 1 in prerequisite_graph.graph


@pytest.mark.parametrize("course_id", [None, -9999])
def test_prerequisite_graph_subgraph_invalid_id(prerequisite_graph, course_id):
    with pytest.raises(ValueError, match="not found in the graph"):
        prerequisite_graph.subgraph(course_id=course_id)


def test_prerequisite_graph_subgraph_by_identifier(prerequisite_graph):
    subgraph = prerequisite_graph.subgraph(course_identifier="CMSC 341")

    assert set(subgraph) == {1, 2, 3, "group_10", "group_20", "group_21"}
    assert set(subgraph.edges) == set(prerequisite_graph.subgraph(course_id=3).edges)


def test_prerequisite_graph_subgraph_invalid_identifier(prerequisite_graph):
    with pytest.raises(ValueError, match="not found in the graph"):
        prerequisite_graph.subgraph(course_identifier="UNKNOWN 999")


@pytest.mark.parametrize("method", ["subgraph", "courses"])
def test_prerequisite_graph_uninitialized(prerequisite_graph, method):
    prerequisite_graph.graph = None

    with pytest.raises(ValueError, match="Graph is not initialized"):
        getattr(prerequisite_graph, method)()


def test_prerequisite_graph_cycle_detection_not_implemented(prerequisite_graph):
    with pytest.raises(NotImplementedError, match="Cycle detection is not implemented yet"):
        prerequisite_graph.isInvalidCycle()


def test_graph_endpoint_returns_full_cytoscape_graph(graph_client, prerequisite_graph):
    response = graph_client.get("/prereq-graph/")

    assert response.status_code == 200
    assert response.json() == json.loads(json.dumps(nx.cytoscape_data(prerequisite_graph.graph)))


@pytest.mark.parametrize("course_id, expected_nodes", [
    (1, {1}),
    (3, {1, 2, 3, "group_10", "group_20", "group_21"}),
])
def test_course_graph_endpoint_returns_prerequisites(graph_client, course_id, expected_nodes):
    response = graph_client.get(f"/prereq-graph/{course_id}")

    assert response.status_code == 200
    subgraph = nx.cytoscape_graph(response.json())
    assert subgraph.is_directed()
    assert set(subgraph) == expected_nodes
    if course_id == 3:
        assert set(subgraph.edges) == {
            (1, "group_10"), (1, "group_20"), ("group_10", 2),
            (2, "group_21"), ("group_21", "group_20"), ("group_20", 3),
        }
        assert subgraph.edges[2, "group_21"]["min_grade"] == "C"
        assert subgraph.nodes[3]["course_identifier"] == "CMSC 341"
    else:
        assert subgraph.number_of_edges() == 0


def test_course_graph_endpoint_unknown_course(graph_client):
    response = graph_client.get("/prereq-graph/-9999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Course ID -9999 not found in the graph."}


@pytest.mark.parametrize("course_id", ["not-a-number", "1.5"])
def test_course_graph_endpoint_invalid_id(graph_client, course_id):
    response = graph_client.get(f"/prereq-graph/{course_id}")

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["path", "course_id"]


@pytest.mark.parametrize("path", ["/prereq-graph/", "/prereq-graph/3"])
def test_graph_endpoints_serialization_error(graph_client, monkeypatch, path):
    monkeypatch.setattr(graph_router.nx, "cytoscape_data", Mock(
        side_effect=RuntimeError("Graph serialization failed")
    ))

    response = graph_client.get(path)

    assert response.status_code == 500
    assert response.json() == {"detail": "Graph serialization failed"}


def test_course_graph_endpoint_unexpected_error(graph_client, prerequisite_graph, monkeypatch):
    monkeypatch.setattr(prerequisite_graph, "subgraph", Mock(
        side_effect=RuntimeError("Subgraph lookup failed")
    ))

    response = graph_client.get("/prereq-graph/3")

    assert response.status_code == 500
    assert response.json() == {"detail": "Subgraph lookup failed"}


def test_graph_endpoint_empty_graph(graph_client, prerequisite_graph):
    prerequisite_graph.graph.clear()

    response = graph_client.get("/prereq-graph/")

    assert response.status_code == 200
    assert response.json()["elements"] == {"nodes": [], "edges": []}
