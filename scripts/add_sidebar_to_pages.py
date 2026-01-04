#!/usr/bin/env python3
"""
add_sidebar_to_pages.py - Inject sidebar into all HTML pages

This script modifies all HTML files in the a/ directory to include
the sidebar CSS, JS, and placeholder elements.

Author: GitHub Copilot
Date: January 2, 2026
"""

import re
import os
from pathlib import Path
from typing import Tuple
import shutil
from datetime import datetime

# Configuration
BACKUP_ENABLED = False  # Set to True to create backups
DRY_RUN = False  # Set to True to see what would change without modifying files

def inject_sidebar(html_content: str, filename: str) -> Tuple[str, bool]:
    """
    Inject sidebar elements into HTML content.
    
    Returns:
        Tuple of (modified_content, was_modified)
    """
    # Skip if already has sidebar
    if 'tbc-sidebar' in html_content:
        return html_content, False
    
    modified = html_content
    changes_made = False
    
    # 1. Add CSS link in <head>
    css_link = '<link rel="stylesheet" href="toc/toc-sidebar.css">'
    
    # Try to insert before </head>
    if '</head>' in modified and css_link not in modified:
        modified = modified.replace('</head>', f'  {css_link}\n</head>')
        changes_made = True
    elif '<head>' in modified and css_link not in modified:
        # Insert after <head>
        modified = modified.replace('<head>', f'<head>\n  {css_link}')
        changes_made = True
    elif '<HEAD>' in modified and css_link not in modified:
        modified = modified.replace('</HEAD>', f'  {css_link}\n</HEAD>')
        changes_made = True
    
    # 2. Add JS script before </body>
    js_script = '<script src="toc/toc-sidebar.js"></script>'
    
    if '</body>' in modified and js_script not in modified:
        modified = modified.replace('</body>', f'{js_script}\n</body>')
        changes_made = True
    elif '</BODY>' in modified and js_script not in modified:
        modified = modified.replace('</BODY>', f'{js_script}\n</BODY>')
        changes_made = True
    elif js_script not in modified:
        # No </body> tag, append at end
        modified = modified + f'\n{js_script}'
        changes_made = True
    
    # 3. Ensure DOCTYPE exists
    if not modified.strip().lower().startswith('<!doctype'):
        modified = '<!DOCTYPE html>\n' + modified
        changes_made = True
    
    return modified, changes_made


def process_file(file_path: Path, stats: dict):
    """Process a single HTML file."""
    try:
        # Read file
        content = file_path.read_text(encoding='utf-8', errors='replace')
        
        # Inject sidebar
        modified_content, was_modified = inject_sidebar(content, file_path.name)
        
        if was_modified:
            if DRY_RUN:
                print(f"  [DRY RUN] Would modify: {file_path.name}")
                stats['would_modify'] += 1
            else:
                # Create backup if enabled
                if BACKUP_ENABLED:
                    backup_path = file_path.with_suffix(file_path.suffix + '.bak')
                    shutil.copy2(file_path, backup_path)
                
                # Write modified content
                file_path.write_text(modified_content, encoding='utf-8')
                stats['modified'] += 1
        else:
            stats['skipped'] += 1
            
    except Exception as e:
        print(f"  ERROR processing {file_path.name}: {e}")
        stats['errors'] += 1


def main():
    """Main function to process all HTML files."""
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    html_dir = repo_root / "a"
    
    print("=" * 60)
    print("Add Sidebar to HTML Pages")
    print("=" * 60)
    print(f"Directory: {html_dir}")
    print(f"Backup: {'Enabled' if BACKUP_ENABLED else 'Disabled'}")
    print(f"Mode: {'DRY RUN' if DRY_RUN else 'LIVE'}")
    print("=" * 60)
    
    if not html_dir.exists():
        print(f"ERROR: Directory not found: {html_dir}")
        return 1
    
    # Find all HTML files
    html_files = list(html_dir.glob("*.html")) + list(html_dir.glob("*.htm"))
    
    # Exclude toc directory
    html_files = [f for f in html_files if 'toc' not in str(f)]
    
    print(f"Found {len(html_files)} HTML files")
    print("-" * 60)
    
    stats = {
        'modified': 0,
        'skipped': 0,
        'errors': 0,
        'would_modify': 0
    }
    
    # Process files
    for i, file_path in enumerate(html_files, 1):
        if i % 100 == 0 or i == len(html_files):
            print(f"Processing: {i}/{len(html_files)} files...")
        process_file(file_path, stats)
    
    # Print summary
    print("-" * 60)
    print("Summary:")
    if DRY_RUN:
        print(f"  Would modify: {stats['would_modify']}")
    else:
        print(f"  Modified: {stats['modified']}")
    print(f"  Skipped (already has sidebar): {stats['skipped']}")
    print(f"  Errors: {stats['errors']}")
    print("=" * 60)
    
    if stats['errors'] > 0:
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
