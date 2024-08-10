from fastapi import HTTPException
from sqlalchemy.orm import Session
from personal_finance_manager.schemas import UserInDB
from personal_finance_manager.services import report_service


def get_monthly_report(year: int, month: int, current_user: UserInDB, db: Session):
    if year < 1900 or year > 2100 or month < 1 or month > 12:
        raise HTTPException(status_code=400, detail="Invalid year or month")
    return report_service.get_monthly_report(db, current_user.id, year, month)


def get_yearly_report(year: int, current_user: UserInDB, db: Session):
    if year < 1900 or year > 2100:
        raise HTTPException(status_code=400, detail="Invalid year")
    return report_service.get_yearly_report(db, current_user.id, year)
