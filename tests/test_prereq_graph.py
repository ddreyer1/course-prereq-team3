#imprts and other connections to the database and the prereq graph
import json
import pytest
import networkx as nx

import matplotlib.pyplot as plt

from database.queries import get_graph_data

from graph.prereq_graph import load_data, build_graph, getCoursePrereqs, draw_graph


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


#tests the loading of data
def test_load_data(tmp_path, database_data):

    #path of data is a test file to create
    path = tmp_path / "testdata.json"

    #opens test file and dumps the data
    with open(path, "w") as file:

        json.dump(database_data, file)

    #loads the file with called load data
    loaded = load_data(path)

    #checks to see if data matches
    assert loaded == database_data

#test to see if file is missing correctly
def test_load_missing_file():

    with pytest.raises(FileNotFoundError):

        load_data("missingfile.json")


#test to see if invalid data fails
def test_load_invalid(tmp_path):

    path = tmp_path / "invalid.json"

    with open(path, "w") as file:

        #writes invalid data in the new file
        file.write("invalid data")

    #when its invalid try to load into data
    with pytest.raises(json.JSONDecodeError):

        load_data(path)


#test to see if graph is built
def test_build_graph(graph, database_data):

    #assets that graph is in instance of nx graph
    assert isinstance(graph, nx.DiGraph)

    #for any course in database data that is cousre, check to see if it matches the database
    for course in database_data["courses"]:

        course_id = course["course_id"]

        assert course_id in graph

        assert graph.nodes[course_id]["node_type"] == "course"

        assert graph.nodes[course_id]["label"] == course["course_title"]

        assert graph.nodes[course_id]["course_identifier"] == course["course_identifier"]

    #checks to see id the group data in database is correct with eachother
    for group in database_data["prerequisite_groups"]:

        group_id = f"group_{group['prerequisite_group_id']}"

        assert group_id in graph

        assert graph.nodes[group_id]["node_type"] == "group"

        assert graph.nodes[group_id]["operator"] == group["group_operator"]


#checks edge cases of the group
def test_build_graph_edge_group(graph, database_data):

    #checks to see if the group data in database match parent and itself
    for group in database_data["prerequisite_groups"]:

        group_id = f"group_{group['prerequisite_group_id']}"

        parent_id = group["parent_group_id"]

        #if not check to see if it has edges
        if parent_id is None:

            assert graph.has_edge(group_id, group["course_id"])

        #otherwise compare data
        else:

            parent_group_id = f"group_{parent_id}"

            assert graph.has_edge(group_id, parent_group_id)


#checks to build of prereq edge data
def test_build_prereq_edges(graph, database_data):

    #checks to see of data in prerequisit graph are the same as the given data
    for prerequisite in database_data["prerequisites"]:

        prereq_course = prerequisite["prerequisite_course_id"]

        group_id =  f"group_{prerequisite['prerequisite_group_id']}"

        assert graph.has_edge(prereq_course, group_id)

        edge_data = graph.edges[prereq_course, group_id]

        assert edge_data["min_grade"] == prerequisite["min_grade"]

        assert edge_data["concurrent_allowed"] == prerequisite["concurrent_allowed"]

        assert edge_data["negative_prerequisite"] == prerequisite["negative_prerequisite"]


#checks getting data by course id
def test_getCoursePrereq_id(graph, database_data):

    course_id = database_data["courses"][0]["course_id"]

    subgraph = getCoursePrereqs(graph, course_id=course_id)

    expected = nx.ancestors(graph, course_id)

    expected.add(course_id)

    assert set(subgraph.nodes()) == expected

    assert course_id in subgraph

    assert isinstance(subgraph, nx.DiGraph)

#test get course id by identifier (id anyways but wrote it anyways)
def test_getCourse_identifier(graph, database_data):

    course = database_data["courses"][0]

    course_id = course["course_id"]

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