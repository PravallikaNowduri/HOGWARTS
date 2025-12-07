"""
GryffinTwin Flask Backend
Financial Management System with SQLite3
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os
import json

# Initialize Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gryfftwin.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database
db = SQLAlchemy(app)

# ==================== DATABASE MODELS ====================

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    expenses = db.relationship('Expense', backref='user', lazy=True, cascade='all, delete-orphan')
    goals = db.relationship('Goal', backref='user', lazy=True, cascade='all, delete-orphan')
    transactions = db.relationship('Transaction', backref='user', lazy=True, cascade='all, delete-orphan')
    alerts = db.relationship('SecurityAlert', backref='user', lazy=True, cascade='all, delete-orphan')

class Expense(db.Model):
    __tablename__ = 'expenses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    status = db.Column(db.String(50), default='Completed')

class Goal(db.Model):
    __tablename__ = 'goals'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    target_amount = db.Column(db.Float, nullable=False)
    current_amount = db.Column(db.Float, default=0)
    status = db.Column(db.String(50), default='Active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    type = db.Column(db.String(50), nullable=False)  # income or expense
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    description = db.Column(db.String(255))

class SecurityAlert(db.Model):
    __tablename__ = 'security_alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    alert_type = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    resolved = db.Column(db.Boolean, default=False)

# ==================== HELPER FUNCTIONS ====================

def check_login():
    """Check if user is logged in"""
    if 'user_id' not in session:
        return None
    user = User.query.get(session['user_id'])
    return user

def login_required(f):
    """Decorator for routes that require login"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not check_login():
            if request.path.startswith('/api/'):
                return jsonify({'error': 'Unauthorized'}), 401
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== AUTHENTICATION ROUTES ====================

@app.route('/')
def index():
    if check_login():
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        email = data.get('email')
        password = data.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.password == password:  # In production, use bcrypt!
            session['user_id'] = user.id
            if request.is_json:
                return jsonify({'success': True, 'user': {
                    'id': user.id,
                    'email': user.email,
                    'name': user.name
                }})
            return redirect(url_for('dashboard'))
        
        if request.is_json:
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
        return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        
        if User.query.filter_by(email=email).first():
            if request.is_json:
                return jsonify({'success': False, 'error': 'Email already registered'}), 400
            return render_template('login.html', error='Email already registered')
        
        user = User(email=email, password=password, name=name)  # In production, use bcrypt!
        db.session.add(user)
        db.session.commit()
        
        session['user_id'] = user.id
        if request.is_json:
            return jsonify({'success': True, 'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name
            }})
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ==================== PAGE ROUTES ====================

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=check_login())

@app.route('/expenses')
@login_required
def expenses():
    return render_template('expenses.html', user=check_login())

@app.route('/goals')
@login_required
def goals():
    return render_template('goals.html', user=check_login())

@app.route('/analytics')
@login_required
def analytics():
    return render_template('analytics.html', user=check_login())

@app.route('/security')
@login_required
def security():
    return render_template('security.html', user=check_login())

# ==================== API ROUTES - DASHBOARD ====================

@app.route('/api/dashboard', methods=['GET'])
@login_required
def api_dashboard():
    user = check_login()
    expenses = Expense.query.filter_by(user_id=user.id).all()
    goals = Goal.query.filter_by(user_id=user.id).all()
    transactions = Transaction.query.filter_by(user_id=user.id).all()
    
    total_expenses = sum(e.amount for e in expenses)
    total_income = sum(t.amount for t in transactions if t.type == 'income')
    balance = total_income - total_expenses
    
    goal_progress = 0
    if goals:
        total_goal = sum(g.target_amount for g in goals)
        current_total = sum(g.current_amount for g in goals)
        goal_progress = round((current_total / total_goal * 100), 1) if total_goal > 0 else 0
    
    return jsonify({
        'balance': balance,
        'total_expenses': total_expenses,
        'total_income': total_income,
        'goal_progress': goal_progress,
        'active_goals': len([g for g in goals if g.status == 'Active']),
        'recent_transactions': len(transactions)
    })

# ==================== API ROUTES - EXPENSES ====================

@app.route('/api/expenses', methods=['GET'])
@login_required
def api_get_expenses():
    user = check_login()
    expenses = Expense.query.filter_by(user_id=user.id).order_by(Expense.date.desc()).all()
    total = sum(e.amount for e in expenses)
    
    return jsonify({
        'total': total,
        'expenses': [{
            'id': e.id,
            'category': e.category,
            'description': e.description,
            'amount': e.amount,
            'date': e.date.strftime('%Y-%m-%d'),
            'status': e.status
        } for e in expenses]
    })

@app.route('/api/expenses', methods=['POST'])
@login_required
def api_add_expense():
    user = check_login()
    data = request.get_json()
    
    expense = Expense(
        user_id=user.id,
        category=data.get('category'),
        description=data.get('description'),
        amount=float(data.get('amount'))
    )
    db.session.add(expense)
    db.session.commit()
    
    return jsonify({'success': True, 'id': expense.id}), 201

@app.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
@login_required
def api_delete_expense(expense_id):
    user = check_login()
    expense = Expense.query.get(expense_id)
    
    if not expense or expense.user_id != user.id:
        return jsonify({'error': 'Not found'}), 404
    
    db.session.delete(expense)
    db.session.commit()
    return jsonify({'success': True})

# ==================== API ROUTES - GOALS ====================

@app.route('/api/goals', methods=['GET'])
@login_required
def api_get_goals():
    user = check_login()
    goals = Goal.query.filter_by(user_id=user.id).all()
    
    return jsonify([{
        'id': g.id,
        'name': g.name,
        'description': g.description,
        'target_amount': g.target_amount,
        'current_amount': g.current_amount,
        'progress': round((g.current_amount / g.target_amount * 100), 1) if g.target_amount > 0 else 0,
        'status': g.status
    } for g in goals])

@app.route('/api/goals', methods=['POST'])
@login_required
def api_add_goal():
    user = check_login()
    data = request.get_json()
    
    goal = Goal(
        user_id=user.id,
        name=data.get('name'),
        description=data.get('description'),
        target_amount=float(data.get('target_amount'))
    )
    db.session.add(goal)
    db.session.commit()
    
    return jsonify({'success': True, 'id': goal.id}), 201

@app.route('/api/goals/<int:goal_id>', methods=['PATCH'])
@login_required
def api_update_goal(goal_id):
    user = check_login()
    goal = Goal.query.get(goal_id)
    
    if not goal or goal.user_id != user.id:
        return jsonify({'error': 'Not found'}), 404
    
    data = request.get_json()
    if 'current_amount' in data:
        goal.current_amount = float(data['current_amount'])
    if 'status' in data:
        goal.status = data['status']
    
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/goals/<int:goal_id>', methods=['DELETE'])
@login_required
def api_delete_goal(goal_id):
    user = check_login()
    goal = Goal.query.get(goal_id)
    
    if not goal or goal.user_id != user.id:
        return jsonify({'error': 'Not found'}), 404
    
    db.session.delete(goal)
    db.session.commit()
    return jsonify({'success': True})

# ==================== API ROUTES - ANALYTICS ====================

@app.route('/api/analytics', methods=['GET'])
@login_required
def api_analytics():
    user = check_login()
    expenses = Expense.query.filter_by(user_id=user.id).all()
    transactions = Transaction.query.filter_by(user_id=user.id).all()
    
    total_expenses = sum(e.amount for e in expenses)
    total_income = sum(t.amount for t in transactions if t.type == 'income')
    net_savings = total_income - total_expenses
    
    # Expenses by category
    category_breakdown = {}
    for e in expenses:
        category_breakdown[e.category] = category_breakdown.get(e.category, 0) + e.amount
    
    return jsonify({
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_savings': net_savings,
        'savings_rate': round((net_savings / total_income * 100), 1) if total_income > 0 else 0,
        'category_breakdown': category_breakdown,
        'expense_count': len(expenses)
    })

# ==================== API ROUTES - SECURITY ====================

@app.route('/api/security', methods=['GET'])
@login_required
def api_security():
    user = check_login()
    alerts = SecurityAlert.query.filter_by(user_id=user.id).all()
    unresolved = [a for a in alerts if not a.resolved]
    
    return jsonify({
        'security_status': 'Excellent' if len(unresolved) == 0 else 'Warning',
        'total_alerts': len(alerts),
        'unresolved_alerts': len(unresolved),
        'two_factor_enabled': True,
        'recent_alerts': [{
            'id': a.id,
            'type': a.alert_type,
            'message': a.message,
            'timestamp': a.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        } for a in unresolved[-5:]]
    })

@app.route('/api/security/alert', methods=['POST'])
@login_required
def api_add_alert():
    user = check_login()
    data = request.get_json()
    
    alert = SecurityAlert(
        user_id=user.id,
        alert_type=data.get('alert_type'),
        message=data.get('message')
    )
    db.session.add(alert)
    db.session.commit()
    
    return jsonify({'success': True}), 201

# ==================== HEALTH CHECK ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'GryffinTwin Flask API is running'})

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error'}), 500

# ==================== CREATE TABLES AND RUN ====================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✓ Database tables created")
    
    print("🚀 Starting GryffinTwin Flask Server...")
    print("📍 Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)
