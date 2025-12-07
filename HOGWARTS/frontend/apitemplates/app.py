# GryffinTwin Flask Backend with SQLite Database
# Complete REST API with CRUD operations

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from functools import wraps
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError


# Initialize Flask apppip install Flask Flask-CORS Flask-SQLAlchemy PyJWT Werkzeug SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gryffintwain.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'

# Initialize extensions
db = SQLAlchemy(app)
CORS(app)

# ==================== DATABASE MODELS ====================

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    expenses = db.relationship('Expense', backref='user', lazy=True, cascade='all, delete-orphan')
    goals = db.relationship('Goal', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }


class Expense(db.Model):
    __tablename__ = 'expenses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='completed')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category,
            'description': self.description,
            'amount': self.amount,
            'date': self.date.isoformat(),
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }


class Goal(db.Model):
    __tablename__ = 'goals'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    target_amount = db.Column(db.Float, nullable=False)
    current_amount = db.Column(db.Float, default=0)
    icon = db.Column(db.String(50), default='🎯')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'targetAmount': self.target_amount,
            'currentAmount': self.current_amount,
            'icon': self.icon,
            'created_at': self.created_at.isoformat()
        }


# ==================== AUTHENTICATION ====================

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'detail': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'detail': 'Token missing'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            if not current_user:
                return jsonify({'detail': 'User not found'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'detail': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'detail': 'Invalid token'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated


def create_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=7)
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token


# ==================== AUTH ENDPOINTS ====================

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login endpoint"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'detail': 'Email and password required'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'detail': 'Invalid credentials'}), 401
    
    token = create_token(user.id)
    
    return jsonify({
        'accessToken': token,
        'tokenType': 'bearer',
        'user': user.to_dict()
    }), 200


@app.route('/api/auth/register', methods=['POST'])
def register():
    """User registration endpoint"""
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({'detail': 'Name, email, and password required'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'detail': 'Email already registered'}), 400
    
    user = User(name=data['name'], email=data['email'])
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    token = create_token(user.id)
    
    return jsonify({
        'accessToken': token,
        'tokenType': 'bearer',
        'user': user.to_dict()
    }), 201


# ==================== DASHBOARD ENDPOINTS ====================

@app.route('/api/dashboard/summary', methods=['GET'])
@token_required
def dashboard_summary(current_user):
    """Get dashboard summary"""
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    goals = Goal.query.filter_by(user_id=current_user.id).all()
    
    total_balance = 50000.00
    monthly_expenses = sum(e.amount for e in expenses if e.date.month == datetime.now().month)
    total_expenses = sum(e.amount for e in expenses)
    investments = 12450.00
    
    goals_progress = 0
    if goals:
        total_current = sum(g.current_amount for g in goals)
        total_target = sum(g.target_amount for g in goals)
        goals_progress = int((total_current / total_target * 100)) if total_target > 0 else 0
    
    return jsonify({
        'totalBalance': total_balance,
        'monthlyExpenses': monthly_expenses,
        'budgetPercentage': int((monthly_expenses / 4200) * 100),
        'investments': investments,
        'goalsProgress': goals_progress,
        'activeGoals': len(goals),
        'securityStatus': 'Secured',
        'financialScore': 850,
        'balanceChange': 12.5,
        'investmentReturn': 8.2
    }), 200


# ==================== EXPENSES ENDPOINTS ====================

@app.route('/api/expenses', methods=['GET'])
@token_required
def get_expenses(current_user):
    """Get all expenses for the user"""
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    
    total_expenses = sum(e.amount for e in expenses)
    monthly_budget = 4200.00
    remaining_budget = monthly_budget - total_expenses
    
    return jsonify({
        'totalExpenses': total_expenses,
        'monthlyBudget': monthly_budget,
        'remainingBudget': remaining_budget,
        'budgetPercentage': int((total_expenses / monthly_budget) * 100),
        'expenses': [e.to_dict() for e in expenses]
    }), 200


@app.route('/api/expenses', methods=['POST'])
@token_required
def create_expense(current_user):
    """Create a new expense"""
    data = request.get_json()
    
    if not all(k in data for k in ['category', 'description', 'amount']):
        return jsonify({'detail': 'Missing required fields'}), 400
    
    expense = Expense(
        user_id=current_user.id,
        category=data['category'],
        description=data['description'],
        amount=float(data['amount']),
        date=datetime.fromisoformat(data.get('date', datetime.utcnow().isoformat())),
        status=data.get('status', 'completed')
    )
    
    db.session.add(expense)
    db.session.commit()
    
    return jsonify(expense.to_dict()), 201


@app.route('/api/expenses/<int:expense_id>', methods=['GET'])
@token_required
def get_expense(current_user, expense_id):
    """Get a specific expense"""
    expense = Expense.query.get(expense_id)
    
    if not expense or expense.user_id != current_user.id:
        return jsonify({'detail': 'Expense not found'}), 404
    
    return jsonify(expense.to_dict()), 200


@app.route('/api/expenses/<int:expense_id>', methods=['PUT'])
@token_required
def update_expense(current_user, expense_id):
    """Update an expense"""
    expense = Expense.query.get(expense_id)
    
    if not expense or expense.user_id != current_user.id:
        return jsonify({'detail': 'Expense not found'}), 404
    
    data = request.get_json()
    
    if 'category' in data:
        expense.category = data['category']
    if 'description' in data:
        expense.description = data['description']
    if 'amount' in data:
        expense.amount = float(data['amount'])
    if 'status' in data:
        expense.status = data['status']
    
    db.session.commit()
    
    return jsonify(expense.to_dict()), 200


@app.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
@token_required
def delete_expense(current_user, expense_id):
    """Delete an expense"""
    expense = Expense.query.get(expense_id)
    
    if not expense or expense.user_id != current_user.id:
        return jsonify({'detail': 'Expense not found'}), 404
    
    db.session.delete(expense)
    db.session.commit()
    
    return jsonify({'message': 'Expense deleted'}), 200


# ==================== GOALS ENDPOINTS ====================

@app.route('/api/goals', methods=['GET'])
@token_required
def get_goals(current_user):
    """Get all goals for the user"""
    goals = Goal.query.filter_by(user_id=current_user.id).all()
    
    return jsonify({
        'goals': [g.to_dict() for g in goals]
    }), 200


@app.route('/api/goals', methods=['POST'])
@token_required
def create_goal(current_user):
    """Create a new goal"""
    data = request.get_json()
    
    if not all(k in data for k in ['name', 'targetAmount']):
        return jsonify({'detail': 'Missing required fields'}), 400
    
    goal = Goal(
        user_id=current_user.id,
        name=data['name'],
        target_amount=float(data['targetAmount']),
        current_amount=float(data.get('currentAmount', 0)),
        icon=data.get('icon', '🎯')
    )
    
    db.session.add(goal)
    db.session.commit()
    
    return jsonify(goal.to_dict()), 201


@app.route('/api/goals/<int:goal_id>', methods=['GET'])
@token_required
def get_goal(current_user, goal_id):
    """Get a specific goal"""
    goal = Goal.query.get(goal_id)
    
    if not goal or goal.user_id != current_user.id:
        return jsonify({'detail': 'Goal not found'}), 404
    
    return jsonify(goal.to_dict()), 200


@app.route('/api/goals/<int:goal_id>', methods=['PUT'])
@token_required
def update_goal(current_user, goal_id):
    """Update a goal"""
    goal = Goal.query.get(goal_id)
    
    if not goal or goal.user_id != current_user.id:
        return jsonify({'detail': 'Goal not found'}), 404
    
    data = request.get_json()
    
    if 'name' in data:
        goal.name = data['name']
    if 'targetAmount' in data:
        goal.target_amount = float(data['targetAmount'])
    if 'currentAmount' in data:
        goal.current_amount = float(data['currentAmount'])
    if 'icon' in data:
        goal.icon = data['icon']
    
    db.session.commit()
    
    return jsonify(goal.to_dict()), 200


@app.route('/api/goals/<int:goal_id>', methods=['DELETE'])
@token_required
def delete_goal(current_user, goal_id):
    """Delete a goal"""
    goal = Goal.query.get(goal_id)
    
    if not goal or goal.user_id != current_user.id:
        return jsonify({'detail': 'Goal not found'}), 404
    
    db.session.delete(goal)
    db.session.commit()
    
    return jsonify({'message': 'Goal deleted'}), 200


# ==================== SECURITY ENDPOINTS ====================

@app.route('/api/security', methods=['GET'])
@token_required
def get_security(current_user):
    """Get security information"""
    return jsonify({
        'overallSecurity': 'Excellent',
        'loginActivity': 'Normal',
        'fraudAlerts': 0,
        'passwordStrength': 'Strong',
        'twoFactorAuth': True,
        'monitoredCards': 4
    }), 200


# ==================== ANALYTICS ENDPOINTS ====================

@app.route('/api/analytics', methods=['GET'])
@token_required
def get_analytics(current_user):
    """Get analytics data"""
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    
    # Calculate by category
    categories = {}
    for expense in expenses:
        if expense.category not in categories:
            categories[expense.category] = 0
        categories[expense.category] += expense.amount
    
    return jsonify({
        'monthlyTrend': [2100, 2300, 2150, 2450, 2200, 2400],
        'categoryBreakdown': categories,
        'topCategories': sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5],
        'totalExpenses': sum(e.amount for e in expenses),
        'averageExpense': sum(e.amount for e in expenses) / len(expenses) if expenses else 0
    }), 200


# ==================== DUMMY DATA ENDPOINTS ====================

@app.route('/api/seed', methods=['POST'])
def seed_database():
    """Seed the database with dummy data"""
    # Check if data already exists
    if User.query.first():
        return jsonify({'message': 'Database already seeded'}), 400
    
    # Create demo user
    user = User(name='Demo User', email='demo@example.com')
    user.set_password('demo123')
    db.session.add(user)
    db.session.flush()
    
    # Create dummy expenses
    expense_categories = ['Food', 'Transport', 'Entertainment', 'Shopping', 'Utilities']
    expense_descriptions = [
        'Grocery shopping', 'Taxi fare', 'Movie tickets', 'Online shopping', 'Electricity bill',
        'Restaurant lunch', 'Bus pass', 'Concert tickets', 'Clothing', 'Internet'
    ]
    
    for i in range(20):
        expense = Expense(
            user_id=user.id,
            category=expense_categories[i % len(expense_categories)],
            description=expense_descriptions[i % len(expense_descriptions)],
            amount=round(50 + (i * 15.5), 2),
            date=datetime.utcnow() - timedelta(days=i),
            status='completed' if i % 3 != 0 else 'pending'
        )
        db.session.add(expense)
    
    # Create dummy goals
    goals_data = [
        {'name': 'Emergency Fund', 'target': 10000, 'current': 6500, 'icon': '🏦'},
        {'name': 'Vacation', 'target': 5000, 'current': 2200, 'icon': '✈️'},
        {'name': 'Car Down Payment', 'target': 15000, 'current': 8900, 'icon': '🚗'},
        {'name': 'Investment Portfolio', 'target': 20000, 'current': 12450, 'icon': '📈'}
    ]
    
    for goal_data in goals_data:
        goal = Goal(
            user_id=user.id,
            name=goal_data['name'],
            target_amount=goal_data['target'],
            current_amount=goal_data['current'],
            icon=goal_data['icon']
        )
        db.session.add(goal)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Database seeded successfully',
        'demo_email': 'demo@example.com',
        'demo_password': 'demo123'
    }), 201


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'detail': 'Endpoint not found'}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({'detail': 'Internal server error'}), 500


# ==================== DATABASE INITIALIZATION ====================

@app.before_request
def initialize_db():
    """Initialize database if it doesn't exist"""
    if not os.path.exists('instance'):
        os.makedirs('instance')


# ==================== MAIN ====================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database tables created!")
    
    app.run(debug=True, host='127.0.0.1', port=8000)
