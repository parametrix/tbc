# The Building Coder - New Post Publishing Guide

## Overview

This guide explains how to add new blog posts to The Building Coder archive. You can write posts in Markdown, and the publishing scripts will automatically convert them to HTML with the proper template, update the index, and prepare the site for GitHub Pages.

---

## Quick Start (TL;DR)

```bash
# 1. Create a new post in Markdown
#    File: a/drafts/my-new-post.md

# 2. Run the publish script
python scripts/publish_post.py a/drafts/my-new-post.md --date 2026-01-05 --title "My New Post Title"

# 3. Commit and push
git add -A
git commit -m "Add post: My New Post Title"
git push
```

**Or with GitHub Actions (automated):**
1. Create `a/drafts/my-new-post.md` with front matter
2. Push to GitHub
3. Done! GitHub Actions publishes automatically

---

## Table of Contents

1. [Writing a New Post](#1-writing-a-new-post)
2. [Post Front Matter](#2-post-front-matter)
3. [Markdown Formatting Guide](#3-markdown-formatting-guide)
4. [Publishing Locally](#4-publishing-locally)
5. [Publishing via GitHub Actions](#5-publishing-via-github-actions)
6. [Troubleshooting](#6-troubleshooting)

---

## 1. Writing a New Post

### 1.1 Create the Draft File

Create a new Markdown file in the `a/drafts/` directory:

```
a/drafts/2026-01-05-my-post-title.md
```

**Naming Convention:**
- Format: `YYYY-MM-DD-slug.md`
- Use lowercase with hyphens
- Keep slugs concise but descriptive

### 1.2 File Location

```
thebuildingcoder-archive/
├── a/
│   ├── drafts/              ← Put new posts here
│   │   └── 2026-01-05-my-post.md
│   ├── img/                 ← Put images here
│   ├── 0001_welcome.htm     ← Published posts
│   └── ...
└── scripts/
    └── publish_post.py      ← Publishing script
```

---

## 2. Post Front Matter

Each post should start with YAML front matter:

```markdown
---
title: "My Post Title"
date: 2026-01-05
categories: [Revit API, Geometry]
tags: [walls, filtering, elements]
---

Your post content starts here...
```

### Required Fields

| Field | Description | Example |
|-------|-------------|---------|
| `title` | Post title (in quotes if special chars) | `"Working with Walls"` |
| `date` | Publication date | `2026-01-05` |

### Optional Fields

| Field | Description | Example |
|-------|-------------|---------|
| `categories` | Topic categories | `[Revit API, MEP]` |
| `tags` | Searchable tags | `[walls, geometry]` |
| `slug` | Custom URL slug | `wall_geometry` |
| `post_number` | Override auto-numbering | `2078` |

### Example Complete Post

```markdown
---
title: "Working with Wall Geometry in Revit API"
date: 2026-01-05
categories: [Geometry, Walls]
tags: [solid, faces, edges, curves]
---

### Working with Wall Geometry in Revit API

Today we explore how to extract and manipulate wall geometry...

#### Getting the Wall Solid

To get the solid geometry from a wall element:

```csharp
Options opt = new Options();
GeometryElement geomElem = wall.get_Geometry(opt);

foreach (GeometryObject geomObj in geomElem)
{
    Solid solid = geomObj as Solid;
    if (solid != null && solid.Volume > 0)
    {
        // Process the solid
        ProcessSolid(solid);
    }
}
```

#### Extracting Faces

Each solid contains faces that can be processed:

<center>
<img src="img/wall_faces.png" alt="Wall faces" title="Wall faces" width="400"/>
</center>

For more information, see the [Geometry API documentation](0283_abg04_curves.htm).
```

---

## 3. Markdown Formatting Guide

### 3.1 Basic Formatting

| Markdown | Result |
|----------|--------|
| `**bold**` | **bold** |
| `*italic*` | *italic* |
| `` `code` `` | `code` |
| `[link](url)` | [link](url) |

### 3.2 Headings

```markdown
### Main Title (H3)
#### Section (H4)
##### Subsection (H5)
```

**Note:** Use H3 (`###`) for the main post title, H4 (`####`) for sections.

### 3.3 Code Blocks

Use fenced code blocks with language identifier:

````markdown
```csharp
public void MyMethod()
{
    // C# code here
}
```

```python
def my_function():
    # Python code here
    pass
```
````

Supported languages: `csharp`, `python`, `javascript`, `xml`, `json`, `bash`, `html`

### 3.4 Images

**Basic image:**
```markdown
![Alt text](img/my_image.png)
```

**Centered image with caption (use HTML):**
```html
<center>
<img src="img/my_image.png" alt="Description" title="Title" width="500"/>
<p style="font-size: 80%; font-style:italic">Caption text</p>
</center>
```

**Important:** 
- Place images in `a/img/` directory
- Use relative paths: `img/filename.png`

### 3.5 Links

**Internal links to other posts:**
```markdown
See [my other post](0283_abg04_curves.htm) for more details.
```

**External links:**
```markdown
Check the [Revit API Forum](https://forums.autodesk.com/t5/revit-api-forum/bd-p/160).
```

### 3.6 Blockquotes

```markdown
> This is a quoted passage from another source.
> It can span multiple lines.
```

### 3.7 Lists

**Unordered:**
```markdown
- Item one
- Item two
  - Nested item
- Item three
```

**Ordered:**
```markdown
1. First step
2. Second step
3. Third step
```

### 3.8 Tables

```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data A   | Data B   | Data C   |
| Data D   | Data E   | Data F   |
```

### 3.9 Anchor Links (for TOC)

Create named anchors for internal navigation:

```markdown
#### <a name="2"></a> Section Title

Later, link to it:
See [Section Title](#2) above.
```

---

## 4. Publishing Locally

### 4.1 Prerequisites

- Python 3.8 or higher
- Required packages:

```bash
pip install markdown beautifulsoup4 python-frontmatter pyyaml
```

### 4.2 Publish a Single Post

```bash
# Basic usage
python scripts/publish_post.py a/drafts/my-post.md

# With explicit date and title
python scripts/publish_post.py a/drafts/my-post.md --date 2026-01-05 --title "My Title"

# Preview without writing files
python scripts/publish_post.py a/drafts/my-post.md --dry-run
```

### 4.3 Command Options

| Option | Description |
|--------|-------------|
| `--date YYYY-MM-DD` | Override publication date |
| `--title "Title"` | Override post title |
| `--slug name` | Custom filename slug |
| `--dry-run` | Preview without writing |
| `--no-index` | Don't update a/index.html |
| `--no-toc` | Don't update toc-data.json (sidebar) |
| `--no-stats` | Don't update homepage stats |

### 4.4 What the Script Does

1. **Reads** the Markdown file and front matter
2. **Converts** Markdown to HTML with syntax highlighting
3. **Wraps** with the site template (nav, sidebar, CSS)
4. **Generates** filename: `NNNN_slug.html` (next number)
5. **Updates** `a/index.html` with new table row
6. **Updates** `a/toc/toc-data.json` - adds to "Recent Posts" in sidebar
7. **Updates** `index.html` (homepage) - post count stats

### 4.5 Post-Publishing

After running the script:

```bash
# Review changes
git status
git diff a/index.html

# Commit
git add -A
git commit -m "Add post NNNN: Title"

# Push to GitHub
git push
```

---

## 5. Publishing via GitHub Actions

### 5.1 Automatic Publishing

When you push a new `.md` file to `a/drafts/`, GitHub Actions automatically:
1. Converts Markdown to HTML
2. Updates the index
3. Commits the changes
4. Deploys to GitHub Pages

### 5.2 Workflow

```
1. Create:    a/drafts/2026-01-05-new-post.md
2. Commit:    git add -A && git commit -m "Draft: new post"
3. Push:      git push
4. Wait:      ~2 minutes for Actions to complete
5. Done:      Post is live!
```

### 5.3 Checking Action Status

1. Go to your repository on GitHub
2. Click "Actions" tab
3. See the "Publish New Posts" workflow
4. Check for ✅ success or ❌ failure

### 5.4 Manual Trigger

You can also manually trigger publishing:

1. Go to Actions → "Publish New Posts"
2. Click "Run workflow"
3. Select branch and run

---

## 6. Troubleshooting

### 6.1 Common Issues

**Issue: Script can't find the markdown file**
```
Solution: Use full path or run from repository root
python scripts/publish_post.py a/drafts/my-post.md
```

**Issue: Missing front matter**
```
Solution: Ensure your file starts with --- and ends with ---
---
title: "My Title"
date: 2026-01-05
---
```

**Issue: Images not showing**
```
Solution: 
1. Put images in a/img/
2. Use relative path: img/filename.png (not /img/ or ../img/)
```

**Issue: Code highlighting not working**
```
Solution: Use fenced code blocks with language:
```csharp
// code here
```
```

**Issue: Post number collision**
```
Solution: The script auto-detects the next number.
If manual, check a/index.html for the latest post number.
```

### 6.2 Validating Your Post

Before publishing, you can preview locally:

```bash
# Convert without publishing
python scripts/publish_post.py a/drafts/my-post.md --dry-run

# Open the preview in browser
start a/drafts/my-post-preview.html
```

### 6.3 Deleting/Reverting a Published Post

If you need to unpublish or delete a post, you must undo all changes made by the publish script:

#### Step 1: Remove the HTML file

```bash
git rm a/NNNN_slug.html
```

#### Step 2: Remove from index.html

Edit `a/index.html` and delete the table row for the post:

```html
<!-- Find and delete this line -->
<tr><td align="right">NNNN</td><td>YYYY-MM-DD</td><td><a href="NNNN_slug.html">Title</a>...</td></tr>
```

#### Step 3: Remove from TOC sidebar

Edit `a/toc/toc-data.json` and remove the post from the "Recent Posts" section:

```json
{
  "id": "0.1",
  "title": "Recent Posts",
  "posts": [
    // Delete this entry:
    { "title": "Your Post Title", "file": "NNNN_slug.html" }
  ]
}
```

Also update `totalPostLinks` count in the same file.

#### Step 4: Commit and push

```bash
git add -A
git commit -m "Delete post NNNN: Title"
git push
```

#### Alternative: Use the Delete Script

A helper script is provided in `scripts/delete_post.py`:

```bash
# Preview what would be deleted
python scripts/delete_post.py NNNN_slug.html --dry-run

# Actually delete
python scripts/delete_post.py NNNN_slug.html
```

The script handles all cleanup automatically (HTML file, index, TOC).

---

## Appendix A: File Templates

### A.1 Minimal Post Template

```markdown
---
title: "Post Title"
date: 2026-01-05
---

### Post Title

Content goes here...
```

### A.2 Full Post Template

```markdown
---
title: "Comprehensive Post Title"
date: 2026-01-05
categories: [Category1, Category2]
tags: [tag1, tag2, tag3]
---

### Comprehensive Post Title

Introduction paragraph explaining what this post covers.

- [Topic One](#2)
- [Topic Two](#3)
- [Conclusion](#4)

#### <a name="2"></a> Topic One

First topic content...

```csharp
// Code example
public void Example()
{
    Console.WriteLine("Hello");
}
```

#### <a name="3"></a> Topic Two

Second topic content...

<center>
<img src="img/example.png" alt="Example" title="Example" width="500"/>
</center>

#### <a name="4"></a> Conclusion

Summary and closing thoughts.

For more information, see [related post](0123_related.htm).
```

---

## Appendix B: Category and Tag Reference

### Common Categories

| Category | Description |
|----------|-------------|
| Getting Started | Introductory content |
| Geometry | Solids, faces, curves, points |
| Elements | Element creation, modification |
| Parameters | Shared, family, project parameters |
| Family API | Family documents, symbols |
| MEP | Mechanical, electrical, plumbing |
| Filtering | Element collectors, filters |
| Events | Document, application events |
| External Commands | IExternalCommand, IExternalApplication |
| UI | Ribbon, dialogs, selection |
| Forge/APS | Cloud services, Data Management |

### Common Tags

`walls`, `floors`, `roofs`, `doors`, `windows`, `rooms`, `spaces`, `views`, `sheets`, `schedules`, `materials`, `transactions`, `regeneration`, `performance`, `debugging`, `samples`

---

## Appendix C: Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│                  PUBLISHING QUICK REFERENCE                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. CREATE DRAFT                                            │
│     Location: a/drafts/YYYY-MM-DD-slug.md                   │
│     Images:   a/img/                                        │
│                                                             │
│  2. FRONT MATTER                                            │
│     ---                                                     │
│     title: "Title"                                          │
│     date: YYYY-MM-DD                                        │
│     ---                                                     │
│                                                             │
│  3. PUBLISH                                                 │
│     python scripts/publish_post.py a/drafts/my-post.md     │
│                                                             │
│  4. COMMIT & PUSH                                           │
│     git add -A && git commit -m "Add post" && git push     │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  HEADINGS:    ### H3  #### H4  ##### H5                    │
│  BOLD:        **text**                                      │
│  ITALIC:      *text*                                        │
│  CODE:        `inline` or ```lang for blocks               │
│  LINK:        [text](url)                                   │
│  IMAGE:       ![alt](img/file.png)                         │
│  LIST:        - item  or  1. item                          │
│  QUOTE:       > quoted text                                 │
└─────────────────────────────────────────────────────────────┘
```
