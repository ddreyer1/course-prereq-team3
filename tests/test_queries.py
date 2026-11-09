from database.queries import get_all_rows, get_courses, get_prereq_groups, get_prereqs, get_graph_data
from database.types import Course, PrerequisiteGroup, Prerequisite

#test get all
def test_get_all():

   #get all rows
    rows = get_all_rows("courses")

    #arrert in the instance
    assert isinstance(rows, list)

    #for row in rows assert in instance
    for row in rows:

        assert isinstance(row, dict)

    #if row is greater then 0 return the course id in row[0]
    if len(rows) > 0:

        assert "course_id" in rows[0]

#the rest of the test are set up similar to eachother

#tests the get courses 
def test_get_courses():

    courses = get_courses()

    assert isinstance(courses, list)

    for course in courses:
        assert type(course) == Course


#tests the get the prereq graph
def test_get_prereq_graph():

    groups = get_prereq_groups()

    assert isinstance(groups, list)

    for group in groups:

        assert type(group) == PrerequisiteGroup



#test to get ptrereqs
def test_get_prereqs():

    prereq = get_prereqs()

    assert isinstance(prereq, list)

    for prerequisite in prereq:

        assert type(prerequisite) == Prerequisite

#test to get graph data
def test_get_graph_data():

    data = get_graph_data()

    assert isinstance(data, dict)

    assert "courses" in data
    assert "prerequisite_groups" in data
    assert "prerequisites" in data

    assert isinstance(data["courses"], list)
    assert isinstance(data["prerequisite_groups"], list)
    assert isinstance(data["prerequisites"], list)

    assert len(data["courses"]) > 0