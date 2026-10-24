from fastapi import FastAPI
from database.init_db import supabase

app = FastAPI()

#initializes a connection to the database, prints the current connection status
def main():
    print("Supabase initialized:", supabase is not None)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    main()
