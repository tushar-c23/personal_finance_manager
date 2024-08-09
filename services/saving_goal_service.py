from sqlalchemy.orm import Session
from personal_finance_manager.schemas import SavingGoalCreate
from personal_finance_manager.models import SavingGoal
from personal_finance_manager.services import category_service


def create_saving_goal(db: Session, saving_goal: SavingGoalCreate, user_id: int):
    category_id = category_service.get_category_id(db, saving_goal.category, user_id).id
    db_saving_goal = SavingGoal(name=saving_goal.name, target=saving_goal.target, user_id=user_id, progress=0.0,
                                category_id=category_id)
    db.add(db_saving_goal)
    db.commit()
    db.refresh(db_saving_goal)
    return db_saving_goal


def get_saving_goal(db: Session, saving_goal_id: int):
    return db.query(SavingGoal).filter(SavingGoal.id == saving_goal_id).first()


def get_user_saving_goals(db: Session, user_id: int):
    return db.query(SavingGoal).filter(SavingGoal.user_id == user_id).all()
