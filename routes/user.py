from fastapi import APIRouter, Depends
from personal_finance_manager.controllers import user_controller
from personal_finance_manager.schemas import UserInDB
from personal_finance_manager.database import get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/users/me", response_model=UserInDB)
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return user_controller.get_current_user(token, db)
