from personal_finance_manager.schemas import CategoryCreate, UserInDB
from sqlalchemy.orm import Session
from personal_finance_manager.services import category_service
from fastapi import HTTPException


def create_category(category: CategoryCreate, current_user: UserInDB, db: Session):
    return category_service.create_category(db, category, current_user.id)


def get_category_name_from_id(category_id: int, current_user: UserInDB, db: Session):
    return category_service.get_category_name_from_id(db, category_id, current_user.id).name


def get_category(category_id: int, current_user: UserInDB, db: Session):
    category = category_service.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    if category.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this category")
    return category


def get_user_categories(current_user: UserInDB, db: Session):
    return category_service.get_user_categories(db, current_user.id)
