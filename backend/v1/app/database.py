import os
from dotenv import load_dotenv
import motor.motor_asyncio

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)
db = client.get_database("ssafy")
users_collection = db.get_collection("users")
