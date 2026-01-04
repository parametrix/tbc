#!/usr/bin/env python3
"""
Final cleanup: handle image popups and remaining about-page links with anchors.
"""

import re
from pathlib import Path

REPO_DIR = Path(__file__).parent
BLOG_DIR = REPO_DIR / "a"

def fix_remaining():
    """Fix remaining edge cases."""
    print("Fixing remaining edge cases...")
    
    stats = {'files': 0, 'links': 0}
    
    patterns = [
        # About page links with anchors
        (re.compile(r'<a\s+href="(https?://thebuildingcoder\.typepad\.com/blog/about-the-author\.html#[^"]+)"(?:\s[^>]*)?>([^<]+)</a>', re.IGNORECASE),
         lambda m: f'<span class="unavailable-link">{m.group(2)}</span>'),
        
        # Image popup links (keep the image, remove the link wrapper)
        (re.compile(r'<a\s+class="asset-img-link"[^>]*href="https?://thebuildingcoder\.typepad\.com/\.a/[^"]+-popup"[^>]*>(<img[^>]+>)</a>', re.IGNORECASE | re.DOTALL),
         lambda m: m.group(1)),  # Keep just the img tag
        
        # Images with typepad src - convert to local if possible or note unavailable
        # These are actually served from typepad, we'll leave them as-is since they may still work
        # or the image is embedded in the HTML
    ]
    
    html_files = list(BLOG_DIR.glob("*.htm")) + list(BLOG_DIR.glob("*.html"))
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        except:
            continue
        
        original = content
        count = 0
        
        for pattern, replacement in patterns:
            new_content = pattern.sub(replacement, content)
            if new_content != content:
                count += len(pattern.findall(content))
                content = new_content
        
        if content != original:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            stats['files'] += 1
            stats['links'] += count
    
    return stats

def main():
    print("=" * 60)
    print("Final cleanup of remaining Typepad links")
    print("=" * 60)
    
    stats = fix_remaining()
    
    print(f"\nFiles modified: {stats['files']}")
    print(f"Links fixed: {stats['links']}")
    print("\nDone!")

if __name__ == '__main__':
    main()
