#!/usr/bin/env python3
"""
Fix all 'about-the-author.html' links by redirecting them to index.html.
This replaces both:
1. href="...about-the-author.html..." with href="../index.html"
2. Plain URLs in text with ../index.html
"""

import re
from pathlib import Path

REPO_DIR = Path(__file__).parent.parent
BLOG_DIR = REPO_DIR / "a"

def fix_about_author_links():
    """Replace about-the-author.html links with ../index.html."""
    print("Fixing about-the-author links to redirect to index.html...")
    
    total_count = 0
    files_modified = 0
    
    # Patterns to match:
    # 1. href attributes with about-the-author.html (with optional anchors)
    href_pattern = re.compile(
        r'href="https?://thebuildingcoder\.typepad\.com/blog/about-the-author\.html[^"]*"',
        re.IGNORECASE
    )
    
    # 2. Plain URLs in text (not in href)
    url_pattern = re.compile(
        r'(?<!href=")https?://thebuildingcoder\.typepad\.com/blog/about-the-author\.html[^\s<"\']*',
        re.IGNORECASE
    )
    
    html_files = list(BLOG_DIR.glob("*.htm")) + list(BLOG_DIR.glob("*.html"))
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            continue
        
        original = content
        count = 0
        
        # Replace href attributes
        def replace_href(match):
            nonlocal count
            count += 1
            return 'href="../index.html"'
        
        content = href_pattern.sub(replace_href, content)
        
        # Replace plain URLs in text
        def replace_url(match):
            nonlocal count
            count += 1
            return '../index.html'
        
        content = url_pattern.sub(replace_url, content)
        
        if content != original:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            files_modified += 1
            total_count += count
            print(f"  {file_path.name}: {count} links fixed")
    
    print(f"\nTotal: {files_modified} files modified, {total_count} links fixed")
    return files_modified, total_count

if __name__ == "__main__":
    fix_about_author_links()
