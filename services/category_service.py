from sqlalchemy.orm import Session
from personal_finance_manager.schemas import CategoryCreate
from personal_finance_manager.models import Category


def create_category(db: Session, category: CategoryCreate, user_id: int):
    db_category = Category(**category.dict(), user_id=user_id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_category_id(db: Session, category: str, user_id: int):
    return db.query(Category).filter(Category.name == category, Category.user_id == user_id).first()


def get_category_name_from_id(db: Session, category_id: int, user_id: int):
    return db.query(Category).filter(Category.id == category_id, Category.user_id == user_id).first()


def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()


def get_user_categories(db: Session, user_id: int):
    return db.query(Category).filter(Category.user_id == user_id).all()
