from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from personal_finance_manager.database import get_db
from personal_finance_manager.controllers import user_controller, category_controller
from personal_finance_manager.schemas import Category, CategoryCreate, UserInDB
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/category/", response_model=Category)
def create_category(
        category: CategoryCreate,
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    current_user = user_controller.get_current_user(token, db)
    return category_controller.create_category(category, current_user, db)
