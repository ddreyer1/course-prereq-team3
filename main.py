from fastapi import FastAPI
from database.init_db import supabase
from catalog.Classes import router as course_route

app = FastAPI()

app.include_router(course_route)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


# tests db connection
@app.get("/db-health")
def check_db():
    try:
        response = supabase.table("courses").select("*").limit(1).execute()
        if response:
            return {"status": "OK", "response": "recieved"}
        # if there is no exception we should always recieve a response
        return {"status": "OK", "response": "not recieved"}
    except Exception as e:
        return {"message": f"Supabase health check failed: {e}"}
