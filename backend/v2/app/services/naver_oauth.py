import os, httpx
from v2.auth.oauth import BaseOAuth2, GetIdEmailError, process_login
from typing import Optional, Dict
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()
NAVER_AUTH_URL = "https://nid.naver.com/oauth2.0/authorize"
NAVER_TOKEN_API = "https://nid.naver.com/oauth2.0/token"
NAVER_PROFILE_ENDPOINT = "https://openapi.naver.com/v1/nid/me"
NAVER_OAUTH_CLIENT_ID = os.getenv("NAVER_OAUTH_CLIENT_ID")
NAVER_OAUTH_CLIENT_SECRET = os.getenv("NAVER_OAUTH_CLIENT_SECRET")
NAVER_REDIRECT_URL = "https://i11a102.p.ssafy.io/oauth/naver/login/callback/"

class NaverOAuth2(BaseOAuth2):
    display_name = "Naver"

    def __init__(self):
        super().__init__(
            client_id=NAVER_OAUTH_CLIENT_ID,
            client_secret=NAVER_OAUTH_CLIENT_SECRET,
            authorize_endpoint=NAVER_AUTH_URL,
            access_token_endpoint=NAVER_TOKEN_API,
            platform="naver"
        )

    # 네이버 유저 정보 조회
    async def get_profile(self, token: str) -> Dict[str, Optional[str]]:
        async with await self.get_httpx_client() as client:

            response = await client.get(
                NAVER_PROFILE_ENDPOINT,
                headers={
                         "Authorization": f"Bearer {token}"
                },
            )

            if response.status_code >= 400:
                raise GetIdEmailError(response.json())
            
            account_info = response.json()
            naver_account = account_info.get('response')

            return {
                "id": str(naver_account.get('id')),
                "email": naver_account.get('email'),
                "name": naver_account.get('name')
            }
        
# 네이버 access_token 요청 / 유저 정보 조회에 사용됨
async def get_naver_access_token(code: str, state: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            NAVER_TOKEN_API,
            params={
                "grant_type": "authorization_code",
                "client_id": NAVER_OAUTH_CLIENT_ID,
                "client_secret": NAVER_OAUTH_CLIENT_SECRET,
                "code": code,
                "state": state,
                "redirect_uri": NAVER_REDIRECT_URL,
            },
        )

        if response.status_code >= 400:
            raise HTTPException(status_code=response.status_code, detail=response.json())

        return response.json().get("access_token")

# 유저 정보 조회한 걸 토대로 db 업데이트 + 로그인 찐막 과정
async def process_naver_login(code: str, state: str):
    return await process_login(
        "naver",
        code,
        state,
        get_naver_access_token,
        NaverOAuth2().get_profile,
    )