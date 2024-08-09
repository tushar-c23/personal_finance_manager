from personal_finance_manager.schemas import CategoryCreate, UserInDB
from sqlalchemy.orm import Session
from personal_finance_manager.services import category_service


def create_category(category: CategoryCreate, current_user: UserInDB, db: Session):
    return category_service.create_category(db, category, current_user.id)


def get_category_name_from_id(category_id: int, current_user: UserInDB, db: Session):
    return category_service.get_category_name_from_id(db, category_id, current_user.id).name