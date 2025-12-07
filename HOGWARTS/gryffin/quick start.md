# GryffinTwin - Quick Start Guide ⚡

## 📋 What You Got

A **complete full-stack financial app** with:
- ✅ FastAPI backend with SQLite database
- ✅ Beautiful, interactive HTML frontend
- ✅ Full user authentication
- ✅ Expense tracking, goals, analytics, security monitoring
- ✅ Ready to run in 1 minute!

---

## 🚀 Get Started (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start the Backend
```bash
python app.py
```

You'll see:
```
INFO:     Started server process [PID]
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 3: Open the App
Open your browser and go to:
```
file://[path-to]/index.html
```

Or if you have Python's http server:
```bash
python -m http.server 8000
```
Then visit: `http://localhost:8000`

---

## 🧪 Test Account

Login with:
- **Email:** test@gryfftwin.com
- **Password:** password123

Or create a new account!

---

## 📁 File Structure

```
gryfftwin/
├── app.py                 # FastAPI backend - runs on port 8000
├── index.html            # All-in-one frontend (single file!)
├── requirements.txt      # Python packages
├── README.md             # Full documentation
├── QUICK_START.md        # This file
└── gryfftwin.db         # SQLite database (auto-created)
```

---

## 🔌 What Each File Does

### `app.py` (Backend)
- FastAPI server with all API endpoints
- SQLite database with 5 tables (Users, Expenses, Goals, Transactions, Alerts)
- CORS enabled for frontend
- Auto-creates database on first run

### `index.html` (Frontend)
- Everything in one file! HTML + CSS + JavaScript
- Authentication pages (login/register)
- Dashboard with stats
- Expense tracking
- Goal management
- Analytics & insights
- Security monitoring
- Real-time API integration

### `requirements.txt`
- FastAPI, Uvicorn, SQLAlchemy, Pydantic

---

## 🎯 Features Overview

### Dashboard
- Total balance calculation
- Monthly expenses summary
- Income tracking
- Goal progress
- Recent transactions

### Expense Tracker
- Add expenses by category
- View spending history
- Delete expenses
- Budget tracking

### Financial Goals
- Create custom goals
- Track progress with visual bars
- Update goal amounts
- Pause/Resume goals

### Analytics
- Total income vs expenses
- Net savings calculation
- Spending breakdown by category
- Savings rate

### Security
- Security status monitoring
- Alert management
- Two-factor auth status
- Login activity

---

## 🔗 API Endpoints

All endpoints run on `http://localhost:8000`

### Auth
- `POST /api/auth/register` - Create account
- `POST /api/auth/login` - Login

### Expenses
- `GET /api/expenses/{user_id}` - Get all expenses
- `POST /api/expenses/{user_id}` - Add expense
- `DELETE /api/expenses/{expense_id}` - Delete expense

### Goals
- `GET /api/goals/{user_id}` - Get all goals
- `POST /api/goals/{user_id}` - Create goal
- `PATCH /api/goals/{goal_id}` - Update goal
- `DELETE /api/goals/{goal_id}` - Delete goal

### Analytics
- `GET /api/analytics/{user_id}` - Get analytics data

### Dashboard
- `GET /api/dashboard/{user_id}` - Get dashboard stats

### Security
- `GET /api/security/{user_id}` - Get security status
- `POST /api/security/alert/{user_id}` - Create alert

### Health
- `GET /api/health` - Check API status

---

## 🛠️ Troubleshooting

### Backend won't start?
```bash
# Check if port 8000 is in use
# Use a different port:
uvicorn app:app --port 8001
```

### Database errors?
```bash
# Delete the database and restart (it recreates automatically)
rm gryfftwin.db
python app.py
```

### Frontend not loading data?
- Open browser console (F12)
- Check Network tab for API calls
- Make sure backend is running at http://localhost:8000
- Check for CORS errors

### "Cannot GET /api/..."?
- Ensure `python app.py` is running
- Check backend console for errors
- Verify the endpoint path is correct

---

## 📚 API Documentation

Once backend is running, visit:

- **Interactive Docs:** http://localhost:8000/docs
- **Alternative Docs:** http://localhost:8000/redoc

---

## 🎓 Next Steps

### Add a Feature?
1. Add database model to `app.py`
2. Create Pydantic schema
3. Add API endpoint
4. Connect frontend (in `index.html`)

### Deploy?
```bash
pip install gunicorn
gunicorn -w 4 app:app
```

### Connect to Real Database?
Change in `app.py`:
```python
DATABASE_URL = "postgresql://user:password@localhost/gryfftwin"
```

---

## 💡 Pro Tips

1. **Test API in browser:**
   - Visit http://localhost:8000/docs
   - Try endpoints directly in Swagger UI

2. **See database:**
   - Install SQLite browser: https://sqlitebrowser.org
   - Open `gryfftwin.db`

3. **Debug frontend:**
   - Open F12 → Console tab
   - Check for JavaScript errors
   - Monitor network requests

4. **Add dummy data:**
   - Use `/docs` to create test data
   - Or modify backend to seed on startup

---

## ✅ Checklist

- [ ] Downloaded all files (app.py, index.html, requirements.txt, README.md)
- [ ] Installed Python 3.8+
- [ ] Ran `pip install -r requirements.txt`
- [ ] Started backend: `python app.py`
- [ ] Opened `index.html` in browser
- [ ] Created account or logged in
- [ ] Can see dashboard

**All checked? You're ready to go! 🎉**

---

## 📞 Common Questions

**Q: Is my data secure?**
A: This is a demo. For production, use real password hashing (bcrypt), HTTPS, etc.

**Q: Can I use this on my phone?**
A: Yes! Open the HTML file on your phone's browser.

**Q: How do I backup my data?**
A: Copy the `gryfftwin.db` file. That's your entire database!

**Q: Can multiple users login?**
A: Yes! Each user has separate data stored in the database.

---

**Happy budgeting! 💰✨**

Questions? Check the README.md for more details!
