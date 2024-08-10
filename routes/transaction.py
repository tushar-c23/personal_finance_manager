from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from personal_finance_manager.schemas import Transaction, TransactionCreate, TransactionUpdate
from personal_finance_manager.database import get_db
from personal_finance_manager.controllers import user_controller, transaction_controller, category_controller
from typing import List


router = APIRouter(prefix="/transactions")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/", response_model=Transaction)
def create_transaction(
        transaction: TransactionCreate,
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    current_user = user_controller.get_current_user(token, db)
    created_transaction = transaction_controller.create_transaction(transaction, current_user, db)
    category = category_controller.get_category_name_from_id(created_transaction.category_id, current_user, db)
    resp_transaction = Transaction(amount=created_transaction.amount, date=created_transaction.date,
                                   description=created_transaction.description,
                                   transaction_type=created_transaction.transaction_type,
                                   category=category, id = created_transaction.id,
                                   user_id = created_transaction.user_id)
    return resp_transaction


@router.get("/", response_model=List[Transaction])
def read_transactions(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    current_user = user_controller.get_current_user(token, db)
    transaction_list = transaction_controller.get_user_transactions(current_user, db)
    resp_transactions = []
    for transaction in transaction_list:
        category = category_controller.get_category_name_from_id(transaction.category_id, current_user, db)
        resp_transaction = Transaction(amount=transaction.amount, date=transaction.date,
                                       description=transaction.description,
                                       transaction_type=transaction.transaction_type,
                                       category=category, id=transaction.id,
                                       user_id=transaction.user_id)
        resp_transactions.append(resp_transaction)
    return resp_transactions


@router.get("/{transaction_id}", response_model=Transaction)
def read_transaction(
    transaction_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    current_user = user_controller.get_current_user(token, db)
    transaction_in_db = transaction_controller.get_transaction(transaction_id, current_user, db)
    category = category_controller.get_category_name_from_id(transaction_in_db.category_id, current_user, db)
    resp_transaction = Transaction(amount=transaction_in_db.amount, date=transaction_in_db.date,
                                      description=transaction_in_db.description,
                                      transaction_type=transaction_in_db.transaction_type,
                                      category=category, id=transaction_in_db.id,
                                      user_id=transaction_in_db.user_id)
    return resp_transaction


@router.put("/{transaction_id}", response_model=Transaction)
def update_transaction(
    transaction_id: int,
    transaction: TransactionUpdate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    current_user = user_controller.get_current_user(token, db)
    modified_transaction = transaction_controller.update_transaction(transaction_id, transaction, current_user, db)
    category = category_controller.get_category_name_from_id(modified_transaction.category_id, current_user, db)
    resp_transaction = Transaction(amount=modified_transaction.amount, date=modified_transaction.date,
                                   description=modified_transaction.description,
                                   transaction_type=modified_transaction.transaction_type,
                                   category=category, id=modified_transaction.id,
                                   user_id=modified_transaction.user_id)
    return resp_transaction


@router.delete("/{transaction_id}", response_model=Transaction)
def delete_transaction(
    transaction_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    current_user = user_controller.get_current_user(token, db)
    deleted_transaction = transaction_controller.delete_transaction(transaction_id, current_user, db)
    category = category_controller.get_category_name_from_id(deleted_transaction.category_id, current_user, db)
    resp_transaction = Transaction(amount=deleted_transaction.amount, date=deleted_transaction.date,
                                   description=deleted_transaction.description,
                                   transaction_type=deleted_transaction.transaction_type,
                                   category=category, id=deleted_transaction.id,
                                   user_id=deleted_transaction.user_id)
    return resp_transaction