from sqlalchemy.orm import Session
from datetime import date, datetime
from calendar import monthrange
from sqlalchemy import func, and_
from personal_finance_manager.models import Transaction, Category, SavingGoal
import matplotlib.pyplot as plt
import io
import base64


def get_monthly_report(db: Session, user_id: int, year: int, month: int):
    start_date = date(year, month, 1)
    _, last_day = monthrange(year, month)
    end_date = date(year, month, last_day)

    return get_report(db, user_id, start_date, end_date)


def get_yearly_report(db: Session, user_id: int, year: int):
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)

    return get_report(db, user_id, start_date, end_date)


def get_monthly_category_report(db: Session, user_id: int, year: int, month: int):
    start_date = date(year, month, 1)
    _, last_day = monthrange(year, month)
    end_date = date(year, month, last_day)

    return get_category_report(db, user_id, start_date, end_date)


def get_yearly_category_report(db: Session, user_id: int, year: int):
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)

    return get_category_report(db, user_id, start_date, end_date)


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


def get_category_report(db: Session, user_id: int, start_date: date, end_date: date):
    # category-based income and expenses
    category_report = db.query(
        Category.name,
        func.sum(Transaction.amount).filter(Transaction.transaction_type == 'credit').label('income'),
        func.sum(Transaction.amount).filter(Transaction.transaction_type == 'debit').label('expense')
    ).join(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.date.between(start_date, end_date)
    ).group_by(Category.id).all()

    print(category_report)

    # Get total income (credit transactions)
    total_income = 0
    for category in category_report:
        if category[1] is not None:
            total_income += category[1]

    # Get total expenses (debit transactions)
    total_expense = 0
    for category in category_report:
        if category[2] is not None:
            total_expense += category[2]

    # Get savings (transactions with categories associated with saving goals)
    saving_category_ids = db.query(SavingGoal.category_id).filter(SavingGoal.user_id == user_id).distinct()
    saving_categories = db.query(Category.name).filter(Category.id.in_(saving_category_ids)).all()
    saving_categories = [category[0] for category in saving_categories]
    total_savings = 0
    for category in category_report:
        if category[1] is not None and category[0] in saving_categories:
            total_savings += category[1]

    category_response = {}
    for category in category_report:
        category_response[category[0]] = {
            "income": category[1] if category[1] is not None else 0,
            "expenses": category[2] if category[2] is not None else 0
        }

    #Income chart
    income_labels = []
    income_values = []
    for category in category_report:
        if category[1] is not None:
            income_labels.append(category[0])
            income_values.append(category[1])
    income_chart = generate_pie_chart(income_labels, income_values, "Income by Category")

    #Expense chart
    expense_labels = []
    expense_values = []
    for category in category_report:
        if category[2] is not None:
            expense_labels.append(category[0])
            expense_values.append(category[2])
    expense_chart = generate_pie_chart(expense_labels, expense_values, "Expense by Category")

    #Summary chart
    summary_labels = ["Income", "Expense", "Savings"]
    summary_values = [total_income, total_expense, total_savings]
    summary_chart = generate_pie_chart(summary_labels, summary_values, "Financial Summary")

    return {
        "category_report": category_response,
        "total_income": total_income,
        "total_expense": total_expense,
        "total_savings": total_savings,
        "net": (total_income - total_expense),
        "start_date": start_date,
        "end_date": end_date,
        "income_chart": income_chart,
        "expense_chart": expense_chart,
        "summary_chart": summary_chart
    }


def get_saving_categories(db: Session, user_id: int):
    return [category.name for category in
            db.query(Category).join(SavingGoal).filter(SavingGoal.user_id == user_id).all()]


def generate_pie_chart(labels, sizes, title):
    plt.figure(figsize=(10, 10))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title(title)

    # Save the plot to a bytes buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Encode the image to base64
    image_png = buffer.getvalue()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    plt.close()

    return graphic