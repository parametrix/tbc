#!/usr/bin/env python3
"""
Generate chrono-data.json from the index.html table of contents.

This script parses the chronological table in a/index.html and extracts
post numbers, dates, titles, and filenames to create a JSON file for
the timeline navigation column.
"""

import re
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def parse_index_html(index_path: Path) -> list[dict]:
    """Parse the index.html and extract post data from the TOC table."""
    
    content = index_path.read_text(encoding='utf-8')
    
    # Pattern to match table rows with post data
    # Format: <tr><td align="right">0001</td><td>2008-08-22</td><td><a href="0001_welcome.htm">Welcome</a>...
    pattern = r'<tr><td[^>]*>(\d{4})</td><td>(\d{4}-\d{2}-\d{2})</td><td><a href="([^"]+)">([^<]+)</a>'
    
    posts = []
    for match in re.finditer(pattern, content):
        num = int(match.group(1))
        date_str = match.group(2)
        filename = match.group(3)
        title = match.group(4)
        
        # Parse date
        date = datetime.strptime(date_str, '%Y-%m-%d')
        
        posts.append({
            'num': num,
            'file': filename,
            'title': title,
            'date': date_str,
            'year': date.year,
            'month': date.month
        })
    
    # Sort by post number (chronological)
    posts.sort(key=lambda p: p['num'])
    
    return posts


def calculate_year_stats(posts: list[dict]) -> list[dict]:
    """Calculate statistics for each year."""
    
    year_data = defaultdict(lambda: {'count': 0, 'firstPost': float('inf'), 'lastPost': 0})
    
    for post in posts:
        year = post['year']
        year_data[year]['count'] += 1
        year_data[year]['firstPost'] = min(year_data[year]['firstPost'], post['num'])
        year_data[year]['lastPost'] = max(year_data[year]['lastPost'], post['num'])
    
    years = []
    for year in sorted(year_data.keys(), reverse=True):
        years.append({
            'year': year,
            'count': year_data[year]['count'],
            'firstPost': year_data[year]['firstPost'],
            'lastPost': year_data[year]['lastPost']
        })
    
    return years


def generate_chrono_data(workspace_root: Path) -> dict:
    """Generate the complete chrono-data.json content."""
    
    index_path = workspace_root / 'a' / 'index.html'
    
    if not index_path.exists():
        raise FileNotFoundError(f"Index file not found: {index_path}")
    
    posts = parse_index_html(index_path)
    years = calculate_year_stats(posts)
    
    chrono_data = {
        'version': '1.0',
        'lastUpdated': datetime.now().strftime('%Y-%m-%d'),
        'totalPosts': len(posts),
        'posts': posts,
        'years': years
    }
    
    return chrono_data


def main():
    # Determine workspace root (script is in scripts/ folder)
    script_dir = Path(__file__).parent
    workspace_root = script_dir.parent
    
    print(f"Workspace root: {workspace_root}")
    print(f"Parsing index.html...")
    
    chrono_data = generate_chrono_data(workspace_root)
    
    print(f"Found {chrono_data['totalPosts']} posts")
    print(f"Years covered: {chrono_data['years'][-1]['year']} - {chrono_data['years'][0]['year']}")
    
    # Output path
    output_path = workspace_root / 'a' / 'toc' / 'chrono-data.json'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(chrono_data, f, indent=2, ensure_ascii=False)
    
    print(f"Generated: {output_path}")
    print(f"File size: {output_path.stat().st_size / 1024:.1f} KB")
    
    # Show sample data
    print("\nSample posts (first 3):")
    for post in chrono_data['posts'][:3]:
        print(f"  #{post['num']:04d} ({post['date']}): {post['title'][:50]}")
    
    print("\nSample posts (last 3):")
    for post in chrono_data['posts'][-3:]:
        print(f"  #{post['num']:04d} ({post['date']}): {post['title'][:50]}")
    
    print("\nYear summary:")
    for year_info in chrono_data['years'][:5]:
        print(f"  {year_info['year']}: {year_info['count']} posts (#{year_info['firstPost']:04d} - #{year_info['lastPost']:04d})")


if __name__ == '__main__':
    main()
