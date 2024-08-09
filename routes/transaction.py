from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from personal_finance_manager.schemas import Transaction, TransactionCreate, TransactionUpdate
from personal_finance_manager.database import get_db
from personal_finance_manager.controllers import user_controller, transaction_controller
from typing import List


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/transaction/", response_model=Transaction)
def create_transaction(
        transaction: TransactionCreate,
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    current_user = user_controller.get_current_user(token, db)
    return transaction_controller.create_transaction(transaction, current_user, db)


@router.get("/transactions/", response_model=List[Transaction])
def read_transactions(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    current_user = user_controller.get_current_user(token, db)
    return transaction_controller.get_user_transactions(current_user, db)


@router.get("/transaction/{transaction_id}", response_model=Transaction)
def read_transaction(
    transaction_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    current_user = user_controller.get_current_user(token, db)
    return transaction_controller.get_transaction(transaction_id, current_user, db)


@router.put("/transaction/{transaction_id}", response_model=TransactionUpdate)
def update_transaction(
    transaction_id: int,
    transaction: TransactionUpdate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    current_user = user_controller.get_current_user(token, db)
    return transaction_controller.update_transaction(transaction_id, transaction, current_user, db)


@router.delete("/transaction/{transaction_id}", response_model=Transaction)
def delete_transaction(
    transaction_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    current_user = user_controller.get_current_user(token, db)
    return transaction_controller.delete_transaction(transaction_id, current_user, db)