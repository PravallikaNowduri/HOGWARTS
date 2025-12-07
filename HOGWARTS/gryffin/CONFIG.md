# GryffinTwin - Configuration & Customization Guide

## 🔧 Configuration Options

### Backend Configuration (app.py)

#### Database URL
Default uses SQLite local file:
```python
DATABASE_URL = "sqlite:///./gryfftwin.db"
```

**For PostgreSQL:**
```python
DATABASE_URL = "postgresql://username:password@localhost/gryfftwin"
```

**For MySQL:**
```python
DATABASE_URL = "mysql://username:password@localhost/gryfftwin"
```

#### Server Port
Default is 8000. To change, modify the startup:
```bash
python -m uvicorn app:app --port 8001
```

Or in app.py, change the bottom:
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)  # Change port here
```

#### CORS Settings
Currently allows all origins. For production:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific domain
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "PATCH"],
    allow_headers=["*"],
)
```

---

## 🎨 Frontend Customization (index.html)

### Colors
In the `<style>` section, modify CSS variables:

```css
:root {
    --primary: #2158aa;      /* Main color */
    --secondary: #1e88e5;    /* Secondary color */
    --success: #43a047;      /* Success alerts */
    --warning: #fb8c00;      /* Warning alerts */
    --danger: #e53935;       /* Danger/Delete */
    --light: #f5f5f5;        /* Light backgrounds */
    --dark: #212121;         /* Dark text */
    --text: #424242;         /* Regular text */
    --border: #e0e0e0;       /* Borders */
}
```

### Logo & Brand Name
Change in sidebar:
```html
<div class="logo">🏰 YourAppName</div>
```

### API Base URL
If running on different server:
```javascript
const API_URL = 'http://your-server.com:8000/api';
```

### Budget Amount
Default budget is $4,200. Change in expenses:
```html
<div>Budget: <strong>$5000</strong></div>
```

---

## 📦 Adding New Database Fields

### Example: Add "Notes" field to expenses

**Step 1: Modify Model (app.py)**
```python
class Expense(Base):
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    category = Column(String)
    description = Column(String)
    amount = Column(Float)
    date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="Completed")
    notes = Column(String, nullable=True)  # Add this
```

**Step 2: Update Pydantic Schema (app.py)**
```python
class ExpenseCreate(BaseModel):
    category: str
    description: str
    amount: float
    date: datetime = None
    notes: str = None  # Add this
```

**Step 3: Update API Endpoint (app.py)**
```python
@app.post("/api/expenses/{user_id}")
def create_expense(user_id: int, expense: ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = Expense(
        user_id=user_id,
        category=expense.category,
        description=expense.description,
        amount=expense.amount,
        date=expense.date or datetime.utcnow(),
        notes=expense.notes  # Add this
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return {"id": db_expense.id, "message": "Expense created"}
```

**Step 4: Update Frontend (index.html)**
```html
<div class="form-group">
    <label>Notes</label>
    <textarea id="expenseNotes" placeholder="Add notes..."></textarea>
</div>
```

---

## 🔐 Security Enhancements

### Password Hashing
**Install bcrypt:**
```bash
pip install bcrypt
```

**Update app.py:**
```python
import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), hash.encode())

@app.post("/api/auth/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed = hash_password(user.password)  # Hash password
    db_user = User(email=user.email, password=hashed, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"id": db_user.id, "email": db_user.email, "name": db_user.name}
```

### JWT Authentication
**Install PyJWT:**
```bash
pip install python-jose[cryptography]
```

Create `auth.py`:
```python
from datetime import datetime, timedelta
from jose import JWTError, jwt

SECRET_KEY = "your-secret-key-change-this"
ALGORITHM = "HS256"

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

---

## 🚀 Deployment Options

### Local Network
```bash
python app.py
# Accessible to others on your network at: http://[YOUR_IP]:8000
```

### Cloud Deployment (Heroku)

**1. Create Procfile:**
```
web: gunicorn app:app
```

**2. Update requirements.txt:**
```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
gunicorn==21.2.0
python-multipart==0.0.6
pydantic==2.5.0
```

**3. Deploy:**
```bash
heroku create your-app-name
heroku config:set DATABASE_URL="postgresql://..."
git push heroku main
```

### Docker
**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Build & Run:**
```bash
docker build -t gryfftwin .
docker run -p 8000:8000 gryfftwin
```

---

## 📊 Database Backup

### SQLite
```bash
# Backup
cp gryfftwin.db gryfftwin_backup.db

# Restore
cp gryfftwin_backup.db gryfftwin.db
```

### PostgreSQL
```bash
# Backup
pg_dump -U username dbname > backup.sql

# Restore
psql -U username dbname < backup.sql
```

---

## 🧪 Testing

### API Testing with cURL
```bash
# Register
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"pass123","name":"Test"}'

# Login
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"pass123"}'

# Add Expense
curl -X POST "http://localhost:8000/api/expenses/1" \
  -H "Content-Type: application/json" \
  -d '{"category":"Food","description":"Lunch","amount":15.50}'

# Get Expenses
curl "http://localhost:8000/api/expenses/1"
```

### Automated Testing (pytest)
**Install pytest:**
```bash
pip install pytest httpx
```

**Create test_app.py:**
```python
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200

def test_register():
    response = client.post(
        "/api/auth/register",
        json={"email": "test@test.com", "password": "test", "name": "Test"}
    )
    assert response.status_code == 200
```

**Run tests:**
```bash
pytest test_app.py
```

---

## 📈 Performance Optimization

### Database Indexing
```python
# In User model
email = Column(String, unique=True, index=True)

# In Expense model
date = Column(DateTime, index=True)
user_id = Column(Integer, index=True)
```

### Query Optimization
```python
# Use select() for specific columns
from sqlalchemy import select

@app.get("/api/expenses/{user_id}")
def get_expenses(user_id: int, db: Session = Depends(get_db)):
    expenses = db.query(Expense).filter(
        Expense.user_id == user_id
    ).order_by(Expense.date.desc()).limit(100).all()  # Limit results
    return expenses
```

### Caching
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_calculation(value):
    return value ** 2
```

---

## 🐛 Debugging

### Enable Debug Mode
```python
# In app.py startup
app.debug = True

# Or run with
python -m uvicorn app:app --reload
```

### Logging
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.post("/api/expenses/{user_id}")
def create_expense(user_id: int, expense: ExpenseCreate, db: Session = Depends(get_db)):
    logger.debug(f"Creating expense for user {user_id}")
    # ... rest of code
```

### Database Debugging
View SQL queries:
```python
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
```

---

## 📝 Next Steps

1. **Test the setup** - Make sure everything works locally
2. **Customize** - Adjust colors, logos, and features
3. **Add security** - Implement password hashing and JWT
4. **Deploy** - Choose a hosting option and go live
5. **Monitor** - Track usage and performance

---

**Questions? Check README.md or review the code comments!**
