#!/usr/bin/env bash
# quick_run.sh — setup and launch the dashboard

set -e

echo "🚀 DebtSage - Quick Setup & Run"
echo "================================"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r app/requirements.txt

# Check if data exists
if [ ! -f "data/data.csv" ]; then
    echo "❌ Error: data/data.csv not found!"
    echo "Please ensure the dataset is in the data/ folder."
    exit 1
fi

echo "✅ Setup complete!"
echo ""
echo "🎯 Starting Streamlit dashboard..."
streamlit run app/streamlit_app.py
