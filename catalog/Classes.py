#this gets the code from other programs and libraries and databases in order to run correctly
from fastapi import FastAPI, HTTPException
from database.init_db import supabase
from database.types import Course

#uses fast api
app = FastAPI()

#when accessing the website if /courses is entered at the end, it will give a list of all courses and lables associated with them
@app.get("/courses", response_model = list[Course])
def get_courses():

    #error handling that tries to get each class in batches of 100 and place them in a list
    try:

        all_courses = []
        size = 100
        start = 0

        #while true gets the data of the class from supabase and sets it to the varible response
        while True:

            response = (

                supabase
                .table("courses")
                .select("*")
                .order("course_id")
                .range(start, start + size -1)
                .execute()

            )

            #stores the data in batch amd places it in the list
            batch = response.data
            all_courses.extend(batch)

            #if length of batch is less then size add change start size
            if len(batch) < size:
                break

            start += size

        #empty list to check for valid clsses
        valid = []

        #if any component is missing in the course populate it with default values
        for course in all_courses:

            course = course.copy()

            if course.get("credits") is None:

                course["credits"] = 0.0

            if course.get("is_repeatable") is None:

                course["is_repeatable"] = False

            if course.get("course_level") is None:

                course["course_level"] = "unknown"

            #add those courses to the valid list
            try:

                validated = Course(**course)
                valid.append(validated)

            #exception incase of failure
            except Exception as e:

                print(f"Course {course.get("course_id")} still has invalid data: {e}")

        #return the valid list   
        return valid

    #exception in case of  failure
    except Exception as e:

        raise HTTPException(status_code = 500, detail = str(e)) from e

#does the same as all courses above but whe adding /(course_id) then it will show only that course
@app.get("/courses/{course_id}", response_model = Course)
def get_course(course_id: int):

    #gets the data of the class from supabase and sets it to the varible response
    try:
        response = (
            supabase
            .table("courses")
            .select("*")
            .eq("course_id", course_id)
            .execute()
        )

        #if not in data set tell user it does not exist
        if not response.data:
            raise HTTPException(status_code  = 404, detail =f"Course with ID {course_id} does not exist")

        #f any component is missing in the course populate it with default values
        course = response.data[0].copy()

        if course.get("credits") is None:

            course["credits"] = 0.0

        if course.get("is_repeatable") is None:

            course["is_repeatable"] = False

        if course.get("course_level") is None:

            course["course_level"] = "unknown"


        try:
            #returns course
            return Course(**course)

        #tells user of failure while stating the error
        except Exception as e:

            print(f"Course validation failed: {e}")

            raise HTTPException(status_code=500, detail="Course data does not match the required model") from e

    #raises missing course as a 404 error
    except HTTPException:
        raise

    #errors and tells user
    except Exception as e:

        raise HTTPException(status_code = 500, detail = f"falied to retrive courses") from e
