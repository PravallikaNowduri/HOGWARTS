# GryffinTwin - Full Stack Financial Management System

A complete financial management application with FastAPI backend and interactive frontend.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ installed
- pip (Python package manager)

### Installation & Setup (1 minute)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the backend server
python app.py
```

The backend will start at: **http://localhost:8000**

### API Documentation
Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📁 Project Structure

```
gryfftwin/
├── app.py                 # FastAPI backend (SQLite + APIs)
├── requirements.txt       # Python dependencies
├── index.html            # Main dashboard
├── login.html            # Authentication page
├── expenses.html         # Expense tracking
├── goals.html            # Goal management
├── analytics.html        # Financial analytics
├── security.html         # Security monitoring
├── gryfftwin.db         # SQLite database (auto-created)
└── README.md            # This file
```

---

## 📊 Features

### Backend (FastAPI + SQLite)
- ✅ User authentication (register/login)
- ✅ Expense tracking with categories
- ✅ Financial goals management
- ✅ Analytics & insights
- ✅ Security alerts
- ✅ Real-time data processing
- ✅ CORS enabled for frontend integration

### Frontend (HTML/CSS/JS)
- ✅ Interactive dashboard
- ✅ Form validations
- ✅ Real-time data sync
- ✅ Responsive design
- ✅ Category-based expense filtering
- ✅ Goal progress tracking
- ✅ Charts & visualizations

---

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register` - Create new account
- `POST /api/auth/login` - Login user

### Dashboard
- `GET /api/dashboard/{user_id}` - Get dashboard data

### Expenses
- `GET /api/expenses/{user_id}` - List all expenses
- `POST /api/expenses/{user_id}` - Add new expense
- `DELETE /api/expenses/{expense_id}` - Delete expense

### Goals
- `GET /api/goals/{user_id}` - List all goals
- `POST /api/goals/{user_id}` - Create new goal
- `PATCH /api/goals/{goal_id}` - Update goal progress
- `DELETE /api/goals/{goal_id}` - Delete goal

### Analytics
- `GET /api/analytics/{user_id}` - Get financial analytics

### Security
- `GET /api/security/{user_id}` - Get security status
- `POST /api/security/alert/{user_id}` - Create security alert

### Health
- `GET /api/health` - Check API status

---

## 💾 Database Schema

### Users Table
```sql
users (
  id INT PRIMARY KEY,
  email VARCHAR UNIQUE,
  password VARCHAR,
  name VARCHAR,
  created_at DATETIME
)
```

### Expenses Table
```sql
expenses (
  id INT PRIMARY KEY,
  user_id INT,
  category VARCHAR,
  description VARCHAR,
  amount FLOAT,
  date DATETIME,
  status VARCHAR
)
```

### Goals Table
```sql
goals (
  id INT PRIMARY KEY,
  user_id INT,
  name VARCHAR,
  description VARCHAR,
  target_amount FLOAT,
  current_amount FLOAT,
  status VARCHAR,
  created_at DATETIME
)
```

### Transactions Table
```sql
transactions (
  id INT PRIMARY KEY,
  user_id INT,
  type VARCHAR,
  amount FLOAT,
  date DATETIME,
  description VARCHAR
)
```

### Security Alerts Table
```sql
security_alerts (
  id INT PRIMARY KEY,
  user_id INT,
  alert_type VARCHAR,
  message VARCHAR,
  timestamp DATETIME,
  resolved BOOLEAN
)
```

---

## 🔑 Test Credentials

Use these to test the system:

```
Email: test@gryfftwin.com
Password: password123
```

Or create your own account via the registration form.

---

## 🛠️ Development

### Adding New Features

1. **Add Database Model** in `app.py`:
```python
class NewFeature(Base):
    __tablename__ = "new_features"
    id = Column(Integer, primary_key=True)
    # ... other columns
```

2. **Create Pydantic Schema**:
```python
class NewFeatureCreate(BaseModel):
    field: str
```

3. **Add API Endpoint**:
```python
@app.get("/api/newfeature/{user_id}")
def get_new_feature(user_id: int, db: Session = Depends(get_db)):
    # Implementation
    pass
```

4. **Connect Frontend** - Update HTML to call the new endpoint

---

## 🚨 Troubleshooting

### Port 8000 already in use?
```bash
python app.py --port 8001
```

### Database issues?
Delete `gryfftwin.db` and restart - it will recreate automatically.

### CORS errors?
The backend already has CORS enabled. If issues persist, check browser console.

### Frontend not connecting?
- Ensure backend is running on `http://localhost:8000`
- Check browser console (F12) for errors
- Verify API endpoints in network tab

---

## 📦 Deployment

### Run on different host/port:
```bash
uvicorn app:app --host 0.0.0.0 --port 8080
```

### Production setup:
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

---

## 📝 License

GryffinTwin - Financial Management System

---

## ❓ Need Help?

1. Check the API docs at `/docs`
2. Review example API calls below
3. Check browser console for frontend errors

### Example API Calls

```bash
# Register user
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@test.com","password":"pass123","name":"John"}'

# Login
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@test.com","password":"pass123"}'

# Add expense
curl -X POST "http://localhost:8000/api/expenses/1" \
  -H "Content-Type: application/json" \
  -d '{"category":"Food","description":"Lunch","amount":50.00}'

# Get expenses
curl "http://localhost:8000/api/expenses/1"

# Get dashboard
curl "http://localhost:8000/api/dashboard/1"
```

---

**Happy budgeting with GryffinTwin! 💰✨**
