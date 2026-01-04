# The Building Coder Archive - Blog Statistics

Last updated: January 5, 2026

## Archive Overview

| Metric | Count |
|--------|-------|
| Total post files | 2,079 |
| Post number range | 0001 - 2080 |
| Years covered | 2008 - 2026 |

### File Extensions

| Extension | Posts | Range |
|-----------|-------|-------|
| `.htm` | 1,350 | 0001 - 1350 |
| `.html` | 729 | 1351 - 2080 (except 1397) |
| **Total** | **2,079** | |

### Markdown Source Files

Posts 1351-2078 have corresponding `.md` source files in the `a/` directory.
These are the markdown sources used to generate the `.html` files.

| Type | Count | Notes |
|------|-------|-------|
| Post `.md` files | 728 | Posts 1351-2078 |
| Documentation `.md` files | 8 | Root-level docs |

*Note: Post 1397 exists only as `.md` (missing `.html` conversion)*

## Posts by Year

| Year | Posts | Notes |
|------|-------|-------|
| 2008 | 61 | Blog started August 2008 |
| 2009 | 212 | |
| 2010 | 233 | |
| 2011 | 191 | |
| 2012 | 178 | |
| 2013 | 207 | |
| 2014 | 181 | |
| 2015 | 126 | |
| 2016 | 121 | |
| 2017 | 104 | |
| 2018 | 98 | |
| 2019 | 96 | |
| 2020 | 73 | |
| 2021 | 52 | |
| 2022 | 43 | |
| 2023 | 45 | |
| 2024 | 40 | |
| 2025 | 18 | Through July 2025 |
| 2026 | 2 | Sample posts |
| **Total** | **~2,080** | |

## Navigation Data Files

### chrono-data.json (Chronological Navigation)

| Metric | Count | Coverage |
|--------|-------|----------|
| Posts indexed | 2,080 | ~100% |
| Years | 18 | 2008-2026 |

All existing posts are included in the chronological timeline.

*Note: Post 1397 is referenced but missing `.html` file*

### toc-data.json (Topic Navigation)

| Metric | Count |
|--------|-------|
| Topics | 57 |
| Subtopics | 3 |
| Posts in topics | 419 unique files |
| Topic coverage | 20% of all posts |

**Note**: Not all posts are categorized into topics. The topic structure comes from Section 5 of index.html, which only categorizes certain posts by subject matter.

#### Topic Coverage Breakdown

| Category | Count | Notes |
|----------|-------|-------|
| Posts categorized into topics | 419 | Included in toc-data.json |
| Posts NOT in any topic | ~1,660 | Only in chronological list |

## index.html Sections

| Section | Description | Post References |
|---------|-------------|-----------------|
| 0 | About Jeremy Tammik | 1 |
| 1 | Contact and Support | 0 |
| 2 | Getting Started | 9 |
| 3 | License | 0 |
| 4 | Disclaimer | 0 |
| 5 | **Topics** (subject-based) | 419 unique |
| 6 | **Chronological** (by date) | 2,080 |
| 7 | Footer | 0 |

## Verification

Run the comprehensive audit script to verify current statistics:

```bash
python scripts/comprehensive_audit.py
```

## History

- **2026-01-05**: Corrected statistics
  - Archive actually contains 2,079 posts (not 1,350)
  - Posts 1351-2080 exist as .html files
  - Fixed typos in index.html (1674, 1691, 1703, 1972, 1999, 2052)
  - Updated chrono-data.json and toc-data.json
  - 2 posts (1397, 2001) have broken references
