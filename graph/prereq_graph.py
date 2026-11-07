import networkx as nx
import matplotlib.pyplot as plt
from database.queries import get_graph_data

def build_graph(data):
    #create empty graph
    G = nx.DiGraph()

    #add course nodes
    for course in data["courses"]:
        course_id = course.course_id

        G.add_node(
            course_id,
            node_type="course",
            label=course.course_title,
            course_identifier=course.course_identifier
        )
    #add group nodes
    for group in data["prerequisite_groups"]:

        group_id = f"group_{group.prerequisite_group_id}"

        G.add_node(
            group_id,
            node_type ="group",
            operator=group.group_operator,
            label=group.group_operator,
            course_id=group.course_id,
            parent_group_id=group.parent_group_id
        )
    #connect groups
    for group in data["prerequisite_groups"]:
        group_id = f"group_{group.prerequisite_group_id}"

        parent_id = group.parent_group_id

        #if the group has no parent group(root group), connect to target class
        if parent_id is None:
            G.add_edge(
                group_id,
                group.course_id
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
        prereq_course = prerequisite.prerequisite_course_id

        group_id = (
            f"group_{prerequisite.prerequisite_group_id}"
        )

        G.add_edge(
            prereq_course,
            group_id,
            min_grade=prerequisite.min_grade,
            concurrent_allowed=prerequisite.concurrent_allowed,
            negative_prerequisite=prerequisite.negative_prerequisite
        )

    return G


#return a subgraph containing the course and its prerequisites
#from course ids or course identifers. 
def getCoursePrereqs(G, course_id=None, course_identifier=None) -> nx.DiGraph:
    target_course_id = None

    if course_id is not None:
        target_course_id = course_id
    #makes a subgraph with course identifier if input is valid
    elif course_identifier is not None:
        for node, node_data in G.nodes(data=True):
            if (node_data.get("node_type") == "course" 
                and node_data.get("course_identifier") == course_identifier):
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

def draw_graph(G : nx.DiGraph):

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

class PrerequisiteGraph:
    def __init__(self, graph=None): # Assuming we will just call PrerequisiteGraph() without arguments, which will build a full graph for all courses
        if graph is None:
            data = get_graph_data()
            graph = build_graph(data)
            self.graph : nx.DiGraph = graph
        else:
            raise NotImplementedError("Initializing with an existing graph is not supported yet")

    def subgraph(self, course_id=None, course_identifier=None) -> nx.DiGraph:
            if self.graph is None:
                raise ValueError("Graph is not initialized")
            return getCoursePrereqs(self.graph, course_id=course_id, course_identifier=course_identifier)

    def courses(self): #returns a list of all courses in the graph
        if self.graph is None:
            raise ValueError("Graph is not initialized")
        courses = []
        for node, node_data in self.graph.nodes(data=True):
            if node_data.get("node_type") == "course":
                courses.append((node, node_data.get("course_identifier"), node_data.get("label")))
        return courses

    
    def isInvalidCycle(self):
        raise NotImplementedError("Cycle detection is not implemented yet")

fullPrereqGraph = PrerequisiteGraph() #import fullPrereqGraph to use throughout the project
