from personal_finance_manager.schemas import TransactionCreate, TransactionUpdate
from sqlalchemy.orm import Session
from personal_finance_manager.services import transaction_service
from personal_finance_manager.schemas import UserInDB
from fastapi import HTTPException


def create_transaction(transaction: TransactionCreate, current_user: UserInDB, db: Session):
    #Check category here
    return transaction_service.create_transaction(db, transaction, current_user.id)


def get_transaction(transaction_id: int, current_user: UserInDB, db: Session):
    transaction = transaction_service.get_transaction(db, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    if transaction.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this transaction")
    return transaction


def get_user_transactions(current_user: UserInDB, db: Session):
    return transaction_service.get_user_transactions(db, current_user.id)


def update_transaction(transaction_id: int, transaction: TransactionUpdate, current_user: UserInDB, db: Session):
    transaction_in_db = transaction_service.get_transaction(db, transaction_id)
    if not transaction_in_db:
        raise HTTPException(status_code=404, detail="Transaction not found")
    if transaction_in_db.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this transaction")
    return transaction_service.update_transaction(db, transaction_id, transaction, current_user.id)


def delete_transaction(transaction_id: int, current_user: dict, db: Session):
    transaction_in_db = transaction_service.get_transaction(db, transaction_id)
    if not transaction_in_db:
        raise HTTPException(status_code=404, detail="Transaction not found")
    if transaction_in_db.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this transaction")
    return transaction_service.delete_transaction(db, transaction_id)