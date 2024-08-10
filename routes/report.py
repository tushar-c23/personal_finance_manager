from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from sqlalchemy.orm import Session
from personal_finance_manager.database import get_db
from personal_finance_manager.schemas import UserInDB
from personal_finance_manager.controllers import report_controller, user_controller

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/reports/monthly/{year}/{month}")
def get_monthly_report(
        year: int,
        month: int,
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    current_user = user_controller.get_current_user(token, db)
    return report_controller.get_monthly_report(year, month, current_user, db)


@router.get("/reports/yearly/{year}")
def get_yearly_report(
        year: int,
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    current_user = user_controller.get_current_user(token, db)
    return report_controller.get_yearly_report(year, current_user, db)
