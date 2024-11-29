from typing import List, Optional
from pydantic import Field, EmailStr, BaseModel
from beanie import Document, PydanticObjectId  
from fastapi_users.db import BaseOAuthAccount

# oauth_name, access_token, refresh_token, expires_at
class OAuthAccount(BaseOAuthAccount):
    pass

class Desk(BaseModel):
    # name: Optional[str] = Field(default=None)
    desk_height: Optional[int] = None
    stand_height: Optional[int] = None

class User(Document):

    class Meta:
        collection = 'users'

    user_id: PydanticObjectId = Field(alias="_id")
    email: Optional[EmailStr] = None
    user_id_platform: str
    name: str
    platform: str
    motion_number: int = None
    xdesk: List[Optional[Desk]] = Field(default_factory=lambda: [None, None, None])
