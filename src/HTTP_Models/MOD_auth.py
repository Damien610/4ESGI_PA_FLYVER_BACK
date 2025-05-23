from pydantic import BaseModel
class UserCreate(BaseModel):
    email: str
    password: str
    is_admin: bool = False
    first_name: str
    name: str


class UserLogin(BaseModel):
    email: str
    password: str