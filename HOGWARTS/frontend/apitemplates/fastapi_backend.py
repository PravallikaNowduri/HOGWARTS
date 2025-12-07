"""
GryffinTwin - FastAPI Backend
Complete working backend with JWT authentication and all required endpoints

Install dependencies:
pip install fastapi uvicorn python-jose pydantic

Run the server:
uvicorn fastapi_backend:app --reload --port 8000
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt

# ============ CONFIGURATION ============
SECRET_KEY = "your-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ============ INITIALIZE APP ============
app = FastAPI(
    title="GryffinTwin API",
    description="Financial Dashboard Backend",
    version="1.0.0"
)

# ============ CORS MIDDLEWARE ============
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

# ============ PYDANTIC MODELS ============

class User(BaseModel):
    id: int
    name: str
    email: str

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: User

class DashboardSummary(BaseModel):
    total_balance: float
    balance_change: float
    monthly_expenses: float
    budget_percentage: int
    investments: float
    investment_return: float
    goals_progress: int
    active_goals: int
    security_status: str
    financial_score: int

class Expense(BaseModel):
    date: str
    category: str
    description: str
    amount: float
    status: str

class ExpensesResponse(BaseModel):
    total_expenses: float
    monthly_budget: float
    remaining_budget: float
    budget_percentage: int
    expenses: List[Expense]

class SecurityResponse(BaseModel):
    overall_security: str
    login_activity: str
    fraud_alerts: int
    password_strength: str
    two_factor_auth: bool
    monitored_cards: int

class Goal(BaseModel):
    id: int
    name: str
    icon: str
    target_amount: float
    current_amount: float
    status: str

class GoalsResponse(BaseModel):
    goals: List[Goal]

class AnalyticsResponse(BaseModel):
    total_income: float
    total_expenses: float
    net_savings: float
    savings_rate: int
    months: List[str]
    income_data: List[float]
    expense_data: List[float]
    categories: List[str]
    category_amounts: List[float]

# ============ JWT FUNCTIONS ============

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token from Authorization header"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ============ API ROUTES ============

@app.get("/")
def read_root():
    """Root endpoint - API status"""
    return {
        "message": "GryffinTwin API is running",
        "version": "1.0.0",
        "docs": "http://localhost:8000/docs"
    }

@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "timestamp": datetime.utcnow(),
        "service": "GryffinTwin API"
    }

# ============ AUTHENTICATION ENDPOINTS ============

@app.post("/api/auth/login", response_model=LoginResponse)
def login(request: LoginRequest):
    """
    Login endpoint - accepts any email/password for demo
    Returns JWT token and user data
    
    In production, validate against database with password hashing
    """
    if not request.email or not request.password:
        raise HTTPException(status_code=400, detail="Email and password required")
    
    # Demo: Accept any email/password combination
    # In production: Hash password and validate against database
    user = User(
        id=1,
        name=request.email.split("@")[0].title(),
        email=request.email
    )
    
    access_token = create_access_token(
        data={"sub": request.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=user
    )

# ============ DASHBOARD ENDPOINTS ============

@app.get("/api/dashboard/summary", response_model=DashboardSummary)
def get_dashboard_summary(email: str = Depends(verify_token)):
    """Get dashboard summary for authenticated user"""
    return DashboardSummary(
        total_balance=24580.00,
        balance_change=12.5,
        monthly_expenses=3240.00,
        budget_percentage=78,
        investments=12450.00,
        investment_return=8.2,
        goals_progress=68,
        active_goals=4,
        security_status="Secure",
        financial_score=850
    )

# ============ EXPENSES ENDPOINTS ============

@app.get("/api/expenses", response_model=ExpensesResponse)
def get_expenses(email: str = Depends(verify_token)):
    """Get expenses for authenticated user"""
    expenses = [
        Expense(
            date="2025-12-05",
            category="🍔 Food",
            description="Lunch at Restaurant",
            amount=45.50,
            status="✓ Completed"
        ),
        Expense(
            date="2025-12-04",
            category="🚗 Transport",
            description="Uber Trip",
            amount=32.00,
            status="✓ Completed"
        ),
        Expense(
            date="2025-12-03",
            category="🎬 Entertainment",
            description="Movie Tickets",
            amount=28.00,
            status="✓ Completed"
        ),
        Expense(
            date="2025-12-02",
            category="🛒 Shopping",
            description="Grocery Shopping",
            amount=156.75,
            status="✓ Completed"
        ),
        Expense(
            date="2025-12-01",
            category="💊 Health",
            description="Pharmacy Purchase",
            amount=65.20,
            status="✓ Completed"
        ),
    ]
    
    return ExpensesResponse(
        total_expenses=3240.00,
        monthly_budget=4200.00,
        remaining_budget=960.00,
        budget_percentage=77,
        expenses=expenses
    )

# ============ SECURITY ENDPOINTS ============

@app.get("/api/security", response_model=SecurityResponse)
def get_security(email: str = Depends(verify_token)):
    """Get security status for authenticated user"""
    return SecurityResponse(
        overall_security="Excellent",
        login_activity="Normal",
        fraud_alerts=0,
        password_strength="Strong",
        two_factor_auth=True,
        monitored_cards=4
    )

# ============ GOALS ENDPOINTS ============

@app.get("/api/goals", response_model=GoalsResponse)
def get_goals(email: str = Depends(verify_token)):
    """Get financial goals for authenticated user"""
    goals = [
        Goal(
            id=1,
            name="Emergency Fund",
            icon="🏦",
            target_amount=15000.00,
            current_amount=10200.00,
            status="Active"
        ),
        Goal(
            id=2,
            name="Vacation Fund",
            icon="✈️",
            target_amount=8000.00,
            current_amount=3600.00,
            status="Active"
        ),
        Goal(
            id=3,
            name="Home Down Payment",
            icon="🏠",
            target_amount=50000.00,
            current_amount=16000.00,
            status="Active"
        ),
        Goal(
            id=4,
            name="Car Purchase",
            icon="🚗",
            target_amount=35000.00,
            current_amount=9800.00,
            status="Paused"
        ),
        Goal(
            id=5,
            name="Professional Development",
            icon="📚",
            target_amount=5000.00,
            current_amount=4100.00,
            status="Active"
        ),
    ]
    
    return GoalsResponse(goals=goals)

# ============ ANALYTICS ENDPOINTS ============

@app.get("/api/analytics", response_model=AnalyticsResponse)
def get_analytics(email: str = Depends(verify_token)):
    """Get financial analytics for authenticated user"""
    return AnalyticsResponse(
        total_income=18500.00,
        total_expenses=9240.00,
        net_savings=9260.00,
        savings_rate=50,
        months=["Week 1", "Week 2", "Week 3", "Week 4", "Week 5", "Week 6"],
        income_data=[1500.0, 1600.0, 1550.0, 1800.0, 1700.0, 1900.0],
        expense_data=[750.0, 780.0, 820.0, 750.0, 900.0, 800.0],
        categories=["Shopping", "Food", "Transport", "Entertainment", "Healthcare", "Other"],
        category_amounts=[2450.0, 1890.0, 1560.0, 980.0, 720.0, 640.0]
    )

# ============ MAIN ============

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)