from sqlalchemy.orm import Session
from personal_finance_manager.schemas import TransactionCreate
from personal_finance_manager.models import Transaction


def create_transaction(db: Session, transaction: TransactionCreate, user_id: int):
    db_transaction = Transaction(**transaction.dict(), user_id=user_id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction