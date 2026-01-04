#!/usr/bin/env python3
"""
Fix the remaining about-the-author links that have code tags inside them.
"""

import re
from pathlib import Path

REPO_DIR = Path(__file__).parent
BLOG_DIR = REPO_DIR / "a"

def fix_remaining_about_links():
    """Fix about-the-author links with nested tags."""
    print("Fixing remaining about-the-author links...")
    
    count = 0
    files_modified = 0
    
    # Pattern for about-the-author links (with any content inside, including nested tags)
    pattern = re.compile(
        r'<a\s+href="https?://thebuildingcoder\.typepad\.com/blog/about-the-author\.html[^"]*">(.+?)</a>',
        re.IGNORECASE | re.DOTALL
    )
    
    html_files = list(BLOG_DIR.glob("*.htm")) + list(BLOG_DIR.glob("*.html"))
    
    for file_path in html_files:
        if file_path.name == 'index_local.html':
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        except:
            continue
        
        original = content
        
        def replace_about(match):
            nonlocal count
            inner = match.group(1)
            count += 1
            return f'<span class="unavailable-link">{inner}</span>'
        
        content = pattern.sub(replace_about, content)
        
        if content != original:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            files_modified += 1
    
    return files_modified, count

def fix_index_local():
    """Fix index_local.html separately as it has various link types."""
    print("Fixing index_local.html...")
    
    file_path = BLOG_DIR / "index_local.html"
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        print(f"Error: {e}")
        return 0
    
    original = content
    count = 0
    
    patterns = [
        # Blog root link
        (r'<a href="http://thebuildingcoder\.typepad\.com">([^<]+)</a>',
         r'<span class="unavailable-link">\1</span>'),
        
        # Wave/CV/jtweb links
        (r'<a href="http://thebuildingcoder\.typepad\.com/[^"]+">([^<]+)</a>',
         r'<span class="unavailable-link">\1 <em>(link unavailable)</em></span>'),
        
        # File downloads with span wrappers
        (r'<span[^>]*><a href="http://thebuildingcoder\.typepad\.com/files/([^"]+)">([^<]+)</a></span>',
         r'<span class="unavailable-link">\2 <em>(file unavailable)</em></span>'),
        
        # Category links
        (r'<a href="http://thebuildingcoder\.typepad\.com/blog/[a-z]+">([^<]+)</a>',
         r'<span class="unavailable-link">\1</span>'),
    ]
    
    for pattern, replacement in patterns:
        new_content, n = re.subn(pattern, replacement, content, flags=re.IGNORECASE)
        if n > 0:
            count += n
            content = new_content
    
    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return count

def main():
    print("=" * 60)
    print("Final fix for remaining Typepad links")
    print("=" * 60)
    
    files1, count1 = fix_remaining_about_links()
    count2 = fix_index_local()
    
    print(f"\nAbout-author links: {count1} in {files1} files")
    print(f"Index_local links: {count2}")
    print(f"Total: {count1 + count2}")
    print("\nDone!")

if __name__ == '__main__':
    main()
