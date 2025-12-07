const express = require('express');
const session = require('express-session');
const bodyParser = require('body-parser');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = 5000;

// ===== MIDDLEWARE =====

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public')));

// Session configuration
app.use(session({
    secret: 'your-secret-key-change-in-production',
    resave: false,
    saveUninitialized: true,
    cookie: { 
        secure: false,  // set true if using HTTPS
        maxAge: 24 * 60 * 60 * 1000  // 24 hours
    }
}));

// View engine setup (EJS for dynamic templates)
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// ===== MOCK DATABASE =====

// Demo users (replace with real DB)
const USERS = {
    'user@example.com': {
        email: 'user@example.com',
        password: 'password123',
        name: 'Harry Potter',
        role: 'admin'
    },
    'hermione@gryffindor.com': {
        email: 'hermione@gryffindor.com',
        password: 'gryffindor123',
        name: 'Hermione Granger',
        role: 'user'
    },
    'ron@gryffindor.com': {
        email: 'ron@gryffindor.com',
        password: 'potter123',
        name: 'Ron Weasley',
        role: 'user'
    }
};

// Demo dashboard data
const DASHBOARD_DATA = {
    total_balance: 24580,
    expenses: 3240,
    investments: 12450,
    goals_progress: 68,
    financial_score: 850,
    accounts: [
        { name: 'Checking Account', type: 'Checking', balance: 5230, status: 'Active' },
        { name: 'Savings Account', type: 'Savings', balance: 12350, status: 'Active' },
        { name: 'Money Market', type: 'Money Market', balance: 4800, status: 'Active' },
        { name: 'Business Account', type: 'Business', balance: 2200, status: 'Active' }
    ]
};

const EXPENSES_DATA = [
    { date: 'Dec 05, 2025', category: 'Food', description: 'Lunch at Restaurant', amount: 45.50, status: 'Completed' },
    { date: 'Dec 04, 2025', category: 'Transport', description: 'Uber Trip', amount: 32.00, status: 'Completed' },
    { date: 'Dec 03, 2025', category: 'Entertainment', description: 'Movie Tickets', amount: 28.00, status: 'Completed' },
    { date: 'Dec 02, 2025', category: 'Shopping', description: 'Grocery Shopping', amount: 156.75, status: 'Completed' },
    { date: 'Dec 01, 2025', category: 'Health', description: 'Pharmacy Purchase', amount: 65.20, status: 'Completed' },
    { date: 'Nov 30, 2025', category: 'Education', description: 'Online Course', amount: 99.99, status: 'Pending' }
];

// ===== MIDDLEWARE: Check Authentication =====

function isAuthenticated(req, res, next) {
    if (req.session.user) {
        return next();
    }
    res.redirect('/');
}

// ===== ROUTES =====

// Root - redirect to login or dashboard
app.get('/', (req, res) => {
    if (req.session.user) {
        return res.redirect('/dashboard');
    }
    res.render('login', { error: req.query.error || null });
});

// LOGIN - GET (show form)
app.get('/login', (req, res) => {
    if (req.session.user) {
        return res.redirect('/dashboard');
    }
    res.render('login', { error: null });
});

// LOGIN - POST (handle form)
app.post('/login', (req, res) => {
    const { email, password } = req.body;

    if (!email || !password) {
        return res.render('login', { error: 'Please enter email and password.' });
    }

    const user = USERS[email];

    if (!user || user.password !== password) {
        return res.render('login', { error: 'Invalid email or password.' });
    }

    // Set session
    req.session.user = {
        email: user.email,
        name: user.name,
        role: user.role
    };

    res.redirect('/dashboard');
});

// DASHBOARD
app.get('/dashboard', isAuthenticated, (req, res) => {
    res.render('dashboard', {
        user: req.session.user,
        data: DASHBOARD_DATA
    });
});

// EXPENSES
app.get('/expenses', isAuthenticated, (req, res) => {
    const totalExpenses = EXPENSES_DATA.reduce((sum, exp) => sum + exp.amount, 0);
    res.render('expenses', {
        user: req.session.user,
        expenses: EXPENSES_DATA,
        total_expenses: totalExpenses,
        budget: 4200
    });
});

// ANALYTICS
app.get('/analytics', isAuthenticated, (req, res) => {
    res.render('analytics', {
        user: req.session.user
    });
});

// GOALS
app.get('/goals', isAuthenticated, (req, res) => {
    res.render('goals', {
        user: req.session.user
    });
});

// SECURITY
app.get('/security', isAuthenticated, (req, res) => {
    res.render('security', {
        user: req.session.user
    });
});

// PORTFOLIO
app.get('/portfolio', isAuthenticated, (req, res) => {
    res.render('portfolio', {
        user: req.session.user
    });
});

// MYFAM
app.get('/myfam', isAuthenticated, (req, res) => {
    res.render('myfam', {
        user: req.session.user
    });
});

// LOGOUT
app.get('/logout', (req, res) => {
    req.session.destroy((err) => {
        if (err) {
            return res.send('Error logging out');
        }
        res.redirect('/');
    });
});

// ===== API ENDPOINTS =====

// API: Get user info
app.get('/api/user', isAuthenticated, (req, res) => {
    res.json({
        success: true,
        user: req.session.user
    });
});

// API: Get dashboard data
app.get('/api/dashboard', isAuthenticated, (req, res) => {
    res.json({
        success: true,
        data: DASHBOARD_DATA
    });
});

// API: Get expenses
app.get('/api/expenses', isAuthenticated, (req, res) => {
    res.json({
        success: true,
        expenses: EXPENSES_DATA,
        total: EXPENSES_DATA.reduce((sum, exp) => sum + exp.amount, 0)
    });
});

// 404 - Not Found
app.use((req, res) => {
    res.status(404).render('404', { user: req.session.user || null });
});

// ===== START SERVER =====

app.listen(PORT, () => {
    console.log(`✨ GryffinTwin server running at http://localhost:${PORT}`);
    console.log(`📝 Demo login: user@example.com / password123`);
});
