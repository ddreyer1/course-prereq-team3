# this is the code to actually initialize the database
# must include valid a .env file. See .env.example for reference
from supabase import create_client, Client
from dotenv import load_dotenv
import os


def init():
    # get the values from the .env file
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    # checks if a valid key and url are used
    if not url or not key:
        raise RuntimeError("Missing URL or KEY")

    try:
        client: Client = create_client(url, key)
    except Exception as e:
        raise RuntimeError(f"Failed to creaet a supabase client: {e}")

    # return initialized client
    return client


load_dotenv()
supabase: Client = init()
