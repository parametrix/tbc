# The Building Coder - Post Publishing Guide

## Overview

This guide explains how to publish and manage blog posts in The Building Coder archive. **The easiest approach uses GitHub Actions** - no local setup required. For advanced users, local Python scripts are also available.

---

## 🚀 Quick Start (TL;DR) - Using GitHub Actions

### Publish a New Post

1. **Create a draft** in `a/drafts/` with front matter:
   ```markdown
   ---
   title: "My Post Title"
   date: 2026-01-05
   ---
   
   Your content here...
   ```

2. **Push to GitHub** - The Action publishes automatically!
   ```bash
   git add a/drafts/my-post.md
   git commit -m "Add draft: My Post Title"
   git push
   ```

3. **Done!** The post appears in the chronological index and Timeline (right column).

### Add Post to a Topic (Optional)

After publishing, add to a subject topic via Actions:

1. Go to **Actions** → **"Manage Topics"**
2. Click **"Run workflow"**
3. Fill in:
   - Action: `add-post`
   - Topic ID: `5.9` (use `list` action to see all topics)
   - Post file: `2079_my_post.html`
   - Post title: `My Post Title`

### Remove a Post

1. Go to **Actions** → **"Remove Post"**
2. Click **"Run workflow"**
3. Fill in:
   - Post filename: `2079_my_post.html`
   - Confirm: `DELETE`
4. The Action removes the post from all locations automatically.

---

## 📋 Table of Contents

1. [Writing a New Post](#1-writing-a-new-post)
2. [Post Front Matter](#2-post-front-matter)
3. [Markdown Formatting Guide](#3-markdown-formatting-guide)
4. [Publishing via GitHub Actions](#4-publishing-via-github-actions)
5. [Managing Topics](#5-managing-topics)
6. [Removing Posts](#6-removing-posts)
7. [Updating Published Posts](#7-updating-published-posts)
8. [Local Scripts Reference](#8-local-scripts-reference)
9. [Troubleshooting](#9-troubleshooting)

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

## 4. Publishing via GitHub Actions

The recommended way to publish posts is via GitHub Actions - no local Python setup required.

### 4.1 Automatic Publishing

When you push a new `.md` file to `a/drafts/`, GitHub Actions automatically:
1. Converts Markdown to HTML
2. Updates the index and TOC
3. Commits the changes
4. Deploys to GitHub Pages

### 4.2 Workflow

```
1. Create:    a/drafts/2026-01-05-new-post.md
2. Commit:    git add -A && git commit -m "Draft: new post"
3. Push:      git push
4. Wait:      ~2 minutes for Actions to complete
5. Done:      Post is live!
```

### 4.3 Checking Action Status

1. Go to your repository on GitHub
2. Click "Actions" tab
3. See the "Publish New Posts" workflow
4. Check for ✅ success or ❌ failure

### 4.4 Manual Trigger

You can also manually trigger publishing:

1. Go to Actions → "Publish New Posts"
2. Click "Run workflow"
3. Optionally specify a draft file path
4. Click "Run workflow" button

---

## 5. Managing Topics

The **left sidebar** organizes posts into **Topics** (subject-based groups). The **right column** shows chronological navigation (timeline). When you publish a post, it automatically appears in:
- **Recent Posts** - The first topic in the left sidebar
- **Timeline** - Chronological navigation on the right (from `a/toc/chrono-data.json`)

You can also add posts to subject topics (like "Custom Exporter" or "Family API").

### 5.1 Understanding the Sidebar Structure

The left sidebar TOC data is stored in `a/toc/toc-data.json`:

```
Left Sidebar Structure (Topic-based)
├── Navigation Links (About, Contact, etc.)
└── Topics (subject-based groups)
    ├── 5.1 Custom Exporter
    ├── 5.2 2D Booleans and Adjacent Areas
    ├── ... (57 topics)
    ├── 5.56 Forge and APS
    └── 5.99 Uncategorized (new posts land here)
```

**Note:** New posts are automatically added to the **Uncategorized** topic (ID 5.99). Use `manage_topics.py` or the "Manage Topics" GitHub Action to move posts to subject-specific categories.

The right column timeline data is stored in `a/toc/chrono-data.json`:

```
Right Column Timeline
├── Previous/Next post navigation
├── Current post indicator
└── Year browser (2008-2026)
```

### 5.2 Managing Topics via GitHub Actions

**List All Topics:**
1. Go to Actions → "Manage Topics"
2. Set Action to `list`
3. Run workflow - see output in Action logs

**Add Post to a Topic:**
1. Go to Actions → "Manage Topics"
2. Fill in:
   - Action: `add-post`
   - Topic ID: e.g., `5.9`
   - Post file: e.g., `2079_my_post.html`
   - Post title: e.g., `My Post Title`
3. Run workflow

**Create a New Topic:**
1. Go to Actions → "Manage Topics"
2. Fill in:
   - Action: `new-topic`
   - Topic ID: e.g., `5.62`
   - Topic title: e.g., `Machine Learning`
3. Run workflow

### 5.3 Managing Topics via Local Script

For local development, use `manage_topics.py`:

```bash
# List all topics
python scripts/manage_topics.py list

# Show topic details
python scripts/manage_topics.py show 5.1

# Add post to topic
python scripts/manage_topics.py add-post 5.9 2079_my_post.html "My Post Title"

# Create new topic
python scripts/manage_topics.py new-topic 5.62 "Machine Learning"

# Preview without saving
python scripts/manage_topics.py add-post 5.9 2079_post.html "Title" --dry-run
```

---

## 6. Removing Posts

### 6.1 Remove via GitHub Actions (Recommended)

The easiest way to remove a post:

1. Go to **Actions** → **"Remove Post"**
2. Click **"Run workflow"**
3. Fill in:
   - **Post filename:** e.g., `2079_my_post.html`
   - **Confirm:** Type `DELETE` (required for safety)
4. Click **"Run workflow"**

The Action automatically:
- Deletes the HTML file
- Removes entry from `a/index.html`
- Removes from any topics in left sidebar (if present)
- Removes from timeline (`a/toc/chrono-data.json`)
- Commits and pushes changes

### 6.2 Remove via Local Script

For local development, use the `delete_post.py` script:

```bash
# Preview what will be removed
python scripts/delete_post.py 2079_my_post.html --dry-run

# Actually remove the post
python scripts/delete_post.py 2079_my_post.html

# Commit and push
git add -A
git commit -m "Remove post #2079"
git push
```

The script automatically:
- Deletes the HTML file
- Removes entry from `a/index.html`
- Removes from any topics in `a/toc/toc-data.json`
- Removes from timeline `a/toc/chrono-data.json`

### 6.3 Remove Manually

If you prefer to remove a post manually:

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

#### Step 3: Remove from left sidebar (if present)

Edit `a/toc/toc-data.json`:

1. Search for the post filename and remove its entry from any topic:
   ```json
   { "title": "Your Post Title", "file": "NNNN_slug.html" }
   ```

2. Update `totalPostLinks` count.

#### Step 4: Remove from timeline

Edit `a/toc/chrono-data.json`:

1. Remove from the "posts" array:
   ```json
   { "num": NNNN, "file": "NNNN_slug.html", "title": "Your Post Title", "date": "YYYY-MM-DD", "year": YYYY, "month": MM }
   ```

2. Update `totalPosts` count and the corresponding year's `count` in the `years` array.

#### Step 5: Commit and push

```bash
git add -A
git commit -m "Remove post NNNN: Title"
git push
```

---

## 7. Updating Published Posts

After publishing, you may need to correct typos, update content, or change metadata. The approach depends on what you're changing.

### 7.1 Content-Only Edits (Most Common)

For typos, content fixes, or adding information, just edit the HTML file directly:

```bash
# Edit the file
code a/2079_my_post.html   # or use any editor

# Commit and push
git add a/2079_my_post.html
git commit -m "Fix typo in post #2079"
git push
```

**No scripts needed!** The TOC files only store metadata (title, filename, date), not content.

### 7.2 Metadata Changes

If you need to change the title, date, or categories, use the `update_post.py` script:

```bash
# Change title
python scripts/update_post.py 2079_my_post.html --title "New Better Title"

# Change date
python scripts/update_post.py 2079_my_post.html --date 2026-01-15

# Change categories (shown in index.html)
python scripts/update_post.py 2079_my_post.html --categories "Geometry, Walls"

# Multiple changes at once
python scripts/update_post.py 2079_my_post.html --title "New Title" --date 2026-01-15

# Preview without making changes
python scripts/update_post.py 2079_my_post.html --title "New Title" --dry-run
```

#### What Gets Updated

| Change | Files Updated |
|--------|---------------|
| **Title** | HTML `<title>`, `chrono-data.json`, `toc-data.json` (if in topic) |
| **Date** | `chrono-data.json` |
| **Categories** | `chrono-data.json` |

**Note:** The chronological table in `a/index.html` is dynamically generated from `chrono-data.json` via JavaScript.

### 7.3 Topic Changes

To move a post between topics, use `manage_topics.py`:

```bash
# Remove from current topic
python scripts/manage_topics.py remove-post 5.99 2079_my_post.html

# Add to new topic
python scripts/manage_topics.py add-post 5.9 2079_my_post.html "My Post Title"
```

Or use the **Manage Topics** GitHub Action.

### 7.4 Manual Metadata Update (Without Script)

If you prefer to edit files manually:

**Note:** The chronological table in `a/index.html` is dynamically generated from `chrono-data.json` via JavaScript, so you only need to update the JSON files.

#### Update Title

1. **Edit the HTML file** - update the `<title>` tag and any H3 heading
2. **Edit `a/toc/chrono-data.json`** - find the entry by post number and update `"title"`
3. **Edit `a/toc/toc-data.json`** - if the post is in a topic, update `"title"` there too

#### Update Date

1. **Edit `a/toc/chrono-data.json`** - update `"date"`, `"year"`, and `"month"` fields

#### Update Categories

1. **Edit `a/toc/chrono-data.json`** - update the `"categories"` field (if present)

### 7.5 Summary: When to Use What

| Task | Method |
|------|--------|
| Fix typo in content | Edit HTML file directly |
| Change title | `python scripts/update_post.py --title "..."` |
| Change date | `python scripts/update_post.py --date YYYY-MM-DD` |
| Change categories | `python scripts/update_post.py --categories "..."` |
| Move to different topic | `python scripts/manage_topics.py remove-post` + `add-post` |
| Add to a topic | `python scripts/manage_topics.py add-post` |

---

## 8. Local Scripts Reference

For advanced users who prefer working locally with Python scripts.

### 8.1 Prerequisites

- Python 3.8 or higher
- Required packages:

```bash
pip install markdown beautifulsoup4 python-frontmatter pyyaml
```

### 8.2 Publish a Single Post

```bash
# Basic usage
python scripts/publish_post.py a/drafts/my-post.md

# With explicit date and title
python scripts/publish_post.py a/drafts/my-post.md --date 2026-01-05 --title "My Title"

# Preview without writing files
python scripts/publish_post.py a/drafts/my-post.md --dry-run
```

### 8.3 Command Options

| Option | Description |
|--------|-------------|
| `--date YYYY-MM-DD` | Override publication date |
| `--title "Title"` | Override post title |
| `--slug name` | Custom filename slug |
| `--dry-run` | Preview without writing |
| `--no-toc` | Don't update a/toc/ files (sidebar + timeline) |
| `--no-stats` | Don't update homepage stats |

### 8.4 What the Script Does

1. **Reads** the Markdown file and front matter
2. **Converts** Markdown to HTML with syntax highlighting
3. **Wraps** with the site template (nav, sidebar, CSS)
4. **Generates** filename: `NNNN_slug.html` (next number)
5. **Updates** `a/toc/chrono-data.json` (right column timeline)
6. **Updates** `a/toc/toc-data.json` (adds to Uncategorized topic)
7. **Updates** `index.html` (homepage) - post count stats

**Note:** The chronological table in `a/index.html` is dynamically generated from `chrono-data.json` via JavaScript. New posts are added to the Uncategorized topic (ID 5.99) in the left sidebar. Use `manage_topics.py` to move posts to subject-specific categories.

### 8.5 Post-Publishing

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

### 8.6 Available Scripts

| Script | Purpose |
|--------|---------|
| `scripts/publish_post.py` | Publish new posts from Markdown |
| `scripts/update_post.py` | Update title, date, or categories of published posts |
| `scripts/delete_post.py` | Remove posts and clean up all references |
| `scripts/manage_topics.py` | Add/remove posts to topics, create topics |

---

## 9. Troubleshooting

### 9.1 Common Issues

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

**Issue: GitHub Action failed**
```
Solution:
1. Check Actions tab for error details
2. Verify front matter is valid YAML
3. Ensure file is in a/drafts/ directory
4. Check that filename ends in .md
```

### 9.2 Validating Your Post

Before publishing, you can preview locally:

```bash
# Convert without publishing
python scripts/publish_post.py a/drafts/my-post.md --dry-run
```

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
