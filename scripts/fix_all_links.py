#!/usr/bin/env python3
"""
Fix all internal links in The Building Coder blog to use local file paths.
Creates backup copies before modifying any files.
"""

import re
import os
import shutil
from pathlib import Path
from datetime import datetime

# Configuration
REPO_DIR = Path(__file__).parent
BLOG_DIR = REPO_DIR / "a"
BACKUP_DIR = REPO_DIR / "a_backup"
INDEX_FILE = BLOG_DIR / "index.html"

def create_backup():
    """Create a backup of the entire 'a' directory."""
    if BACKUP_DIR.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"a_backup_{timestamp}"
        backup_path = REPO_DIR / backup_name
        print(f"Existing backup found. Creating new backup as: {backup_name}")
    else:
        backup_path = BACKUP_DIR
    
    print(f"Creating backup of '{BLOG_DIR}' to '{backup_path}'...")
    shutil.copytree(BLOG_DIR, backup_path)
    print(f"Backup created successfully: {backup_path}")
    return backup_path

def parse_index_for_mapping():
    """
    Parse index.html to build a mapping of Typepad URLs to local filenames.
    Returns a dict: { 'typepad_url_path': 'local_filename' }
    """
    print("Parsing index.html for URL mappings...")
    
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match table rows with both Typepad and local links
    # Format: <a href="http://thebuildingcoder.typepad.com/blog/YYYY/MM/slug.html">Title</a>...<a href="NNNN_name.htm">^</a>
    pattern = r'<a href="(https?://thebuildingcoder\.typepad\.com/blog/[^"]+)">([^<]+)</a>&nbsp;&nbsp;&nbsp;<a href="([^"]+)">\^</a>'
    
    matches = re.findall(pattern, content)
    
    url_mapping = {}
    for typepad_url, title, local_file in matches:
        # Normalize to handle both http and https
        # Store the path portion after the domain
        url_path = re.sub(r'^https?://thebuildingcoder\.typepad\.com', '', typepad_url)
        url_mapping[url_path] = local_file
        
        # Also store full URLs for direct lookup
        url_mapping[typepad_url] = local_file
        # Handle both http and https variants
        if typepad_url.startswith('http://'):
            https_url = typepad_url.replace('http://', 'https://')
            url_mapping[https_url] = local_file
        elif typepad_url.startswith('https://'):
            http_url = typepad_url.replace('https://', 'http://')
            url_mapping[http_url] = local_file
    
    print(f"Found {len(matches)} URL mappings in index.html")
    return url_mapping

def fix_links_in_file(file_path, url_mapping, stats):
    """
    Fix all internal Typepad links in a single file.
    Returns the number of links fixed.
    """
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    original_content = content
    links_fixed = 0
    unresolved_links = []
    
    # Pattern to match Typepad blog links (with optional anchor and query params)
    pattern = r'href="(https?://thebuildingcoder\.typepad\.com/blog/[^"#?]+)([#][^"?]*)?(\?[^"]*)?'
    
    def replace_link(match):
        nonlocal links_fixed, unresolved_links
        
        full_url = match.group(1)
        anchor = match.group(2) or ''  # Preserve anchor if present
        query = match.group(3) or ''   # Query params (usually discard)
        
        # Try to find local file
        if full_url in url_mapping:
            local_file = url_mapping[full_url]
            links_fixed += 1
            return f'href="{local_file}{anchor}"'
        else:
            # Try without trailing slash variations
            url_variations = [
                full_url,
                full_url.rstrip('/'),
                full_url + '/',
            ]
            for url in url_variations:
                if url in url_mapping:
                    local_file = url_mapping[url]
                    links_fixed += 1
                    return f'href="{local_file}{anchor}"'
            
            # Not found - log and keep original
            unresolved_links.append(full_url)
            return match.group(0)
    
    content = re.sub(pattern, replace_link, content)
    
    # Track stats
    if unresolved_links:
        stats['unresolved'].extend([(file_path.name, url) for url in unresolved_links])
    
    # Only write if changes were made
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        stats['files_modified'] += 1
    
    stats['links_fixed'] += links_fixed
    return links_fixed

def fix_index_file(url_mapping, stats):
    """
    Fix the index.html to make local links primary.
    """
    print("Fixing index.html...")
    
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Pattern to swap Typepad and local links in index
    pattern = r'(<a href=")(https?://thebuildingcoder\.typepad\.com/blog/[^"]+)(">)([^<]+)(</a>&nbsp;&nbsp;&nbsp;<a href=")([^"]+)(">)\^(</a>)'
    
    def replace_index_link(match):
        typepad_url = match.group(2)
        title = match.group(4)
        local_file = match.group(6)
        
        # Swap: make local link primary, Typepad link secondary with "web" label
        return f'<a href="{local_file}">{title}</a>&nbsp;&nbsp;&nbsp;<a href="{typepad_url}">web</a>&nbsp;&nbsp;'
    
    content = re.sub(pattern, replace_index_link, content)
    
    # Update the table header
    content = content.replace(
        '<th>Title (Internet hyperlink) &ndash; ^ (local)</th>',
        '<th>Title (local) &ndash; web (Internet)</th>'
    )
    
    if content != original_content:
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        print("index.html updated: local links are now primary")
        stats['files_modified'] += 1

def process_all_files(url_mapping):
    """
    Process all HTML/HTM files in the blog directory.
    """
    stats = {
        'files_processed': 0,
        'files_modified': 0,
        'links_fixed': 0,
        'unresolved': []
    }
    
    # Get all HTML files
    html_files = list(BLOG_DIR.glob("*.htm")) + list(BLOG_DIR.glob("*.html"))
    html_files = [f for f in html_files if f.name != 'index.html']  # Process index separately
    
    print(f"Processing {len(html_files)} blog post files...")
    
    for i, file_path in enumerate(html_files):
        fix_links_in_file(file_path, url_mapping, stats)
        stats['files_processed'] += 1
        
        # Progress indicator every 100 files
        if (i + 1) % 100 == 0:
            print(f"  Processed {i + 1}/{len(html_files)} files...")
    
    # Fix index.html
    fix_index_file(url_mapping, stats)
    
    return stats

def write_report(stats, backup_path):
    """Write a summary report."""
    report_path = REPO_DIR / "fix_links_report.txt"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("The Building Coder - Internal Links Fix Report\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")
        
        f.write("SUMMARY\n")
        f.write("-" * 40 + "\n")
        f.write(f"Backup location: {backup_path}\n")
        f.write(f"Files processed: {stats['files_processed']}\n")
        f.write(f"Files modified: {stats['files_modified']}\n")
        f.write(f"Links fixed: {stats['links_fixed']}\n")
        f.write(f"Unresolved links: {len(stats['unresolved'])}\n\n")
        
        if stats['unresolved']:
            f.write("UNRESOLVED LINKS (require manual review)\n")
            f.write("-" * 40 + "\n")
            for filename, url in stats['unresolved']:
                f.write(f"  {filename}: {url}\n")
    
    print(f"\nReport written to: {report_path}")
    return report_path

def main():
    print("=" * 60)
    print("The Building Coder - Fix Internal Links")
    print("=" * 60)
    print()
    
    # Step 1: Create backup
    backup_path = create_backup()
    print()
    
    # Step 2: Build URL mapping from index
    url_mapping = parse_index_for_mapping()
    print()
    
    # Step 3: Process all files
    stats = process_all_files(url_mapping)
    print()
    
    # Step 4: Write report
    write_report(stats, backup_path)
    
    # Summary
    print()
    print("=" * 60)
    print("COMPLETE!")
    print("=" * 60)
    print(f"Files processed: {stats['files_processed']}")
    print(f"Files modified: {stats['files_modified']}")
    print(f"Links fixed: {stats['links_fixed']}")
    print(f"Unresolved links: {len(stats['unresolved'])}")
    print()
    print(f"Backup saved to: {backup_path}")
    print("Original files are safe in the backup directory.")
    print()
    
    if stats['unresolved']:
        print(f"WARNING: {len(stats['unresolved'])} links could not be resolved.")
        print("See fix_links_report.txt for details.")

if __name__ == "__main__":
    main()
