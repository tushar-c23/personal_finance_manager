from pydantic import BaseModel, EmailStr
from enum import Enum


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


class TransactionType(str, Enum):
    debit = "debit"
    credit = "credit"


class TransactionBase(BaseModel):
    amount: float
    category: str
    description: str
    transaction_type: TransactionType


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
