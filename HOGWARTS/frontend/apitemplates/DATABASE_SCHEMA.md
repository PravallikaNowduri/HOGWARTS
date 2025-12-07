# GryffinTwin Database Schema & API Documentation

## Database Architecture

### ER Diagram
```
┌─────────────────┐
│     USERS       │
├─────────────────┤
│ id (PK)         │
│ name            │
│ email (UNIQUE)  │
│ password        │
│ created_at      │
└────────┬────────┘
         │
         ├─────────────────────────┐
         │                         │
         ▼                         ▼
    ┌──────────────┐      ┌──────────────┐
    │  EXPENSES    │      │    GOALS     │
    ├──────────────┤      ├──────────────┤
    │ id (PK)      │      │ id (PK)      │
    │ user_id (FK) │      │ user_id (FK) │
    │ category     │      │ name         │
    │ description  │      │ target_amt   │
    │ amount       │      │ current_amt  │
    │ date         │      │ icon         │
    │ status       │      │ created_at   │
    │ created_at   │      │              │
    └──────────────┘      └──────────────┘
```

---

## Database Tables

### 1. USERS Table

**Purpose**: Store user account information

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | User unique identifier |
| name | VARCHAR(120) | NOT NULL | User full name |
| email | VARCHAR(120) | UNIQUE, NOT NULL | User email (login credential) |
| password | VARCHAR(255) | NOT NULL | Hashed password |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Account creation timestamp |

**SQL**:
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Sample Data**:
```json
{
  "id": 1,
  "name": "Demo User",
  "email": "demo@example.com",
  "password": "pbkdf2:sha256:...",
  "created_at": "2024-12-06T10:30:00"
}
```

---

### 2. EXPENSES Table

**Purpose**: Store user expense transactions

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Expense unique identifier |
| user_id | INTEGER | FOREIGN KEY, NOT NULL | Reference to user |
| category | VARCHAR(50) | NOT NULL | Expense category (Food, Transport, etc.) |
| description | VARCHAR(255) | NOT NULL | Expense description |
| amount | FLOAT | NOT NULL | Expense amount in currency |
| date | DATETIME | DEFAULT CURRENT_TIMESTAMP | Transaction date |
| status | VARCHAR(20) | DEFAULT 'completed' | Status (completed, pending, failed) |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |

**SQL**:
```sql
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    category VARCHAR(50) NOT NULL,
    description VARCHAR(255) NOT NULL,
    amount FLOAT NOT NULL,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'completed',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**Sample Data**:
```json
{
  "id": 1,
  "user_id": 1,
  "category": "Food",
  "description": "Grocery shopping",
  "amount": 85.50,
  "date": "2024-12-06T14:30:00",
  "status": "completed",
  "created_at": "2024-12-06T14:30:00"
}
```

**Common Categories**:
- Food
- Transport
- Entertainment
- Shopping
- Utilities
- Healthcare
- Education

---

### 3. GOALS Table

**Purpose**: Store user financial goals

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Goal unique identifier |
| user_id | INTEGER | FOREIGN KEY, NOT NULL | Reference to user |
| name | VARCHAR(120) | NOT NULL | Goal name/title |
| target_amount | FLOAT | NOT NULL | Goal target amount |
| current_amount | FLOAT | DEFAULT 0 | Currently saved amount |
| icon | VARCHAR(50) | DEFAULT '🎯' | Goal emoji icon |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Goal creation timestamp |

**SQL**:
```sql
CREATE TABLE goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name VARCHAR(120) NOT NULL,
    target_amount FLOAT NOT NULL,
    current_amount FLOAT DEFAULT 0,
    icon VARCHAR(50) DEFAULT '🎯',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**Sample Data**:
```json
{
  "id": 1,
  "user_id": 1,
  "name": "Emergency Fund",
  "target_amount": 10000,
  "current_amount": 6500,
  "icon": "🏦",
  "created_at": "2024-12-06T10:30:00"
}
```

**Common Icons**:
- 🏦 Emergency Fund
- ✈️ Vacation/Travel
- 🚗 Car Purchase
- 📈 Investment
- 🎓 Education
- 🏠 House

---

## API Endpoints

### Authentication Endpoints

#### POST `/api/auth/register`
**Description**: Create a new user account

**Request**:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securePassword123"
}
```

**Response** (201):
```json
{
  "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "tokenType": "bearer",
  "user": {
    "id": 2,
    "name": "John Doe",
    "email": "john@example.com",
    "created_at": "2024-12-06T15:00:00"
  }
}
```

---

#### POST `/api/auth/login`
**Description**: Authenticate user and get token

**Request**:
```json
{
  "email": "demo@example.com",
  "password": "demo123"
}
```

**Response** (200):
```json
{
  "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "tokenType": "bearer",
  "user": {
    "id": 1,
    "name": "Demo User",
    "email": "demo@example.com",
    "created_at": "2024-12-06T10:30:00"
  }
}
```

---

### Dashboard Endpoints

#### GET `/api/dashboard/summary`
**Auth**: Required (Bearer token)

**Description**: Get financial dashboard overview

**Response** (200):
```json
{
  "totalBalance": 50000.00,
  "monthlyExpenses": 3240.50,
  "budgetPercentage": 77,
  "investments": 12450.00,
  "goalsProgress": 68,
  "activeGoals": 4,
  "securityStatus": "Secured",
  "financialScore": 850,
  "balanceChange": 12.5,
  "investmentReturn": 8.2
}
```

---

### Expense Endpoints

#### GET `/api/expenses`
**Auth**: Required

**Description**: Get all expenses for logged-in user

**Query Parameters**:
- None (gets all expenses)

**Response** (200):
```json
{
  "totalExpenses": 3240.50,
  "monthlyBudget": 4200.00,
  "remainingBudget": 959.50,
  "budgetPercentage": 77,
  "expenses": [
    {
      "id": 1,
      "category": "Food",
      "description": "Grocery shopping",
      "amount": 85.50,
      "date": "2024-12-06T14:30:00",
      "status": "completed",
      "created_at": "2024-12-06T14:30:00"
    }
  ]
}
```

---

#### POST `/api/expenses`
**Auth**: Required

**Description**: Create new expense

**Request**:
```json
{
  "category": "Transport",
  "description": "Taxi to airport",
  "amount": 45.00,
  "date": "2024-12-06T10:00:00",
  "status": "completed"
}
```

**Response** (201):
```json
{
  "id": 25,
  "category": "Transport",
  "description": "Taxi to airport",
  "amount": 45.00,
  "date": "2024-12-06T10:00:00",
  "status": "completed",
  "created_at": "2024-12-06T14:30:00"
}
```

---

#### GET `/api/expenses/<expense_id>`
**Auth**: Required

**Description**: Get specific expense

**Response** (200):
```json
{
  "id": 1,
  "category": "Food",
  "description": "Grocery shopping",
  "amount": 85.50,
  "date": "2024-12-06T14:30:00",
  "status": "completed",
  "created_at": "2024-12-06T14:30:00"
}
```

---

#### PUT `/api/expenses/<expense_id>`
**Auth**: Required

**Description**: Update existing expense

**Request**:
```json
{
  "amount": 95.00,
  "status": "pending"
}
```

**Response** (200):
```json
{
  "id": 1,
  "category": "Food",
  "description": "Grocery shopping",
  "amount": 95.00,
  "date": "2024-12-06T14:30:00",
  "status": "pending",
  "created_at": "2024-12-06T14:30:00"
}
```

---

#### DELETE `/api/expenses/<expense_id>`
**Auth**: Required

**Description**: Delete expense

**Response** (200):
```json
{
  "message": "Expense deleted"
}
```

---

### Goal Endpoints

#### GET `/api/goals`
**Auth**: Required

**Description**: Get all goals for user

**Response** (200):
```json
{
  "goals": [
    {
      "id": 1,
      "name": "Emergency Fund",
      "targetAmount": 10000,
      "currentAmount": 6500,
      "icon": "🏦",
      "created_at": "2024-12-06T10:30:00"
    },
    {
      "id": 2,
      "name": "Vacation",
      "targetAmount": 5000,
      "currentAmount": 2200,
      "icon": "✈️",
      "created_at": "2024-12-06T10:30:00"
    }
  ]
}
```

---

#### POST `/api/goals`
**Auth**: Required

**Description**: Create new goal

**Request**:
```json
{
  "name": "New Car",
  "targetAmount": 25000,
  "currentAmount": 5000,
  "icon": "🚗"
}
```

**Response** (201):
```json
{
  "id": 5,
  "name": "New Car",
  "targetAmount": 25000,
  "currentAmount": 5000,
  "icon": "🚗",
  "created_at": "2024-12-06T14:30:00"
}
```

---

#### PUT `/api/goals/<goal_id>`
**Auth**: Required

**Description**: Update goal progress

**Request**:
```json
{
  "currentAmount": 8500
}
```

**Response** (200):
```json
{
  "id": 5,
  "name": "New Car",
  "targetAmount": 25000,
  "currentAmount": 8500,
  "icon": "🚗",
  "created_at": "2024-12-06T14:30:00"
}
```

---

#### DELETE `/api/goals/<goal_id>`
**Auth**: Required

**Description**: Delete goal

**Response** (200):
```json
{
  "message": "Goal deleted"
}
```

---

### Security & Analytics Endpoints

#### GET `/api/security`
**Auth**: Required

**Response** (200):
```json
{
  "overallSecurity": "Excellent",
  "loginActivity": "Normal",
  "fraudAlerts": 0,
  "passwordStrength": "Strong",
  "twoFactorAuth": true,
  "monitoredCards": 4
}
```

---

#### GET `/api/analytics`
**Auth**: Required

**Response** (200):
```json
{
  "monthlyTrend": [2100, 2300, 2150, 2450, 2200, 2400],
  "categoryBreakdown": {
    "Food": 450.50,
    "Transport": 280.00,
    "Entertainment": 125.00
  },
  "topCategories": [
    ["Food", 450.50],
    ["Transport", 280.00]
  ],
  "totalExpenses": 855.50,
  "averageExpense": 42.77
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Missing required fields"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid credentials"
}
```

### 404 Not Found
```json
{
  "detail": "Expense not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Data Types & Validation

| Field | Type | Min | Max | Format |
|-------|------|-----|-----|--------|
| amount | Float | 0 | 999999.99 | Decimal 2 places |
| name | String | 1 | 120 | Text |
| email | String | 5 | 120 | Email format |
| password | String | 6 | 255 | Hashed |
| category | String | 1 | 50 | Text |
| description | String | 1 | 255 | Text |

---

## Query Examples

### Get user expenses for current month
```sql
SELECT * FROM expenses 
WHERE user_id = ? 
AND STRFTIME('%Y-%m', date) = STRFTIME('%Y-%m', 'now')
ORDER BY date DESC;
```

### Calculate total by category
```sql
SELECT category, SUM(amount) as total 
FROM expenses 
WHERE user_id = ? 
GROUP BY category 
ORDER BY total DESC;
```

### Get goal progress percentage
```sql
SELECT 
  id, 
  name, 
  target_amount, 
  current_amount,
  ROUND((current_amount / target_amount) * 100, 2) as progress_percent
FROM goals 
WHERE user_id = ?;
```

---

**Database Version**: SQLite 3.x  
**Created**: 2024-12-06  
**Last Updated**: 2024-12-06
