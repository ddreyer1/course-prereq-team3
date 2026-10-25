# this file is used to test the database initialization
import pytest
from pydantic import ValidationError
from database.init_db import supabase
from database.types import Course


def test_course_table():
    # tests getting data from the database (specifically the courses table)
    response = supabase.table("courses").select("*").limit(1).execute()
    row = response.data[0]

    course = Course(**row)

    # makes sure the types match, returns an error if not
    assert isinstance(course, Course)

    # will print if there is no type errors
    print("Test success. Types matched")


def test_bad_format():
    # tests that an invalid row throws an exception
    response = supabase.table("courses").select("*").limit(1).execute()
    row = response.data[0].copy()
    row["course_id"] = "not-an-integer"

    with pytest.raises(ValidationError):
        Course(**row)
