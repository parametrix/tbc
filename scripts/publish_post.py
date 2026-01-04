#!/usr/bin/env python3
"""
publish_post.py - Publish a new blog post from Markdown to HTML

This script converts a Markdown file to HTML with the proper template,
updates the index page, TOC sidebar, and homepage stats.

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
INDEX_FILE = POSTS_DIR / "index.html"
TOC_FILE = POSTS_DIR / "toc" / "toc-data.json"
CHRONO_FILE = POSTS_DIR / "toc" / "chrono-data.json"
ROOT_INDEX = REPO_ROOT / "index.html"

# Recent Posts topic ID (will be first in sidebar)
RECENT_POSTS_ID = "0.1"
RECENT_POSTS_TITLE = "Recent Posts"
MAX_RECENT_POSTS = 20  # Keep only the most recent N posts in this section

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


def update_index(post_number, date, title, filename, categories, dry_run=False):
    """Add a new entry to the index.html file."""
    if not INDEX_FILE.exists():
        print(f"Warning: Index file not found: {INDEX_FILE}")
        return False
    
    content = INDEX_FILE.read_text(encoding='utf-8')
    
    # Format the new table row
    date_str = date.strftime("%Y-%m-%d")
    categories_str = ", ".join(categories) if categories else ""
    
    new_row = (
        f'<tr><td align="right">{post_number}</td>'
        f'<td>{date_str}</td>'
        f'<td><a href="{filename}">{title}</a>'
        f'&nbsp;&nbsp;&nbsp;<a href="{filename}">web</a>'
        f'&nbsp;&nbsp;&nbsp;&nbsp;</td>'
        f'<td>{categories_str}</td></tr>\n'
    )
    
    # Find the last table row and insert after it
    # Look for the pattern of the last post entry
    last_row_pattern = r'(<tr><td align="right">\d+</td><td>\d{4}-\d{2}-\d{2}</td>.*?</tr>)\s*</table>'
    match = re.search(last_row_pattern, content, re.DOTALL)
    
    if match:
        # Insert the new row after the last existing row
        insert_pos = match.end(1)
        new_content = content[:insert_pos] + '\n' + new_row + content[insert_pos:]
        
        if dry_run:
            print(f"[DRY RUN] Would add to index: {new_row.strip()}")
        else:
            INDEX_FILE.write_text(new_content, encoding='utf-8')
            print(f"Updated index.html with post #{post_number}")
        return True
    else:
        print("Warning: Could not find insertion point in index.html")
        print("You may need to manually add the post to the index.")
        return False


def read_post(md_file):
    """Read and parse a Markdown file with front matter."""
    content = Path(md_file).read_text(encoding='utf-8')
    post = frontmatter.loads(content)
    return post


def update_toc(title, filename, post_number, post_date, dry_run=False):
    """Add the new post to 'Recent Posts' in toc-data.json (left sidebar)."""
    if not TOC_FILE.exists():
        print(f"Warning: TOC file not found: {TOC_FILE}")
        return False
    
    try:
        toc_data = json.loads(TOC_FILE.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e:
        print(f"Warning: Could not parse TOC file: {e}")
        return False
    
    # Find or create the "Recent Posts" topic
    recent_topic = None
    recent_index = -1
    
    for i, topic in enumerate(toc_data.get('topics', [])):
        if topic.get('id') == RECENT_POSTS_ID:
            recent_topic = topic
            recent_index = i
            break
    
    if recent_topic is None:
        # Create new "Recent Posts" topic at the beginning
        recent_topic = {
            "id": RECENT_POSTS_ID,
            "title": RECENT_POSTS_TITLE,
            "posts": []
        }
        toc_data['topics'].insert(0, recent_topic)
        recent_index = 0
    
    # Create new post entry for Recent Posts
    new_post = {
        "title": title,
        "file": filename
    }
    
    # Add to the beginning of Recent Posts (most recent first)
    recent_topic['posts'].insert(0, new_post)
    
    # Limit the number of posts in Recent Posts section
    if len(recent_topic['posts']) > MAX_RECENT_POSTS:
        recent_topic['posts'] = recent_topic['posts'][:MAX_RECENT_POSTS]
    
    # Update the topic in the list
    toc_data['topics'][recent_index] = recent_topic
    
    # Update metadata
    toc_data['lastUpdated'] = datetime.now().strftime("%Y-%m-%d")
    toc_data['totalPostLinks'] = sum(len(t.get('posts', [])) for t in toc_data['topics'])
    
    if dry_run:
        print(f"[DRY RUN] Would add to TOC 'Recent Posts': {title}")
        print(f"[DRY RUN] TOC would have {toc_data['totalPostLinks']} topic post links")
    else:
        # Write with proper formatting
        TOC_FILE.write_text(
            json.dumps(toc_data, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
        print(f"Updated toc-data.json:")
        print(f"  - Added to 'Recent Posts': {title}")
    
    return True


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
                 dry_run=False, update_idx=True, update_toc_flag=True, 
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
    
    # Update index.html
    if update_idx:
        update_index(post_number, post_date, post_title, filename, categories, dry_run)
    
    # Update TOC sidebar (left sidebar - topic-based)
    if update_toc_flag:
        update_toc(post_title, filename, post_number, post_date, dry_run)
    
    # Update chrono-data.json (right column - timeline navigation)
    if update_toc_flag:
        update_chrono_data(post_title, filename, post_number, post_date, dry_run)
    
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
  - Adds entry to a/index.html post table (chronological TOC)
  - Adds to "Recent Posts" in a/toc/toc-data.json (left sidebar topics)
  - Adds to a/toc/chrono-data.json (right column timeline navigation)
  - Updates post count on homepage (index.html)
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
        "--no-index",
        action="store_true",
        help="Don't update a/index.html"
    )
    parser.add_argument(
        "--no-toc",
        action="store_true",
        help="Don't update a/toc/ files (toc-data.json and chrono-data.json)"
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
        update_idx=not args.no_index,
        update_toc_flag=not args.no_toc,
        update_stats=not args.no_stats
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
