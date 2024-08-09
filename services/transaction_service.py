from sqlalchemy.orm import Session
from personal_finance_manager.schemas import TransactionCreate, TransactionUpdate
from personal_finance_manager.models import Transaction
from personal_finance_manager.services import category_service


def create_transaction(db: Session, transaction: TransactionCreate, user_id: int):
    # Handle none category
    category_id = category_service.get_category_id(db, transaction.category, user_id).id
    db_transaction = Transaction(category_id=category_id, user_id=user_id, amount=transaction.amount,
                                 date=transaction.date, description=transaction.description,
                                 transaction_type=transaction.transaction_type)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def get_transaction(db: Session, transaction_id: int):
    return db.query(Transaction).filter(Transaction.id == transaction_id).first()


def get_user_transactions(db: Session, user_id: int):
    return db.query(Transaction).filter(Transaction.user_id == user_id).all()


def update_transaction(db: Session, transaction_id: int, transaction: TransactionUpdate):
    transaction_in_db = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if transaction_in_db:
        for key, value in transaction.dict().items():
            setattr(transaction_in_db, key, value)
        db.commit()
        db.refresh(transaction_in_db)
    return transaction_in_db


def delete_transaction(db: Session, transaction_id: int):
    transaction_in_db = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if transaction_in_db:
        db.delete(transaction_in_db)
        db.commit()
    return transaction_in_db
