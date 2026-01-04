#!/usr/bin/env python3
"""
Find matching local files for unresolved blog post links based on title slugs.
"""

import re
from pathlib import Path
from collections import defaultdict

REPO_DIR = Path(__file__).parent.parent
BLOG_DIR = REPO_DIR / "a"

def normalize_slug(slug):
    """Normalize a slug for comparison."""
    # Remove .html extension
    slug = re.sub(r'\.html?$', '', slug)
    # Replace hyphens with underscores
    slug = slug.replace('-', '_')
    # Remove common prefixes/suffixes
    slug = slug.lower()
    return slug

def extract_slug_from_url(url):
    """Extract the blog post slug from a typepad URL."""
    # Pattern: /blog/YYYY/MM/slug.html
    match = re.search(r'/blog/\d{4}/\d{2}/([^/?#]+)', url)
    if match:
        slug = match.group(1)
        # Remove .html extension
        slug = re.sub(r'\.html?$', '', slug)
        return slug
    return None

def build_local_file_index():
    """Build an index of local files by their slug portions."""
    index = {}
    
    for file_path in list(BLOG_DIR.glob("*.htm")) + list(BLOG_DIR.glob("*.html")):
        name = file_path.stem  # e.g., 0036_dwg_shared_param
        
        # Skip special files
        if name in ['index', 'index_local']:
            continue
        
        # Extract the slug portion (after the number prefix)
        parts = name.split('_', 1)
        if len(parts) == 2 and parts[0].isdigit():
            slug_portion = parts[1].lower()
            index[slug_portion] = file_path.name
            
            # Also index with hyphens replaced
            slug_with_hyphens = slug_portion.replace('_', '-')
            index[slug_with_hyphens] = file_path.name
    
    return index

def find_matches():
    """Find potential matches for unresolved blog post URLs."""
    print("Building local file index...")
    local_index = build_local_file_index()
    print(f"Indexed {len(local_index)} slug variations\n")
    
    # Read fix_links_report.txt
    report_file = REPO_DIR / "fix_links_report.txt"
    with open(report_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all unresolved blog post URLs (not file downloads)
    url_pattern = re.compile(r'^\s+(\S+\.html?): (https?://thebuildingcoder\.typepad\.com/blog/\d{4}/\d{2}/[^\s]+)', re.MULTILINE)
    
    matches_found = []
    no_match = []
    
    for match in url_pattern.finditer(content):
        source_file = match.group(1)
        url = match.group(2)
        
        slug = extract_slug_from_url(url)
        if not slug:
            continue
        
        normalized = normalize_slug(slug)
        
        # Try to find a match
        found = None
        
        # Direct match
        if normalized in local_index:
            found = local_index[normalized]
        else:
            # Try partial matching - find files containing the key words
            for local_slug, local_file in local_index.items():
                # Check if significant parts match
                slug_words = set(normalized.split('_'))
                local_words = set(local_slug.split('_'))
                
                # If most words match, consider it a potential match
                common = slug_words & local_words
                if len(common) >= 2 and len(common) >= len(slug_words) * 0.5:
                    found = local_file
                    break
        
        if found:
            matches_found.append((source_file, url, slug, found))
        else:
            no_match.append((source_file, url, slug))
    
    # Print results
    print("=" * 70)
    print("POTENTIAL MATCHES FOUND")
    print("=" * 70)
    
    for source, url, slug, local_file in matches_found:
        print(f"\nSource: {source}")
        print(f"URL slug: {slug}")
        print(f"Match: {local_file}")
    
    print(f"\n\nTotal matches found: {len(matches_found)}")
    print(f"No match found: {len(no_match)}")
    
    if no_match:
        print("\n" + "=" * 70)
        print("UNMATCHED SLUGS (first 20)")
        print("=" * 70)
        for source, url, slug in no_match[:20]:
            print(f"  {slug}")
    
    return matches_found, no_match

if __name__ == "__main__":
    find_matches()
