# Quick Start Guide - GryffinTwin Backend

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Server
```bash
python app.py
```

You should see:
```
Database tables created!
 * Running on http://127.0.0.1:8000
 * Press CTRL+C to quit
```

### Step 3: Seed Dummy Data
In a new terminal:
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

### Step 4: Login with Demo Account
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@example.com","password":"demo123"}'
```

Save the `accessToken` from the response.

### Step 5: Test an Endpoint (Replace TOKEN with your token)
```bash
curl -X GET http://127.0.0.1:8000/api/dashboard/summary \
  -H "Authorization: Bearer TOKEN"
```

---

## 📋 Common API Operations

### Create an Expense
```bash
curl -X POST http://127.0.0.1:8000/api/expenses \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "Food",
    "description": "Grocery shopping",
    "amount": 85.50
  }'
```

### Get All Expenses
```bash
curl -X GET http://127.0.0.1:8000/api/expenses \
  -H "Authorization: Bearer TOKEN"
```

### Update an Expense (Replace ID with expense ID)
```bash
curl -X PUT http://127.0.0.1:8000/api/expenses/1 \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 95.00,
    "status": "completed"
  }'
```

### Delete an Expense
```bash
curl -X DELETE http://127.0.0.1:8000/api/expenses/1 \
  -H "Authorization: Bearer TOKEN"
```

### Create a Goal
```bash
curl -X POST http://127.0.0.1:8000/api/goals \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Summer Vacation",
    "targetAmount": 5000,
    "currentAmount": 1500,
    "icon": "✈️"
  }'
```

### Get All Goals
```bash
curl -X GET http://127.0.0.1:8000/api/goals \
  -H "Authorization: Bearer TOKEN"
```

### Update Goal Progress
```bash
curl -X PUT http://127.0.0.1:8000/api/goals/1 \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "currentAmount": 2500
  }'
```

### Get Analytics
```bash
curl -X GET http://127.0.0.1:8000/api/analytics \
  -H "Authorization: Bearer TOKEN"
```

---

## 🗄️ Database CRUD Operations

| Operation | Method | Endpoint | Example |
|-----------|--------|----------|---------|
| **CREATE** Expense | POST | `/api/expenses` | Creates new expense |
| **READ** Expenses | GET | `/api/expenses` | Gets all expenses |
| **READ** One | GET | `/api/expenses/1` | Gets expense #1 |
| **UPDATE** | PUT | `/api/expenses/1` | Updates expense #1 |
| **DELETE** | DELETE | `/api/expenses/1` | Deletes expense #1 |
| **CREATE** Goal | POST | `/api/goals` | Creates new goal |
| **READ** Goals | GET | `/api/goals` | Gets all goals |
| **READ** One | GET | `/api/goals/1` | Gets goal #1 |
| **UPDATE** | PUT | `/api/goals/1` | Updates goal #1 |
| **DELETE** | DELETE | `/api/goals/1` | Deletes goal #1 |

---

## 🔐 Authentication Notes

Every protected endpoint requires the `Authorization` header:
```bash
Authorization: Bearer YOUR_TOKEN_HERE
```

Get your token by logging in:
```bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "demo@example.com",
  "password": "demo123"
}
```

---

## 📁 Database Files

After running the app, you'll have:
- `instance/gryffintwain.db` - SQLite database file

To reset the database:
```bash
rm instance/gryffintwain.db
python app.py
curl -X POST http://127.0.0.1:8000/api/seed
```

---

## ⚡ Using Postman (Alternative to cURL)

1. Open Postman
2. Create new request
3. Set method to GET/POST/PUT/DELETE
4. Enter URL: `http://127.0.0.1:8000/api/endpoint`
5. Go to Headers tab
6. Add header: `Authorization: Bearer YOUR_TOKEN`
7. Add header: `Content-Type: application/json`
8. Paste JSON body in Body tab (for POST/PUT)
9. Click Send

---

## 🐛 Troubleshooting

**Issue**: Port 8000 already in use
```bash
# Change port in app.py last line:
app.run(debug=True, host='127.0.0.1', port=8001)
```

**Issue**: Module not found error
```bash
# Install dependencies
pip install -r requirements.txt
```

**Issue**: Database locked
```bash
# Delete and reseed database
rm instance/gryffintwain.db
python app.py
curl -X POST http://127.0.0.1:8000/api/seed
```

---

## 📝 Example Workflow

1. **Start server**: `python app.py`
2. **Seed data**: `curl -X POST http://127.0.0.1:8000/api/seed`
3. **Login**: Get token from `/api/auth/login`
4. **Create expense**: `POST /api/expenses` with token
5. **View expenses**: `GET /api/expenses` with token
6. **Update expense**: `PUT /api/expenses/1` with token
7. **Create goal**: `POST /api/goals` with token
8. **View analytics**: `GET /api/analytics` with token

---

## 🎯 Next Steps

✅ Backend is ready to use!

Now:
1. Open your frontend HTML files in a browser
2. They will connect to `http://127.0.0.1:8000/api`
3. Login with demo@example.com / demo123
4. Test all features!

---

**Questions?** Check the full README.md for detailed documentation!
