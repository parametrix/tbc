#!/usr/bin/env python3
"""
Fix unresolved typepad links by matching URL date (yyyy/mm) and slug to local files.
Uses the index.html table to get publication dates for each local file.
"""

import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

REPO_DIR = Path(__file__).parent.parent
BLOG_DIR = REPO_DIR / "a"

def parse_index_for_dates():
    """
    Parse index.html to get publication dates for each local file.
    Returns dict: local_filename -> (year, month, title)
    """
    print("Parsing index.html for publication dates...")
    
    index_file = BLOG_DIR / "index.html"
    with open(index_file, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    file_dates = {}
    
    # Pattern to match table rows: <tr><td>NUM</td><td>YYYY-MM-DD</td><td><a href="file.html">Title</a>
    pattern = re.compile(
        r'<tr><td[^>]*>\s*(\d+)\s*</td><td>(\d{4})-(\d{2})-(\d{2})</td><td><a href="([^"]+)">([^<]+)</a>',
        re.IGNORECASE
    )
    
    for match in pattern.finditer(content):
        num, year, month, day, filename, title = match.groups()
        file_dates[filename] = {
            'num': int(num),
            'year': int(year),
            'month': int(month),
            'day': int(day),
            'title': title.lower(),
            'slug': filename.replace('.html', '').replace('.htm', '')
        }
    
    print(f"Found {len(file_dates)} files with dates")
    return file_dates

def extract_url_info(url):
    """Extract year, month, and slug from a typepad URL."""
    # Pattern: /blog/YYYY/MM/slug.html
    match = re.search(r'/blog/(\d{4})/(\d{2})/([^/?#]+)', url)
    if match:
        year, month, slug = match.groups()
        # Clean up slug
        slug = re.sub(r'\.html?$', '', slug).lower()
        return int(year), int(month), slug
    return None, None, None

def normalize_slug(slug):
    """Normalize a slug for comparison."""
    return slug.replace('-', '_').replace(' ', '_').lower()

def calculate_similarity(slug1, slug2):
    """Calculate word-based similarity between two slugs."""
    words1 = set(normalize_slug(slug1).split('_'))
    words2 = set(normalize_slug(slug2).split('_'))
    
    # Remove common short words
    stopwords = {'a', 'an', 'the', 'and', 'or', 'to', 'in', 'on', 'at', 'for', 'of', 'with'}
    words1 = words1 - stopwords
    words2 = words2 - stopwords
    
    if not words1 or not words2:
        return 0
    
    common = words1 & words2
    return len(common) / max(len(words1), len(words2))

def find_best_match(year, month, slug, file_dates):
    """Find the best matching local file for a given year/month/slug."""
    candidates = []
    
    for filename, info in file_dates.items():
        # Check if file is from same year and month
        if info['year'] == year and info['month'] == month:
            # Calculate similarity
            sim = calculate_similarity(slug, info['slug'])
            title_sim = calculate_similarity(slug, info['title'])
            best_sim = max(sim, title_sim)
            
            if best_sim > 0:
                candidates.append((filename, best_sim, info))
    
    # Also check files from adjacent months (in case of date boundary issues)
    for filename, info in file_dates.items():
        if (info['year'] == year and abs(info['month'] - month) == 1) or \
           (info['year'] == year - 1 and month == 1 and info['month'] == 12) or \
           (info['year'] == year + 1 and month == 12 and info['month'] == 1):
            sim = calculate_similarity(slug, info['slug'])
            title_sim = calculate_similarity(slug, info['title'])
            best_sim = max(sim, title_sim)
            
            if best_sim >= 0.4:  # Higher threshold for adjacent months
                candidates.append((filename, best_sim * 0.9, info))  # Slightly penalize
    
    if candidates:
        # Sort by similarity, return best match
        candidates.sort(key=lambda x: x[1], reverse=True)
        best = candidates[0]
        if best[1] >= 0.3:  # Minimum similarity threshold
            return best[0], best[1]
    
    return None, 0

def scan_and_fix():
    """Scan for unresolved links and try to fix them using date+slug matching."""
    file_dates = parse_index_for_dates()
    
    # Pattern to find typepad blog post links
    blog_url_pattern = re.compile(
        r'(https?://thebuildingcoder\.typepad\.com/blog/\d{4}/\d{2}/[^"\s<>]+\.html?[^"\s<>]*)',
        re.IGNORECASE
    )
    
    files_modified = 0
    links_fixed = 0
    fixed_mappings = []
    unresolved = []
    
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
            year, month, slug = extract_url_info(url)
            
            if not year or not slug:
                continue
            
            local_file, similarity = find_best_match(year, month, slug, file_dates)
            
            if local_file and similarity >= 0.3:
                # Preserve anchor from original URL
                anchor_match = re.search(r'(#[^"\s<>]*)$', url)
                anchor = anchor_match.group(1) if anchor_match else ''
                
                new_ref = local_file + anchor
                content = content.replace(url, new_ref)
                file_fixes += 1
                fixed_mappings.append((file_path.name, slug, local_file, similarity))
            else:
                unresolved.append((file_path.name, url, slug, year, month))
        
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
        print("FIXED MAPPINGS (showing all)")
        print("=" * 70)
        for source, slug, target, sim in sorted(fixed_mappings, key=lambda x: -x[3]):
            print(f"  [{sim:.2f}] {source}: {slug} -> {target}")
    
    if unresolved:
        # Group by year/month
        by_date = defaultdict(list)
        for source, url, slug, year, month in unresolved:
            by_date[(year, month)].append((source, slug))
        
        print("\n" + "=" * 70)
        print("UNRESOLVED BY DATE (first 50)")
        print("=" * 70)
        count = 0
        for (year, month), items in sorted(by_date.items()):
            for source, slug in items[:5]:
                print(f"  {year}/{month:02d}: {slug} (in {source})")
                count += 1
                if count >= 50:
                    break
            if count >= 50:
                break
    
    return files_modified, links_fixed, unresolved

if __name__ == "__main__":
    scan_and_fix()
