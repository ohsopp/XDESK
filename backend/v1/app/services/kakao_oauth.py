import os, httpx
from typing import Optional, Dict
from dotenv import load_dotenv

from v1.auth.oauth import BaseOAuth2, GetIdEmailError, process_login
from fastapi import HTTPException

load_dotenv()
KAKAO_AUTH_URL = "https://kauth.kakao.com/oauth/authorize"
KAKAO_TOKEN_API = "https://kauth.kakao.com/oauth/token"
KAKAO_PROFILE_ENDPOINT = "https://kapi.kakao.com/v2/user/me"
KAKAO_OAUTH_CLIENT_ID = os.getenv("KAKAO_OAUTH_CLIENT_ID")
KAKAO_OAUTH_CLIENT_SECRET = os.getenv("KAKAO_OAUTH_CLIENT_SECRET")
KAKAO_REDIRECT_URL = "https://i11a102.p.ssafy.io/oauth/kakao/login/callback"

class KakaoOAuth2(BaseOAuth2):
    display_name = "Kakao"

    def __init__(self):
        super().__init__(
            client_id=KAKAO_OAUTH_CLIENT_ID,
            client_secret=KAKAO_OAUTH_CLIENT_SECRET,
            authorize_endpoint=KAKAO_AUTH_URL,
            access_token_endpoint=KAKAO_TOKEN_API,
            platform="kakao"
        )

    # 카카오 유저 정보 조회
    async def get_profile(self, token: str) -> Dict[str, Optional[str]]:
        async with await self.get_httpx_client() as client:
            response = await client.get(
                KAKAO_PROFILE_ENDPOINT,
                headers={
                         "Authorization": f"Bearer {token}"},
            )

            if response.status_code >= 400:
                raise GetIdEmailError(response.json())
            
            account_info = response.json()
            kakao_account = account_info.get('kakao_account')

            return {
                "id": str(account_info.get('id')), 
                "email": kakao_account.get('email'),
                "name": kakao_account['profile']['nickname'],
            }

# access_token 요청 (카카오 유저 정보 조회에 사용됨) 
async def get_kakao_access_token(code: str, state: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            KAKAO_TOKEN_API,
            params={
                "grant_type": "authorization_code",
                "client_id": KAKAO_OAUTH_CLIENT_ID,
                "client_secret": KAKAO_OAUTH_CLIENT_SECRET,
                "code": code,
                "state": state,
                "redirect_url": KAKAO_REDIRECT_URL,
            },
        )

        if response.status_code >= 400:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        return response.json().get("access_token")

# db 업데이트 + 로그인 찐막 과정
async def process_kakao_login(code: str, state: str):
    return await process_login(
        "kakao",
        code,
        state,
        get_kakao_access_token,
        KakaoOAuth2().get_profile
    )