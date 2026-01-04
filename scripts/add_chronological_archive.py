#!/usr/bin/env python3
"""
add_chronological_archive.py - Add chronological archive to TOC data

This script extracts all posts from the chronological TOC (Section #6) 
in index.html and adds them as year-grouped entries to toc-data.json.

Author: GitHub Copilot
Date: January 2, 2026
"""

import re
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# Paths
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
INDEX_FILE = REPO_ROOT / "a" / "index.html"
TOC_DATA_FILE = REPO_ROOT / "a" / "toc" / "toc-data.json"


def extract_chronological_posts(html_content: str) -> list:
    """
    Extract all posts from the chronological TOC table.
    
    Returns:
        List of dicts with keys: number, date, year, file, title, categories
    """
    posts = []
    
    # Pattern to match TOC table rows
    # <tr><td align="right">0001</td><td>2008-08-22</td><td><a href="0001_welcome.htm">Welcome</a>...
    pattern = r'<tr><td align="right">(\d+)</td><td>(\d{4})-(\d{2})-(\d{2})</td><td><a href="([^"]+)">([^<]+)</a>.*?</td><td>([^<]*)</td></tr>'
    
    matches = re.findall(pattern, html_content, re.DOTALL)
    
    for match in matches:
        number, year, month, day, file, title, categories = match
        posts.append({
            'number': int(number),
            'date': f"{year}-{month}-{day}",
            'year': int(year),
            'file': file,
            'title': title.strip(),
            'categories': categories.strip()
        })
    
    return posts


def group_posts_by_year(posts: list) -> dict:
    """
    Group posts by year, sorted in reverse chronological order.
    
    Returns:
        Dict mapping year to list of posts for that year
    """
    by_year = defaultdict(list)
    
    for post in posts:
        by_year[post['year']].append({
            'title': post['title'],
            'file': post['file'],
            'date': post['date'],
            'number': post['number']
        })
    
    # Sort posts within each year by number (ascending)
    for year in by_year:
        by_year[year].sort(key=lambda p: p['number'])
    
    return dict(by_year)


def create_archive_entries(posts_by_year: dict) -> list:
    """
    Create archive entries for the TOC data.
    
    Returns:
        List of archive year entries, sorted newest first
    """
    archive = []
    
    for year in sorted(posts_by_year.keys(), reverse=True):
        posts = posts_by_year[year]
        archive.append({
            'id': f"archive-{year}",
            'title': str(year),
            'posts': [
                {
                    'title': f"#{p['number']:04d} - {p['title']}",
                    'file': p['file'],
                    'date': p['date']
                }
                for p in posts
            ]
        })
    
    return archive


def main():
    print("=" * 60)
    print("Add Chronological Archive to TOC Data")
    print("=" * 60)
    
    # Read index.html
    print(f"\nReading: {INDEX_FILE}")
    html_content = INDEX_FILE.read_text(encoding='utf-8', errors='replace')
    
    # Extract posts from chronological TOC
    posts = extract_chronological_posts(html_content)
    print(f"Extracted {len(posts)} posts from chronological TOC")
    
    if not posts:
        print("ERROR: No posts found! Check the regex pattern.")
        return
    
    # Group by year
    posts_by_year = group_posts_by_year(posts)
    years = sorted(posts_by_year.keys())
    print(f"Years covered: {years[0]} - {years[-1]}")
    
    # Show distribution
    print("\nPosts per year:")
    for year in sorted(posts_by_year.keys(), reverse=True):
        print(f"  {year}: {len(posts_by_year[year])} posts")
    
    # Create archive entries
    archive = create_archive_entries(posts_by_year)
    
    # Read existing TOC data
    print(f"\nReading: {TOC_DATA_FILE}")
    toc_data = json.loads(TOC_DATA_FILE.read_text(encoding='utf-8'))
    
    print(f"Existing topics: {toc_data['totalTopics']}")
    print(f"Existing post links: {toc_data['totalPostLinks']}")
    
    # Add archive section
    toc_data['archive'] = archive
    toc_data['totalArchiveYears'] = len(archive)
    toc_data['totalArchivePosts'] = len(posts)
    toc_data['lastUpdated'] = datetime.now().strftime('%Y-%m-%d')
    
    # Write updated TOC data
    print(f"\nWriting updated TOC data...")
    TOC_DATA_FILE.write_text(
        json.dumps(toc_data, indent=2, ensure_ascii=False),
        encoding='utf-8'
    )
    
    # Summary
    print("\n" + "-" * 60)
    print("Summary:")
    print(f"  Topic groups: {toc_data['totalTopics']} ({toc_data['totalPostLinks']} curated posts)")
    print(f"  Archive years: {toc_data['totalArchiveYears']} ({toc_data['totalArchivePosts']} total posts)")
    print(f"  Updated: {TOC_DATA_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()
