#!/bin/bash
# Lighthouse AI - Databricks App Deployment Script
# Quick deployment guide for Databricks Apps

echo "🚀 Lighthouse AI - Databricks App Deployment"
echo "=============================================="
echo ""

echo "📋 Prerequisites Check:"
echo "----------------------"
echo ""

# Check required files
echo "Checking required files..."
if [ -f "app.yaml" ]; then
    echo "✅ app.yaml found"
else
    echo "❌ app.yaml missing"
    exit 1
fi

if [ -f "app.py" ]; then
    echo "✅ app.py found"
else
    echo "❌ app.py missing"
    exit 1
fi

if [ -f "requirements.txt" ]; then
    echo "✅ requirements.txt found"
else
    echo "❌ requirements.txt missing"
    exit 1
fi

echo ""
echo "=============================================="
echo ""
echo "🎯 Deployment Options:"
echo "----------------------"
echo ""
echo "OPTION 1: Deploy via Databricks UI"
echo "  1. Go to your Databricks workspace"
echo "  2. Navigate: Compute → Apps"
echo "  3. Click 'Create App'"
echo "  4. Select source: This folder"
echo "  5. Name: lighthouse-ai"
echo "  6. Click Deploy"
echo ""
echo "OPTION 2: Deploy via CLI"
echo "  databricks apps create lighthouse-ai --source-code-path ."
echo "  databricks apps deploy lighthouse-ai"
echo ""
echo "=============================================="
echo ""
echo "📊 After Deployment:"
echo "-------------------"
echo ""
echo "Your app will be available at:"
echo "https://<workspace>.cloud.databricks.com/apps/lighthouse-ai"
echo ""
echo "To check status:"
echo "  databricks apps get lighthouse-ai"
echo ""
echo "To view logs:"
echo "  databricks apps logs lighthouse-ai"
echo ""
echo "=============================================="
echo ""
echo "✅ Ready to deploy!"
echo ""
