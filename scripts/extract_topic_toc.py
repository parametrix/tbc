#!/usr/bin/env python3
"""
extract_topic_toc.py - Extract topic-based TOC from a/index.html to JSON

This script parses the homepage and extracts all 61+ topic groups from section #5,
creating a structured JSON file for the sidebar navigation.

Author: GitHub Copilot
Date: January 2, 2026
"""

import re
import json
from pathlib import Path
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


def extract_topics_with_regex(html_content: str) -> List[Dict[str, Any]]:
    """
    Extract topics using regex as a more robust fallback.
    This handles the actual structure better than the HTML parser.
    """
    topics = []
    
    # Pattern to find topic anchors and their content
    # <a name="5.X"></a>\n\n<h4>5.X. Title</h4>\n\n<ul>...</ul>
    topic_pattern = re.compile(
        r'<a\s+name="(5\.\d+(?:\.\d+)?)">\s*</a>\s*'
        r'<h4>([^<]+)</h4>\s*'
        r'(?:<[^>]+>\s*)*'  # Skip any intermediate tags/comments
        r'<ul>(.*?)</ul>',
        re.DOTALL | re.IGNORECASE
    )
    
    # Pattern to extract links from ul content
    link_pattern = re.compile(
        r'<li>\s*<a\s+href="([^"]+)"[^>]*>([^<]+)</a>',
        re.IGNORECASE
    )
    
    for match in topic_pattern.finditer(html_content):
        topic_id = match.group(1)
        title_raw = match.group(2)
        ul_content = match.group(3)
        
        # Clean title - remove leading number
        title = re.sub(r'^5\.\d+\.?\d*\.?\s*', '', title_raw).strip()
        # Convert HTML entities
        title = title.replace('&ndash;', '–').replace('&mdash;', '—')
        title = title.replace('<code>', '').replace('</code>', '')
        
        # Extract posts
        posts = []
        for link_match in link_pattern.finditer(ul_content):
            href = link_match.group(1)
            link_text = link_match.group(2).strip()
            # Convert HTML entities in link text
            link_text = link_text.replace('&ndash;', '–').replace('&mdash;', '—')
            posts.append({
                "title": link_text,
                "file": href
            })
        
        # Determine if this is a subtopic
        is_subtopic = bool(re.match(r'^5\.\d+\.\d+$', topic_id))
        
        if is_subtopic and topics:
            # Add as subtopic to previous main topic
            parent_id = '.'.join(topic_id.split('.')[:2])
            for t in reversed(topics):
                if t["id"] == parent_id:
                    t.setdefault("subTopics", []).append({
                        "id": topic_id,
                        "title": title,
                        "posts": posts
                    })
                    break
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
    # Paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    index_path = repo_root / "a" / "index.html"
    output_dir = repo_root / "a" / "toc"
    output_path = output_dir / "toc-data.json"
    
    print(f"Reading {index_path}...")
    
    if not index_path.exists():
        print(f"ERROR: {index_path} not found!")
        return 1
    
    # Read HTML content
    html_content = index_path.read_text(encoding="utf-8", errors="replace")
    
    print("Extracting topics...")
    
    # Use regex-based extraction (more reliable for this HTML structure)
    topics = extract_topics_with_regex(html_content)
    
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
        "lastUpdated": "2026-01-02",
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
