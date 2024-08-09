from sqlalchemy.orm import Session
from personal_finance_manager.schemas import TransactionCreate, TransactionUpdate
from personal_finance_manager.models import Transaction


def create_transaction(db: Session, transaction: TransactionCreate, user_id: int):
    db_transaction = Transaction(**transaction.dict(), user_id=user_id)
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
