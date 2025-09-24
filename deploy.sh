#!/bin/bash

# Vercel Deployment Script for Payroll Management System

echo "🚀 Deploying Payroll Management System to Vercel..."
echo

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI is not installed."
    echo "📦 Install it with: npm i -g vercel"
    echo "🔗 More info: https://vercel.com/cli"
    exit 1
fi

echo "✅ Vercel CLI found"

# Check if user is logged in
if ! vercel whoami &> /dev/null; then
    echo "🔐 Please log in to Vercel first:"
    vercel login
fi

echo "✅ Vercel authentication verified"

# Show current project structure
echo
echo "📁 Project files ready for deployment:"
echo "├── api/index.py (serverless entry point)"
echo "├── templates/ (HTML templates)"
echo "├── vercel.json (deployment config)"
echo "├── requirements.txt (Python dependencies)"
echo "└── .vercelignore (excluded files)"
echo

# Deploy
echo "🚀 Starting deployment..."
if [ "$1" = "--prod" ]; then
    echo "📦 Deploying to PRODUCTION..."
    vercel --prod
else
    echo "🧪 Deploying to PREVIEW..."
    echo "💡 Use './deploy.sh --prod' for production deployment"
    vercel
fi

echo
echo "✅ Deployment complete!"
echo
echo "📋 Next steps:"
echo "1. Test your deployed application"
echo "2. Check Vercel dashboard for logs and analytics"
echo "3. Consider setting up a persistent database for production use"
echo
echo "⚠️  Note: SQLite database will reset on each serverless function restart"
echo "💡 For production, consider using Vercel Postgres or another cloud database"