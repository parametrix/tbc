#!/usr/bin/env python3
"""
Scan for remaining unresolved Typepad links and generate a report.
"""

import re
from pathlib import Path
from collections import defaultdict

# Configuration - correct paths
REPO_DIR = Path(__file__).parent.parent
BLOG_DIR = REPO_DIR / "a"

def main():
    print("=" * 60)
    print("Scanning for remaining unresolved Typepad links")
    print("=" * 60)
    
    # Pattern to find typepad links
    typepad_pattern = re.compile(
        r'https?://thebuildingcoder\.typepad\.com[^\s"\'<>]*',
        re.IGNORECASE
    )
    
    unresolved = []
    
    # Scan HTML files
    html_files = list(BLOG_DIR.glob("*.htm")) + list(BLOG_DIR.glob("*.html"))
    print(f"Scanning {len(html_files)} files...")
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            continue
        
        # Find all typepad links
        for match in typepad_pattern.finditer(content):
            url = match.group(0)
            # Clean up trailing punctuation
            url = url.rstrip('.,;:)')
            unresolved.append((file_path.name, url))
    
    # Also scan markdown files
    md_files = list(BLOG_DIR.glob("*.md"))
    for file_path in md_files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        except Exception as e:
            continue
        
        for match in typepad_pattern.finditer(content):
            url = match.group(0)
            url = url.rstrip('.,;:)')
            unresolved.append((file_path.name, url))
    
    # Remove duplicates and sort
    unresolved = sorted(set(unresolved))
    
    print(f"\nFound {len(unresolved)} unresolved Typepad links")
    
    if unresolved:
        # Group by URL pattern
        by_pattern = defaultdict(list)
        for file, url in unresolved:
            if '/files/' in url:
                by_pattern['File downloads'].append((file, url))
            elif '/blog/200' in url or '/blog/201' in url:
                by_pattern['Blog posts'].append((file, url))
            else:
                by_pattern['Other'].append((file, url))
        
        print("\nBy category:")
        for cat, items in sorted(by_pattern.items()):
            print(f"  {cat}: {len(items)}")
        
        # Write report
        report_file = REPO_DIR / "remaining_links_report.txt"
        with open(report_file, 'w') as f:
            f.write("Remaining unresolved Typepad links\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Total: {len(unresolved)} unresolved links\n")
            f.write(f"Generated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for cat, items in sorted(by_pattern.items()):
                f.write(f"\n{cat} ({len(items)}):\n")
                f.write("-" * 40 + "\n")
                for file, url in sorted(set(items)):
                    f.write(f"  {file}: {url}\n")
        
        print(f"\nReport written to: {report_file}")
    else:
        # No unresolved links - write empty report
        report_file = REPO_DIR / "remaining_links_report.txt"
        with open(report_file, 'w') as f:
            f.write("Remaining unresolved Typepad links\n")
            f.write("=" * 60 + "\n\n")
            f.write("No unresolved Typepad links found!\n")
            f.write(f"Generated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        print(f"\nReport written to: {report_file}")
    
    print("\nDone!")

if __name__ == '__main__':
    main()
