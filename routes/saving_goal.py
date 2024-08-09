from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from personal_finance_manager.database import get_db
from personal_finance_manager.schemas import SavingGoalCreate, SavingGoal
from personal_finance_manager.schemas import UserInDB
from personal_finance_manager.controllers import saving_goal_controller, user_controller, category_controller
from fastapi.security import OAuth2PasswordBearer

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