from sqlalchemy.orm import Session
from personal_finance_manager.schemas import SavingGoalCreate, SavingGoalUpdate
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


def update_saving_goal(db: Session, saving_goal_id: int, saving_goal: SavingGoalUpdate):
    db_saving_goal = db.query(SavingGoal).filter(SavingGoal.id == saving_goal_id).first()
    if db_saving_goal:
        update_data = saving_goal.dict(exclude_unset=True)
        for key, value in update_data.items():
            print(key, value)
            if key == 'category':
                category_id = category_service.get_category_id(db, value, db_saving_goal.user_id).id
                setattr(db_saving_goal, 'category_id', category_id)
                continue
            setattr(db_saving_goal, key, value)
        db.commit()
        db.refresh(db_saving_goal)
    return db_saving_goal


def delete_saving_goal(db: Session, saving_goal_id: int):
    db_saving_goal = db.query(SavingGoal).filter(SavingGoal.id == saving_goal_id).first()
    if db_saving_goal:
        db.delete(db_saving_goal)
        db.commit()
    return db_saving_goal


def update_saving_goal_progress(db: Session, user_id: int, category_id: int, amount: float):
    saving_goals = db.query(SavingGoal).filter(
        SavingGoal.user_id == user_id,
        SavingGoal.category_id == category_id
    ).all()

    for goal in saving_goals:
        goal.progress += amount
        if goal.progress > goal.target:
            goal.progress = goal.target

    db.commit()