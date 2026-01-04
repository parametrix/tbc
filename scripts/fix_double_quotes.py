"""
Fix double-quote issues in HTML files introduced by link replacement.
Patterns like href="file.htm""> should be href="file.htm">
"""
import os
import re
from pathlib import Path

# Directory containing blog posts
blog_dir = Path(__file__).parent / 'a'

# Pattern to find double quotes at end of href/src attributes
pattern = re.compile(r'"">')

fixed_count = 0
error_count = 0
files_processed = 0

print("Fixing double-quote issues in HTML files...")

for file_path in sorted(blog_dir.glob('*.htm*')):
    if file_path.suffix in ['.htm', '.html']:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if file has the issue
            if '"">' in content:
                # Fix the double quotes
                fixed_content = pattern.sub('">', content)
                
                # Write back
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                # Count occurrences
                count = content.count('"">')
                fixed_count += count
                print(f"Fixed {count} occurrences in {file_path.name}")
            
            files_processed += 1
            
            if files_processed % 100 == 0:
                print(f"Processed {files_processed} files...")
                
        except Exception as e:
            print(f"Error processing {file_path.name}: {e}")
            error_count += 1

print(f"\n=== Summary ===")
print(f"Files processed: {files_processed}")
print(f"Total double-quotes fixed: {fixed_count}")
print(f"Errors: {error_count}")
