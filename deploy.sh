#!/bin/bash

# 📚 UPSC PIQ Website - Complete Build and Deploy Script
# This script handles everything: PIQ generation, building, and deployment

set -e  # Exit on any error

echo "🚀 Starting complete deployment process..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ Virtual environment not found!${NC}"
    echo -e "${YELLOW}💡 Please create one first: python3 -m venv venv${NC}"
    exit 1
fi

# Check if data directory exists
if [ ! -d "data" ]; then
    echo -e "${RED}❌ Data directory not found!${NC}"
    echo -e "${YELLOW}💡 Please ensure data/prelimsJson/ directory exists with JSON files${NC}"
    exit 1
fi

echo -e "${BLUE}📦 Step 1: Activating virtual environment...${NC}"
source venv/bin/activate

echo -e "${BLUE}📝 Step 2: Generating PIQ pages from JSON data...${NC}"
python src/generate_piq.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ PIQ pages generated successfully!${NC}"
else
    echo -e "${RED}❌ Failed to generate PIQ pages${NC}"
    exit 1
fi

echo -e "${BLUE}🔧 Step 3: Building website with MkDocs...${NC}"
mkdocs build

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Website built successfully!${NC}"
else
    echo -e "${RED}❌ Failed to build website${NC}"
    exit 1
fi

echo -e "${BLUE}🌐 Step 4: Deploying to GitHub Pages...${NC}"
mkdocs gh-deploy --clean

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Successfully deployed to GitHub Pages!${NC}"
    echo -e "${GREEN}🎉 Your website is now live!${NC}"
    echo ""
    echo -e "${YELLOW}📊 Deployment Summary:${NC}"
    echo -e "  • PIQ pages generated from JSON data"
    echo -e "  • Website built with MkDocs"
    echo -e "  • Deployed to GitHub Pages"
    echo -e "  • JSON data kept private (not pushed to repo)"
    echo ""
    echo -e "${BLUE}🔗 Your site should be available at:${NC}"
    echo -e "  https://$(git config --get remote.origin.url | sed 's/.*github.com[:/]\([^/]*\)\/\([^.]*\).*/\1.github.io\/\2/')"
else
    echo -e "${RED}❌ Failed to deploy to GitHub Pages${NC}"
    exit 1
fi

echo -e "${GREEN}🎯 Deployment completed successfully!${NC}"