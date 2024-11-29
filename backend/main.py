from fastapi import FastAPI, HTTPException
from v1.app.routers.users_routers import social_router, auth_router
from v1.app.routers.xdesk_routers import xdesk_router
from v2.app.routers.users_routers import social_router, auth_router
from v2.app.routers.xdesk_routers import xdesk_router

from v2.app.database import database_client, mongos_client
from v2.app.config import cors_middleware

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# DB 연결 확인용
from bson import json_util
import json
def bson_to_json(data):
    return json.loads(json_util.dumps(data))
@app.get("/ping/")
async def ping():
    try:
        central_result = await database_client["ssafy"].command("ping")
        mongos_result = await mongos_client["ssafy"].command("ping")
        return {
            "중앙 DB": bson_to_json(central_result),
            "지역 DB": bson_to_json(mongos_result),
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

cors_middleware(app)


routers_v1 = [
    (social_router, {"tags": ["oauth"]}),
    (auth_router, {"tags": ["accounts"]}),
    (xdesk_router, {"tags": ["xdesk"]}),
]

routers_v2 = [
    (social_router, {"tags": ["oauth"]}),
    (auth_router, {"tags": ["accounts"]}),
    (xdesk_router, {"tags": ["xdesk"]}),
]

for router, kwargs in routers_v1:
    app.include_router(router=router, prefix="/api/v1", **kwargs)

for router, kwargs in routers_v2:
    app.include_router(router=router, prefix="/api/v2", **kwargs)