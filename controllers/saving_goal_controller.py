from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from personal_finance_manager.database import get_db
from personal_finance_manager.schemas import SavingGoalCreate, UserInDB
from personal_finance_manager.services import saving_goal_service, category_service


def create_saving_goal(saving_goal: SavingGoalCreate, current_user: UserInDB, db: Session):
    category_id = category_service.get_category_id(db, saving_goal.category, current_user.id).id
    if not category_service.category_exists(db, category_id, current_user.id):
        raise HTTPException(status_code=400, detail="Invalid category for this user")
    return saving_goal_service.create_saving_goal(db, saving_goal, current_user.id)


def get_saving_goal(saving_goal_id: int, current_user: UserInDB, db: Session):
    saving_goal = saving_goal_service.get_saving_goal(db, saving_goal_id)
    if not saving_goal:
        raise HTTPException(status_code=404, detail="Saving goal not found")
    if saving_goal.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this saving goal")
    return saving_goal


def get_user_saving_goals(current_user: UserInDB, db: Session):
    return saving_goal_service.get_user_saving_goals(db, current_user.id)
