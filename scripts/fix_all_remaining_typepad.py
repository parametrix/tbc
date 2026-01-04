#!/usr/bin/env python3
"""
Convert ALL remaining unavailable Typepad links to text with notes.
This is a comprehensive cleanup for any Typepad links that couldn't be resolved.
"""

import re
from pathlib import Path

# Configuration
REPO_DIR = Path(__file__).parent
BLOG_DIR = REPO_DIR / "a"

def fix_all_remaining_typepad_links():
    """
    Find and convert all remaining Typepad links that don't have local copies.
    """
    print("Finding and converting ALL remaining Typepad links...")
    
    stats = {
        'files_modified': 0,
        'links_converted': 0,
        'by_type': {}
    }
    
    def count_type(link_type):
        stats['by_type'][link_type] = stats['by_type'].get(link_type, 0) + 1
    
    # Define replacement patterns and their handlers
    replacements = [
        # 1. File downloads: /blog/files/ or /files/
        (re.compile(r'<a\s+href="(https?://thebuildingcoder\.typepad\.com/(?:blog/)?files/([^"]+))"\s*>([^<]+)</a>', re.IGNORECASE),
         lambda m: (f'<span class="unavailable-link" title="Original: {m.group(1)}">{m.group(3)} <em>(file unavailable: {m.group(2)})</em></span>', 'file_download')),
        
        # 2. SVG folder links
        (re.compile(r'<a\s+href="(https?://thebuildingcoder\.typepad\.com/svg/[^"]+)"\s*>([^<]*(?:<[^>]+>[^<]*)*)</a>', re.IGNORECASE),
         lambda m: (f'<span class="unavailable-link" title="Original: {m.group(1)}">{re.sub(r"<[^>]+>", "", m.group(2)) or "SVG demo"} <em>(demo unavailable)</em></span>', 'svg_demo')),
        
        # 3. Blog root links (just the domain or /blog)
        (re.compile(r'<a\s+href="(https?://thebuildingcoder\.typepad\.com/?(?:blog)?/?)"(?:\s[^>]*)?>([^<]+)</a>', re.IGNORECASE),
         lambda m: (f'<span class="unavailable-link">{m.group(2)}</span>', 'blog_root')),
        
        # 4. About/author pages
        (re.compile(r'<a\s+href="(https?://thebuildingcoder\.typepad\.com/blog/about[^"]*)"(?:\s[^>]*)?>([^<]+)</a>', re.IGNORECASE),
         lambda m: (f'<span class="unavailable-link">{m.group(2)}</span>', 'about_page')),
        
        # 5. Category/archive pages (no .html extension)
        (re.compile(r'<a\s+href="(https?://thebuildingcoder\.typepad\.com/blog/[a-z0-9_-]+)/?"\s*>([^<]+)</a>', re.IGNORECASE),
         lambda m: (f'<span class="unavailable-link" title="Category: {m.group(1)}">{m.group(2)}</span>', 'category')),
        
        # 6. Malformed/truncated blog post URLs (year only or year/month only)
        (re.compile(r'<a\s+href="(https?://thebuildingcoder\.typepad\.com/blog/\d{4}(?:/\d{2})?/?)"(?:\s[^>]*)?>([^<]+)</a>', re.IGNORECASE),
         lambda m: (f'<span class="unavailable-link" title="Original: {m.group(1)}">{m.group(2)} <em>(link unavailable)</em></span>', 'truncated')),
        
        # 7. Blog post URLs with query params that couldn't be resolved
        (re.compile(r'<a\s+href="(https?://thebuildingcoder\.typepad\.com/blog/\d{4}/\d{2}/[^"]+\?[^"]+)"(?:\s[^>]*)?>([^<]+)</a>', re.IGNORECASE),
         lambda m: (f'<span class="unavailable-link" title="Original: {m.group(1)}">{m.group(2)} <em>(link unavailable)</em></span>', 'query_params')),
        
        # 8. Blog posts with trailing space in URL
        (re.compile(r'<a\s+href="(https?://thebuildingcoder\.typepad\.com/blog/[^"]+)\s+"(?:\s[^>]*)?>([^<]+)</a>', re.IGNORECASE),
         lambda m: (f'<span class="unavailable-link" title="Original: {m.group(1)}">{m.group(2)} <em>(link unavailable)</em></span>', 'trailing_space')),
        
        # 9. Blog posts with placeholder URLs (???)
        (re.compile(r'<a\s+href="(https?://thebuildingcoder\.typepad\.com/blog/[^"]*\?\?\?[^"]*)"(?:\s[^>]*)?>([^<]+)</a>', re.IGNORECASE),
         lambda m: (f'<span class="unavailable-link">{m.group(2)} <em>(link unavailable)</em></span>', 'placeholder')),
        
        # 10. Revit 2014 API recording link (special case)
        (re.compile(r'<a\s+href="(https?://thebuildingcoder\.typepad\.com/revit_2014_api/[^"]+)"(?:\s[^>]*)?>([^<]+)</a>', re.IGNORECASE),
         lambda m: (f'<span class="unavailable-link" title="Original: {m.group(1)}">{m.group(2)} <em>(resource unavailable)</em></span>', 'revit_api')),
        
        # 11. Any remaining .htm/.html blog post URLs that weren't resolved
        (re.compile(r'<a\s+href="(https?://thebuildingcoder\.typepad\.com/blog/\d{4}/\d{2}/[^"]+\.html?)"(?:\s[^>]*)?>([^<]+)</a>', re.IGNORECASE),
         lambda m: (f'<span class="unavailable-link" title="Original: {m.group(1)}">{m.group(2)} <em>(post unavailable)</em></span>', 'unresolved_post')),
        
        # 12. Catch-all for any other typepad.com links
        (re.compile(r'<a\s+href="(https?://thebuildingcoder\.typepad\.com[^"]*)"(?:\s[^>]*)?>([^<]+)</a>', re.IGNORECASE),
         lambda m: (f'<span class="unavailable-link" title="Original: {m.group(1)}">{m.group(2)}</span>', 'other')),
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
        for pattern, handler in replacements:
            def replacer(match):
                nonlocal file_links_converted
                replacement, link_type = handler(match)
                file_links_converted += 1
                count_type(link_type)
                return replacement
            
            content = pattern.sub(replacer, content)
        
        # Write if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            stats['files_modified'] += 1
            stats['links_converted'] += file_links_converted
    
    return stats

def fix_markdown_files():
    """
    Also fix Typepad links in markdown files.
    """
    print("Fixing remaining Typepad links in markdown files...")
    
    count = 0
    
    # Pattern for markdown links
    pattern = re.compile(r'\[([^\]]+)\]\((https?://thebuildingcoder\.typepad\.com[^)]+)\)')
    
    for md_file in BLOG_DIR.glob("*.md"):
        try:
            with open(md_file, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        except:
            continue
        
        original = content
        
        def replace_md(match):
            nonlocal count
            text = match.group(1)
            url = match.group(2)
            count += 1
            return f'{text} *(link unavailable)*'
        
        content = pattern.sub(replace_md, content)
        
        if content != original:
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(content)
    
    return count

def main():
    print("=" * 60)
    print("Converting ALL remaining Typepad links to text")
    print("=" * 60)
    
    # Fix HTML files
    stats = fix_all_remaining_typepad_links()
    
    # Fix markdown files
    md_count = fix_markdown_files()
    
    print("\n" + "=" * 60)
    print("Summary:")
    print(f"  Files modified: {stats['files_modified']}")
    print(f"  Links converted: {stats['links_converted']}")
    print(f"  Markdown links: {md_count}")
    
    if stats['by_type']:
        print("\nBy type:")
        for link_type, count in sorted(stats['by_type'].items(), key=lambda x: -x[1]):
            print(f"  {link_type}: {count}")
    
    print("\nDone!")

if __name__ == '__main__':
    main()
