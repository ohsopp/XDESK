import httpx
from bson import ObjectId
from fastapi.responses import JSONResponse
from v1.app.database import users_collection
from v1.auth.jwt import create_jwt_token
from fastapi import HTTPException

class GetIdEmailError(Exception):
    pass

class BaseOAuth2:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        authorize_endpoint: str,
        access_token_endpoint: str,
        platform: str,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.authorize_endpoint = authorize_endpoint
        self.access_token_endpoint = access_token_endpoint
        self.platform = platform

    def get_authorization_url(self, redirect_uri: str) -> str:
        return f"{self.authorize_endpoint}?response_type=code&client_id={self.client_id}&redirect_uri={redirect_uri}&state=RANDOM_STATE"

    async def get_httpx_client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient()
    
async def process_login(platform: str, code: str, state: str, get_access_token, fetch_user_profile):
    access_token = await get_access_token(code, state)

    user_info = await fetch_user_profile(access_token)

    db_user = await users_collection.find_one({"user_id_platform": user_info["id"]})

    if db_user:
        db_user["_id"] = str(db_user["_id"])
        response = JSONResponse(content=db_user)
        jwt_token = create_jwt_token(db_user)
        print('기존 회원 db_user: ', db_user)
                
    else:
        new_user = {
            "_id": ObjectId(),
            "user_id_platform": user_info["id"],
            "email": user_info["email"],
            "platform": platform,
            "name": user_info["name"],
            "motion_number": None,
            "xdesk": [] 
        }
        await users_collection.insert_one(new_user)
        new_user["_id"] = str(new_user["_id"])
        response = JSONResponse(content=new_user)
        jwt_token = create_jwt_token(new_user)

    return {"jwt_token": jwt_token, "response": response}

async def process_face_login(user_id: str, motion_number: int):
    user_id = ObjectId(user_id)
    db_user = await users_collection.find_one({"_id": user_id})

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user["motion_number"] != motion_number:
        raise HTTPException(status_code=401, detail="Invalid motion password")

    # response = JSONResponse(content=db_user)
    db_user["_id"] = str(db_user["_id"])
    jwt_token = create_jwt_token(db_user)

    # return {"jwt_token": jwt_token, "response": response}
    return {"jwt_token": jwt_token, "response": db_user}