from fastapi import APIRouter, HTTPException, Depends
from v1.app.models.users_models import Desk
from v1.auth.jwt import verify_token, get_user, oauth2_scheme
from v1.app.database import db
from bson import ObjectId
import requests

xdesk_router = APIRouter()

@xdesk_router.get("/xdesk/index")
async def index_desk(token: str = Depends(oauth2_scheme)):
    user_id = verify_token(token)
    user = await get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"xdesk": user.get("xdesk", [])}

@xdesk_router.post("/xdesk/add/{desk_index}")
async def add_desk(desk_index: int, desk: Desk, token: str = Depends(oauth2_scheme)):
    if desk_index not in [1, 2, 3]:
        raise HTTPException(status_code=400, detail="Invalid desk index")

    if desk.desk_height is None or desk.stand_height is None:
        raise HTTPException(status_code=400, detail="desk_height and stand_height are required")

    user_id = verify_token(token)
    user = await get_user(user_id)

    desk_data = desk.model_dump()
    user_xdesks = user.get("xdesk", [None, None, None])

    if user_xdesks is None or len(user_xdesks) == 0:
        user_xdesks = [None, None, None]
    elif len(user_xdesks) < 3:
        user_xdesks.extend([None] * (3 - len(user_xdesks)))


    user_xdesks[desk_index - 1] = desk_data

    result = await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"xdesk": user_xdesks}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="desk not added or updated")
    return desk


@xdesk_router.put("/xdesk/update/{desk_index}")
async def update_desk(desk_index: int, desk: Desk, token: str = Depends(oauth2_scheme)):
    if desk_index not in [1, 2, 3]:
        raise HTTPException(status_code=400, detail="Invalid desk index")

    if desk.desk_height is None or desk.stand_height is None:
        raise HTTPException(status_code=400, detail="desk_height and stand_height are required")    
    
    user_id = verify_token(token)
    user = await get_user(user_id)
    user_xdesks = user.get("xdesk", [None, None, None])
    
    # Ensure desk exists at the given index
    if user_xdesks[desk_index - 1] is None:
        raise HTTPException(status_code=404, detail="Desk not found")
    
    # Update desk information
    user_xdesks[desk_index - 1] = desk.model_dump()
    
    result = await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"xdesk": user_xdesks}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Desk not updated")
    
    return desk

@xdesk_router.delete("/xdesk/delete/{desk_index}", status_code=204)
async def delete_desk(desk_index: int, token: str = Depends(oauth2_scheme)):
    if desk_index not in [1, 2, 3]:
        raise HTTPException(status_code=400, detail="Invalid desk index")
    
    user_id = verify_token(token)
    user = await get_user(user_id)
    user_xdesks = user.get("xdesk", [None, None, None])
    
    # Ensure desk exists at the given index
    if user_xdesks[desk_index - 1] is None:
        raise HTTPException(status_code=404, detail="Desk not found")
    
    # Remove desk
    user_xdesks[desk_index - 1] = None
    
    result = await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"xdesk": user_xdesks}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Desk not deleted")
    
    return None
