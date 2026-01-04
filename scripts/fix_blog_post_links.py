#!/usr/bin/env python3
"""
Fix blog post links by matching URL slugs to local files using the index.html table.
"""

import re
from pathlib import Path
from collections import defaultdict

REPO_DIR = Path(__file__).parent.parent
BLOG_DIR = REPO_DIR / "a"

def build_slug_to_file_mapping():
    """
    Build a mapping from blog post slugs to local files.
    Uses a combination of index.html table and direct filename analysis.
    """
    print("Building slug-to-file mapping...")
    
    slug_to_file = {}
    
    # Parse all local htm/html files and create mappings
    for file_path in list(BLOG_DIR.glob("*.htm")) + list(BLOG_DIR.glob("*.html")):
        name = file_path.stem  # e.g., 1159_va3c_resolve_assembly or 0036_dwg_shared_param
        
        if name in ['index', 'index_local']:
            continue
        
        # Extract the slug portion (after the number prefix)
        parts = name.split('_', 1)
        if len(parts) == 2 and parts[0].isdigit():
            slug_portion = parts[1].lower()
            
            # Store with underscores
            slug_to_file[slug_portion] = file_path.name
            
            # Also store with hyphens (URL format)
            slug_with_hyphens = slug_portion.replace('_', '-')
            slug_to_file[slug_with_hyphens] = file_path.name
    
    print(f"Built mapping with {len(slug_to_file)} entries")
    return slug_to_file

def extract_slug_from_url(url):
    """Extract the blog post slug from a typepad URL."""
    # Pattern: /blog/YYYY/MM/slug.html
    match = re.search(r'/blog/\d{4}/\d{2}/([^/?#]+)', url)
    if match:
        slug = match.group(1)
        # Remove .html extension and anchors
        slug = re.sub(r'\.html?$', '', slug)
        return slug.lower()
    return None

def find_best_match(slug, slug_to_file):
    """Try to find the best matching local file for a slug."""
    if not slug:
        return None
    
    # Direct match
    if slug in slug_to_file:
        return slug_to_file[slug]
    
    # Try with hyphens replaced by underscores
    normalized = slug.replace('-', '_')
    if normalized in slug_to_file:
        return slug_to_file[normalized]
    
    # Try partial matching - split into words
    slug_words = set(slug.replace('-', '_').split('_'))
    
    best_match = None
    best_score = 0
    
    for local_slug, local_file in slug_to_file.items():
        local_words = set(local_slug.replace('-', '_').split('_'))
        
        # Calculate overlap score
        common = slug_words & local_words
        if len(common) >= 2:
            # Score based on overlap and similarity
            score = len(common) / max(len(slug_words), len(local_words))
            if score > best_score and score >= 0.5:
                best_score = score
                best_match = local_file
    
    return best_match

def scan_and_fix_links():
    """Scan files for typepad blog links and fix them."""
    slug_to_file = build_slug_to_file_mapping()
    
    # Pattern to find typepad blog post links
    blog_url_pattern = re.compile(
        r'(https?://thebuildingcoder\.typepad\.com/blog/\d{4}/\d{2}/[^"\s<>]+)',
        re.IGNORECASE
    )
    
    files_modified = 0
    links_fixed = 0
    unresolved = []
    fixed_mappings = []
    
    html_files = list(BLOG_DIR.glob("*.htm")) + list(BLOG_DIR.glob("*.html"))
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        except Exception as e:
            continue
        
        original = content
        file_fixes = 0
        
        for match in blog_url_pattern.finditer(content):
            url = match.group(1)
            slug = extract_slug_from_url(url)
            
            if not slug:
                continue
            
            local_file = find_best_match(slug, slug_to_file)
            
            if local_file:
                # Replace the URL with local file reference
                # Keep any anchor from original URL
                anchor_match = re.search(r'(#[^"\s<>]*)$', url)
                anchor = anchor_match.group(1) if anchor_match else ''
                
                new_ref = local_file + anchor
                content = content.replace(url, new_ref)
                file_fixes += 1
                fixed_mappings.append((file_path.name, slug, local_file))
            else:
                unresolved.append((file_path.name, url, slug))
        
        if content != original:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            files_modified += 1
            links_fixed += file_fixes
            print(f"  {file_path.name}: {file_fixes} links fixed")
    
    # Report
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Files modified: {files_modified}")
    print(f"Links fixed: {links_fixed}")
    print(f"Unresolved: {len(unresolved)}")
    
    if fixed_mappings:
        print("\n" + "=" * 70)
        print("FIXED MAPPINGS (first 30)")
        print("=" * 70)
        for source, slug, target in fixed_mappings[:30]:
            print(f"  {source}: {slug} -> {target}")
    
    if unresolved:
        print("\n" + "=" * 70)
        print("UNRESOLVED (first 30)")
        print("=" * 70)
        for source, url, slug in unresolved[:30]:
            print(f"  {source}: {slug}")
    
    return files_modified, links_fixed, unresolved

if __name__ == "__main__":
    scan_and_fix_links()
