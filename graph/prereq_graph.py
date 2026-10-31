import json
import networkx as nx
import matplotlib.pyplot as plt

from database.queries import get_graph_data
def load_data(file_path):
    with open(file_path,"r") as file:
        return json.load(file)

def build_graph(data):
    #create empty graph
    G = nx.DiGraph()

    #add course nodes
    for course in data["courses"]:
        course_id = course["course_id"]

        G.add_node(
            course_id,
            node_type="course",
            label=course["course_title"],
            course_identifier=course["course_identifier"]
        )
    #add group nodes
    for group in data["prerequisite_groups"]:

        group_id = f"group_{group['prerequisite_group_id']}"

        G.add_node(
            group_id,
            node_type ="group",
            operator=group["group_operator"],
            label=group["group_operator"],
            course_id=group["course_id"],
            parent_group_id=group["parent_group_id"]
        )
    #connect groups
    for group in data["prerequisite_groups"]:
        group_id = f"group_{group['prerequisite_group_id']}"

        parent_id = group["parent_group_id"]

        #if the group has no parent group(root group), connect to target class
        if parent_id is None:
            G.add_edge(
                group_id,
                group["course_id"]
            )
        #connect sub group to parent group
        else:
            parent_group_id = f"group_{parent_id}"

            G.add_edge(
                group_id,
                parent_group_id
            )

  
    #connect prereq courses to groups
    for prerequisite in data["prerequisites"]:
        prereq_course = prerequisite["prerequisite_course_id"]

        group_id = (
            f"group_{prerequisite['prerequisite_group_id']}"
        )

        G.add_edge(
            prereq_course,
            group_id,
            min_grade=prerequisite["min_grade"],
            concurrent_allowed=prerequisite["concurrent_allowed"],
            negative_prerequisite=prerequisite["negative_prerequisite"]
        )

    return G

def draw_graph(G, course_id):
    prereqs = nx.ancestors(G, course_id)
    prereqs.add(course_id)

    subgraph = G.subgraph(prereqs).copy()

    pos = nx.spring_layout(subgraph)

    labels = {
        node: data.get("label", str(node))
        for node, data in subgraph.nodes(data=True)
    }

    nx.draw_networkx(
        subgraph,
        pos,
        with_labels=False,
        node_size=2500,
        arrows=True
    )

    nx.draw_networkx_labels(
        subgraph,
        pos,
        labels=labels
    )

    plt.show()

if __name__ == "__main__":
    data = get_graph_data()

    graph = build_graph(data)
    '''
    print("Nodes: ")
    print(graph.nodes(data=True))

    print("\nEdges: ")
    print(graph.edges())
    '''
    draw_graph(graph, 2571)

