#query from supabase through init() 
from database.init_db import init

#query courses
def get_courses():
    #initiate communication to supabase named clint through init()
    client = init()
    response = (
        #get "courses" from supabase
        client.table("courses")
        #all cloumns
        .select("*")
        #return at most 5 rows
        .limit(5)
        #send query
        .execute()
    )
    return response.data

#query prerequisite_groups
def get_prereq_groups():
    #initiate communication to supabase named clint through init()
    client = init()
    response = (
        #get "prerequisite_groups" from supabase
        client.table("prerequisite_groups")
        #all cloumns
        .select("*")
        #return at most 5 rows
        .limit(5)
        #send query
        .execute()
    )
    return response.data

#query prerequisites
def get_prereqs():
    #initiate communication to supabase named clint through init()
    client = init()
    response = (
        #get "prerequisites" from supabase
        client.table("prerequisites")
        #all cloumns
        .select("*")
        #return at most 5 rows
        .limit(5)
        #send query
        .execute()
    )
    return response.data

if __name__ == "__main__":
    courses = get_courses()
    groups = get_prereq_groups()
    prereqs = get_prereqs()

    print("\ncourses yes: ")
    for course in courses:
        print(course)

    print("\ngroups yes: ")
    for group in groups:
        print(group)

    print("\ncourses yes: ")
    for prereq in prereqs:
        print(prereq)