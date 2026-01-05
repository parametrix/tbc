#!/usr/bin/env python3
"""
manage_topics.py - Manage topics in the sidebar TOC

This script provides tools to:
- Add a post to an existing topic
- Create a new topic
- List all topics
- Move a post between topics

Usage:
    python manage_topics.py list                             # List all topics
    python manage_topics.py add-post <topic_id> <file> <title>  # Add post to topic
    python manage_topics.py new-topic <id> <title>           # Create new topic
    python manage_topics.py --help                           # Show help

Author: GitHub Copilot
Date: January 4, 2026
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

# Configuration
REPO_ROOT = Path(__file__).parent.parent
TOC_FILE = REPO_ROOT / "a" / "toc" / "toc-data.json"


def load_toc():
    """Load the TOC data file."""
    if not TOC_FILE.exists():
        print(f"Error: TOC file not found: {TOC_FILE}")
        sys.exit(1)
    
    try:
        return json.loads(TOC_FILE.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e:
        print(f"Error: Could not parse TOC file: {e}")
        sys.exit(1)


def save_toc(toc_data):
    """Save the TOC data file."""
    toc_data['lastUpdated'] = datetime.now().strftime("%Y-%m-%d")
    TOC_FILE.write_text(
        json.dumps(toc_data, indent=2, ensure_ascii=False),
        encoding='utf-8'
    )


def list_topics(args):
    """List all topics with post counts."""
    toc_data = load_toc()
    topics = toc_data.get('topics', [])
    
    print(f"\n{'='*60}")
    print(f"TOC Topics ({len(topics)} total)")
    print(f"{'='*60}\n")
    
    for topic in topics:
        topic_id = topic.get('id', '?')
        title = topic.get('title', 'Untitled')
        posts = topic.get('posts', [])
        post_count = len(posts)
        
        # Check for subtopics
        subtopics = topic.get('subTopics', [])
        subtopic_info = f" (+{len(subtopics)} subtopics)" if subtopics else ""
        
        print(f"  {topic_id:<8} {title:<45} ({post_count} posts){subtopic_info}")
    
    print(f"\n{'='*60}")
    print(f"Total topics: {len(topics)}")
    print(f"Total post links: {toc_data.get('totalPostLinks', 0)}")
    print(f"{'='*60}\n")


def show_topic(args):
    """Show details of a specific topic."""
    toc_data = load_toc()
    topics = toc_data.get('topics', [])
    
    topic_id = args.topic_id
    
    # Find the topic
    topic = None
    for t in topics:
        if t.get('id') == topic_id:
            topic = t
            break
    
    if topic is None:
        print(f"Error: Topic '{topic_id}' not found.")
        print("Use 'python manage_topics.py list' to see all topics.")
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print(f"Topic: {topic.get('id')} - {topic.get('title')}")
    print(f"{'='*60}\n")
    
    posts = topic.get('posts', [])
    print(f"Posts ({len(posts)}):\n")
    
    for i, post in enumerate(posts, 1):
        title = post.get('title', 'Untitled')
        file = post.get('file', '?')
        print(f"  {i:3}. {title}")
        print(f"       File: {file}\n")
    
    # Show subtopics
    subtopics = topic.get('subTopics', [])
    if subtopics:
        print(f"\nSubtopics ({len(subtopics)}):\n")
        for st in subtopics:
            st_id = st.get('id', '?')
            st_title = st.get('title', 'Untitled')
            st_posts = st.get('posts', [])
            print(f"  {st_id} - {st_title} ({len(st_posts)} posts)")


def add_post(args):
    """Add a post to an existing topic."""
    toc_data = load_toc()
    topics = toc_data.get('topics', [])
    
    topic_id = args.topic_id
    post_file = args.file
    post_title = args.title
    
    # Validate file exists
    post_path = REPO_ROOT / "a" / post_file
    if not post_path.exists():
        print(f"Warning: Post file not found: {post_path}")
        if not args.force:
            print("Use --force to add anyway.")
            sys.exit(1)
    
    # Find the topic
    topic = None
    topic_index = -1
    for i, t in enumerate(topics):
        if t.get('id') == topic_id:
            topic = t
            topic_index = i
            break
    
    if topic is None:
        print(f"Error: Topic '{topic_id}' not found.")
        print("Use 'python manage_topics.py list' to see all topics.")
        print("Use 'python manage_topics.py new-topic' to create a new topic.")
        sys.exit(1)
    
    # Check if post already exists in topic
    existing_files = [p.get('file') for p in topic.get('posts', [])]
    if post_file in existing_files:
        print(f"Post '{post_file}' already exists in topic '{topic_id}'.")
        sys.exit(0)
    
    # Add the post
    new_post = {
        "title": post_title,
        "file": post_file
    }
    
    if 'posts' not in topic:
        topic['posts'] = []
    
    topic['posts'].append(new_post)
    topics[topic_index] = topic
    
    # Update metadata
    toc_data['topics'] = topics
    toc_data['totalPostLinks'] = sum(len(t.get('posts', [])) for t in topics)
    
    if args.dry_run:
        print(f"[DRY RUN] Would add post to topic '{topic_id}':")
        print(f"  Title: {post_title}")
        print(f"  File: {post_file}")
    else:
        save_toc(toc_data)
        print(f"Added post to topic '{topic_id}':")
        print(f"  Title: {post_title}")
        print(f"  File: {post_file}")
        print(f"\nTopic '{topic.get('title')}' now has {len(topic['posts'])} posts.")


def new_topic(args):
    """Create a new topic."""
    toc_data = load_toc()
    topics = toc_data.get('topics', [])
    
    topic_id = args.topic_id
    topic_title = args.title
    
    # Check if topic ID already exists
    existing_ids = [t.get('id') for t in topics]
    if topic_id in existing_ids:
        print(f"Error: Topic ID '{topic_id}' already exists.")
        sys.exit(1)
    
    # Create new topic
    new_topic = {
        "id": topic_id,
        "title": topic_title,
        "posts": []
    }
    
    # Determine insertion position
    # Topics are typically numbered 5.1, 5.2, ... so insert in order
    insert_index = len(topics)  # Default: end
    
    # Try to find the right position based on ID
    if args.after:
        for i, t in enumerate(topics):
            if t.get('id') == args.after:
                insert_index = i + 1
                break
    elif args.before:
        for i, t in enumerate(topics):
            if t.get('id') == args.before:
                insert_index = i
                break
    else:
        # Insert in numeric order if ID starts with a number
        try:
            new_num = float(topic_id.replace('-', '.'))
            for i, t in enumerate(topics):
                try:
                    existing_num = float(t.get('id', '999').replace('-', '.'))
                    if new_num < existing_num:
                        insert_index = i
                        break
                except ValueError:
                    continue
        except ValueError:
            pass  # Keep at end
    
    topics.insert(insert_index, new_topic)
    
    # Update metadata
    toc_data['topics'] = topics
    toc_data['totalTopics'] = len(topics)
    
    if args.dry_run:
        print(f"[DRY RUN] Would create new topic:")
        print(f"  ID: {topic_id}")
        print(f"  Title: {topic_title}")
        print(f"  Position: {insert_index + 1} of {len(topics)}")
    else:
        save_toc(toc_data)
        print(f"Created new topic:")
        print(f"  ID: {topic_id}")
        print(f"  Title: {topic_title}")
        print(f"  Position: {insert_index + 1} of {len(topics)}")
        print(f"\nNext steps:")
        print(f"  python manage_topics.py add-post {topic_id} <file.html> \"Post Title\"")


def remove_post(args):
    """Remove a post from a topic."""
    toc_data = load_toc()
    topics = toc_data.get('topics', [])
    
    topic_id = args.topic_id
    post_file = args.file
    
    # Find the topic
    topic = None
    topic_index = -1
    for i, t in enumerate(topics):
        if t.get('id') == topic_id:
            topic = t
            topic_index = i
            break
    
    if topic is None:
        print(f"Error: Topic '{topic_id}' not found.")
        sys.exit(1)
    
    # Find and remove the post
    posts = topic.get('posts', [])
    original_count = len(posts)
    topic['posts'] = [p for p in posts if p.get('file') != post_file]
    
    if len(topic['posts']) == original_count:
        print(f"Post '{post_file}' not found in topic '{topic_id}'.")
        sys.exit(0)
    
    topics[topic_index] = topic
    
    # Update metadata
    toc_data['topics'] = topics
    toc_data['totalPostLinks'] = sum(len(t.get('posts', [])) for t in topics)
    
    if args.dry_run:
        print(f"[DRY RUN] Would remove post '{post_file}' from topic '{topic_id}'")
    else:
        save_toc(toc_data)
        print(f"Removed post '{post_file}' from topic '{topic_id}'")
        print(f"Topic now has {len(topic['posts'])} posts.")


def main():
    parser = argparse.ArgumentParser(
        description="Manage topics in the sidebar TOC",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python manage_topics.py list                          # List all topics
  python manage_topics.py show 5.1                      # Show topic 5.1 details
  python manage_topics.py add-post 5.1 0123_my_post.html "My Post Title"
  python manage_topics.py new-topic 5.62 "My New Topic"
  python manage_topics.py new-topic 5.62 "My Topic" --after 5.61
  python manage_topics.py remove-post 5.1 0123_my_post.html

Topic IDs:
  - Subject topics: 5.1, 5.2, ..., 5.56 (see 'list' command)
  - Uncategorized: 5.99 (new posts land here)
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # list command
    list_parser = subparsers.add_parser('list', help='List all topics')
    list_parser.set_defaults(func=list_topics)
    
    # show command
    show_parser = subparsers.add_parser('show', help='Show topic details')
    show_parser.add_argument('topic_id', help='Topic ID (e.g., 5.1)')
    show_parser.set_defaults(func=show_topic)
    
    # add-post command
    add_parser = subparsers.add_parser('add-post', help='Add a post to a topic')
    add_parser.add_argument('topic_id', help='Topic ID (e.g., 5.1)')
    add_parser.add_argument('file', help='Post filename (e.g., 0123_my_post.html)')
    add_parser.add_argument('title', help='Post title')
    add_parser.add_argument('--dry-run', action='store_true', help='Preview without saving')
    add_parser.add_argument('--force', '-f', action='store_true', help='Add even if file not found')
    add_parser.set_defaults(func=add_post)
    
    # new-topic command
    new_parser = subparsers.add_parser('new-topic', help='Create a new topic')
    new_parser.add_argument('topic_id', help='New topic ID (e.g., 5.62)')
    new_parser.add_argument('title', help='Topic title')
    new_parser.add_argument('--after', help='Insert after this topic ID')
    new_parser.add_argument('--before', help='Insert before this topic ID')
    new_parser.add_argument('--dry-run', action='store_true', help='Preview without saving')
    new_parser.set_defaults(func=new_topic)
    
    # remove-post command
    remove_parser = subparsers.add_parser('remove-post', help='Remove a post from a topic')
    remove_parser.add_argument('topic_id', help='Topic ID (e.g., 5.1)')
    remove_parser.add_argument('file', help='Post filename to remove')
    remove_parser.add_argument('--dry-run', action='store_true', help='Preview without saving')
    remove_parser.set_defaults(func=remove_post)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(0)
    
    args.func(args)


if __name__ == "__main__":
    main()
