#!/usr/bin/env python3
"""
audit_posts.py - Audit all blog posts against TOC files

Checks that every .htm file in a/ is accounted for in both:
1. toc-data.json (topic-based navigation)
2. chrono-data.json (chronological navigation)
"""

import os
import re
import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
A_DIR = REPO_ROOT / 'a'
TOC_DIR = A_DIR / 'toc'

def get_htm_files():
    """Get all .htm files in a/ directory."""
    files = set()
    for f in os.listdir(A_DIR):
        if f.endswith('.htm') and f != 'index.html':
            files.add(f)
    return files

def get_toc_posts():
    """Get all posts from toc-data.json topics."""
    with open(TOC_DIR / 'toc-data.json', 'r', encoding='utf-8') as f:
        toc = json.load(f)
    
    posts = set()
    for topic in toc.get('topics', []):
        for post in topic.get('posts', []):
            # Remove anchor if present
            base = post['file'].split('#')[0]
            posts.add(base)
        for sub in topic.get('subTopics', []):
            for post in sub.get('posts', []):
                base = post['file'].split('#')[0]
                posts.add(base)
    
    # Also check recentPosts
    for post in toc.get('recentPosts', []):
        base = post['file'].split('#')[0]
        posts.add(base)
    
    return posts

def get_chrono_posts():
    """Get all posts from chrono-data.json."""
    with open(TOC_DIR / 'chrono-data.json', 'r', encoding='utf-8') as f:
        chrono = json.load(f)
    
    posts = set()
    for post in chrono.get('posts', []):
        posts.add(post['file'])
    
    return posts

def analyze_index_html():
    """Analyze index.html to understand post references by section."""
    content = (A_DIR / 'index.html').read_text(encoding='utf-8')
    
    # Find all numbered section anchors
    section_pattern = re.compile(r'<a\s+name="(\d+)"', re.IGNORECASE)
    sections = [(m.group(1), m.start()) for m in section_pattern.finditer(content)]
    sections.append(('END', len(content)))
    
    print(f"\n=== INDEX.HTML SECTIONS ===")
    for i, (num, pos) in enumerate(sections[:-1]):
        next_pos = sections[i+1][1]
        section_content = content[pos:next_pos]
        # Count .htm references in this section
        hrefs = re.findall(r'href="(\d+[^"]+\.htm)', section_content)
        unique_files = set(h.split('#')[0] for h in hrefs)
        print(f"Section {num}: {len(unique_files)} unique posts referenced")
    
    # Analyze Section 5 (topics) vs Section 6 (chronological)
    s5_idx = next((i for i, (n, _) in enumerate(sections) if n == '5'), None)
    s6_idx = next((i for i, (n, _) in enumerate(sections) if n == '6'), None)
    
    if s5_idx is not None and s6_idx is not None:
        s5_content = content[sections[s5_idx][1]:sections[s6_idx][1]]
        s5_hrefs = re.findall(r'href="(\d+[^"]+\.htm)', s5_content)
        s5_files = set(h.split('#')[0] for h in s5_hrefs)
        
        s6_content = content[sections[s6_idx][1]:sections[s6_idx+1][1] if s6_idx+1 < len(sections) else len(content)]
        s6_hrefs = re.findall(r'href="(\d+[^"]+\.htm)', s6_content)
        s6_files = set(h.split('#')[0] for h in s6_hrefs)
        
        print(f"\nSection 5 (Topics): {len(s5_files)} unique posts")
        print(f"Section 6 (Chronological): {len(s6_files)} unique posts")
        
        return s5_files, s6_files
    
    return set(), set()

def main():
    print("=" * 60)
    print("BLOG POST AUDIT REPORT")
    print("=" * 60)
    
    # Get all data
    htm_files = get_htm_files()
    toc_posts = get_toc_posts()
    chrono_posts = get_chrono_posts()
    
    print(f"\n=== FILE COUNTS ===")
    print(f"Total .htm files in a/: {len(htm_files)}")
    print(f"Posts in toc-data.json (topics): {len(toc_posts)}")
    print(f"Posts in chrono-data.json: {len(chrono_posts)}")
    
    # Analyze index.html
    s5_files, s6_files = analyze_index_html()
    
    # Check chrono-data.json accuracy
    print(f"\n=== CHRONO-DATA.JSON ANALYSIS ===")
    in_chrono_not_files = chrono_posts - htm_files
    in_files_not_chrono = htm_files - chrono_posts
    print(f"Entries for non-existent files: {len(in_chrono_not_files)}")
    print(f"Files missing from chrono-data: {len(in_files_not_chrono)}")
    
    if in_chrono_not_files:
        print(f"\nNon-existent files in chrono-data (sample):")
        for f in sorted(in_chrono_not_files)[:5]:
            print(f"  - {f}")
    
    if in_files_not_chrono:
        print(f"\nFiles missing from chrono-data (sample):")
        for f in sorted(in_files_not_chrono)[:5]:
            print(f"  - {f}")
    
    # Check toc-data.json accuracy
    print(f"\n=== TOC-DATA.JSON ANALYSIS ===")
    in_topics_not_files = toc_posts - htm_files
    in_files_not_topics = htm_files - toc_posts
    print(f"Topic entries for non-existent files: {len(in_topics_not_files)}")
    print(f"Files not in any topic: {len(in_files_not_topics)}")
    
    if in_topics_not_files:
        print(f"\nNon-existent files in topics (these are likely anchor refs):")
        for f in sorted(in_topics_not_files)[:10]:
            print(f"  - {f}")
    
    # Compare with index.html Section 5
    print(f"\n=== COMPARISON WITH INDEX.HTML ===")
    if s5_files:
        # toc_posts should match s5_files
        missing_from_toc = s5_files - toc_posts
        extra_in_toc = toc_posts - s5_files
        print(f"Files in index.html Section 5 but NOT in toc-data topics: {len(missing_from_toc)}")
        print(f"Files in toc-data topics but NOT in index.html Section 5: {len(extra_in_toc)}")
        
        if missing_from_toc:
            print(f"\nMissing from toc-data (sample):")
            for f in sorted(missing_from_toc)[:10]:
                print(f"  - {f}")
    
    # Summary
    print(f"\n=== SUMMARY ===")
    print(f"✅ All {len(htm_files)} .htm files exist")
    
    if len(in_chrono_not_files) > 0:
        print(f"⚠️  chrono-data.json has {len(in_chrono_not_files)} entries for non-existent files")
        print(f"   (These appear to be future posts not yet in this archive)")
    
    if len(in_files_not_chrono) == 0:
        print(f"✅ All existing files are in chrono-data.json")
    else:
        print(f"❌ {len(in_files_not_chrono)} files missing from chrono-data.json")
    
    # Calculate topic coverage more accurately
    # Section 5 has some posts that don't exist (posts 1355+)
    if s5_files:
        s5_existing = s5_files & htm_files
        topic_coverage_of_s5 = len(toc_posts & s5_existing) / len(s5_existing) * 100 if s5_existing else 0
        print(f"\n📊 Topic TOC Analysis:")
        print(f"   Section 5 of index.html references {len(s5_files)} unique posts")
        print(f"   - {len(s5_existing)} exist in this archive")
        print(f"   - {len(s5_files - htm_files)} are posts 1355+ (not yet migrated)")
        print(f"   toc-data.json captures {len(toc_posts)} unique existing files ({topic_coverage_of_s5:.1f}% of existing Section 5 posts)")
    
    print(f"\n📋 Overall Coverage:")
    print(f"   chrono-data.json: {len(chrono_posts)}/{len(htm_files)} posts ({len(chrono_posts)/len(htm_files)*100:.1f}%)")
    print(f"   toc-data.json topics: {len(toc_posts)}/{len(htm_files)} posts ({len(toc_posts)/len(htm_files)*100:.1f}%)")
    print(f"   (Not all posts are categorized into topics - this is by design)")

if __name__ == '__main__':
    main()
