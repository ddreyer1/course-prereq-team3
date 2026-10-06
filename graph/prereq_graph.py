import json
import networkx as nx
import matplotlib.pyplot as plt

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
            label=course["course_title"]
        )
    #add group nodes
    for group in data["prereq_groups"]:

        group_id = f"group_{group['prereq_group_id']}"

        G.add_node(
            group_id,
            node_type ="group",
            operator=group["group_operator"],
            label=group["group_operator"]
        )
        #connect group to course that requires it
        G.add_edge(
            group_id,
            group["course_id"]
        )
    #connect prereq courses to groups
    for prereq in data["prereqs"]:
        prereq_course = prereq["prereq_course_id"]

        group_id = (
            f"group_{prereq['prereq_group_id']}"
        )

        G.add_edge(
            prereq_course,
            group_id
        )

    return G
def draw_graph(G):
    pos = nx.spring_layout(G)

    labels = {
        node: data.get("label", str(node))
        for node, data in G.nodes(data=True)
    }

    nx.draw_networkx(
        G,
        pos,
        with_labels=False,
        node_size=3000,
        arrows=True
    )

    nx.draw_networkx_labels(
        G,
        pos,
        labels=labels
    )

    plt.show()

if __name__ == "__main__":
    data = load_data("data/sampledata.json")

    graph = build_graph(data)

    print("Nodes: ")
    print(graph.nodes(data=True))

    print("\nEdges: ")
    print(graph.edges())

    draw_graph(graph)

