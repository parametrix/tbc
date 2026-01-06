#!/usr/bin/env python3
"""
publish_post.py - Publish a new blog post from Markdown to HTML

This script converts a Markdown file to HTML with the proper template,
updates the TOC sidebar, timeline navigation, and homepage stats.

Note: The chronological table in a/index.html is dynamically generated from
chrono-data.json via JavaScript, so updating the JSON updates the table.

Usage:
    python publish_post.py a/drafts/my-post.md
    python publish_post.py a/drafts/my-post.md --date 2026-01-05 --title "My Title"
    python publish_post.py a/drafts/my-post.md --dry-run

Author: parametrix
Date: January 4, 2026
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
DRAFTS_DIR = POSTS_DIR / "drafts"
CHRONO_FILE = POSTS_DIR / "toc" / "chrono-data.json"
TOC_FILE = POSTS_DIR / "toc" / "toc-data.json"
ROOT_INDEX = REPO_ROOT / "index.html"

# Topic assignment:
# - New posts are automatically added to the "Uncategorized" topic (ID 5.99)
# - Use manage_topics.py to move posts to subject-specific topics
# - The right-side timeline (chrono-data.json) is always updated

# HTML template for new posts
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


def get_next_post_number():
    """Determine the next post number by scanning existing files."""
    max_num = 0
    for f in POSTS_DIR.glob("*.htm*"):
        match = re.match(r"(\d{4})_", f.name)
        if match:
            num = int(match.group(1))
            if num > max_num:
                max_num = num
    return max_num + 1


def slugify(title):
    """Convert a title to a URL-friendly slug."""
    # Remove special characters and convert to lowercase
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    # Replace spaces with underscores
    slug = re.sub(r'[\s-]+', '_', slug)
    # Limit length
    return slug[:50].strip('_')


def convert_markdown_to_html(md_content):
    """Convert Markdown content to HTML."""
    # Configure markdown with extensions
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


def read_post(md_file):
    """Read and parse a Markdown file with front matter."""
    content = Path(md_file).read_text(encoding='utf-8')
    post = frontmatter.loads(content)
    return post


def update_chrono_data(title, filename, post_number, post_date, dry_run=False):
    """Add the new post to chrono-data.json (right-side timeline navigation)."""
    if not CHRONO_FILE.exists():
        print(f"Warning: Chrono file not found: {CHRONO_FILE}")
        return False
    
    try:
        chrono_data = json.loads(CHRONO_FILE.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e:
        print(f"Warning: Could not parse chrono file: {e}")
        return False
    
    year = post_date.year
    date_str = post_date.strftime("%Y-%m-%d")
    
    # Create new post entry
    new_post = {
        "num": post_number,
        "file": filename,
        "title": title,
        "date": date_str,
        "year": year,
        "month": post_date.month
    }
    
    # Check if post already exists (avoid duplicates)
    existing_nums = [p.get('num') for p in chrono_data.get('posts', [])]
    if post_number not in existing_nums:
        # Add post and re-sort by number
        chrono_data['posts'].append(new_post)
        chrono_data['posts'].sort(key=lambda p: p['num'])
        chrono_data['totalPosts'] = len(chrono_data['posts'])
    
    # Update year statistics
    year_found = False
    for year_entry in chrono_data.get('years', []):
        if year_entry.get('year') == year:
            year_entry['count'] += 1
            year_entry['lastPost'] = max(year_entry['lastPost'], post_number)
            year_found = True
            break
    
    if not year_found:
        # Create new year entry
        new_year = {
            "year": year,
            "count": 1,
            "firstPost": post_number,
            "lastPost": post_number
        }
        chrono_data['years'].append(new_year)
        chrono_data['years'].sort(key=lambda y: y['year'], reverse=True)
    
    # Update metadata
    chrono_data['lastUpdated'] = datetime.now().strftime("%Y-%m-%d")
    
    if dry_run:
        print(f"[DRY RUN] Would add to chrono-data.json: #{post_number:04d}")
        print(f"[DRY RUN] Chrono would have {chrono_data['totalPosts']} posts")
    else:
        CHRONO_FILE.write_text(
            json.dumps(chrono_data, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
        print(f"Updated chrono-data.json:")
        print(f"  - Added post #{post_number:04d} ({year})")
    
    return True


def update_toc_data(title, filename, dry_run=False):
    """Add the new post to the Uncategorized topic in toc-data.json."""
    if not TOC_FILE.exists():
        print(f"Warning: TOC file not found: {TOC_FILE}")
        return False
    
    try:
        toc_data = json.loads(TOC_FILE.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e:
        print(f"Warning: Could not parse TOC file: {e}")
        return False
    
    # Find the Uncategorized topic (ID 5.99)
    uncategorized = None
    for topic in toc_data.get('topics', []):
        if topic.get('id') == '5.99':
            uncategorized = topic
            break
    
    if uncategorized is None:
        print("Warning: Uncategorized topic (ID 5.99) not found in toc-data.json")
        return False
    
    # Create new post entry
    new_post = {
        "title": title,
        "file": filename
    }
    
    # Check if post already exists (avoid duplicates)
    existing_files = [p.get('file') for p in uncategorized.get('posts', [])]
    if filename not in existing_files:
        uncategorized['posts'].append(new_post)
        toc_data['totalPostLinks'] = toc_data.get('totalPostLinks', 0) + 1
    
    # Update metadata
    toc_data['lastUpdated'] = datetime.now().strftime("%Y-%m-%d")
    
    if dry_run:
        print(f"[DRY RUN] Would add to Uncategorized topic in toc-data.json")
    else:
        TOC_FILE.write_text(
            json.dumps(toc_data, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
        print(f"Updated toc-data.json:")
        print(f"  - Added to Uncategorized topic")
    
    return True


def update_homepage_stats(post_count, dry_run=False):
    """Update the post count on the homepage."""
    if not ROOT_INDEX.exists():
        print(f"Warning: Homepage not found: {ROOT_INDEX}")
        return False
    
    content = ROOT_INDEX.read_text(encoding='utf-8')
    
    # Update the stats number (e.g., "2000+" -> "2100+")
    # Round down to nearest 100 for display
    display_count = (post_count // 100) * 100
    new_stat = f"{display_count}+"
    
    # Pattern to find the blog posts stat (handles newlines between divs)
    pattern = r'(<div class="number">)\d+\+?(</div>\s*<div class="label">Blog Posts)'
    replacement = rf'\g<1>{new_stat}\g<2>'
    
    new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)
    
    if count > 0:
        if dry_run:
            print(f"[DRY RUN] Would update homepage stats to {new_stat} posts")
        else:
            ROOT_INDEX.write_text(new_content, encoding='utf-8')
            print(f"Updated homepage stats to {new_stat} posts")
        return True
    else:
        # Try alternate pattern
        pattern2 = r'(<div class="number">)[\d,]+\+?(</div>)'
        if re.search(pattern2, content):
            new_content = re.sub(pattern2, rf'\g<1>{new_stat}\g<2>', content, count=1)
            if not dry_run:
                ROOT_INDEX.write_text(new_content, encoding='utf-8')
            print(f"{'[DRY RUN] Would update' if dry_run else 'Updated'} homepage stats")
            return True
    
    return False


def publish_post(md_file, date=None, title=None, slug=None, 
                 dry_run=False, update_toc_flag=True, 
                 update_stats=True):
    """Publish a Markdown file as an HTML blog post."""
    
    md_path = Path(md_file)
    if not md_path.exists():
        print(f"Error: File not found: {md_file}")
        return False
    
    print(f"Processing: {md_path.name}")
    
    # Read the Markdown file
    post = read_post(md_path)
    
    # Extract metadata from front matter or arguments
    post_title = title or post.get('title', md_path.stem.replace('-', ' ').title())
    post_date = date
    if not post_date:
        fm_date = post.get('date')
        if fm_date:
            if isinstance(fm_date, str):
                post_date = datetime.strptime(fm_date, "%Y-%m-%d")
            else:
                post_date = fm_date
        else:
            post_date = datetime.now()
    elif isinstance(post_date, str):
        post_date = datetime.strptime(post_date, "%Y-%m-%d")
    
    categories = post.get('categories', [])
    if isinstance(categories, str):
        categories = [c.strip() for c in categories.split(',')]
    
    tags = post.get('tags', [])
    
    # Generate post number and filename
    post_number = post.get('post_number') or get_next_post_number()
    post_slug = slug or post.get('slug') or slugify(post_title)
    filename = f"{post_number:04d}_{post_slug}.html"
    
    print(f"  Title: {post_title}")
    print(f"  Date: {post_date.strftime('%Y-%m-%d')}")
    print(f"  Number: {post_number}")
    print(f"  Filename: {filename}")
    print(f"  Categories: {categories}")
    
    # Convert Markdown to HTML
    html_content = convert_markdown_to_html(post.content)
    
    # Wrap with template
    full_html = POST_TEMPLATE.format(content=html_content)
    
    # Write the HTML file
    output_path = POSTS_DIR / filename
    
    if dry_run:
        print(f"\n[DRY RUN] Would create: {output_path}")
        print(f"[DRY RUN] HTML preview (first 500 chars):")
        print(full_html[:500])
    else:
        output_path.write_text(full_html, encoding='utf-8')
        print(f"Created: {output_path}")
    
    # Update chrono-data.json (right column - timeline navigation)
    # Note: This also populates the chronological table in a/index.html (dynamically generated)
    if update_toc_flag:
        update_chrono_data(post_title, filename, post_number, post_date, dry_run)
    
    # Update toc-data.json (left sidebar - add to Uncategorized topic)
    if update_toc_flag:
        update_toc_data(post_title, filename, dry_run)
    
    # Update homepage stats
    if update_stats:
        update_homepage_stats(post_number, dry_run)
    
    # Summary
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Successfully published post #{post_number}")
    
    if not dry_run:
        print("\nNext steps:")
        print("  git add -A")
        print(f'  git commit -m "Add post {post_number}: {post_title}"')
        print("  git push")
        print("\nTo move this post to a specific topic (from Uncategorized):")
        print(f"  python scripts/manage_topics.py remove-post 5.99 {filename}")
        print(f"  python scripts/manage_topics.py add-post <topic_id> {filename} \"{post_title}\"")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Publish a Markdown file as a blog post",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python publish_post.py a/drafts/my-post.md
  python publish_post.py a/drafts/my-post.md --date 2026-01-05 --title "My Title"
  python publish_post.py a/drafts/my-post.md --dry-run

Updates performed:
  - Creates HTML file in a/ directory
  - Adds to a/toc/chrono-data.json (right column timeline navigation)
  - Adds to Uncategorized topic in a/toc/toc-data.json (left sidebar)
  - Updates post count on homepage (index.html)
  
Note: The chronological table is dynamically generated from chrono-data.json.
      New posts are added to the Uncategorized topic (ID 5.99) by default.
      Use manage_topics.py to move posts to subject-specific topics.
        """
    )
    
    parser.add_argument(
        "markdown_file",
        help="Path to the Markdown file to publish"
    )
    parser.add_argument(
        "--date", "-d",
        help="Publication date (YYYY-MM-DD). Overrides front matter."
    )
    parser.add_argument(
        "--title", "-t",
        help="Post title. Overrides front matter."
    )
    parser.add_argument(
        "--slug", "-s",
        help="URL slug for the filename. Auto-generated if not provided."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing files"
    )
    parser.add_argument(
        "--no-toc",
        action="store_true",
        help="Don't update a/toc/chrono-data.json (timeline navigation)"
    )
    parser.add_argument(
        "--no-stats",
        action="store_true",
        help="Don't update homepage stats"
    )
    
    args = parser.parse_args()
    
    success = publish_post(
        args.markdown_file,
        date=args.date,
        title=args.title,
        slug=args.slug,
        dry_run=args.dry_run,
        update_toc_flag=not args.no_toc,
        update_stats=not args.no_stats
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
