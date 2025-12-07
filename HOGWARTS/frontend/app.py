from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
import logging
import requests

app = Flask(__name__)
app.secret_key = 'gryffin-twin-secret-key-change-in-production'

# Explicit session cookie settings to avoid browser cookie/SameSite issues during local dev
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True

# Enable debug logging for tracing login/session behavior
logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.DEBUG)

# Backend URL configuration
BACKEND_URL = "http://127.0.0.1:8000/api"

# Route to mock/handle login if backend is empty (Helper for demo purposes)
# In a real scenario, you'd register via the backend API.
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not email or not password:
            error = '⚠️ Please fill in all fields'
        else:
            try:
                # Attempt to login via Backend API
                response = requests.post(f"{BACKEND_URL}/auth/login", json={
                    "email": email,
                    "password": password
                })
                
                if response.status_code == 200:
                    user_data = response.json()
                    session['user_id'] = user_data['id'] # Store ID for path parameters
                    session['user_email'] = user_data['email']
                    session['user_name'] = user_data['name']
                    
                    app.logger.info('User logged in: %s', email)
                    return redirect(url_for('dashboard'))
                elif response.status_code == 401:
                    error = '⚠️ Invalid email or password'
                else:
                    error = '⚠️ Login failed. Please try again.'
                    
            except requests.exceptions.ConnectionError:
                error = '⚠️ Backend server is unreachable. Is it running on port 8000?'
            except Exception as e:
                app.logger.error(f"Login error: {e}")
                error = '⚠️ An unexpected error occurred'

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Protected Routes
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Legacy session check: If user_id is string (email), force logout to get int ID
    if isinstance(session['user_id'], str):
        app.logger.info("Legacy session detected (string ID). Clearing session.")
        session.clear()
        return redirect(url_for('login'))

    try:
        user_id = session['user_id']
        response = requests.get(f"{BACKEND_URL}/dashboard/{user_id}")
        
        if response.status_code == 200:
            dashboard_data = response.json()
            # Map API response to template expected format if necessary
            # API returns: balance, total_expenses, total_income, goal_progress, active_goals, recent_transactions
            
            # The template expects a 'dashboard_data' object with specific fields.
            # We construct it from the API response.
            
            template_data = {
                'total_balance': dashboard_data.get('balance', 0),
                'expenses': dashboard_data.get('total_expenses', 0),
                'investments': 12450, # Mocked as backend doesn't have investment portfolio yet
                'goals_progress': dashboard_data.get('goal_progress', 0),
                'financial_score': 850, # Mocked
                'accounts': [ # Mocked as backend doesn't track specific accounts yet
                    {'name': 'Checking Account', 'type': 'Checking', 'balance': dashboard_data.get('balance', 0) * 0.4, 'status': 'Active'},
                    {'name': 'Savings Account', 'type': 'Savings', 'balance': dashboard_data.get('balance', 0) * 0.6, 'status': 'Active'}
                ]
            }
            
            return render_template('dashboard.html', 
                                 user_name=session.get('user_name', 'User'),
                                 user_email=session.get('user_email', ''),
                                 dashboard_data=template_data)
        else:
            error_details = f"Status: {response.status_code}\nResponse: {response.text}"
            app.logger.error(f"Backend API error: {error_details}")
            return render_template('error.html', message="Failed to load dashboard data from Backend.", details=error_details)
            
    except Exception as e:
        app.logger.error(f"Dashboard error: {e}")
        return render_template('error.html', message="An unexpected error occurred.", details=str(e))

@app.route('/expenses')
def expenses():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    try:
        user_id = session['user_id']
        response = requests.get(f"{BACKEND_URL}/expenses/{user_id}")
        
        if response.status_code == 200:
            data = response.json()
            return render_template('expenses.html', 
                                 user_name=session.get('user_name', 'User'),
                                 user_email=session.get('user_email', ''),
                                 expenses=data.get('expenses', []),
                                 total_expenses=data.get('total', 0),
                                 budget=5000) # Hardcoded budget for now
        return "Failed to load expenses"
    except Exception as e:
        return f"Error: {e}"

@app.route('/goals')
def goals():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    try:
        user_id = session['user_id']
        response = requests.get(f"{BACKEND_URL}/goals/{user_id}")
        
        if response.status_code == 200:
            goals_data = response.json()
            return render_template('goals.html', 
                                 user_name=session.get('user_name', 'User'),
                                 user_email=session.get('user_email', ''),
                                 goals=goals_data)
        return "Failed to load goals"
    except Exception as e:
        return f"Error: {e}"

@app.route('/analytics')
def analytics():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    try:
        user_id = session['user_id']
        response = requests.get(f"{BACKEND_URL}/analytics/{user_id}")
        
        if response.status_code == 200:
            analytics_data = response.json()
            return render_template('analytics.html', 
                                 user_name=session.get('user_name', 'User'),
                                 user_email=session.get('user_email', ''),
                                 analytics=analytics_data)
        return "Failed to load analytics"
    except Exception as e:
        return f"Error: {e}"

@app.route('/security')
def security():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    try:
        user_id = session['user_id']
        response = requests.get(f"{BACKEND_URL}/security/{user_id}")
        
        if response.status_code == 200:
            return render_template('security.html', 
                                 user_name=session.get('user_name', 'User'),
                                 user_email=session.get('user_email', ''),
                                 security_data=response.json())
        return "Failed to load security data"
    except Exception as e:
        return f"Error: {e}"

@app.route('/portfolio')
def portfolio():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    # Backend doesn't have portfolio endpoint yet, using static template
    return render_template('portfolio.html', 
                         user_name=session.get('user_name', 'User'),
                         user_email=session.get('user_email', ''))

@app.route('/myfam')
def myfam():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    # Backend doesn't have family endpoint yet, using static template
    return render_template('myfam.html', 
                         user_name=session.get('user_name', 'User'),
                         user_email=session.get('user_email', ''))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
