from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from .database import Base
from sqlalchemy.orm import relationship
import enum


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)

    transactions = relationship("Transaction", back_populates="user")


class TransactionType(str, enum.Enum):
    debit = "debit"
    credit = "credit"


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    category = Column(String)
    description = Column(String)
    transaction_type = Column(Enum(TransactionType))

    user = relationship("User", back_populates="transactions")