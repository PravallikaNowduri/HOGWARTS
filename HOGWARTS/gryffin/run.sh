#!/bin/bash
# GryffinTwin Setup & Run Script

echo "🏰 GryffinTwin - Financial Management System"
echo "==========================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

echo "✓ Python 3 found"

# Check pip
if ! command -v pip &> /dev/null; then
    echo "❌ pip not found. Please install pip"
    exit 1
fi

echo "✓ pip found"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✓ Dependencies installed"
echo ""

# Start server
echo "🚀 Starting GryffinTwin backend..."
echo ""
echo "Backend will run on: http://localhost:8000"
echo "API Docs available at: http://localhost:8000/docs"
echo ""
echo "Open index.html in your browser to start using the app!"
echo "Press Ctrl+C to stop the server"
echo ""

python app.py
