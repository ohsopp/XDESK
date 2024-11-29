from beanie import PydanticObjectId
from fastapi_users import schemas
from pydantic import EmailStr

class UserRead(schemas.BaseUser[PydanticObjectId]):
    pass

class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUserUpdate):
    pass