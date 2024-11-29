import os
import random
from dotenv import load_dotenv
from fastapi import APIRouter, Request, HTTPException, Depends, Response,status    
from fastapi.responses import RedirectResponse, StreamingResponse

from v1.app.services.naver_oauth import process_naver_login
from v1.app.services.kakao_oauth import process_kakao_login
from v1.auth.oauth import process_face_login
from v1.app.database import db
from v1.auth.jwt import verify_token, get_user_logs, get_user, save_user_log, oauth2_scheme
from v2.app.services.user_log_services import logs_to_graph
from v2.app.models.users_models import LogoutRequest
from bson import ObjectId
from urllib.parse import quote

from io import BytesIO
from pydantic import Field, EmailStr, BaseModel

social_router = APIRouter()
auth_router = APIRouter()
motion_index_list = [3, 9, 11, 13, 14, 18, 22, 25, 32, 33]

load_dotenv()
NAVER_OAUTH_CLIENT_ID = os.getenv("NAVER_OAUTH_CLIENT_ID")
KAKAO_OAUTH_CLIENT_ID = os.getenv("KAKAO_OAUTH_CLIENT_ID")
KAKAO_REDIRECT_URL = "http://i11a102.p.ssafy.io/api/v1/oauth/kakao/login/callback"
NAVER_REDIRECT_URL = "http://i11a102.p.ssafy.io/api/v1/oauth/naver/login/callback/"

@social_router.get("/oauth/naver/login")
def get_naver_qr_login_url():
    authorize_url = (
        f"https://nid.naver.com/oauth2.0/authorize?"
        f"response_type=code"
        f"&state=RANDOM_STATE"
        f"&client_id={NAVER_OAUTH_CLIENT_ID}"
        f"&redirect_uri={quote(NAVER_REDIRECT_URL)}"
    )
    qr_login_url = (
        f"https://nid.naver.com/nidlogin.login?mode=qrcode"
        f"&url={quote(authorize_url)}"
        f"&locale=ko_KR"
        f"&svctype=1"
    )
    return RedirectResponse(qr_login_url)

@social_router.get("/oauth/naver/login/callback")
async def naver_callback(code: str, state: str):
    try:
        return await process_naver_login(code, state)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

@social_router.get("/oauth/kakao/login")
async def kakao_login(request: Request):
    redirect_uri = request.url_for("kakao_callback")
    authorize_endpoint = (
        f"https://accounts.kakao.com/qr_login/?append_stay_signed_in=false&continue="
        f"https%3A%2F%2Fkauth.kakao.com%2Foauth%2Fauthorize%3Fresponse_type%3Dcode%26"
        f"redirect_uri%3D{redirect_uri}%26state%3DRANDOM_STATE%26through_account%3Dtrue%26"
        f"client_id%3D{KAKAO_OAUTH_CLIENT_ID}&lang=ko&stay_signed_in=false#main"
    )

    return RedirectResponse(authorize_endpoint)

@social_router.get("/oauth/kakao/login/callback")
async def kakao_callback(code: str, state: str):
    try:
        result = await process_kakao_login(code, state)
        return result
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

@auth_router.post("/graph")
async def make_graph(token: str = Depends(oauth2_scheme)):
    user_id = verify_token(token)
    
    user_logs, log_count = await get_user_logs(user_id)
    
    graph_plt = await logs_to_graph(user_logs)
    
    if log_count <= 3:
        image_path = os.path.join(os.getcwd(), f'{log_count}data.png')
        print(f"Looking for image at: {image_path}")

        with open(image_path, "rb") as image_file:
            buf = BytesIO(image_file.read())
            buf.seek(0)
            return StreamingResponse(buf, media_type="image/png")

    buf = BytesIO()
    graph_plt.savefig(buf, format='png', bbox_inches='tight')
    graph_plt.close()
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

@auth_router.post("/logout")
async def logout(request: LogoutRequest, token: str = Depends(oauth2_scheme)):
    user_id = verify_token(token)

    result = await save_user_log(user_id, request.posture_percentage)
    
    if result == 204:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to save user log.")


@auth_router.post("/auth/face/login")
async def face_login(user_id: str, motion_number: int):
    try:
        result = await process_face_login(user_id, motion_number)
        return result
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

@auth_router.post("/auth/get-motion")
async def get_motion_number(token: str = Depends(oauth2_scheme)):
    random_number = random.choice(motion_index_list)
    
    user_id = verify_token(token)
    user = await get_user(user_id)

    result = await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"motion_number": random_number}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Motion number not updated")

    return {"motion_number": random_number}


