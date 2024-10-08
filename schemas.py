from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import date


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    name: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserInDB(BaseModel):
    id: int
    username: str
    email: EmailStr
    name: str

    class Config:
        orm_mode = True
        from_attributes = True


class TransactionType(str, Enum):
    debit = "debit"
    credit = "credit"


class TransactionBase(BaseModel):
    amount: float
    category: str
    description: str
    transaction_type: TransactionType
    date: date


class TransactionCreate(TransactionBase):
    # Derive all from transaction base, userid will be taken separately
    pass


class TransactionUpdate(TransactionBase):
    # Derive all from transaction base, userid will be taken separately
    pass


class Transaction(TransactionBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class SavingGoalBase(BaseModel):
    name: str
    target: float
    category: str


class SavingGoalCreate(SavingGoalBase):
    pass


class SavingGoalUpdate(SavingGoalBase):
    pass


class SavingGoal(SavingGoalBase):
    id: int
    user_id: int
    progress: float

    class Config:
        orm_mode = True
