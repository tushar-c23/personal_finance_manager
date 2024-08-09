from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from personal_finance_manager.database import get_db
from personal_finance_manager.services import user_service, auth_service
from personal_finance_manager.schemas import UserInDB
from jose import jwt, JWTError


def get_current_user(token: str, db: Session):
    try:
        payload = jwt.decode(token, auth_service.SECRET_KEY, algorithms=[auth_service.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    user = user_service.get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserInDB(username=user.username, email=user.email, name=user.name)