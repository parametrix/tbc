#!/usr/bin/env python3
"""
update_from_markdown.py - Regenerate HTML from updated Markdown source

This script takes a markdown file from a/drafts/published/ and regenerates
the corresponding HTML file, updating the JSON metadata if title/date changed.

Usage:
    python update_from_markdown.py a/drafts/published/2026-01-05-my-post.md
    python update_from_markdown.py a/drafts/published/2026-01-05-my-post.md --dry-run

Author: parametrix
Date: January 6, 2026
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    import markdown
    import frontmatter
except ImportError:
    print("Missing required packages. Install with:")
    print("  pip install markdown python-frontmatter")
    sys.exit(1)

# Configuration
REPO_ROOT = Path(__file__).parent.parent
POSTS_DIR = REPO_ROOT / "a"
CHRONO_FILE = POSTS_DIR / "toc" / "chrono-data.json"
TOC_FILE = POSTS_DIR / "toc" / "toc-data.json"

# HTML template (same as publish_post.py)
POST_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Building Coder</title>
    <link rel="stylesheet" href="bc.css">
    <link rel="stylesheet" href="google-code-prettify/prettify.css">
    <script src="google-code-prettify/run_prettify.js"></script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        a {{ color: #0066cc; }}
        img {{ max-width: 100%; height: auto; }}
        .nav {{ margin-bottom: 20px; padding: 10px; background: #f5f5f5; border-radius: 5px; }}
        .nav a {{ margin-right: 15px; }}
    </style>
  <link rel="stylesheet" href="toc/toc-sidebar.css">
</head>
<body>
    <div class="nav">
        <a href="index.html">← Back to Index</a>
    </div>
    <article>
{content}
    </article>
    <div class="nav">
        <a href="index.html">← Back to Index</a>
    </div>
<script src="toc/toc-sidebar.js"></script>
<script src="toc/copy-code.js"></script>
</body>
</html>
'''


def convert_markdown_to_html(md_content):
    """Convert Markdown content to HTML."""
    md = markdown.Markdown(extensions=[
        'fenced_code',
        'tables',
        'toc',
        'nl2br',
        'sane_lists',
    ])
    html = md.convert(md_content)
    
    # Add prettyprint class to code blocks for syntax highlighting
    html = re.sub(
        r'<pre><code class="language-(\w+)">',
        r'<pre class="prettyprint lang-\1"><code>',
        html
    )
    html = re.sub(
        r'<pre><code>',
        r'<pre class="prettyprint"><code>',
        html
    )
    
    return html


def find_html_file(md_filename):
    """Find the corresponding HTML file for a published markdown file."""
    md_path = Path(md_filename)
    if not md_path.exists():
        return None
    
    content = md_path.read_text(encoding='utf-8')
    post = frontmatter.loads(content)
    
    # First, check for html_file in front matter (most reliable)
    if post.get('html_file'):
        html_path = POSTS_DIR / post.get('html_file')
        if html_path.exists():
            return html_path
    
    # Second, check for post_number in front matter
    if post.get('post_number'):
        post_num = post.get('post_number')
        # Find HTML file with this number
        for f in POSTS_DIR.glob(f"{post_num:04d}_*.html"):
            return f
        for f in POSTS_DIR.glob(f"{post_num:04d}_*.htm"):
            return f
    
    # Try to match by slug
    stem = md_path.stem
    # Remove date prefix if present (YYYY-MM-DD-)
    slug_match = re.match(r'\d{4}-\d{2}-\d{2}[_-](.+)', stem)
    if slug_match:
        slug = slug_match.group(1).lower().replace('-', '_')
    else:
        slug = stem.lower().replace('-', '_')
    
    # Search for matching HTML file
    for f in POSTS_DIR.glob("*.html"):
        if slug in f.stem.lower():
            return f
    for f in POSTS_DIR.glob("*.htm"):
        if slug in f.stem.lower():
            return f
    
    return None


def update_chrono_data(html_filename, new_title, new_date, dry_run=False):
    """Update post metadata in chrono-data.json if changed."""
    if not CHRONO_FILE.exists():
        print(f"Warning: Chrono file not found: {CHRONO_FILE}")
        return False
    
    try:
        chrono_data = json.loads(CHRONO_FILE.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e:
        print(f"Warning: Could not parse chrono file: {e}")
        return False
    
    updated = False
    for post in chrono_data.get('posts', []):
        if post.get('file') == html_filename:
            if post.get('title') != new_title:
                print(f"  Updating title: '{post.get('title')}' → '{new_title}'")
                post['title'] = new_title
                updated = True
            
            new_date_str = new_date.strftime("%Y-%m-%d")
            if post.get('date') != new_date_str:
                print(f"  Updating date: '{post.get('date')}' → '{new_date_str}'")
                post['date'] = new_date_str
                post['year'] = new_date.year
                post['month'] = new_date.month
                updated = True
            break
    
    if updated:
        chrono_data['lastUpdated'] = datetime.now().strftime("%Y-%m-%d")
        if not dry_run:
            CHRONO_FILE.write_text(
                json.dumps(chrono_data, indent=2, ensure_ascii=False),
                encoding='utf-8'
            )
            print(f"  Updated chrono-data.json")
        else:
            print(f"  [DRY RUN] Would update chrono-data.json")
    
    return updated


def update_toc_data(html_filename, new_title, dry_run=False):
    """Update post title in toc-data.json if changed."""
    if not TOC_FILE.exists():
        print(f"Warning: TOC file not found: {TOC_FILE}")
        return False
    
    try:
        toc_data = json.loads(TOC_FILE.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e:
        print(f"Warning: Could not parse TOC file: {e}")
        return False
    
    updated = False
    for topic in toc_data.get('topics', []):
        for post in topic.get('posts', []):
            if post.get('file') == html_filename:
                if post.get('title') != new_title:
                    print(f"  Updating title in topic: '{post.get('title')}' → '{new_title}'")
                    post['title'] = new_title
                    updated = True
                break
        
        for subtopic in topic.get('subTopics', []):
            for post in subtopic.get('posts', []):
                if post.get('file') == html_filename:
                    if post.get('title') != new_title:
                        print(f"  Updating title in subtopic: '{post.get('title')}' → '{new_title}'")
                        post['title'] = new_title
                        updated = True
                    break
    
    if updated:
        toc_data['lastUpdated'] = datetime.now().strftime("%Y-%m-%d")
        if not dry_run:
            TOC_FILE.write_text(
                json.dumps(toc_data, indent=2, ensure_ascii=False),
                encoding='utf-8'
            )
            print(f"  Updated toc-data.json")
        else:
            print(f"  [DRY RUN] Would update toc-data.json")
    
    return updated


def update_post(md_file, dry_run=False):
    """Regenerate HTML from updated markdown and update metadata."""
    md_path = Path(md_file)
    
    if not md_path.exists():
        print(f"Error: Markdown file not found: {md_file}")
        return False
    
    print(f"Processing: {md_path.name}")
    
    # Find the corresponding HTML file
    html_file = find_html_file(md_file)
    if not html_file:
        print(f"Error: Could not find corresponding HTML file for {md_file}")
        print("  Make sure the markdown has 'post_number' in front matter")
        print("  or the filename slug matches an existing post")
        return False
    
    print(f"  Found HTML: {html_file.name}")
    
    # Read the markdown file
    content = md_path.read_text(encoding='utf-8')
    post = frontmatter.loads(content)
    
    # Extract metadata
    new_title = post.get('title', md_path.stem.replace('-', ' ').title())
    new_date = post.get('date')
    if new_date:
        if isinstance(new_date, str):
            new_date = datetime.strptime(new_date, "%Y-%m-%d")
    else:
        new_date = datetime.now()
    
    print(f"  Title: {new_title}")
    print(f"  Date: {new_date.strftime('%Y-%m-%d')}")
    
    # Convert markdown to HTML
    html_content = convert_markdown_to_html(post.content)
    full_html = POST_TEMPLATE.format(content=html_content)
    
    # Write the updated HTML
    if dry_run:
        print(f"  [DRY RUN] Would update: {html_file}")
    else:
        html_file.write_text(full_html, encoding='utf-8')
        print(f"  Updated: {html_file}")
    
    # Update JSON metadata
    html_filename = html_file.name
    update_chrono_data(html_filename, new_title, new_date, dry_run)
    update_toc_data(html_filename, new_title, dry_run)
    
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Successfully updated post from {md_path.name}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Regenerate HTML from updated Markdown source",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python update_from_markdown.py a/drafts/published/2026-01-05-my-post.md
  python update_from_markdown.py a/drafts/published/2026-01-05-my-post.md --dry-run

The markdown file must have either:
  - 'post_number' in front matter (e.g., post_number: 2079)
  - A filename slug that matches an existing HTML file
        """
    )
    
    parser.add_argument(
        "markdown_file",
        help="Path to the published Markdown file to regenerate from"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing files"
    )
    
    args = parser.parse_args()
    
    success = update_post(args.markdown_file, dry_run=args.dry_run)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
