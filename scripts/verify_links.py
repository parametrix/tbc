"""
Verify all local links and images in HTML files.
"""
import os
import re
from pathlib import Path
from collections import defaultdict

# Directory containing blog posts
blog_dir = Path(__file__).parent / 'a'

# Patterns to find local hrefs and srcs
href_pattern = re.compile(r'href="([^"]+)"')
src_pattern = re.compile(r'src="([^"]+)"')

missing_files = defaultdict(list)
files_checked = 0
links_checked = 0
images_checked = 0

print("Verifying local links and images in HTML files...")

def is_external(url):
    """Check if URL is external"""
    return url.startswith(('http://', 'https://', 'mailto:', 'ftp://')) or url.startswith('#')

for file_path in sorted(blog_dir.glob('*.htm*')):
    if file_path.suffix in ['.htm', '.html']:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find all hrefs
            for match in href_pattern.finditer(content):
                url = match.group(1)
                if not is_external(url):
                    # Remove anchor
                    file_ref = url.split('#')[0]
                    if file_ref:  # Skip empty refs (just anchors)
                        links_checked += 1
                        target_path = blog_dir / file_ref
                        if not target_path.exists():
                            missing_files[file_ref].append(file_path.name)
            
            # Find all srcs
            for match in src_pattern.finditer(content):
                url = match.group(1)
                if not is_external(url):
                    images_checked += 1
                    target_path = blog_dir / url
                    if not target_path.exists():
                        missing_files[url].append(file_path.name)
            
            files_checked += 1
            
            if files_checked % 100 == 0:
                print(f"Checked {files_checked} files...")
                
        except Exception as e:
            print(f"Error processing {file_path.name}: {e}")

print(f"\n=== Summary ===")
print(f"Files checked: {files_checked}")
print(f"Local links checked: {links_checked}")
print(f"Local images checked: {images_checked}")
print(f"Missing resources: {len(missing_files)}")

if missing_files:
    print(f"\n=== Missing Resources (Top 20) ===")
    sorted_missing = sorted(missing_files.items(), key=lambda x: len(x[1]), reverse=True)
    for resource, referrers in sorted_missing[:20]:
        print(f"\n{resource}")
        print(f"  Referenced by {len(referrers)} file(s)")
        if len(referrers) <= 5:
            for ref in referrers:
                print(f"    - {ref}")
        else:
            for ref in referrers[:3]:
                print(f"    - {ref}")
            print(f"    ... and {len(referrers) - 3} more")
