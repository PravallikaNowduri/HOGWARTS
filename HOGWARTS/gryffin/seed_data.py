from app import SessionLocal, User, Expense, Goal, Transaction, SecurityAlert
from datetime import datetime, timedelta
import random

def seed():
    db = SessionLocal()
    try:
        # Get the user
        user = db.query(User).filter(User.email == "user@example.com").first()
        if not user:
            print("User 'user@example.com' not found! Please run the registration step first.")
            return

        print(f"Seeding data for user: {user.email}")

        # Clear existing data for this user to avoid duplicates if run multiple times
        db.query(Transaction).filter(Transaction.user_id == user.id).delete()
        db.query(Expense).filter(Expense.user_id == user.id).delete()
        db.query(Goal).filter(Goal.user_id == user.id).delete()

        # 1. Add Income (Transactions) - Needed for Balance Calculation
        incomes = [
            Transaction(user_id=user.id, type="income", amount=5000.00, description="Monthly Salary", date=datetime.utcnow() - timedelta(days=2)),
            Transaction(user_id=user.id, type="income", amount=1500.00, description="Freelance Project", date=datetime.utcnow() - timedelta(days=10)),
            Transaction(user_id=user.id, type="income", amount=200.00, description="Dividend Income", date=datetime.utcnow() - timedelta(days=15))
        ]
        db.add_all(incomes)

        # 2. Add Expenses
        categories = ["Food", "Transport", "Housing", "Entertainment", "Utilities", "Shopping"]
        expenses = []
        for i in range(10):
            expenses.append(Expense(
                user_id=user.id, 
                category=random.choice(categories), 
                description=f"Expense #{i+1}", 
                amount=round(random.uniform(10.0, 150.0), 2), 
                date=datetime.utcnow() - timedelta(days=random.randint(0, 30))
            ))
        db.add_all(expenses)

        # 3. Add Goals
        goals = [
            Goal(user_id=user.id, name="Emergency Fund", description="3 months of expenses", target_amount=10000, current_amount=8500, status="Active"),
            Goal(user_id=user.id, name="New Car", description="Tesla Model 3", target_amount=40000, current_amount=15000, status="Active"),
            Goal(user_id=user.id, name="Holiday Gift", description="For family", target_amount=500, current_amount=500, status="Completed")
        ]
        db.add_all(goals)

        db.commit()
        print("Database seeded successfully!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
