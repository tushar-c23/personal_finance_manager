from personal_finance_manager.schemas import TransactionCreate
from sqlalchemy.orm import Session
from personal_finance_manager.services import transaction_service
from personal_finance_manager.schemas import UserInDB


def create_transaction(transaction: TransactionCreate, current_user: UserInDB, db: Session):
    return transaction_service.create_transaction(db, transaction, current_user.id)
