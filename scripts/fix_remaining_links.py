#!/usr/bin/env python3
"""
Fix ALL remaining internal Typepad links by matching blog slugs to local files.
This script handles links that weren't in the index.html mapping table.
"""

import re
import os
from pathlib import Path
from collections import defaultdict

# Configuration
REPO_DIR = Path(__file__).parent
BLOG_DIR = REPO_DIR / "a"
INDEX_FILE = BLOG_DIR / "index.html"

def build_slug_to_file_mapping():
    """
    Build a comprehensive mapping from blog URL slugs to local files.
    Parses the full index.html to extract all possible mappings.
    """
    print("Building slug-to-file mapping from index.html...")
    
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern 1: Table rows with typepad and local links
    # <a href="http://...typepad.../blog/YYYY/MM/slug.html">Title</a>...<a href="local_file">
    pattern1 = r'<a href="https?://thebuildingcoder\.typepad\.com/blog/(\d{4})/(\d{2})/([^"]+)\.html">[^<]+</a>&nbsp;&nbsp;&nbsp;<a href="([^"]+)"'
    
    slug_mapping = {}
    
    # Extract from table format
    for match in re.finditer(pattern1, content):
        year, month, slug, local_file = match.groups()
        # Store multiple lookup keys
        full_path = f"/blog/{year}/{month}/{slug}.html"
        slug_mapping[full_path] = local_file
        slug_mapping[slug] = local_file
        slug_mapping[f"{slug}.html"] = local_file
    
    # Also build mapping from local files themselves
    # Many local files are named like NNNN_slug_name.htm
    # We can match the slug portion
    for htm_file in BLOG_DIR.glob("*.htm"):
        # Extract slug-like portion from filename
        # e.g., 1159_va3c_resolve_assembly.htm
        name = htm_file.stem  # e.g., 1159_va3c_resolve_assembly
        parts = name.split('_', 1)
        if len(parts) == 2 and parts[0].isdigit():
            # Create variations for matching
            slug_portion = parts[1].replace('_', '-')  # va3c-resolve-assembly
            slug_mapping[slug_portion] = htm_file.name
            # Also without dashes
            slug_nodash = parts[1].replace('_', '')
            slug_mapping[slug_nodash] = htm_file.name
    
    for html_file in BLOG_DIR.glob("*.html"):
        if html_file.name == "index.html" or html_file.name == "index_local.html":
            continue
        name = html_file.stem
        parts = name.split('_', 1)
        if len(parts) == 2 and parts[0].isdigit():
            slug_portion = parts[1].replace('_', '-')
            slug_mapping[slug_portion] = html_file.name
            slug_nodash = parts[1].replace('_', '')
            slug_mapping[slug_nodash] = html_file.name
    
    print(f"Built mapping with {len(slug_mapping)} entries")
    return slug_mapping

def build_comprehensive_url_mapping():
    """
    Parse index.html to get exact URL to local file mappings.
    """
    print("Parsing index.html for exact URL mappings...")
    
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Multiple patterns to capture all mapping types
    patterns = [
        # Table rows: typepad link followed by local link with ^ or web label
        r'<a href="(https?://thebuildingcoder\.typepad\.com/blog/[^"]+)">[^<]+</a>&nbsp;&nbsp;&nbsp;<a href="([^"]+)">(?:\^|web)',
        # Reversed: local link followed by typepad link
        r'<a href="([^"]+)">[^<]+</a>&nbsp;&nbsp;&nbsp;<a href="(https?://thebuildingcoder\.typepad\.com/blog/[^"]+)"',
    ]
    
    url_mapping = {}
    
    # Pattern 1: typepad -> local
    for match in re.finditer(patterns[0], content):
        typepad_url, local_file = match.groups()
        url_mapping[typepad_url] = local_file
        # Also store http/https variants
        if typepad_url.startswith('http://'):
            url_mapping[typepad_url.replace('http://', 'https://')] = local_file
        else:
            url_mapping[typepad_url.replace('https://', 'http://')] = local_file
    
    # Pattern 2: local -> typepad (reversed format)
    for match in re.finditer(patterns[1], content):
        local_file, typepad_url = match.groups()
        if not local_file.startswith('http'):
            url_mapping[typepad_url] = local_file
            if typepad_url.startswith('http://'):
                url_mapping[typepad_url.replace('http://', 'https://')] = local_file
            else:
                url_mapping[typepad_url.replace('https://', 'http://')] = local_file
    
    print(f"Found {len(url_mapping)} exact URL mappings")
    return url_mapping

def find_local_file_for_url(url, url_mapping, slug_mapping):
    """
    Try to find a local file for a given Typepad URL.
    """
    # Try exact match first
    if url in url_mapping:
        return url_mapping[url]
    
    # Extract slug from URL
    # URL format: http://thebuildingcoder.typepad.com/blog/YYYY/MM/slug.html
    match = re.search(r'/blog/\d{4}/\d{2}/([^.]+)\.html?', url)
    if match:
        slug = match.group(1)
        
        # Try slug directly
        if slug in slug_mapping:
            return slug_mapping[slug]
        
        # Try slug with .html
        if f"{slug}.html" in slug_mapping:
            return slug_mapping[f"{slug}.html"]
        
        # Try normalized slug (replace - with _)
        normalized = slug.replace('-', '_')
        if normalized in slug_mapping:
            return slug_mapping[normalized]
    
    # Try path-based lookup
    path_match = re.search(r'(/blog/\d{4}/\d{2}/[^"#?]+)', url)
    if path_match:
        path = path_match.group(1)
        if path in slug_mapping:
            return slug_mapping[path]
    
    return None

def fix_file(file_path, url_mapping, slug_mapping, stats):
    """
    Fix all Typepad links in a single file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return 0
    
    original_content = content
    links_fixed = 0
    
    # Pattern to match all Typepad blog links
    pattern = r'href="(https?://thebuildingcoder\.typepad\.com/blog/[^"#?]+)([#][^"?]*)?"'
    
    def replace_link(match):
        nonlocal links_fixed
        
        full_url = match.group(1)
        anchor = match.group(2) or ''
        
        local_file = find_local_file_for_url(full_url, url_mapping, slug_mapping)
        
        if local_file:
            links_fixed += 1
            return f'href="{local_file}{anchor}"'
        else:
            stats['unresolved'].append((file_path.name, full_url))
            return match.group(0)
    
    content = re.sub(pattern, replace_link, content)
    
    # Also fix links in index.html TOC section (li items)
    if file_path.name == 'index.html':
        # Fix TOC entries like <li><a href="http://...">Title</a></li>
        toc_pattern = r'(<li><a href=")(https?://thebuildingcoder\.typepad\.com/blog/[^"]+)(">)([^<]+)(</a></li>)'
        
        def replace_toc_link(match):
            nonlocal links_fixed
            prefix = match.group(1)
            typepad_url = match.group(2)
            mid = match.group(3)
            title = match.group(4)
            suffix = match.group(5)
            
            local_file = find_local_file_for_url(typepad_url, url_mapping, slug_mapping)
            if local_file:
                links_fixed += 1
                return f'{prefix}{local_file}{mid}{title}{suffix}'
            else:
                stats['unresolved'].append((file_path.name, typepad_url))
                return match.group(0)
        
        content = re.sub(toc_pattern, replace_toc_link, content)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        stats['files_modified'] += 1
    
    stats['links_fixed'] += links_fixed
    return links_fixed

def fix_markdown_files(url_mapping, slug_mapping, stats):
    """
    Fix Typepad links in markdown files.
    """
    print("Fixing markdown files...")
    
    md_pattern = r'\[([^\]]+)\]\((https?://thebuildingcoder\.typepad\.com/blog/[^)#]+)(#[^)]*)?\)'
    
    for md_file in BLOG_DIR.glob("*.md"):
        try:
            with open(md_file, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        except:
            continue
        
        original_content = content
        links_fixed = 0
        
        def replace_md_link(match):
            nonlocal links_fixed
            title = match.group(1)
            url = match.group(2)
            anchor = match.group(3) or ''
            
            local_file = find_local_file_for_url(url, url_mapping, slug_mapping)
            if local_file:
                links_fixed += 1
                return f'[{title}]({local_file}{anchor})'
            else:
                stats['unresolved'].append((md_file.name, url))
                return match.group(0)
        
        content = re.sub(md_pattern, replace_md_link, content)
        
        if content != original_content:
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(content)
            stats['files_modified'] += 1
            stats['links_fixed'] += links_fixed

def main():
    print("=" * 60)
    print("Fixing remaining Typepad links")
    print("=" * 60)
    
    # Build mappings
    url_mapping = build_comprehensive_url_mapping()
    slug_mapping = build_slug_to_file_mapping()
    
    stats = {
        'files_modified': 0,
        'links_fixed': 0,
        'unresolved': []
    }
    
    # Process all HTML files
    print("\nProcessing HTML files...")
    html_files = list(BLOG_DIR.glob("*.htm")) + list(BLOG_DIR.glob("*.html"))
    
    for i, file_path in enumerate(html_files):
        if file_path.name == 'index_local.html':
            continue
        fix_file(file_path, url_mapping, slug_mapping, stats)
        if (i + 1) % 200 == 0:
            print(f"  Processed {i + 1}/{len(html_files)} files...")
    
    # Process markdown files
    fix_markdown_files(url_mapping, slug_mapping, stats)
    
    # Report
    print("\n" + "=" * 60)
    print("Summary:")
    print(f"  Files modified: {stats['files_modified']}")
    print(f"  Links fixed: {stats['links_fixed']}")
    print(f"  Unresolved links: {len(stats['unresolved'])}")
    
    if stats['unresolved']:
        # Group by URL pattern
        by_pattern = defaultdict(list)
        for file, url in stats['unresolved']:
            # Categorize
            if '/files/' in url:
                by_pattern['File downloads'].append((file, url))
            elif '/blog/200' in url or '/blog/201' in url:
                by_pattern['Blog posts'].append((file, url))
            else:
                by_pattern['Other'].append((file, url))
        
        print("\nUnresolved by category:")
        for cat, items in by_pattern.items():
            print(f"  {cat}: {len(items)}")
        
        # Write report
        report_file = REPO_DIR / "remaining_links_report.txt"
        with open(report_file, 'w') as f:
            f.write("Remaining unresolved Typepad links\n")
            f.write("=" * 60 + "\n\n")
            for cat, items in sorted(by_pattern.items()):
                f.write(f"\n{cat} ({len(items)}):\n")
                f.write("-" * 40 + "\n")
                for file, url in sorted(set(items)):
                    f.write(f"  {file}: {url}\n")
        print(f"\nDetailed report written to: {report_file}")
    
    print("\nDone!")

if __name__ == '__main__':
    main()
