# 🚀 Deployment Guide

## Quick Deploy (One Command)

To build and deploy everything in one go:

```bash
./deploy.sh
```

This script will:
1. ✅ Generate PIQ pages from JSON data
2. ✅ Build the website with MkDocs  
3. ✅ Deploy to GitHub Pages
4. ✅ Keep JSON data private

## Manual Steps

If you prefer to run steps manually:

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Generate PIQ pages
python src/generate_piq.py

# 3. Build website
mkdocs build

# 4. Deploy to GitHub Pages
mkdocs gh-deploy
```

## Project Structure

```
📁 dpjb_web/
├── 📁 src/               # Python scripts
│   └── generate_piq.py   # PIQ generator
├── 📁 data/              # Private JSON files (not in git)
│   └── prelimsJson/      # Question data
├── 📁 docs/              # Website content
│   ├── 📁 piq/           # Generated PIQ pages
│   └── 📁 stylesheets/   # Custom CSS
├── 📁 venv/              # Python virtual environment
├── deploy.sh             # One-click deploy script
└── mkdocs.yml            # Site configuration
```

## Features Implemented

### ✅ Fixed Issues
- **Pink color scheme** - Matches main site theme
- **Question number circles** - Now resize properly for multi-digit numbers
- **Breadcrumb navigation** - Fixed all links
- **Markdown processing** - Tables and formatting work correctly
- **Private JSON data** - Files excluded from git repository
- **Organized code** - Python scripts moved to `src/` folder

### ✅ PIQ System Features
- **1,300+ questions** from 2011-2023
- **Individual question pages** for SEO
- **Markdown table support** for complex questions
- **Clean navigation** with Previous/Next buttons
- **Mobile responsive** design
- **Search functionality** through MkDocs

## Notes

- JSON files in `data/` folder are kept private and not pushed to GitHub
- Generated PIQ pages are committed to repository for static hosting
- Deploy script handles everything automatically
- Pink theme matches main website design