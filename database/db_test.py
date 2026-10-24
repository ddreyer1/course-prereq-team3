#this file is used to test the database initialization
from init_db import supabase
from db_types import Course

def test_course_table():
    #tests getting data from the database (specifically the courses table)
    response = supabase.table("courses").select("*").limit(1).execute()
    row = response.data[0]

    course = Course(**row)

    #makes sure the types match, returns an error if not
    assert isinstance(course.course_id, int)

    #will print if there is no type errors
    print("Test success. Types matched")
