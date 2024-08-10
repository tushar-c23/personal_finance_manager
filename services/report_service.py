from sqlalchemy.orm import Session
from datetime import date, datetime
from calendar import monthrange
from sqlalchemy import func, and_
from personal_finance_manager.models import Transaction, Category, SavingGoal



def get_monthly_report(db: Session, user_id: int, year: int, month: int):
    start_date = date(year, month, 1)
    _, last_day = monthrange(year, month)
    end_date = date(year, month, last_day)

    return get_report(db, user_id, start_date, end_date)


def get_yearly_report(db: Session, user_id: int, year: int):
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)

    return get_report(db, user_id, start_date, end_date)


def get_report(db: Session, user_id: int, start_date: date, end_date: date):
    # Get total income (credit transactions)
    income = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == user_id,
        Transaction.transaction_type == 'credit',
        Transaction.date.between(start_date, end_date)
    ).scalar() or 0

    # Get total expenses (debit transactions)
    expenses = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == user_id,
        Transaction.transaction_type == 'debit',
        Transaction.date.between(start_date, end_date)
    ).scalar() or 0

    # Get savings (transactions with categories associated with saving goals)
    saving_categories = db.query(SavingGoal.category_id).filter(SavingGoal.user_id == user_id).distinct()
    savings = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == user_id,
        Transaction.category_id.in_(saving_categories),
        Transaction.transaction_type == 'credit',
        Transaction.date.between(start_date, end_date)
    ).scalar() or 0

    return {
        "income": income,
        "expenses": expenses,
        "savings": savings,
        "net": income - expenses,
        "start_date": start_date,
        "end_date": end_date
    }