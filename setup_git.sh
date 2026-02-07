#!/bin/bash

# Setup script for Asian Option Pricer GitHub repository
# Run this after cloning/creating the repo

echo "======================================"
echo "Asian Option Pricer - Git Setup"
echo "======================================"

# Step 1: Initialize Git (if not already done)
if [ ! -d ".git" ]; then
    echo "Initializing Git repository..."
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git already initialized"
fi

# Step 2: Create initial commit
echo ""
echo "Creating initial commit..."
git add .
git commit -m "Initial commit: Asian option Monte Carlo pricer with variance reduction

- Implemented three variance reduction methods (basic MC, antithetic variates, control variates)
- Achieved 73.8% variance reduction with control variate method
- Integrated real market data via yfinance
- Added comprehensive documentation and examples
- Created visualizations for convergence and performance analysis"

echo "✅ Initial commit created"

# Step 3: Instructions for GitHub
echo ""
echo "======================================"
echo "Next Steps:"
echo "======================================"
echo ""
echo "1. Create a new repository on GitHub:"
echo "   - Go to https://github.com/new"
echo "   - Name: asian-option-pricer"
echo "   - Description: Monte Carlo pricer for Asian options with variance reduction"
echo "   - Keep it PUBLIC (so recruiters can see it)"
echo "   - DON'T initialize with README (we already have one)"
echo ""
echo "2. Connect to GitHub and push:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/asian-option-pricer.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Add GitHub link to your CV:"
echo "   GitHub: github.com/YOUR_USERNAME/asian-option-pricer"
echo ""
echo "======================================"
echo "✅ Setup complete!"
echo "======================================"
