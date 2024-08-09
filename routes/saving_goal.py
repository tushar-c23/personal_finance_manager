from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from personal_finance_manager.database import get_db
from personal_finance_manager.schemas import SavingGoalCreate, SavingGoal, SavingGoalUpdate
from personal_finance_manager.schemas import UserInDB
from personal_finance_manager.controllers import saving_goal_controller, user_controller, category_controller
from fastapi.security import OAuth2PasswordBearer
from typing import List

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/saving-goal/", response_model=SavingGoal)
def create_saving_goal(
        saving_goal: SavingGoalCreate,
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    current_user = user_controller.get_current_user(token, db)
    created_saving_goal = saving_goal_controller.create_saving_goal(saving_goal, current_user, db)
    category = category_controller.get_category_name_from_id(created_saving_goal.category_id, current_user, db)
    resp_saving_goal = SavingGoal(name=created_saving_goal.name, target=created_saving_goal.target,
                                  progress=created_saving_goal.progress, category=category, id=created_saving_goal.id,
                                  user_id=created_saving_goal.user_id)
    return resp_saving_goal


@router.get("/saving-goals/", response_model=List[SavingGoal])
def read_saving_goals(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    current_user = user_controller.get_current_user(token, db)
    saving_goal_arr_in_db = saving_goal_controller.get_user_saving_goals(current_user, db)
    resp_saving_goal_arr: List[SavingGoal] = []
    for saving_goal in saving_goal_arr_in_db:
        category = category_controller.get_category_name_from_id(saving_goal.category_id, current_user, db)
        resp_saving_goal = SavingGoal(name=saving_goal.name, target=saving_goal.target,
                                      progress=saving_goal.progress, category=category, id=saving_goal.id,
                                      user_id=saving_goal.user_id)
        resp_saving_goal_arr.append(resp_saving_goal)
    return resp_saving_goal_arr


@router.get("/saving-goals/{saving_goal_id}", response_model=SavingGoal)
def read_saving_goal(
        saving_goal_id: int,
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    current_user = user_controller.get_current_user(token, db)
    saving_goal_in_db = saving_goal_controller.get_saving_goal(saving_goal_id, current_user, db)
    category = category_controller.get_category_name_from_id(saving_goal_in_db.category_id, current_user, db)
    resp_saving_goal = SavingGoal(name=saving_goal_in_db.name, target=saving_goal_in_db.target,
                                  progress=saving_goal_in_db.progress, category=category, id=saving_goal_in_db.id,
                                  user_id=saving_goal_in_db.user_id)
    return resp_saving_goal


@router.put("/saving-goals/{saving_goal_id}", response_model=SavingGoal)
def update_saving_goal(
        saving_goal_id: int,
        saving_goal: SavingGoalUpdate,
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    current_user = user_controller.get_current_user(token, db)
    saving_goal_in_db = saving_goal_controller.update_saving_goal(saving_goal_id, saving_goal, current_user, db)
    category = category_controller.get_category_name_from_id(saving_goal_in_db.category_id, current_user, db)
    resp_saving_goal = SavingGoal(name=saving_goal_in_db.name, target=saving_goal_in_db.target,
                                  progress=saving_goal_in_db.progress, category=category, id=saving_goal_in_db.id,
                                  user_id=saving_goal_in_db.user_id)
    return resp_saving_goal


@router.delete("/saving-goals/{saving_goal_id}", response_model=SavingGoal)
def delete_saving_goal(
        saving_goal_id: int,
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    current_user = user_controller.get_current_user(token, db)
    saving_goal_in_db = saving_goal_controller.delete_saving_goal(saving_goal_id, current_user, db)
    category = category_controller.get_category_name_from_id(saving_goal_in_db.category_id, current_user, db)
    resp_saving_goal = SavingGoal(name=saving_goal_in_db.name, target=saving_goal_in_db.target,
                                  progress=saving_goal_in_db.progress, category=category, id=saving_goal_in_db.id,
                                  user_id=saving_goal_in_db.user_id)
    return resp_saving_goal
