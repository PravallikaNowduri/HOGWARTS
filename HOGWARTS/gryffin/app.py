"""
GryffinTwin FastAPI Backend
Financial Management System with SQLite
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime, timedelta
import os

# Database Setup
DATABASE_URL = "sqlite:///./gryfftwin.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI App
app = FastAPI(title="GryffinTwin API", version="1.0")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== DATABASE MODELS ====================

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Expense(Base):
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    category = Column(String)
    description = Column(String)
    amount = Column(Float)
    date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="Completed")

class Goal(Base):
    __tablename__ = "goals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    name = Column(String)
    description = Column(String)
    target_amount = Column(Float)
    current_amount = Column(Float, default=0)
    status = Column(String, default="Active")
    created_at = Column(DateTime, default=datetime.utcnow)

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    type = Column(String)  # income or expense
    amount = Column(Float)
    date = Column(DateTime, default=datetime.utcnow)
    description = Column(String)

class SecurityAlert(Base):
    __tablename__ = "security_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    alert_type = Column(String)
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    resolved = Column(Boolean, default=False)

# Create tables
Base.metadata.create_all(bind=engine)

# ==================== PYDANTIC SCHEMAS ====================

class UserCreate(BaseModel):
    email: str
    password: str
    name: str

class UserLogin(BaseModel):
    email: str
    password: str

class ExpenseCreate(BaseModel):
    category: str
    description: str
    amount: float
    date: datetime = None

class GoalCreate(BaseModel):
    name: str
    description: str
    target_amount: float

class GoalUpdate(BaseModel):
    current_amount: float = None
    status: str = None

class TransactionCreate(BaseModel):
    type: str
    amount: float
    description: str = ""

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==================== API ENDPOINTS ====================

# Auth Endpoints
@app.post("/api/auth/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = User(email=user.email, password=user.password, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"id": db_user.id, "email": db_user.email, "name": db_user.name}

@app.post("/api/auth/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"id": db_user.id, "email": db_user.email, "name": db_user.name}

# Dashboard Endpoints
@app.get("/api/dashboard/{user_id}")
def get_dashboard(user_id: int, db: Session = Depends(get_db)):
    expenses = db.query(Expense).filter(Expense.user_id == user_id).all()
    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
    goals = db.query(Goal).filter(Goal.user_id == user_id).all()
    
    total_expenses = sum(e.amount for e in expenses)
    total_income = sum(t.amount for t in transactions if t.type == "income")
    balance = total_income - total_expenses
    
    goal_progress = sum(g.current_amount for g in goals) / sum(g.target_amount for g in goals) * 100 if goals else 0
    
    return {
        "balance": balance,
        "total_expenses": total_expenses,
        "total_income": total_income,
        "goal_progress": round(goal_progress, 1),
        "active_goals": len([g for g in goals if g.status == "Active"]),
        "recent_transactions": len(transactions),
    }

# Expense Endpoints
@app.get("/api/expenses/{user_id}")
def get_expenses(user_id: int, db: Session = Depends(get_db)):
    expenses = db.query(Expense).filter(Expense.user_id == user_id).order_by(Expense.date.desc()).all()
    total = sum(e.amount for e in expenses)
    return {
        "total": total,
        "expenses": [
            {
                "id": e.id,
                "category": e.category,
                "description": e.description,
                "amount": e.amount,
                "date": e.date,
                "status": e.status,
            }
            for e in expenses
        ]
    }

@app.post("/api/expenses/{user_id}")
def create_expense(user_id: int, expense: ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = Expense(
        user_id=user_id,
        category=expense.category,
        description=expense.description,
        amount=expense.amount,
        date=expense.date or datetime.utcnow(),
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return {"id": db_expense.id, "message": "Expense created"}

@app.delete("/api/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
    return {"message": "Expense deleted"}

# Goals Endpoints
@app.get("/api/goals/{user_id}")
def get_goals(user_id: int, db: Session = Depends(get_db)):
    goals = db.query(Goal).filter(Goal.user_id == user_id).all()
    return [
        {
            "id": g.id,
            "name": g.name,
            "description": g.description,
            "target_amount": g.target_amount,
            "current_amount": g.current_amount,
            "progress": round(g.current_amount / g.target_amount * 100, 1) if g.target_amount > 0 else 0,
            "status": g.status,
        }
        for g in goals
    ]

@app.post("/api/goals/{user_id}")
def create_goal(user_id: int, goal: GoalCreate, db: Session = Depends(get_db)):
    db_goal = Goal(
        user_id=user_id,
        name=goal.name,
        description=goal.description,
        target_amount=goal.target_amount,
    )
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return {"id": db_goal.id, "message": "Goal created"}

@app.patch("/api/goals/{goal_id}")
def update_goal(goal_id: int, goal_update: GoalUpdate, db: Session = Depends(get_db)):
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    if goal_update.current_amount is not None:
        goal.current_amount = goal_update.current_amount
    if goal_update.status is not None:
        goal.status = goal_update.status
    
    db.commit()
    db.refresh(goal)
    return {"message": "Goal updated", "goal": goal}

@app.delete("/api/goals/{goal_id}")
def delete_goal(goal_id: int, db: Session = Depends(get_db)):
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    db.delete(goal)
    db.commit()
    return {"message": "Goal deleted"}

# Analytics Endpoints
@app.get("/api/analytics/{user_id}")
def get_analytics(user_id: int, db: Session = Depends(get_db)):
    expenses = db.query(Expense).filter(Expense.user_id == user_id).all()
    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
    
    total_expenses = sum(e.amount for e in expenses)
    total_income = sum(t.amount for t in transactions if t.type == "income")
    net_savings = total_income - total_expenses
    
    # Expenses by category
    category_breakdown = {}
    for e in expenses:
        category_breakdown[e.category] = category_breakdown.get(e.category, 0) + e.amount
    
    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_savings": net_savings,
        "savings_rate": round(net_savings / total_income * 100, 1) if total_income > 0 else 0,
        "category_breakdown": category_breakdown,
        "expense_count": len(expenses),
    }

# Security Endpoints
@app.get("/api/security/{user_id}")
def get_security(user_id: int, db: Session = Depends(get_db)):
    alerts = db.query(SecurityAlert).filter(SecurityAlert.user_id == user_id).all()
    unresolved = [a for a in alerts if not a.resolved]
    
    return {
        "security_status": "Excellent" if len(unresolved) == 0 else "Warning",
        "total_alerts": len(alerts),
        "unresolved_alerts": len(unresolved),
        "two_factor_enabled": True,
        "recent_alerts": [
            {
                "id": a.id,
                "type": a.alert_type,
                "message": a.message,
                "timestamp": a.timestamp,
            }
            for a in unresolved[-5:]
        ],
    }

@app.post("/api/security/alert/{user_id}")
def create_alert(user_id: int, alert_type: str, message: str, db: Session = Depends(get_db)):
    db_alert = SecurityAlert(user_id=user_id, alert_type=alert_type, message=message)
    db.add(db_alert)
    db.commit()
    return {"message": "Alert created"}

# Health check
@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "GryffinTwin API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
