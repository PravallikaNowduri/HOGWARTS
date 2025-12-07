# GryffinTwin - FastAPI Backend Integration Guide

## Overview
All HTML files have been updated to connect with a FastAPI backend. The files now make API calls instead of using static data.

## Files Created
- ✅ `login-api.html` - Login page with FastAPI authentication
- ✅ `dashboard-api.html` - Dashboard with dynamic data
- ✅ `expenses-api.html` - Expenses tracker with API integration
- ✅ `security-api.html` - Security page with API data
- ✅ `goals-api.html` - Goals tracker with dynamic goals
- ✅ `analytics-api.html` - Analytics with charts from API data

## Setup Instructions

### 1. Configure API Base URL
In each HTML file, locate this line at the top of the `<script>` section:
```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

Change `http://localhost:8000/api` to your FastAPI server URL if different.

### 2. CORS Configuration
Your FastAPI backend must have CORS enabled. Add this to your FastAPI app:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Required API Endpoints

### Authentication
**POST** `/api/auth/login`
- Request body:
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```
- Response:
```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "name": "User Name",
    "email": "user@example.com"
  }
}
```

### Dashboard
**GET** `/api/dashboard/summary`
- Headers: `Authorization: Bearer {token}`
- Response:
```json
{
  "total_balance": 24580,
  "balance_change": 12.5,
  "monthly_expenses": 3240,
  "budget_percentage": 78,
  "investments": 12450,
  "investment_return": 8.2,
  "goals_progress": 68,
  "active_goals": 4,
  "security_status": "Secure",
  "financial_score": 850
}
```

### Expenses
**GET** `/api/expenses`
- Headers: `Authorization: Bearer {token}`
- Response:
```json
{
  "total_expenses": 3240,
  "monthly_budget": 4200,
  "remaining_budget": 960,
  "budget_percentage": 77,
  "expenses": [
    {
      "date": "2025-12-05",
      "category": "🍔 Food",
      "description": "Lunch at Restaurant",
      "amount": 45.50,
      "status": "✓ Completed"
    }
  ]
}
```

### Security
**GET** `/api/security`
- Headers: `Authorization: Bearer {token}`
- Response:
```json
{
  "overall_security": "Excellent",
  "login_activity": "Normal",
  "fraud_alerts": 0,
  "password_strength": "Strong",
  "two_factor_auth": true,
  "monitored_cards": 4
}
```

### Goals
**GET** `/api/goals`
- Headers: `Authorization: Bearer {token}`
- Response:
```json
{
  "goals": [
    {
      "id": 1,
      "name": "Emergency Fund",
      "icon": "🏦",
      "target_amount": 15000,
      "current_amount": 10200,
      "status": "Active"
    }
  ]
}
```

### Analytics
**GET** `/api/analytics`
- Headers: `Authorization: Bearer {token}`
- Response:
```json
{
  "total_income": 18500,
  "total_expenses": 9240,
  "net_savings": 9260,
  "savings_rate": 50,
  "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
  "income_data": [1500, 1600, 1700, 1800, 1900, 2000],
  "expense_data": [800, 850, 900, 750, 900, 850],
  "categories": ["Shopping", "Food", "Transport", "Entertainment", "Healthcare", "Other"],
  "category_amounts": [2450, 1890, 1560, 980, 720, 640]
}
```

## Authentication Flow

1. User enters email and password on login-api.html
2. Frontend sends POST request to `/api/auth/login`
3. Backend validates credentials and returns JWT token
4. Frontend stores token in localStorage:
   - `access_token` - JWT token for API requests
   - `token_type` - "bearer"
   - `user` - User object (JSON string)
5. All subsequent API calls include token in Authorization header:
   ```javascript
   headers: {
     'Authorization': `Bearer ${token}`
   }
   ```
6. If token is invalid (401 response), user is redirected to login

## Token Management

Tokens are stored in localStorage with keys:
- `access_token` - The JWT token
- `token_type` - Token type (usually "bearer")
- `user` - Stringified user object

When user logs out, all three are cleared.

## Error Handling

The frontend checks for:
- **401 Unauthorized** - Token expired or invalid → Redirect to login
- **Network errors** - Connection issues → Display error message with API URL for debugging

## Testing the Frontend

1. Make sure your FastAPI server is running on `http://localhost:8000`
2. Open `login-api.html` in browser
3. The default credentials are displayed on the login page
4. After login, you'll be redirected to dashboard-api.html
5. Navigation between pages works via the sidebar menu

## Debugging Tips

1. Check browser console (F12) for error messages
2. Check Network tab to see API requests and responses
3. Verify CORS is configured correctly in FastAPI
4. Ensure Authorization header format is: `Bearer {token}`
5. Check that token hasn't expired (implement refresh token for production)

## Production Checklist

- [ ] Update `API_BASE_URL` to production FastAPI URL
- [ ] Implement token refresh/expiration handling
- [ ] Add HTTPS to all API calls
- [ ] Implement proper error logging
- [ ] Add loading states and spinners
- [ ] Implement session timeout
- [ ] Add input validation on frontend
- [ ] Implement rate limiting on frontend
- [ ] Add user feedback/notifications
- [ ] Test with actual backend data

## File Naming Convention

- `*-api.html` - Files that connect to FastAPI backend
- Original files (dashboard.html, login.html, etc.) - Static demos without API

Use the `-api.html` versions in production with your FastAPI backend!