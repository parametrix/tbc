#!/usr/bin/env python3
"""
extract_topic_toc.py - Extract topic-based TOC from a/index.html to JSON

This script parses the homepage and extracts all 58 topic groups (55 main + 3 subtopics)
from section #5, creating a structured JSON file for the sidebar navigation.

Note: There are 61 anchors in index.html, but:
- 2 are sub-section markers (5.9b, 5.28b) embedded within topic lists
- 1 is a redirect (5.12 -> 5.9) with no content

Author: parametrix
Date: January 2, 2026
"""

import re
import json
from pathlib import Path
from datetime import datetime
from html.parser import HTMLParser
from typing import List, Dict, Optional, Any

class TopicTOCExtractor(HTMLParser):
    """Parse a/index.html and extract topic-based TOC structure."""
    
    def __init__(self):
        super().__init__()
        self.topics: List[Dict[str, Any]] = []
        self.current_topic: Optional[Dict[str, Any]] = None
        self.current_subtopic: Optional[Dict[str, Any]] = None
        self.in_topic_section = False
        self.in_h4 = False
        self.in_ul = False
        self.in_li = False
        self.in_a = False
        self.current_href = ""
        self.current_text = ""
        self.ul_depth = 0
        self.capture_text = False
        
    def handle_starttag(self, tag: str, attrs: List[tuple]):
        attrs_dict = dict(attrs)
        
        # Detect topic anchor: <a name="5.X">
        if tag == "a" and "name" in attrs_dict:
            name = attrs_dict["name"]
            if re.match(r'^5\.\d+', name):
                self.in_topic_section = True
                # Save previous topic if exists
                if self.current_topic:
                    if self.current_subtopic:
                        self.current_topic.setdefault("subTopics", []).append(self.current_subtopic)
                        self.current_subtopic = None
                    self.topics.append(self.current_topic)
                
                # Check if this is a subtopic (e.g., 5.25.1)
                if re.match(r'^5\.\d+\.\d+', name):
                    self.current_subtopic = {
                        "id": name,
                        "title": "",
                        "posts": []
                    }
                else:
                    self.current_topic = {
                        "id": name,
                        "title": "",
                        "posts": []
                    }
                    self.current_subtopic = None
        
        # Capture topic title from h4
        if tag == "h4" and self.in_topic_section:
            self.in_h4 = True
            self.current_text = ""
            self.capture_text = True
        
        # Track ul nesting
        if tag == "ul" and self.in_topic_section:
            self.ul_depth += 1
            self.in_ul = True
        
        # Track list items
        if tag == "li" and self.in_ul:
            self.in_li = True
            self.current_text = ""
        
        # Capture post links
        if tag == "a" and self.in_li and "href" in attrs_dict:
            self.in_a = True
            self.current_href = attrs_dict["href"]
            self.current_text = ""
            self.capture_text = True
    
    def handle_endtag(self, tag: str):
        if tag == "h4" and self.in_h4:
            self.in_h4 = False
            self.capture_text = False
            title = self.clean_title(self.current_text)
            if self.current_subtopic:
                self.current_subtopic["title"] = title
            elif self.current_topic:
                self.current_topic["title"] = title
        
        if tag == "ul" and self.in_ul:
            self.ul_depth -= 1
            if self.ul_depth == 0:
                self.in_ul = False
        
        if tag == "li" and self.in_li:
            self.in_li = False
        
        if tag == "a" and self.in_a:
            self.in_a = False
            self.capture_text = False
            # Only save if we have a valid href and text
            if self.current_href and self.current_text.strip():
                post = {
                    "title": self.current_text.strip(),
                    "file": self.current_href
                }
                if self.current_subtopic:
                    self.current_subtopic["posts"].append(post)
                elif self.current_topic:
                    self.current_topic["posts"].append(post)
            self.current_href = ""
            self.current_text = ""
    
    def handle_data(self, data: str):
        if self.capture_text:
            self.current_text += data
    
    def clean_title(self, title: str) -> str:
        """Clean up topic title."""
        # Remove leading number (5.1., 5.25.1, etc.)
        title = re.sub(r'^5\.\d+\.?\d*\.?\s*', '', title)
        # Clean whitespace
        title = ' '.join(title.split())
        # Convert HTML entities
        title = title.replace('&ndash;', '–').replace('&mdash;', '—')
        return title.strip()
    
    def finalize(self):
        """Finalize parsing - save last topic."""
        if self.current_topic:
            if self.current_subtopic:
                self.current_topic.setdefault("subTopics", []).append(self.current_subtopic)
            self.topics.append(self.current_topic)


def find_all_post_links(content: str) -> List[Dict[str, str]]:
    """
    Find all post links (href to .htm/.html files) in the content.
    Handles various HTML structures including nested lists.
    """
    # Pattern to find links to post files - allows <code> tags in title
    link_pattern = re.compile(
        r'<a\s+href="([^"]+\.htm[l]?(?:#[^"]*)?)"[^>]*>(.*?)</a>',
        re.IGNORECASE | re.DOTALL
    )
    
    posts = []
    for match in link_pattern.finditer(content):
        href = match.group(1)
        title = match.group(2).strip()
        
        # Skip external links and non-post files
        if href.startswith('http://') or href.startswith('https://'):
            continue
        if not re.match(r'\d{4}_', href):
            continue
        
        # Remove <code> tags from title
        title = re.sub(r'</?code>', '', title)
            
        # Convert HTML entities
        title = title.replace('&ndash;', '–').replace('&mdash;', '—')
        title = title.replace('&amp;', '&').replace('&gt;', '>').replace('&lt;', '<')
        
        # Normalize whitespace
        title = ' '.join(title.split())
        
        posts.append({
            "title": title,
            "file": href
        })
    
    return posts


def find_matching_ul(content: str, start_pos: int) -> Optional[str]:
    """
    Find a complete <ul>...</ul> block starting from start_pos,
    properly handling nested <ul> tags.
    """
    ul_start = content.find('<ul>', start_pos)
    if ul_start == -1:
        ul_start = content.find('<ul ', start_pos)  # ul with attributes
    if ul_start == -1:
        return None
    
    # Find the matching </ul> by counting nesting
    depth = 0
    pos = ul_start
    while pos < len(content):
        next_open = content.find('<ul', pos + 1)
        next_close = content.find('</ul>', pos + 1)
        
        if next_close == -1:
            return None  # No closing tag found
        
        if next_open != -1 and next_open < next_close:
            # Found nested <ul> before </ul>
            depth += 1
            pos = next_open
        else:
            # Found </ul>
            if depth == 0:
                # This is our matching </ul>
                ul_end = next_close + len('</ul>')
                return content[ul_start:ul_end]
            else:
                depth -= 1
                pos = next_close
    
    return None


def extract_topics_with_regex(html_content: str) -> List[Dict[str, Any]]:
    """
    Extract topics using regex.
    Uses <h4> headers as the primary topic delimiter since some anchors may be missing.
    """
    topics = []
    
    # Find all <h4>5.X... headers to define topic boundaries
    # This is more reliable than anchors since some anchors are missing
    h4_pattern = re.compile(
        r'<h4>\s*(5\.(\d+)(?:\.(\d+))?\.?\s*)(.*?)</h4>',
        re.IGNORECASE | re.DOTALL
    )
    
    h4_matches = list(h4_pattern.finditer(html_content))
    
    for i, match in enumerate(h4_matches):
        full_num = match.group(1).strip().rstrip('.')  # e.g. "5.32"
        major = match.group(2)  # e.g. "32"
        minor = match.group(3)  # e.g. "1" for subtopics, None for main
        title_raw = match.group(4)
        
        # Build topic ID
        if minor:
            topic_id = f"5.{major}.{minor}"
        else:
            topic_id = f"5.{major}"
        
        # Determine section boundaries (from this h4 to next h4)
        section_start = match.end()
        if i + 1 < len(h4_matches):
            section_end = h4_matches[i + 1].start()
        else:
            # Find end of section 5 (look for section 6)
            s6_match = re.search(r'<a\s+name="6"', html_content[section_start:])
            if s6_match:
                section_end = section_start + s6_match.start()
            else:
                section_end = len(html_content)
        
        section_content = html_content[section_start:section_end]
        
        # Clean title
        title = title_raw.strip()
        title = title.replace('&ndash;', '–').replace('&mdash;', '—')
        title = title.replace('<code>', '').replace('</code>', '')
        title = ' '.join(title.split())  # Normalize whitespace
        
        # Extract all post links from this section
        posts = find_all_post_links(section_content)
        
        if not posts:
            continue  # Skip topics with no posts
        
        # Determine if this is a subtopic
        is_subtopic = minor is not None
        
        if is_subtopic:
            # Add as subtopic to parent main topic
            parent_id = f"5.{major}"
            parent_found = False
            for t in reversed(topics):
                if t["id"] == parent_id:
                    t.setdefault("subTopics", []).append({
                        "id": topic_id,
                        "title": title,
                        "posts": posts
                    })
                    parent_found = True
                    break
            
            # If parent wasn't found, create it
            if not parent_found:
                topics.append({
                    "id": parent_id,
                    "title": f"Topic {parent_id}",
                    "posts": [],
                    "subTopics": [{
                        "id": topic_id,
                        "title": title,
                        "posts": posts
                    }]
                })
        else:
            topics.append({
                "id": topic_id,
                "title": title,
                "posts": posts
            })
    
    return topics


def extract_navigation_links(html_content: str) -> List[Dict[str, str]]:
    """Extract the main navigation links (sections 0-4)."""
    nav_links = []
    
    # These are the standard sections before the topics
    sections = [
        ("0", "About Jeremy Tammik"),
        ("1", "Contact and Support"),
        ("2", "Getting Started"),
        ("3", "License"),
        ("4", "Disclaimer"),
    ]
    
    for anchor, label in sections:
        nav_links.append({
            "label": label,
            "href": f"index.html#{anchor}"
        })
    
    return nav_links


def main():
    """Main function to extract TOC and create JSON."""
    import os
    
    # Paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    index_path = repo_root / "a" / "index.html"
    a_dir = repo_root / "a"
    output_dir = repo_root / "a" / "toc"
    output_path = output_dir / "toc-data.json"
    
    print(f"Reading {index_path}...")
    
    if not index_path.exists():
        print(f"ERROR: {index_path} not found!")
        return 1
    
    # Get list of existing files (both .htm and .html)
    existing_files = set(f for f in os.listdir(a_dir) if f.endswith('.htm') or f.endswith('.html'))
    print(f"Found {len(existing_files)} existing post files")
    
    # Read HTML content
    html_content = index_path.read_text(encoding="utf-8", errors="replace")
    
    print("Extracting topics...")
    
    # Use regex-based extraction (more reliable for this HTML structure)
    topics = extract_topics_with_regex(html_content)
    
    # Filter out posts for non-existent files
    removed_count = 0
    for topic in topics:
        orig_count = len(topic.get("posts", []))
        topic["posts"] = [
            p for p in topic.get("posts", [])
            if p["file"].split("#")[0] in existing_files
        ]
        removed_count += orig_count - len(topic["posts"])
        
        for subtopic in topic.get("subTopics", []):
            orig_count = len(subtopic.get("posts", []))
            subtopic["posts"] = [
                p for p in subtopic.get("posts", [])
                if p["file"].split("#")[0] in existing_files
            ]
            removed_count += orig_count - len(subtopic["posts"])
    
    if removed_count > 0:
        print(f"Filtered out {removed_count} entries for non-existent files")
    
    # Get navigation links
    nav_links = extract_navigation_links(html_content)
    
    # Count total posts
    total_posts = 0
    for topic in topics:
        total_posts += len(topic.get("posts", []))
        for subtopic in topic.get("subTopics", []):
            total_posts += len(subtopic.get("posts", []))
    
    # Build final JSON structure
    toc_data = {
        "version": "1.0",
        "lastUpdated": datetime.now().strftime("%Y-%m-%d"),
        "totalTopics": len(topics),
        "totalPostLinks": total_posts,
        "navigation": nav_links,
        "topics": topics
    }
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Write JSON
    print(f"Writing {output_path}...")
    output_path.write_text(
        json.dumps(toc_data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    
    # Print summary
    print(f"\n✅ Extraction complete!")
    print(f"   Topics: {len(topics)}")
    print(f"   Post links: {total_posts}")
    print(f"   Output: {output_path}")
    print(f"   File size: {output_path.stat().st_size:,} bytes")
    
    # Print first few topics as sample
    print(f"\n📋 Sample topics:")
    for topic in topics[:5]:
        post_count = len(topic.get("posts", []))
        subtopic_count = len(topic.get("subTopics", []))
        print(f"   {topic['id']}: {topic['title']} ({post_count} posts" + 
              (f", {subtopic_count} subtopics)" if subtopic_count else ")"))
    
    if len(topics) > 5:
        print(f"   ... and {len(topics) - 5} more topics")
    
    return 0


if __name__ == "__main__":
    exit(main())
