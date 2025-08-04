#!/usr/bin/env python3
"""
Generate clean PIQ pages with fixed navigation and minimalistic design.
Single file solution for UPSC Previous Year Questions.
"""

import json
import os
import re
from pathlib import Path
import markdown

def sanitize_filename(text):
    """Create a safe filename from question text."""
    clean_text = re.sub(r'<[^>]+>', '', text)
    clean_text = re.sub(r'[^\w\s-]', '', clean_text)
    clean_text = re.sub(r'[-\s]+', '-', clean_text)
    return clean_text[:50].strip('-').lower()

def process_markdown_content(text):
    """Convert markdown content to HTML while preserving structure."""
    if not text or not text.strip():
        return text
    
    # Initialize markdown processor with table extension
    md = markdown.Markdown(extensions=['tables', 'nl2br'])
    
    # Convert markdown to HTML
    html_content = md.convert(text.strip())
    
    return html_content

def create_breadcrumb(year=None, question_num=None):
    """Create clean breadcrumb navigation."""
    if question_num:
        return f"""<nav class="breadcrumb">
    <a href="../../">PIQ</a>
    <span>›</span>
    <a href="../">{year}</a>
    <span>›</span>
    <span>Question {question_num}</span>
</nav>"""
    elif year:
        return f"""<nav class="breadcrumb">
    <a href="../">PIQ</a>
    <span>›</span>
    <span>{year} Questions</span>
</nav>"""
    else:
        return f"""<nav class="breadcrumb">
    <span>PIQ</span>
</nav>"""

def create_question_page(question, year, question_num, output_dir, total_questions, all_questions):
    """Create clean individual question page."""
    question_id = question.get('id', f"{year}_q{question_num}")
    
    # Create filename
    filename = f"q{question_num:03d}-{sanitize_filename(question['question'])}.md"
    filepath = output_dir / filename
    
    # Clean question text
    question_text = question['question']
    clean_question = re.sub(r'<[^>]+>', '', question_text)
    clean_question = re.sub(r'\n+', ' ', clean_question)
    title = clean_question[:60].strip() + ("..." if len(clean_question) > 60 else "")
    
    # Calculate progress
    progress_percent = (question_num / total_questions) * 100
    
    # Process question text through markdown to handle tables and formatting
    processed_question_text = process_markdown_content(question_text)
    
    # Create content
    content = f"""---
title: "UPSC {year} Prelims Q{question_num}: {title}"
description: "UPSC Civil Services Preliminary Examination {year} Question {question_num} with options and answer"
keywords: "UPSC, Prelims, {year}, Question {question_num}, Civil Services, IAS, Previous Year Questions"
---

{create_breadcrumb(year, question_num)}

<div class="question-header" style="margin-bottom: 8px;">
    <div class="question-meta" style="padding: 0.5em 0;">
        <a href="../" class="year-badge">{year}</a>
        <span class="question-number">Question {question_num}</span>
        <span class="progress">{question_num}/{total_questions}</span>
    </div>
    <div class="progress-bar">
        <div class="progress-fill" style="width: {progress_percent:.1f}%"></div>
    </div>
</div>

<div class="question-content" style="padding: 0.5em 0;">
    <div class="question-text" style="font-size: 0.95em; line-height: 1.4;">
        {processed_question_text}
    </div>
    
    <div class="options">
"""
    
    # Add options
    correct_option = None
    for i, option in enumerate(question.get('options', []), 1):
        is_correct = option.get('correct', False)
        if is_correct:
            correct_option = i
        
        class_name = "option correct" if is_correct else "option"
        processed_option_text = process_markdown_content(option["value"])
        content += f'        <div class="{class_name}">\n'
        content += f'            <span class="option-letter">{chr(64+i)}</span>\n'
        content += f'            <span class="option-text" style="font-size: 0.95em; line-height: 1.4;">{processed_option_text}</span>\n'
        content += f'        </div>\n'
    
    content += "    </div>\n"
    
    # Add answer if available
    if correct_option:
        content += f"""
    <div class="answer-box">
        <strong>Correct Answer:</strong> Option {chr(64+correct_option)}
    </div>
"""
    
    # Add explanation if available
    explanation = question.get('explanation', '').strip()
    if explanation:
        processed_explanation = process_markdown_content(explanation)
        content += f"""
    <div class="explanation">
        <h4>Explanation</h4>
        <p>{processed_explanation}</p>
    </div>
"""
    
    content += "</div>\n\n"
    
    # Add navigation - use clean URLs without .md extension
    prev_num = question_num - 1 if question_num > 1 else None
    next_num = question_num + 1 if question_num < total_questions else None
    
    content += '<div class="question-nav">\n'
    
    if prev_num:
        prev_question = all_questions[prev_num - 1]  # 0-indexed
        prev_filename = f"q{prev_num:03d}-{sanitize_filename(prev_question['question'])}"
        content += f'    <a href="../{prev_filename}/" class="nav-btn prev">← Previous</a>\n'
    else:
        content += '    <div></div>\n'
    
    content += '    <a href="../" class="nav-btn center">All Questions</a>\n'
    
    if next_num:
        next_question = all_questions[next_num - 1]  # 0-indexed
        next_filename = f"q{next_num:03d}-{sanitize_filename(next_question['question'])}"
        content += f'    <a href="../{next_filename}/" class="nav-btn next">Next →</a>\n'
    else:
        content += '    <div></div>\n'
    
    content += '</div>\n'
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filename

def create_year_index(year, questions, output_dir):
    """Create clean year index page."""
    index_path = output_dir / "index.md"
    
    total_questions = len(questions)
    
    content = f"""---
title: "UPSC Prelims {year} Previous Year Questions"
description: "Complete collection of UPSC Civil Services Preliminary Examination {year} questions with answers"
keywords: "UPSC Prelims {year}, Previous Year Questions, Civil Services Examination, IAS, Question Papers"
---

{create_breadcrumb(year)}

<div class="year-header">
    <h1>UPSC Prelims {year}</h1>
    <div class="year-stats">
        <div class="stat">
            <span class="stat-number">{total_questions}</span>
            <span class="stat-label">Questions</span>
        </div>
        <div class="stat">
            <span class="stat-number">{year}</span>
            <span class="stat-label">Year</span>
        </div>
    </div>
</div>

<div class="questions-grid">
"""
    
    # Add questions in a clean grid
    for i, question in enumerate(questions, 1):
        question_text = question['question']
        clean_question = re.sub(r'<[^>]+>', '', question_text)
        clean_question = re.sub(r'\n+', ' ', clean_question)
        preview = clean_question[:80].strip() + ("..." if len(clean_question) > 80 else "")
        
        filename = f"q{i:03d}-{sanitize_filename(question['question'])}.md"
        clean_name = f"q{i:03d}-{sanitize_filename(question['question'])}"
        
        content += f"""    <a href="{clean_name}/" class="question-card">
        <div class="question-number">{i}</div>
        <div class="question-preview">{preview}</div>
    </a>
"""
    
    content += f"""</div>

<div class="year-nav">
    <a href="../" class="nav-btn">← All Years</a>
    <a href="q001-{sanitize_filename(questions[0]['question'])}/" class="nav-btn primary">Start Practice</a>
</div>
"""
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)

def create_main_index(output_base):
    """Create clean main PIQ index page."""
    index_path = output_base / "index.md"
    
    # Get years
    years = []
    for year_dir in sorted(output_base.glob("20*"), reverse=True):
        if year_dir.is_dir():
            year = year_dir.name
            question_files = list(year_dir.glob("q*.md"))
            years.append((year, len(question_files)))
    
    total_questions = sum(count for _, count in years)
    
    content = f"""---
title: "UPSC Prelims Previous Year Questions (PIQ)"
description: "Complete collection of UPSC Civil Services Preliminary Examination questions from 2011 to 2023"
keywords: "UPSC Prelims, Previous Year Questions, Civil Services Examination, IAS, Question Bank, PIQ"
---

{create_breadcrumb()}

<div class="piq-header">
    <h1>UPSC Prelims Questions</h1>
    <p>Complete collection of previous year questions from 2011 to 2023</p>
    
    <div class="piq-stats">
        <div class="stat">
            <span class="stat-number">{total_questions}</span>
            <span class="stat-label">Questions</span>
        </div>
        <div class="stat">
            <span class="stat-number">{len(years)}</span>
            <span class="stat-label">Years</span>
        </div>
        <div class="stat">
            <span class="stat-number">2011-2023</span>
            <span class="stat-label">Range</span>
        </div>
    </div>
</div>

<div class="years-grid">
"""
    
    # Add year cards
    for year, count in years:
        content += f"""    <a href="{year}/" class="year-card">
        <div class="year-title">{year}</div>
        <div class="year-count">{count} Questions</div>
    </a>
"""
    
    content += """</div>

<div class="features">
    <div class="feature">
        <h3>Complete Coverage</h3>
        <p>All questions from 2011 to 2023 with verified answers</p>
    </div>
    <div class="feature">
        <h3>Easy Navigation</h3>
        <p>Browse by year or search for specific topics</p>
    </div>
    <div class="feature">
        <h3>Mobile Friendly</h3>
        <p>Study anywhere with responsive design</p>
    </div>
</div>
"""
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    """Main function to generate clean PIQ pages."""
    data_dir = Path("data/prelimsJson")
    output_base = Path("docs/piq")
    
    if not data_dir.exists():
        print("❌ Data directory not found!")
        return
    
    print("🚀 Generating clean PIQ pages...")
    
    # Clean existing content
    if output_base.exists():
        import shutil
        shutil.rmtree(output_base)
    output_base.mkdir(exist_ok=True)
    
    # Get all JSON files
    json_files = sorted(data_dir.glob("*.json"))
    
    for json_file in json_files:
        year = json_file.stem
        print(f"📅 Processing {year}...")
        
        # Load questions
        with open(json_file, 'r', encoding='utf-8') as f:
            questions = json.load(f)
        
        # Create year directory
        year_dir = output_base / year
        year_dir.mkdir(exist_ok=True)
        
        print(f"  📝 Creating {len(questions)} question pages...")
        
        # Create question pages
        for i, question in enumerate(questions, 1):
            create_question_page(question, year, i, year_dir, len(questions), questions)
        
        # Create year index
        create_year_index(year, questions, year_dir)
        
        print(f"  ✅ Completed {year}")
    
    # Create main index
    create_main_index(output_base)
    
    print(f"🎉 Generated clean PIQ pages!")
    print(f"📁 Files: {output_base}")
    print("\n✨ Features:")
    print("  • Fixed navigation links")
    print("  • Clean minimalistic design") 
    print("  • Proper breadcrumbs")
    print("  • No markdown artifacts")

if __name__ == "__main__":
    main()