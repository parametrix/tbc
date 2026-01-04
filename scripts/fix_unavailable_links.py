#!/usr/bin/env python3
"""
Convert unavailable Typepad links to text with a note indicating the resource is not available.
This handles file downloads and other resources that don't have local copies.
"""

import re
from pathlib import Path

# Configuration
REPO_DIR = Path(__file__).parent
BLOG_DIR = REPO_DIR / "a"

def fix_unavailable_links():
    """
    Find links to Typepad resources that don't have local copies and convert them to text.
    """
    print("Finding and converting unavailable Typepad links...")
    
    stats = {
        'files_modified': 0,
        'links_converted': 0
    }
    
    # Patterns for Typepad links that are unlikely to have local copies
    # 1. File downloads: /blog/files/...
    # 2. Category pages: /blog/category_name (no .html)
    # 3. Other non-blog-post URLs
    
    # Pattern to match Typepad links
    typepad_pattern = re.compile(
        r'<a\s+href="(https?://thebuildingcoder\.typepad\.com/blog/(?:files/[^"]+|[^"/]+/?|[^"]*\.[^"html][^"]*))">([^<]+)</a>',
        re.IGNORECASE
    )
    
    # More specific patterns
    patterns = [
        # File downloads: <a href="http://...typepad.../blog/files/xxx.zip">text</a>
        (re.compile(r'<a\s+href="(https?://thebuildingcoder\.typepad\.com/blog/files/[^"]+)">([^<]+)</a>', re.IGNORECASE),
         lambda m: f'<span class="unavailable-link" title="Original: {m.group(1)}">{m.group(2)} <em>(file no longer available)</em></span>'),
        
        # Category/tag pages: <a href="http://...typepad.../blog/category">text</a> (no .html extension)
        (re.compile(r'<a\s+href="(https?://thebuildingcoder\.typepad\.com/blog/[a-z_]+)/?">([^<]+)</a>', re.IGNORECASE),
         lambda m: f'<span class="unavailable-link" title="Original: {m.group(1)}">{m.group(2)} <em>(category page)</em></span>'),
        
        # Truncated/malformed blog URLs that couldn't be resolved
        (re.compile(r'<a\s+href="(https?://thebuildingcoder\.typepad\.com/blog/\d{4}(?:/\d{2})?)"(?:\s[^>]*)?>([^<]+)</a>', re.IGNORECASE),
         lambda m: f'<span class="unavailable-link" title="Original: {m.group(1)}">{m.group(2)} <em>(link unavailable)</em></span>'),
    ]
    
    # Process all HTML files
    html_files = list(BLOG_DIR.glob("*.htm")) + list(BLOG_DIR.glob("*.html"))
    
    for file_path in html_files:
        if file_path.name == 'index_local.html':
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            continue
        
        original_content = content
        file_links_converted = 0
        
        # Apply each pattern
        for pattern, replacement in patterns:
            new_content, count = pattern.subn(replacement, content)
            if count > 0:
                file_links_converted += count
                content = new_content
        
        # Write if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            stats['files_modified'] += 1
            stats['links_converted'] += file_links_converted
    
    return stats

def add_css_for_unavailable_links():
    """
    Add CSS styling for unavailable links to bc.css
    """
    css_file = BLOG_DIR / "bc.css"
    
    css_addition = """
/* Styling for unavailable/archived links */
.unavailable-link {
    color: #666;
}
.unavailable-link em {
    font-size: 0.85em;
    color: #999;
}
"""
    
    try:
        with open(css_file, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        if '.unavailable-link' not in css_content:
            with open(css_file, 'a', encoding='utf-8') as f:
                f.write(css_addition)
            print("Added CSS styling for unavailable links")
    except Exception as e:
        print(f"Could not update CSS: {e}")

def main():
    print("=" * 60)
    print("Converting unavailable Typepad links to text")
    print("=" * 60)
    
    # Add CSS styling
    add_css_for_unavailable_links()
    
    # Fix links
    stats = fix_unavailable_links()
    
    print("\n" + "=" * 60)
    print("Summary:")
    print(f"  Files modified: {stats['files_modified']}")
    print(f"  Links converted to text: {stats['links_converted']}")
    print("\nDone!")

if __name__ == '__main__':
    main()
