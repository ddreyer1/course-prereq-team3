from database.init_db import supabase
from database.types import Course, PrerequisiteGroup, Prerequisite

#supabase returns max of 1000 rows. using range() to get all the course/prereq group/prereq data
def get_all_rows(table_name, type_=None):
    
    all_rows = []
    start = 0
    page_size = 1000

    #loop to get all data past 1000th row
    #range(0, 999) -> range(1000, 1999) so on.
    while True:
        response= (
            #get data in table_name from supabase
            supabase.table(table_name)
            #all columns
            .select("*")
            .range(start, start + page_size -1)
            #send query
            .execute()
        )
        rows = response.data
        all_rows.extend(rows)
        #stop once we received less than 1000 rows
        if len(rows) < page_size:
            break
        
        start += page_size

    if type_:
        return [type_(**row) for row in all_rows]
    return all_rows
#query courses
def get_courses():
    return get_all_rows("courses", Course)

#query prerequisite_groups
def get_prereq_groups():
    return get_all_rows("prerequisite_groups", PrerequisiteGroup)

#query prerequisites
def get_prereqs():
    return get_all_rows("prerequisites", Prerequisite)

#return all of them
def get_graph_data():
    return{
        "courses": get_courses(),
        "prerequisite_groups": get_prereq_groups(),
        "prerequisites": get_prereqs()
    }