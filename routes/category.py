from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from personal_finance_manager.database import get_db
from personal_finance_manager.controllers import user_controller, category_controller
from personal_finance_manager.schemas import Category, CategoryCreate, UserInDB, CategoryUpdate
from fastapi.security import OAuth2PasswordBearer
from typing import List

router = APIRouter(prefix="/categories")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/", response_model=Category)
def create_category(
        category: CategoryCreate,
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    current_user = user_controller.get_current_user(token, db)
    return category_controller.create_category(category, current_user, db)


@router.get("/", response_model=List[Category])
def read_categories(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    current_user = user_controller.get_current_user(token, db)
    return category_controller.get_user_categories(current_user, db)


@router.get("/{category_id}", response_model=Category)
def read_category(
        category_id: int,
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    current_user = user_controller.get_current_user(token, db)
    return category_controller.get_category(category_id, current_user, db)


@router.put("/{category_id}", response_model=Category)
def update_category(
        category_id: int,
        category: CategoryUpdate,
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    current_user = user_controller.get_current_user(token, db)
    return category_controller.update_category(category_id, category, current_user, db)


@router.delete("/{category_id}", response_model=Category)
def delete_category(
        category_id: int,
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    current_user = user_controller.get_current_user(token, db)
    return category_controller.delete_category(category_id, current_user, db)
