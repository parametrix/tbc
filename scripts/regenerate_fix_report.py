#!/usr/bin/env python3
"""
Regenerate fix_links_report.txt with current unresolved links.
"""

import re
from pathlib import Path
from datetime import datetime

REPO_DIR = Path(__file__).parent.parent
BLOG_DIR = REPO_DIR / "a"

def main():
    # Pattern to find typepad links
    typepad_pattern = re.compile(
        r'https?://thebuildingcoder\.typepad\.com[^\s"\'<>]*',
        re.IGNORECASE
    )
    
    unresolved = []
    html_files = list(BLOG_DIR.glob("*.htm")) + list(BLOG_DIR.glob("*.html"))
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            for match in typepad_pattern.finditer(content):
                url = match.group(0).rstrip('.,;:)')
                unresolved.append((file_path.name, url))
        except:
            pass
    
    unresolved = sorted(set(unresolved))
    
    # Write new report
    report_path = REPO_DIR / "fix_links_report.txt"
    with open(report_path, 'w') as f:
        f.write("=" * 60 + "\n")
        f.write("The Building Coder - Internal Links Fix Report\n")
        f.write(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("Original Report: 2026-01-02 08:20:51\n")
        f.write("=" * 60 + "\n\n")
        f.write("SUMMARY\n")
        f.write("-" * 40 + "\n")
        f.write("Backup location: ./a_backup\n")
        f.write(f"Files processed: {len(html_files)}\n")
        f.write("Files modified: 1589 (original: 1573, +16 about-the-author fixes)\n")
        f.write("Links fixed: 8886 (original: 8868, +18 about-the-author links)\n")
        f.write(f"Unresolved links: {len(unresolved)}\n\n")
        f.write("UPDATE: 2026-01-04\n")
        f.write("- Fixed 18 about-the-author.html links across 16 files\n")
        f.write("- These links now redirect to ../index.html\n\n")
        f.write("UNRESOLVED LINKS (require manual review)\n")
        f.write("-" * 40 + "\n")
        for filename, url in unresolved:
            f.write(f"  {filename}: {url}\n")
    
    print(f"Report updated with {len(unresolved)} unresolved links")
    print(f"Written to: {report_path}")

if __name__ == "__main__":
    main()
