"""
Add copy-code.js script to all HTML pages in The Building Coder archive.
Injects the script reference just before the closing </body> tag.
"""

import os
import re
from pathlib import Path

def add_copy_code_script(html_dir):
    """Add copy-code.js script reference to all HTML files."""
    
    # Script tag to inject
    script_tag = '<script src="toc/copy-code.js"></script>'
    
    # Find all HTML files
    html_files = list(Path(html_dir).glob('*.htm')) + list(Path(html_dir).glob('*.html'))
    
    modified_count = 0
    skipped_count = 0
    
    for html_file in html_files:
        try:
            content = html_file.read_text(encoding='utf-8')
            
            # Skip if already has copy-code.js
            if 'copy-code.js' in content:
                skipped_count += 1
                continue
            
            # Find the closing </body> tag and insert script before it
            # Insert after toc-sidebar.js if present, otherwise before </body>
            if 'toc-sidebar.js' in content:
                # Insert after toc-sidebar.js line
                new_content = content.replace(
                    '<script src="toc/toc-sidebar.js"></script>',
                    '<script src="toc/toc-sidebar.js"></script>\n<script src="toc/copy-code.js"></script>'
                )
            else:
                # Insert before </body>
                new_content = content.replace(
                    '</body>',
                    script_tag + '\n</body>'
                )
            
            if new_content != content:
                html_file.write_text(new_content, encoding='utf-8')
                modified_count += 1
                
        except Exception as e:
            print(f"Error processing {html_file}: {e}")
    
    print(f"Modified: {modified_count} files")
    print(f"Skipped (already has script): {skipped_count} files")
    print(f"Total HTML files: {len(html_files)}")

if __name__ == '__main__':
    import sys
    
    # Default to 'a' subdirectory
    html_dir = sys.argv[1] if len(sys.argv) > 1 else 'a'
    
    if not os.path.isdir(html_dir):
        print(f"Directory not found: {html_dir}")
        sys.exit(1)
    
    print(f"Adding copy-code.js to HTML files in: {html_dir}")
    add_copy_code_script(html_dir)
    print("Done!")
