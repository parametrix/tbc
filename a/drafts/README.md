# Drafts Folder

Place new blog post drafts here as Markdown files.

## File Naming

Use the format: `YYYY-MM-DD-slug.md`

Example: `2026-01-05-revit-wall-geometry.md`

## Required Front Matter

```yaml
---
title: "Your Post Title"
date: 2026-01-05
---
```

## Publishing

### Option 1: Local Python Script
```bash
python scripts/publish_post.py a/drafts/your-post.md
git add -A && git commit -m "Add post" && git push
```

### Option 2: Push to Trigger GitHub Actions
Just push your draft file - GitHub Actions will automatically publish it.

## Template

Copy `_TEMPLATE.md` as a starting point for new posts.

## After Publishing

Published drafts are moved to `published/` subfolder with `post_number` and `html_file` added to front matter.

## Updating Published Posts

To update a published post, edit the markdown file in `published/` and push:

```bash
# Edit the markdown
code a/drafts/published/2026-01-05-your-post.md

# Push - GitHub Actions regenerates HTML automatically
git add a/drafts/published/2026-01-05-your-post.md
git commit -m "Update: fixed typo"
git push
```

The workflow will:
1. Regenerate the HTML from the updated markdown
2. Update title/date in JSON files if changed
3. Deploy the updated site
