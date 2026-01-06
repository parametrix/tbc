#!/usr/bin/env python3
"""
delete_post.py - Delete a published blog post

This script removes a post and updates all related files:
- Deletes the HTML file
- Removes entry from a/toc/chrono-data.json (timeline navigation)
- Removes entry from a/toc/toc-data.json (topic sidebar)

Note: The chronological table in a/index.html is dynamically generated from
chrono-data.json via JavaScript, so updating the JSON updates the table.

Usage:
    python delete_post.py 2079_sample_post.html
    python delete_post.py 2079_sample_post.html --dry-run

Author: parametrix
Date: January 4, 2026
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

# Configuration
REPO_ROOT = Path(__file__).parent.parent
POSTS_DIR = REPO_ROOT / "a"
TOC_FILE = POSTS_DIR / "toc" / "toc-data.json"
CHRONO_FILE = POSTS_DIR / "toc" / "chrono-data.json"


def delete_html_file(filename, dry_run=False):
    """Delete the HTML post file."""
    file_path = POSTS_DIR / filename
    
    if not file_path.exists():
        print(f"Warning: File not found: {file_path}")
        return False
    
    if dry_run:
        print(f"[DRY RUN] Would delete: {file_path}")
    else:
        file_path.unlink()
        print(f"Deleted: {file_path}")
    
    return True


def remove_from_toc(filename, dry_run=False):
    """Remove the post from toc-data.json."""
    if not TOC_FILE.exists():
        print(f"Warning: TOC file not found: {TOC_FILE}")
        return False
    
    try:
        toc_data = json.loads(TOC_FILE.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e:
        print(f"Warning: Could not parse TOC file: {e}")
        return False
    
    removed = False
    
    # Search all topics for the file
    for topic in toc_data.get('topics', []):
        posts = topic.get('posts', [])
        original_len = len(posts)
        
        # Filter out the post with matching filename
        topic['posts'] = [p for p in posts if p.get('file') != filename]
        
        if len(topic['posts']) < original_len:
            removed = True
            if dry_run:
                print(f"[DRY RUN] Would remove from TOC topic '{topic.get('title')}': {filename}")
            else:
                print(f"Removed from TOC topic '{topic.get('title')}': {filename}")
    
    if removed:
        # Update metadata
        toc_data['lastUpdated'] = datetime.now().strftime("%Y-%m-%d")
        toc_data['totalPostLinks'] = sum(len(t.get('posts', [])) for t in toc_data['topics'])
        
        if not dry_run:
            TOC_FILE.write_text(
                json.dumps(toc_data, indent=2, ensure_ascii=False),
                encoding='utf-8'
            )
            print(f"Updated toc-data.json (now {toc_data['totalPostLinks']} links)")
    else:
        print(f"Note: {filename} was not found in toc-data.json")
    
    return removed


def remove_from_chrono(filename, dry_run=False):
    """Remove the post from chrono-data.json (right column timeline)."""
    if not CHRONO_FILE.exists():
        print(f"Warning: Chrono file not found: {CHRONO_FILE}")
        return False
    
    try:
        chrono_data = json.loads(CHRONO_FILE.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e:
        print(f"Warning: Could not parse chrono file: {e}")
        return False
    
    # Find and remove the post
    original_len = len(chrono_data.get('posts', []))
    removed_post = None
    
    for post in chrono_data.get('posts', []):
        if post.get('file') == filename:
            removed_post = post
            break
    
    if removed_post:
        chrono_data['posts'] = [p for p in chrono_data['posts'] if p.get('file') != filename]
        chrono_data['totalPosts'] = len(chrono_data['posts'])
        
        # Update year statistics
        year = removed_post.get('year')
        for year_entry in chrono_data.get('years', []):
            if year_entry.get('year') == year:
                year_entry['count'] -= 1
                if year_entry['count'] <= 0:
                    # Remove the year entry if no posts left
                    chrono_data['years'] = [y for y in chrono_data['years'] if y.get('year') != year]
                break
        
        chrono_data['lastUpdated'] = datetime.now().strftime("%Y-%m-%d")
        
        if dry_run:
            print(f"[DRY RUN] Would remove from chrono-data.json: {filename}")
        else:
            CHRONO_FILE.write_text(
                json.dumps(chrono_data, indent=2, ensure_ascii=False),
                encoding='utf-8'
            )
            print(f"Removed from chrono-data.json: {filename}")
        return True
    else:
        print(f"Note: {filename} was not found in chrono-data.json")
        return False


def delete_post(filename, dry_run=False):
    """Delete a post and update all related files."""
    
    # Normalize filename
    filename = Path(filename).name
    
    print(f"Deleting post: {filename}")
    print("=" * 50)
    
    # Delete HTML file
    html_deleted = delete_html_file(filename, dry_run)
    
    # Remove from TOC
    toc_updated = remove_from_toc(filename, dry_run)
    
    # Remove from chrono-data.json
    chrono_updated = remove_from_chrono(filename, dry_run)
    
    # Summary
    print()
    print("=" * 50)
    if dry_run:
        print("[DRY RUN] Summary:")
        print(f"  Would delete HTML file: {'Yes' if html_deleted else 'No (not found)'}")
        print(f"  Would update toc-data.json: {'Yes' if toc_updated else 'No'}")
        print(f"  Would update chrono-data.json: {'Yes' if chrono_updated else 'No'}")
    else:
        print("Deletion complete.")
        print("\nNext steps:")
        print("  git add -A")
        print(f'  git commit -m "Delete post: {filename}"')
        print("  git push")
    
    return html_deleted or chrono_updated


def main():
    parser = argparse.ArgumentParser(
        description="Delete a published blog post",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python delete_post.py 2079_sample_post.html
  python delete_post.py 2079_sample_post.html --dry-run
  python delete_post.py a/2079_sample_post.html  # Path is also accepted

This script removes:
  - The HTML file from a/
  - The entry from a/toc/toc-data.json (left sidebar)
  - The entry from a/toc/chrono-data.json (right column timeline)
  
Note: The chronological table is dynamically generated from chrono-data.json.
        """
    )
    
    parser.add_argument(
        "filename",
        help="Filename of the post to delete (e.g., 2079_sample_post.html)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without deleting files"
    )
    
    args = parser.parse_args()
    
    success = delete_post(args.filename, dry_run=args.dry_run)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
