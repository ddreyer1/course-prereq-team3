import networkx as nx
import matplotlib.pyplot as plt
from database.queries import get_graph_data

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
#return a subgraph containing the course and its prerequisites
#from course ids or course identifers. 
def getCoursePrereqs(G, course_id=None, course_identifier=None):
    target_course_id = None

    if course_id is not None:
        target_course_id = course_id
    #makes a subgraph with course identifier if input is valid
    elif course_identifier is not None:
        for node,node.data in G.nodes(data=True):
            if (node.data.get("node_type") == "course" 
                and node.data.get("course_identifier") == course_identifier):
                target_course_id = node
                break
    #if the input is neither a valid course ID nor a valid course identifier
    if target_course_id is None or target_course_id not in G:
        raise ValueError(f"Course ID {course_id} not found in the graph.")
    
    #make a subgraph with all ancestor nodes of the target course, 
    #including the target course itself
    nodes = nx.ancestors(G, target_course_id)
    nodes.add(target_course_id)
    return G.subgraph(nodes).copy()

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
        node_size=2500,
        arrows=True
    )

    nx.draw_networkx_labels(
        G,
        pos,
        labels=labels
    )

    plt.show()

if __name__ == "__main__":
    data = get_graph_data()
    graph = build_graph(data)
    #display all courseid/identifier
    print("\nAvailable courses:")
    for node, node_data in graph.nodes(data=True):
        if node_data.get("node_type") == "course":
            print(
                f"{node}: "
                f"{node_data.get('course_identifier')} - "
                f"{node_data.get('label')}"
            )

    user_input = input("Enter course id or course identifier:")
    #validate input
    try:
        if user_input.isdigit():
            course_subgraph = getCoursePrereqs(graph, course_id=int(user_input))
        else:
            course_subgraph = getCoursePrereqs(graph, course_identifier=user_input)
        print("\nsubgraph nodes: ")
        for node, node_data in course_subgraph.nodes(data=True):
            print(node,node_data)
        print("\nsubgraph edges: ")
        for edge in course_subgraph.edges():
            print(edge)
        
        draw_graph(course_subgraph)
    except ValueError as error:
        print(error)



class PrerequisiteGraph:
    def __init__(self, graph):
        self.graph = graph

    def get_course_prereqs(self, course_id=None, course_identifier=None):
        return getCoursePrereqs(self.graph, course_id=course_id, course_identifier=course_identifier)