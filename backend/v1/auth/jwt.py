import jwt, os
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from dotenv import load_dotenv
from v1.app.database import db
from bson import ObjectId
from pymongo.errors import PyMongoError

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

# ALGORITHM = os.getenv("ALGORITHM")

def create_jwt_token(user_info):
    payload = {
        "sub": str(user_info["_id"]), # 몽고DB가 부여한 사용자 PK
        "exp": datetime.now(timezone.utc) + timedelta(hours = 1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256") 
    return token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="JWT 인증 에러",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
async def get_user(user_id: str):
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def get_user_logs(user_id: str):
    user = await get_user(user_id)

    user_logs = await db.user_log.find({"user_id": ObjectId(user_id)}).to_list(None)

    if not user_logs: # 기존 로그가 없는 경우, 첫 로그인일 뿐 오류가 아님
        user_logs = []
    log_count = len(user_logs)

    return user_logs, log_count 

async def save_user_log(user_id: str, posture_percentage: int):
    user = await get_user(user_id)

    log_datetime_utc = datetime.now(timezone.utc)
    new_log = {
        'user_id': ObjectId(user_id),
        'date': log_datetime_utc,
        'posture_percentage': posture_percentage
    }

    try:
        await db.user_log.insert_one(new_log)
    except PyMongoError as e:
        raise Exception("Failed to save user log.") from e
    
    return 204