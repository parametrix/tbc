# Jekyll Markdown Conversion Requirements Specification

## Executive Summary

This document specifies the requirements for converting The Building Coder blog archive from HTML (`.htm`/`.html`) files to Jekyll-compatible Markdown (`.md`) format, while preserving:
- Exact visual rendering matching current pages
- TOC sidebar functionality with search and navigation
- Code syntax highlighting
- All images, media, and links
- Mobile responsiveness

---

## Feasibility Assessment

### ✅ **YES, This Conversion Is Possible**

However, it requires careful attention to several challenges:

| Aspect | Feasibility | Notes |
|--------|-------------|-------|
| Basic content conversion | ✅ Easy | HTML to Markdown is well-supported |
| Code blocks with syntax highlighting | ✅ Possible | Jekyll supports Rouge/Prism highlighters |
| Images and media | ✅ Possible | Relative paths work in Markdown |
| Internal links | ⚠️ Moderate | URLs change from `.htm`/`.html` to permalinks |
| TOC sidebar | ⚠️ Complex | Requires custom Jekyll include or JavaScript |
| Exact visual match | ⚠️ Complex | Requires custom theme matching current CSS |
| Inline HTML/styles | ⚠️ Complex | Some posts have complex HTML that must be preserved |
| 2,079 files | ⚠️ Time-intensive | Automated conversion with manual review needed |

### Key Challenges

1. **Mixed Content**: ~728 files are already `.md` (with HTML fragments), ~1,350 are pure `.htm`, ~729 are `.html`
2. **Inline HTML**: Many posts contain complex HTML (tables, styled divs, centered images) that Markdown doesn't support natively
3. **Code Highlighting**: Currently uses Google Prettify and Prism.js; needs migration to Jekyll-native Rouge
4. **TOC Sidebar**: Currently JavaScript-based; needs Jekyll/Liquid reimplementation
5. **URL Compatibility**: Old `.htm`/`.html` URLs need redirects for SEO

---

## 1. Current Architecture

### 1.1 File Statistics

| Type | Count | Notes |
|------|-------|-------|
| `.htm` files | 1,350 | Posts #0001-1350, HTML format |
| `.html` files | 729 | Posts #1351+, HTML with wrapper |
| `.md` files | 728 | Markdown sources (often with HTML fragments) |
| Total posts | ~2,079 | Unique blog posts |

### 1.2 Current HTML Structure

Each post currently has:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>The Building Coder</title>
    <link rel="stylesheet" href="bc.css">
    <link rel="stylesheet" href="google-code-prettify/prettify.css">
    <script src="google-code-prettify/run_prettify.js"></script>
    <link rel="stylesheet" href="toc/toc-sidebar.css">
</head>
<body>
    <div class="nav">
        <a href="index.html">← Back to Index</a>
    </div>
    <article>
        <!-- Post content -->
    </article>
    <script src="toc/toc-sidebar.js"></script>
    <script src="toc/copy-code.js"></script>
</body>
</html>
```

### 1.3 Current Features

| Feature | Implementation |
|---------|----------------|
| Syntax highlighting | Google Prettify + Prism.js |
| TOC sidebar | Custom JavaScript (`toc-sidebar.js`) |
| Search | Real-time JavaScript filter |
| Navigation | JSON-based topic structure (`toc-data.json`) |
| Code copy button | Custom JavaScript (`copy-code.js`) |
| Styling | `bc.css` + inline styles |
| Mobile menu | Hamburger menu via JavaScript |

---

## 2. Target Architecture

### 2.1 Jekyll Directory Structure

```
thebuildingcoder-archive/
├── _config.yml                    # Jekyll configuration
├── _layouts/
│   ├── default.html               # Base layout with sidebar
│   ├── post.html                  # Post layout
│   └── home.html                  # Index page layout
├── _includes/
│   ├── head.html                  # <head> content
│   ├── header.html                # Site header/banner
│   ├── sidebar.html               # TOC sidebar
│   ├── footer.html                # Footer
│   ├── nav.html                   # Navigation
│   └── search.html                # Search component
├── _sass/
│   ├── _base.scss                 # Base styles
│   ├── _layout.scss               # Layout (sidebar, content)
│   ├── _syntax.scss               # Code highlighting
│   ├── _sidebar.scss              # Sidebar styles
│   └── _mobile.scss               # Responsive styles
├── assets/
│   ├── css/
│   │   └── main.scss              # Main stylesheet (imports _sass)
│   ├── js/
│   │   ├── sidebar.js             # Sidebar functionality
│   │   ├── search.js              # Search functionality
│   │   └── copy-code.js           # Copy button
│   └── img/                       # Site-wide images
├── _posts/                        # Blog posts (dated format)
│   ├── 2008-09-22-welcome.md
│   ├── 2008-09-23-devtech.md
│   └── ...
├── _data/
│   ├── toc.yml                    # Table of contents structure
│   └── navigation.yml             # Navigation links
├── img/                           # Post images (or in assets/)
├── downloads/                     # Downloadable files
├── index.md                       # Home page
├── about.md                       # About page
├── Gemfile                        # Ruby dependencies
└── .nojekyll                      # REMOVE - we want Jekyll now
```

### 2.2 Post Format (Front Matter)

Each Markdown post requires Jekyll front matter:

```markdown
---
layout: post
title: "Welcome"
date: 2008-09-22
categories: [getting-started]
tags: [introduction, revit-api]
post_number: 0001
original_file: 0001_welcome.htm
permalink: /a/0001_welcome.html
---

Welcome to The Building Coder...
```

### 2.3 Jekyll Configuration (`_config.yml`)

```yaml
# Site settings
title: The Building Coder
description: "Revit API Archive by Jeremy Tammik"
url: "https://parametrix.github.io"
baseurl: "/tbc"
author: "Jeremy Tammik"

# Build settings
markdown: kramdown
highlighter: rouge
permalink: /a/:title.html

kramdown:
  input: GFM
  syntax_highlighter: rouge
  syntax_highlighter_opts:
    block:
      line_numbers: false
    span:
      line_numbers: false

# Sass processing
sass:
  style: compressed
  sass_dir: _sass

# Plugins
plugins:
  - jekyll-seo-tag
  - jekyll-sitemap
  - jekyll-feed
  - jekyll-redirect-from

# Collections (optional - for non-date-based organization)
collections:
  posts:
    output: true
    permalink: /a/:name.html

# Defaults
defaults:
  - scope:
      path: ""
      type: "posts"
    values:
      layout: "post"

# Exclude from processing
exclude:
  - scripts/
  - a_backup/
  - Gemfile
  - Gemfile.lock
  - README.md
  - "*.py"
```

---

## 3. Conversion Process

### 3.1 Phase 1: Setup Jekyll Infrastructure

| Task | Details |
|------|---------|
| Create `_config.yml` | Site configuration |
| Create `_layouts/` | default.html, post.html, home.html |
| Create `_includes/` | sidebar.html, head.html, etc. |
| Create `_sass/` | Convert bc.css to SCSS modules |
| Create `assets/` | JS and compiled CSS |
| Create `Gemfile` | Jekyll dependencies |

### 3.2 Phase 2: Convert Styles

Convert current CSS to Jekyll-compatible SCSS:

| Source | Target |
|--------|--------|
| `bc.css` | `_sass/_base.scss` |
| `toc/toc-sidebar.css` | `_sass/_sidebar.scss` |
| Inline styles | `_sass/_post.scss` |
| `google-code-prettify/prettify.css` | `_sass/_syntax.scss` (or use Rouge) |

### 3.3 Phase 3: Sidebar Implementation

**Option A: Static Liquid-Based Sidebar**
- Generate sidebar from `_data/toc.yml` using Liquid templates
- Pros: Pure Jekyll, no JavaScript needed for basic nav
- Cons: No dynamic search without JS

**Option B: JavaScript Sidebar (Recommended)**
- Keep current sidebar approach with modifications
- Load TOC data from `_data/toc.json` or generate via Liquid
- Maintain search, collapse, and resize features
- Pros: Feature parity with current implementation
- Cons: Requires JavaScript

```html
<!-- _includes/sidebar.html -->
<nav id="tbc-sidebar">
  <div class="sidebar-header">
    <h2>The Building Coder</h2>
  </div>
  <div class="sidebar-search">
    <input type="text" id="toc-search" placeholder="Search posts...">
  </div>
  <div class="sidebar-content">
    {% for topic in site.data.toc.topics %}
    <div class="topic-group" data-topic="{{ topic.id }}">
      <button class="topic-toggle">{{ topic.title }}</button>
      <ul class="topic-posts">
        {% for post in topic.posts %}
        <li><a href="{{ post.url | relative_url }}">{{ post.title }}</a></li>
        {% endfor %}
      </ul>
    </div>
    {% endfor %}
  </div>
</nav>
```

### 3.4 Phase 4: Content Conversion

#### 3.4.1 Conversion Script Requirements

Create `scripts/convert_to_markdown.py`:

```python
# Pseudocode for conversion
for each html_file in ['*.htm', '*.html']:
    1. Parse HTML content
    2. Extract title from <h3> or <title>
    3. Extract date from index.html mapping
    4. Generate front matter (layout, title, date, permalink)
    5. Convert HTML body to Markdown:
       - <h3>, <h4>, etc. → #, ##, etc.
       - <p> → plain paragraphs
       - <a href="..."> → [text](url)
       - <img src="..."> → ![alt](src)
       - <pre class="prettyprint"> → ```language
       - <ul>, <ol>, <li> → Markdown lists
       - <blockquote> → > blockquote
       - <center><img>...</center> → keep as HTML (Markdown supports inline HTML)
       - Complex tables → keep as HTML
    6. Preserve inline HTML that Markdown can't represent
    7. Write to _posts/YYYY-MM-DD-slug.md
    8. Create redirect from old URL if needed
```

#### 3.4.2 HTML Elements Requiring Special Handling

| HTML Element | Conversion Strategy |
|--------------|---------------------|
| `<h3>Title</h3>` | `### Title` (or extract to front matter) |
| `<p>text</p>` | Plain text with blank lines |
| `<a href="url">text</a>` | `[text](url)` |
| `<img src="..." alt="...">` | `![alt](src)` |
| `<pre class="prettyprint">` | ````language ... ``` `` |
| `<code>inline</code>` | `` `inline` `` |
| `<ul><li>` | `- item` |
| `<ol><li>` | `1. item` |
| `<blockquote>` | `> quote` |
| `<b>`, `<strong>` | `**bold**` |
| `<i>`, `<em>` | `*italic*` |
| `<center><img></center>` | Keep as HTML (centered images) |
| `<table>` | Keep as HTML (complex tables) |
| `<div class="...">` | Keep as HTML (styled containers) |
| Twitter/LinkedIn blocks | Keep as HTML comments |

### 3.5 Phase 5: URL Redirects

Ensure old URLs continue to work:

```yaml
# In each post's front matter
---
redirect_from:
  - /a/0001_welcome.htm
  - /blog/2008/09/welcome.html
---
```

Or use `jekyll-redirect-from` plugin with a redirects file.

---

## 4. Visual Parity Requirements

### 4.1 Layout Matching

| Current | Target |
|---------|--------|
| Fixed left sidebar (280px default) | Same - use CSS Grid or Flexbox |
| Resizable sidebar | Same - JavaScript drag handle |
| Main content area (max-width: 900px) | Same |
| Navigation bar at top of posts | Same |
| Mobile hamburger menu | Same |

### 4.2 Typography Matching

| Element | Current Style | Target |
|---------|---------------|--------|
| Body font | `-apple-system, BlinkMacSystemFont, "Segoe UI"...` | Same |
| Headings | Georgia for index, system fonts for posts | Same |
| Code font | Monospace, 95% size | Same |
| Line height | 1.6 | Same |
| Link color | #0066cc | Same |

### 4.3 Code Block Styling

Rouge (Jekyll's default) can match current Prettify styling:

```scss
// _sass/_syntax.scss
.highlight {
  background-color: linen;
  padding: 10px;
  border-radius: 4px;
  overflow-x: auto;
  
  pre {
    font-size: 95%;
    line-height: 120%;
    color: darkblue;
    white-space: pre-wrap;
    word-wrap: break-word;
    margin: 0;
  }
  
  // Rouge token colors to match Prettify
  .k { color: #008; }  // keyword
  .s { color: #080; }  // string
  .c { color: #888; }  // comment
  .n { color: #000; }  // name
  // ... etc
}
```

---

## 5. Index Page Conversion

### 5.1 Current Index Features

The current `index.html` includes:
- Header banner with title
- About section with author photo
- Social links
- Statistics (post count, etc.)
- Full post table with dates

### 5.2 Jekyll Index Implementation

```markdown
---
layout: home
title: "The Building Coder - Revit API Archive"
---

{% include about-section.html %}

{% include stats-section.html %}

## All Posts

<table class="posts-table">
  <thead>
    <tr>
      <th>#</th>
      <th>Date</th>
      <th>Title</th>
    </tr>
  </thead>
  <tbody>
    {% for post in site.posts reversed %}
    <tr>
      <td>{{ post.post_number }}</td>
      <td>{{ post.date | date: "%Y-%m-%d" }}</td>
      <td><a href="{{ post.url | relative_url }}">{{ post.title }}</a></td>
    </tr>
    {% endfor %}
  </tbody>
</table>
```

---

## 6. TOC Data Migration

### 6.1 Convert `toc-data.json` to Jekyll Data

Create `_data/toc.yml`:

```yaml
version: "1.0"
lastUpdated: "2026-01-04"

navigation:
  - label: "About Jeremy Tammik"
    href: "#about"
  - label: "Getting Started"
    href: "#getting-started"

topics:
  - id: "5.1"
    title: "Custom Exporter"
    posts:
      - title: "Graphics Pipeline Custom Exporter"
        file: "0979_custom_exporter"
      - title: "Texture Bitmap and UV Coordinates"
        file: "0980_texture_uv_coord"
      # ...
  
  - id: "5.2"
    title: "DirectShape"
    posts:
      # ...
```

### 6.2 JavaScript Sidebar Integration

The sidebar JavaScript can load data from Jekyll-generated JSON:

```html
<!-- In _layouts/default.html -->
<script>
  window.tocData = {{ site.data.toc | jsonify }};
</script>
<script src="{{ '/assets/js/sidebar.js' | relative_url }}"></script>
```

---

## 7. Conversion Scripts

### 7.1 Required Python Scripts

| Script | Purpose |
|--------|---------|
| `convert_html_to_md.py` | Main conversion script |
| `extract_metadata.py` | Extract titles, dates from index |
| `generate_toc_yaml.py` | Convert toc-data.json to YAML |
| `verify_conversion.py` | Compare rendered output |
| `create_redirects.py` | Generate redirect mappings |

### 7.2 Dependencies

```
# scripts/requirements.txt
beautifulsoup4>=4.12.0
html2text>=2020.1.16
pyyaml>=6.0
python-frontmatter>=1.0.0
lxml>=4.9.0
markdownify>=0.11.0
```

### 7.3 Conversion Workflow

```bash
# 1. Install dependencies
pip install -r scripts/requirements.txt

# 2. Extract metadata from index
python scripts/extract_metadata.py

# 3. Convert HTML files to Markdown
python scripts/convert_html_to_md.py

# 4. Generate TOC YAML
python scripts/generate_toc_yaml.py

# 5. Build Jekyll site locally
bundle exec jekyll serve

# 6. Verify visual parity
python scripts/verify_conversion.py

# 7. Create redirects for old URLs
python scripts/create_redirects.py
```

---

## 8. Testing and Validation

### 8.1 Visual Comparison

For each converted page:
1. Screenshot original HTML page
2. Screenshot Jekyll-rendered page
3. Compare using image diff tool
4. Document and fix discrepancies

### 8.2 Functional Testing

| Feature | Test |
|---------|------|
| Sidebar toggle | Click topic to expand/collapse |
| Search | Type query, verify filtering |
| Navigation | Click posts, verify correct page loads |
| Code highlighting | Verify syntax colors match |
| Images | All images load correctly |
| Internal links | All post links work |
| External links | External links open correctly |
| Mobile menu | Hamburger opens sidebar |
| Resize | Drag handle resizes sidebar |
| Copy code button | Copies code to clipboard |

### 8.3 Link Validation

```bash
# Use htmlproofer or linkchecker
bundle exec htmlproofer ./_site --disable-external
```

---

## 9. Deployment

### 9.1 GitHub Pages with Jekyll

```yaml
# .github/workflows/jekyll.yml
name: Deploy Jekyll site to Pages

on:
  push:
    branches: ["main"]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'
          bundler-cache: true
      - name: Build with Jekyll
        run: bundle exec jekyll build
        env:
          JEKYLL_ENV: production
      - uses: actions/upload-pages-artifact@v3

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
    steps:
      - uses: actions/deploy-pages@v4
```

### 9.2 Gemfile

```ruby
source "https://rubygems.org"

gem "jekyll", "~> 4.3"
gem "minima", "~> 2.5"  # or custom theme

group :jekyll_plugins do
  gem "jekyll-feed"
  gem "jekyll-seo-tag"
  gem "jekyll-sitemap"
  gem "jekyll-redirect-from"
end
```

---

## 10. Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Complex HTML not converting properly | Visual differences | Keep HTML inline in Markdown |
| 2,079 files take too long | Delayed timeline | Batch processing, prioritize recent posts |
| Code highlighting mismatch | Poor readability | Custom Rouge theme matching Prettify |
| Broken internal links | Navigation failures | Comprehensive link validation |
| SEO impact from URL changes | Lost search rankings | 301 redirects for all old URLs |
| Sidebar feature regression | Poor UX | Thorough JavaScript testing |

---

## 11. Timeline Estimate

| Phase | Duration | Notes |
|-------|----------|-------|
| Phase 1: Jekyll setup | 1 day | Layouts, includes, config |
| Phase 2: Style conversion | 1-2 days | SCSS, visual matching |
| Phase 3: Sidebar implementation | 2-3 days | Liquid + JavaScript |
| Phase 4: Content conversion | 3-5 days | Automated with manual review |
| Phase 5: Testing and fixes | 2-3 days | Visual comparison, bug fixes |
| Phase 6: Deployment | 1 day | GitHub Pages, redirects |
| **Total** | **10-15 days** | |

---

## 12. Alternatives Considered

### 12.1 Keep HTML, Add Jekyll Wrapper Only

- Pros: Minimal changes, low risk
- Cons: Doesn't achieve Markdown goal

### 12.2 Use Hugo Instead of Jekyll

- Pros: Faster builds, Go-based
- Cons: Less GitHub Pages integration, different templating

### 12.3 Static Site Generator Comparison

| Generator | Markdown | GitHub Pages | Build Speed | Template Language |
|-----------|----------|--------------|-------------|-------------------|
| Jekyll | ✅ | Native support | Slow | Liquid |
| Hugo | ✅ | Via Actions | Fast | Go templates |
| Eleventy | ✅ | Via Actions | Fast | Multiple |
| Gatsby | ✅ | Via Actions | Medium | React/JSX |

**Recommendation**: Jekyll for native GitHub Pages support and Liquid templating simplicity.

---

## 13. Conclusion

**Converting to Jekyll Markdown is feasible and will provide:**

✅ Native GitHub Pages support
✅ Easier content editing in Markdown
✅ Better SEO with jekyll-seo-tag
✅ Automatic sitemap generation
✅ Cleaner repository structure

**Key success factors:**

1. Preserve inline HTML where Markdown falls short
2. Custom SCSS to match current styling exactly
3. JavaScript sidebar with search/resize features
4. Comprehensive redirect strategy for old URLs
5. Thorough testing with visual comparison

**Recommended approach:**

1. Start with Jekyll infrastructure setup
2. Convert a batch of 10-20 posts as proof of concept
3. Validate visual parity and functionality
4. Scale to full conversion with automation
5. Deploy with redirects from old URLs

---

## Appendix A: Sample Converted Post

### Original HTML (`0001_welcome.htm`)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>The Building Coder</title>
    <link rel="stylesheet" href="bc.css">
</head>
<body>
    <article>
        <h3>Welcome</h3>
        <p>Welcome to The Building Coder, a blog dedicated to programmers 
        working with the Revit API...</p>
    </article>
</body>
</html>
```

### Converted Markdown (`_posts/2008-09-22-welcome.md`)

```markdown
---
layout: post
title: "Welcome"
date: 2008-09-22
categories: [getting-started]
post_number: "0001"
permalink: /a/0001_welcome.html
redirect_from:
  - /a/0001_welcome.htm
---

Welcome to The Building Coder, a blog dedicated to programmers 
working with the Revit API...
```

---

## Appendix B: Complex HTML Preservation Example

Some posts contain HTML that must be preserved:

```markdown
---
layout: post
title: "DevCon 2025"
date: 2025-05-22
---

## Main Topic: Agents Using Data

[Amir Dezfouli](https://www.linkedin.com/in/amir-dezfouli-55a79b32/), 
CEO of [Bimlogiq](https://bimlogiq.com/), summarised the main technical topics:

> Raji Arasu shared a forward-looking vision: replacing traditional 
> add-ins with intelligent agents...

<!-- Complex HTML that Markdown can't represent -->
<center>
<img src="img/adskteam1.jpg" alt="Autodesk DevCon team" title="Autodesk DevCon team" width="500"/>
</center>

The team photo was taken after the closing session.
```
