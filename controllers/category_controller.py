from personal_finance_manager.schemas import CategoryCreate, UserInDB, CategoryUpdate
from sqlalchemy.orm import Session
from personal_finance_manager.services import category_service, transaction_service
from fastapi import HTTPException


def create_category(category: CategoryCreate, current_user: UserInDB, db: Session):
    if category_service.category_name_exists_for_user(db, category.name, current_user.id):
        raise HTTPException(status_code=400, detail="Category with this name already exists")
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


def update_category(category_id: int, category: CategoryUpdate, current_user: UserInDB, db: Session):
    db_category = category_service.get_category(db, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    if db_category.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this category")
    return category_service.update_category(db, category_id, category)


def delete_category(category_id: int, current_user: UserInDB, db: Session):
    if transaction_service.get_transactions_by_category(db, current_user.id, category_id) is not None:
        raise HTTPException(status_code=400, detail="Cannot delete category with transactions")
    db_category = category_service.get_category(db, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    if db_category.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this category")
    return category_service.delete_category(db, category_id)
