#!/usr/bin/env python3
"""
Comprehensive audit of all blog post files against TOC and chronological data.
This script systematically verifies:
1. All .htm, .html, and .md files in the archive
2. All entries in chrono-data.json
3. All entries in toc-data.json
4. Cross-references to find discrepancies
"""

import os
import json
import re
from pathlib import Path
from collections import defaultdict

# Paths
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
A_DIR = REPO_ROOT / 'a'
TOC_DIR = A_DIR / 'toc'
CHRONO_FILE = TOC_DIR / 'chrono-data.json'
TOC_FILE = TOC_DIR / 'toc-data.json'
INDEX_FILE = A_DIR / 'index.html'

def get_all_post_files():
    """Get all .htm, .html files in the a/ directory that are numbered posts."""
    post_files = set()
    non_post_files = set()
    
    # Pattern for numbered posts (e.g., 0001_welcome.htm, 1351_md_fusion.html)
    post_pattern = re.compile(r'^(\d{4})_.+\.(htm|html)$')
    
    for f in os.listdir(A_DIR):
        full_path = A_DIR / f
        if not full_path.is_file():
            continue
        
        if f.endswith('.htm') or f.endswith('.html'):
            match = post_pattern.match(f)
            if match:
                post_files.add(f)
            else:
                non_post_files.add(f)
    
    return post_files, non_post_files

def get_all_md_files():
    """Get all .md files in the repo (excluding a_backup)."""
    md_files = {}  # path -> filename
    
    # Root level .md files
    for f in os.listdir(REPO_ROOT):
        if f.endswith('.md'):
            md_files[str(REPO_ROOT / f)] = f
    
    # a/ directory .md files
    for f in os.listdir(A_DIR):
        if f.endswith('.md'):
            md_files[str(A_DIR / f)] = f
    
    return md_files

def load_chrono_data():
    """Load chronological data file."""
    with open(CHRONO_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_toc_data():
    """Load topic TOC data file."""
    with open(TOC_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_post_number(filename):
    """Extract the post number from a filename."""
    match = re.match(r'^(\d{4})_', filename)
    if match:
        return int(match.group(1))
    return None

def analyze_chrono_data(chrono_data, post_files):
    """Analyze chrono-data.json entries against actual files."""
    chrono_files = set()
    chrono_missing = []  # Files in chrono but not in a/
    
    for post in chrono_data.get('posts', []):
        file = post.get('file', '')
        chrono_files.add(file)
        
        if file not in post_files:
            chrono_missing.append({
                'num': post.get('num'),
                'file': file,
                'title': post.get('title'),
                'date': post.get('date')
            })
    
    return chrono_files, chrono_missing

def analyze_toc_data(toc_data, post_files):
    """Analyze toc-data.json entries against actual files."""
    toc_files = set()
    toc_missing = []  # Files in TOC but not in a/
    
    for topic in toc_data.get('topics', []):
        for post in topic.get('posts', []):
            file = post.get('file', '')
            # Handle anchor links (e.g., "1016_linked_project_element.htm#5")
            file = file.split('#')[0]
            toc_files.add(file)
            
            if file not in post_files:
                toc_missing.append({
                    'topic': topic.get('id'),
                    'topic_title': topic.get('title'),
                    'file': file,
                    'title': post.get('title')
                })
    
    return toc_files, toc_missing

def find_gaps_in_numbering(post_files):
    """Find gaps in post numbering."""
    numbers = set()
    for f in post_files:
        num = extract_post_number(f)
        if num:
            numbers.add(num)
    
    if not numbers:
        return []
    
    min_num = min(numbers)
    max_num = max(numbers)
    
    gaps = []
    for n in range(min_num, max_num + 1):
        if n not in numbers:
            gaps.append(n)
    
    return gaps

def main():
    print("=" * 70)
    print("COMPREHENSIVE BLOG POST AUDIT")
    print("=" * 70)
    print()
    
    # 1. Get all files
    post_files, non_post_files = get_all_post_files()
    md_files = get_all_md_files()
    
    print("1. FILE INVENTORY")
    print("-" * 50)
    
    htm_files = {f for f in post_files if f.endswith('.htm')}
    html_files = {f for f in post_files if f.endswith('.html')}
    
    print(f"   Post files (.htm):   {len(htm_files)}")
    print(f"   Post files (.html):  {len(html_files)}")
    print(f"   Total post files:    {len(post_files)}")
    print(f"   Non-post .htm/.html: {len(non_post_files)}")
    print(f"   Markdown files:      {len(md_files)}")
    print()
    
    if non_post_files:
        print("   Non-post files (not numbered):")
        for f in sorted(non_post_files):
            print(f"     - {f}")
        print()
    
    # Extract post numbers
    post_numbers = {}
    for f in post_files:
        num = extract_post_number(f)
        if num:
            if num in post_numbers:
                print(f"   WARNING: Duplicate post number {num}:")
                print(f"     - {post_numbers[num]}")
                print(f"     - {f}")
            post_numbers[num] = f
    
    min_num = min(post_numbers.keys()) if post_numbers else 0
    max_num = max(post_numbers.keys()) if post_numbers else 0
    print(f"   Post number range:   {min_num:04d} - {max_num:04d}")
    print()
    
    # 2. Load JSON data files
    chrono_data = load_chrono_data()
    toc_data = load_toc_data()
    
    print("2. DATA FILE SUMMARY")
    print("-" * 50)
    print(f"   chrono-data.json:")
    print(f"     Total posts:       {chrono_data.get('totalPosts', 0)}")
    print(f"     Last updated:      {chrono_data.get('lastUpdated', 'unknown')}")
    print()
    print(f"   toc-data.json:")
    print(f"     Total topics:      {toc_data.get('totalTopics', 0)}")
    print(f"     Total post links:  {toc_data.get('totalPostLinks', 0)}")
    print(f"     Last updated:      {toc_data.get('lastUpdated', 'unknown')}")
    print()
    
    # 3. Analyze chrono-data.json
    chrono_files, chrono_missing = analyze_chrono_data(chrono_data, post_files)
    
    print("3. CHRONO-DATA.JSON ANALYSIS")
    print("-" * 50)
    print(f"   Files referenced:    {len(chrono_files)}")
    print(f"   Missing files:       {len(chrono_missing)}")
    
    if chrono_missing:
        print("   Files in chrono-data.json but NOT in a/ directory:")
        for item in chrono_missing:
            print(f"     #{item['num']:04d}: {item['file']}")
    print()
    
    # 4. Analyze toc-data.json  
    toc_files, toc_missing = analyze_toc_data(toc_data, post_files)
    
    print("4. TOC-DATA.JSON ANALYSIS")
    print("-" * 50)
    print(f"   Unique files in topics: {len(toc_files)}")
    print(f"   Missing files:          {len(toc_missing)}")
    
    if toc_missing:
        print("   Files in toc-data.json but NOT in a/ directory:")
        for item in toc_missing:
            print(f"     Topic {item['topic']}: {item['file']}")
    print()
    
    # 5. Cross-reference analysis
    print("5. CROSS-REFERENCE ANALYSIS")
    print("-" * 50)
    
    # Files in a/ but not in chrono
    not_in_chrono = post_files - chrono_files
    print(f"   Post files NOT in chrono-data.json: {len(not_in_chrono)}")
    if not_in_chrono:
        for f in sorted(not_in_chrono)[:20]:  # Show first 20
            print(f"     - {f}")
        if len(not_in_chrono) > 20:
            print(f"     ... and {len(not_in_chrono) - 20} more")
    print()
    
    # Files in chrono but not in a/
    print(f"   Chrono entries without files: {len(chrono_missing)}")
    print()
    
    # Files in topics
    in_topics = post_files & toc_files
    not_in_topics = post_files - toc_files
    print(f"   Post files in topics:       {len(in_topics)} ({len(in_topics)*100/len(post_files):.1f}%)")
    print(f"   Post files NOT in topics:   {len(not_in_topics)} ({len(not_in_topics)*100/len(post_files):.1f}%)")
    print()
    
    # 6. Gap analysis
    gaps = find_gaps_in_numbering(post_files)
    print("6. NUMBERING GAP ANALYSIS")
    print("-" * 50)
    print(f"   Gaps in post numbering: {len(gaps)}")
    if gaps:
        print("   Missing post numbers:")
        for g in gaps:
            print(f"     - {g:04d}")
    print()
    
    # 7. Markdown files analysis
    print("7. MARKDOWN FILES")
    print("-" * 50)
    print(f"   Total .md files: {len(md_files)}")
    
    # Separate by category
    root_md = []
    post_md = []
    other_md = []
    
    post_pattern = re.compile(r'^(\d{4})_')
    
    for path, filename in md_files.items():
        if 'a/' in path or 'a\\' in path:
            if post_pattern.match(filename):
                post_md.append((path, filename))
            else:
                other_md.append((path, filename))
        else:
            root_md.append((path, filename))
    
    # Check which .md files have corresponding .html files
    md_with_html = []
    md_without_html = []
    for path, filename in post_md:
        base_name = filename.rsplit('.', 1)[0]
        html_filename = base_name + '.html'
        if html_filename in post_files:
            md_with_html.append((path, filename))
        else:
            md_without_html.append((path, filename))
    
    print(f"   Documentation (root): {len(root_md)}")
    for path, f in sorted(root_md):
        print(f"     - {f}")
    
    print(f"   Post-like .md in a/: {len(post_md)}")
    print(f"     - With .html conversion: {len(md_with_html)} (source files)")
    print(f"     - Missing .html:         {len(md_without_html)}")
    if md_without_html:
        for path, f in sorted(md_without_html):
            print(f"       * {f}")
    
    if other_md:
        print(f"   Other .md in a/: {len(other_md)}")
        for path, f in sorted(other_md):
            print(f"     - {f}")
    print()
    
    # 8. Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print("Archive Status:")
    print(f"  - Total post files:              {len(post_files)}")
    print(f"  - Posts in chrono-data.json:     {chrono_data.get('totalPosts', 0)}")
    print(f"  - Posts in toc-data.json topics: {len(toc_files)}")
    print()
    
    issues = []
    if chrono_missing:
        issues.append(f"- {len(chrono_missing)} chrono entries reference non-existent files")
    if toc_missing:
        issues.append(f"- {len(toc_missing)} topic entries reference non-existent files")
    if not_in_chrono:
        issues.append(f"- {len(not_in_chrono)} post files not in chrono-data.json")
    if gaps:
        issues.append(f"- {len(gaps)} gaps in post numbering")
    if md_without_html:
        issues.append(f"- {len(md_without_html)} .md files missing .html conversion")
    
    if issues:
        print("Issues Found:")
        for issue in issues:
            print(f"  {issue}")
    else:
        print("No issues found! All files are properly accounted for.")
    
    print()
    return len(issues) == 0

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
