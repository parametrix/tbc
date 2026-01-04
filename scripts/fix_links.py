import re

# Read the index.html file
with open('a/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to match the table rows with links
# Format: <a href="EXTERNAL_URL">TITLE</a>&nbsp;&nbsp;&nbsp;<a href="LOCAL_FILE">^</a>
pattern = r'(<a href="http://thebuildingcoder\.typepad\.com/[^"]+">)([^<]+)(</a>&nbsp;&nbsp;&nbsp;<a href=")([^"]+)(">)\^(</a>)'

# Replace with: <a href="LOCAL_FILE">TITLE</a>&nbsp;&nbsp;&nbsp;<a href="EXTERNAL_URL">web</a>
def replace_func(match):
    external_url = match.group(1)[9:-2]  # Extract URL without <a href=" and ">
    title = match.group(2)
    local_file = match.group(4)
    
    return f'<a href="{local_file}">{title}</a>&nbsp;&nbsp;&nbsp;<a href="{external_url}">web</a>&nbsp;&nbsp;'

# Apply the replacement
new_content = re.sub(pattern, replace_func, content)

# Update the table header
new_content = new_content.replace(
    '<th>Title (Internet hyperlink) &ndash; ^ (local)</th>',
    '<th>Title (local) &ndash; web (Internet hyperlink)</th>'
)

# Write the modified content
with open('a/index_local.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Modified index created as index_local.html")
print("Original index.html preserved unchanged")
