from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    name: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserInDB(BaseModel):
    username: str
    email: EmailStr
    name: str
