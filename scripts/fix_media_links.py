#!/usr/bin/env python3
"""
Fix media file links (zip, pdf, etc.) by matching them to local files.
Uses EXACT filename matching only to avoid false positives.
"""

import os
import re
from pathlib import Path

# Configuration
ARCHIVE_DIR = Path(r"c:\Users\pratticole\source\repos\thebuildingcoder-archive\a")
DRY_RUN = False  # Set to False to apply fixes

def find_all_local_files():
    """Find all non-HTML files that might be media downloads."""
    local_files = {}
    for f in ARCHIVE_DIR.glob("**/*"):
        if f.is_file() and f.suffix.lower() not in ['.htm', '.html']:
            # Store by filename (case-insensitive key, actual name as value)
            local_files[f.name.lower()] = f.name
    return local_files

def find_all_html_files():
    """Get all HTML files in the archive."""
    files = []
    for ext in ['*.htm', '*.html']:
        files.extend(ARCHIVE_DIR.glob(ext))
    return sorted(files)

def extract_media_links(content):
    """Extract all typepad media links (non-html files)."""
    # Match typepad URLs that end with file extensions other than .html/.htm
    pattern = r'(https?://thebuildingcoder\.typepad\.com[^"\'\s<>]+\.(zip|pdf|doc|docx|xls|xlsx|png|jpg|jpeg|gif|mp3|mp4|avi))'
    matches = re.findall(pattern, content, re.IGNORECASE)
    return [(m[0], m[1]) for m in matches]

def get_filename_from_url(url):
    """Extract the filename from a URL."""
    # Get the last part of the URL
    filename = url.split('/')[-1]
    # Remove any query params
    if '?' in filename:
        filename = filename.split('?')[0]
    return filename

def find_local_match(url_filename, local_files):
    """Try to find a matching local file - EXACT match only."""
    url_filename_lower = url_filename.lower()
    
    # Direct exact match only
    if url_filename_lower in local_files:
        return local_files[url_filename_lower]
    
    return None

def fix_media_links():
    """Fix media links by replacing typepad URLs with local paths."""
    html_files = find_all_html_files()
    local_files = find_all_local_files()
    
    print(f"Found {len(local_files)} local non-HTML files")
    print(f"Scanning {len(html_files)} HTML files...")
    
    files_modified = 0
    links_fixed = 0
    unresolved_urls = set()
    
    for html_file in html_files:
        try:
            content = html_file.read_text(encoding='utf-8', errors='ignore')
            original_content = content
        except Exception as e:
            print(f"Error reading {html_file}: {e}")
            continue
        
        media_links = extract_media_links(content)
        file_fixes = 0
        
        for url, ext in media_links:
            filename = get_filename_from_url(url)
            local_match = find_local_match(filename, local_files)
            
            if local_match:
                # Replace the typepad URL with local path
                new_url = local_match
                content = content.replace(url, new_url)
                file_fixes += 1
            else:
                unresolved_urls.add(url)
        
        if file_fixes > 0 and content != original_content:
            if not DRY_RUN:
                html_file.write_text(content, encoding='utf-8')
            print(f"  {html_file.name}: {file_fixes} links fixed")
            files_modified += 1
            links_fixed += file_fixes
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Files modified: {files_modified}")
    print(f"Links fixed: {links_fixed}")
    print(f"Unresolved URLs: {len(unresolved_urls)}")
    
    if unresolved_urls:
        print("\n" + "="*70)
        print("UNRESOLVED MEDIA LINKS")
        print("="*70)
        for url in sorted(unresolved_urls):
            print(f"  {url}")

if __name__ == "__main__":
    fix_media_links()
