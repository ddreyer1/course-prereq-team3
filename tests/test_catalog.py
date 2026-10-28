#file to test getting courses from the database
import pytest
from catalog.Classes import get_courses
from catalog.Classes import get_course
from fastapi import HTTPException

#test getting a course
def test_get_course():
    #makes sure a valid class is called
    course = get_course(270)

    assert course is not None
    assert course.course_id == 270
    print("A known course was gotten succesfully")

    #makes sure an invalid course id has an exception
    with pytest.raises(HTTPException):
        get_course(0)
    print("An unkown course id threw an exception")

    #makes sure no id throws an error
    with pytest.raises(TypeError):
        get_course()
    print("No course id threw an exception")

        #makes sure an invalid course id has an exception
    with pytest.raises(HTTPException):
        get_course('a')
    print("An unkown course id threw an exception")

#tests getting all the courses
def test_get_courses():
    courses = get_courses()

    #makes sure all courses have been gotten
    assert len(courses) == 2236 #total number of courses in the courses table. Should not change
    print("All courses succesfully gotten")

    #tests that all courses have the required fields
    for course in courses:
        assert course.department_id is not None
        assert course.course_id is not None
        assert course.course_title is not None
        assert course.credits is not None

