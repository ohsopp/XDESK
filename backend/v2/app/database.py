import os
from dotenv import load_dotenv
import motor.motor_asyncio

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# social_login_db
database_client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, readPreference="secondaryPreferred"
    )
db = database_client.get_database("ssafy")
users_collection = db.get_collection("users")

# region_facial_login_db
MONGOS_URL = os.getenv("MONGOS_URL")
mongos_client = motor.motor_asyncio.AsyncIOMotorClient(
    MONGOS_URL, readPreference="secondaryPreferred"
    )

# mongos db 사용법
# async def store_data():
#     mongos_db = mongos_client["ssafy"]
#     mongos_collection = mongos_db["face_gesture_info"]
#     
#     ip 첫 세 숫자를 기준으로 샤딩된 db로 분배됨/ 받은 데이터는 item
#     ip_first_octet = int(item["ip_address"].split('.')[0])
#     document = {
#         "__id": 소셜로그인 db에서 정해진 id로
#         "ip_first_octet": ip_first_octet,
#         "face_data": item["face_data"],
#         "gesture_data": item["gesture_data"]
#     }
#     result = await mongos_collection.insert_one(document)
#     print(f"Inserted document with ID: {result.inserted_id}")