# GryffinTwin Flask Backend

A complete Flask REST API backend with SQLite database for the GryffinTwin financial management application. This backend includes user authentication, expense tracking, goals management, and full CRUD operations.

## Features

✅ **User Authentication**
- User registration and login with JWT tokens
- Password hashing with Werkzeug security
- 7-day token expiration

✅ **Expense Management (CRUD)**
- Create expenses with category, description, and amount
- Read all expenses or specific expense
- Update expense details
- Delete expenses
- Calculate total expenses, budget usage, and category breakdowns

✅ **Goals Management (CRUD)**
- Create financial goals with target and current amounts
- Read all goals or specific goal
- Update goal progress
- Delete goals
- Track progress percentage

✅ **Dashboard Summary**
- Total balance overview
- Monthly expense tracking
- Investment portfolio value
- Goals progress tracking
- Security status

✅ **Security Monitoring**
- Security status endpoint
- Fraud alerts
- Login activity tracking

✅ **Analytics**
- Expense analytics by category
- Monthly spending trends
- Top spending categories
- Average expense calculation

✅ **Database Management**
- SQLite database with automatic table creation
- Dummy data seeding endpoint
- Relationship management between users and data

## Project Structure

```
gryffintwain/
├── app.py                 # Main Flask application with all endpoints
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── instance/
    └── gryffintwain.db   # SQLite database (created on first run)
```

## Installation & Setup

### 1. Clone or Download the Project
```bash
cd gryffintwain
```

### 2. Create a Virtual Environment (Recommended)
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```

The server will start on `http://127.0.0.1:8000`

### 5. Seed Database with Dummy Data
Make a POST request to initialize the database with demo data:

```bash
curl -X POST http://127.0.0.1:8000/api/seed
```

Response:
```json
{
  "message": "Database seeded successfully",
  "demo_email": "demo@example.com",
  "demo_password": "demo123"
}
```

## API Endpoints

### Authentication

**POST** `/api/auth/login`
- Login with email and password
- Request: `{"email": "demo@example.com", "password": "demo123"}`
- Response: `{"accessToken": "...", "tokenType": "bearer", "user": {...}}`

**POST** `/api/auth/register`
- Register a new user
- Request: `{"name": "John Doe", "email": "john@example.com", "password": "password123"}`
- Response: `{"accessToken": "...", "tokenType": "bearer", "user": {...}}`

### Dashboard

**GET** `/api/dashboard/summary` (Auth Required)
- Get dashboard summary with balance, expenses, investments, and goals progress
- Headers: `Authorization: Bearer <token>`

### Expenses (CRUD)

**GET** `/api/expenses` (Auth Required)
- Get all expenses for logged-in user
- Response includes: total expenses, monthly budget, remaining budget, and expense list

**POST** `/api/expenses` (Auth Required)
- Create new expense
- Request: `{"category": "Food", "description": "Lunch", "amount": 25.50, "status": "completed"}`

**GET** `/api/expenses/<expense_id>` (Auth Required)
- Get specific expense details

**PUT** `/api/expenses/<expense_id>` (Auth Required)
- Update expense
- Request: `{"category": "Transport", "amount": 30.00}`

**DELETE** `/api/expenses/<expense_id>` (Auth Required)
- Delete expense
- Response: `{"message": "Expense deleted"}`

### Goals (CRUD)

**GET** `/api/goals` (Auth Required)
- Get all goals for logged-in user
- Response: `{"goals": [{id, name, targetAmount, currentAmount, icon, ...}]}`

**POST** `/api/goals` (Auth Required)
- Create new goal
- Request: `{"name": "Emergency Fund", "targetAmount": 10000, "currentAmount": 6500, "icon": "🏦"}`

**GET** `/api/goals/<goal_id>` (Auth Required)
- Get specific goal details

**PUT** `/api/goals/<goal_id>` (Auth Required)
- Update goal
- Request: `{"currentAmount": 7500}`

**DELETE** `/api/goals/<goal_id>` (Auth Required)
- Delete goal
- Response: `{"message": "Goal deleted"}`

### Security

**GET** `/api/security` (Auth Required)
- Get security status information
- Response: `{overallSecurity, loginActivity, fraudAlerts, passwordStrength, twoFactorAuth, monitoredCards}`

### Analytics

**GET** `/api/analytics` (Auth Required)
- Get financial analytics
- Response: `{monthlyTrend, categoryBreakdown, topCategories, totalExpenses, averageExpense}`

## Database Models

### User Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
```

### Expense Table
```sql
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    category VARCHAR(50) NOT NULL,
    description VARCHAR(255) NOT NULL,
    amount FLOAT NOT NULL,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'completed',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
```

### Goal Table
```sql
CREATE TABLE goals (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    name VARCHAR(120) NOT NULL,
    target_amount FLOAT NOT NULL,
    current_amount FLOAT DEFAULT 0,
    icon VARCHAR(50) DEFAULT '🎯',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
```

## Testing with cURL

### 1. Register New User
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","password":"password123"}'
```

### 2. Login
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"password123"}'
```

### 3. Get Dashboard (Use token from login response)
```bash
curl -X GET http://127.0.0.1:8000/api/dashboard/summary \
  -H "Authorization: Bearer <your_token_here>"
```

### 4. Create Expense
```bash
curl -X POST http://127.0.0.1:8000/api/expenses \
  -H "Authorization: Bearer <your_token_here>" \
  -H "Content-Type: application/json" \
  -d '{"category":"Food","description":"Dinner","amount":45.50}'
```

### 5. Get All Expenses
```bash
curl -X GET http://127.0.0.1:8000/api/expenses \
  -H "Authorization: Bearer <your_token_here>"
```

## CORS Configuration

The backend is configured with CORS enabled for development:
```python
CORS(app)  # Allows requests from any origin
```

For production, restrict CORS:
```python
CORS(app, resources={r"/api/*": {"origins": ["https://yourdomain.com"]}})
```

## Security Notes

⚠️ **Important for Production:**

1. **Change the SECRET_KEY**: Replace the default secret key in production
   ```python
   app.config['SECRET_KEY'] = 'generate-a-secure-random-key'
   ```

2. **Use Environment Variables**: Store sensitive config in `.env` file
   ```python
   import os
   from dotenv import load_dotenv
   load_dotenv()
   app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
   ```

3. **Enable HTTPS**: Use SSL/TLS in production

4. **Database**: Switch to PostgreSQL for production

5. **Rate Limiting**: Implement rate limiting to prevent abuse

## Troubleshooting

### Issue: "ModuleNotFoundError" when running the app
**Solution**: Ensure virtual environment is activated and all dependencies are installed
```bash
pip install -r requirements.txt
```

### Issue: Database locked error
**Solution**: Delete the database file and reseed
```bash
rm instance/gryffintwain.db
python app.py
curl -X POST http://127.0.0.1:8000/api/seed
```

### Issue: Token authentication fails
**Solution**: Ensure the Authorization header format is correct
```bash
Authorization: Bearer <token_value>
```

## Frontend Integration

The frontend files (dashboard-api.html, expenses-api.html, etc.) are configured to make requests to:
```javascript
const APIBASEURL = 'http://127.0.0.1:8000/api'
```

Ensure the backend is running on the same URL for seamless integration.

## Development Tips

1. **Enable Debug Mode**: Already enabled in the main block for development
2. **Check Logs**: The console will show all requests and errors
3. **Database Inspection**: Use SQLite tools to view/edit database directly
4. **API Testing**: Use Postman, Insomnia, or cURL for testing endpoints

## File Descriptions

| File | Purpose |
|------|---------|
| app.py | Main Flask application with all routes, models, and business logic |
| requirements.txt | Python package dependencies |
| README.md | Documentation and setup guide |
| instance/gryffintwain.db | SQLite database (auto-created) |

## Next Steps

1. ✅ Install and run the backend
2. ✅ Seed dummy data using `/api/seed`
3. ✅ Test endpoints with cURL or Postman
4. ✅ Connect frontend to the backend
5. ✅ Deploy to production with proper security measures

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the API endpoint documentation
3. Examine the console logs for detailed error messages

---

**Happy Coding! 🚀**
