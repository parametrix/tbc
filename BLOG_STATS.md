# The Building Coder Archive - Blog Statistics

Last updated: January 5, 2026

## Archive Overview

| Metric | Count |
|--------|-------|
| Total posts in archive | 1,350 |
| Post number range | 0001 - 1350 |
| File extension | `.htm` |
| Years covered | 2008 - 2015 (Aug) |

## Posts by Year (In Archive)

| Year | Posts | Notes |
|------|-------|-------|
| 2008 | 61 | Blog started August 2008 |
| 2009 | 212 | |
| 2010 | 233 | |
| 2011 | 191 | |
| 2012 | 178 | |
| 2013 | 207 | |
| 2014 | 181 | |
| 2015 | 87 | Through August 21, 2015 |
| **Total** | **1,350** | |

## Posts NOT in Archive

The original Building Coder blog continues beyond this archive. The index.html references posts 1351-2080+ with `.html` extension that have not been migrated:

| Year | Posts | Status |
|------|-------|--------|
| 2015 (Sep-Dec) | 39 | NOT in archive |
| 2016 | 121 | NOT in archive |
| 2017 | 103 | NOT in archive |
| 2018 | 95 | NOT in archive |
| 2019 | 96 | NOT in archive |
| 2020 | 73 | NOT in archive |
| 2021 | 52 | NOT in archive |
| 2022 | 43 | NOT in archive |
| 2023 | 45 | NOT in archive |
| 2024 | 40 | NOT in archive |
| 2025 | 18 | NOT in archive |
| **Total** | **~725** | Posts 1351-2080 |

These posts are still available on the original WordPress blog at thebuildingcoder.typepad.com.

## Navigation Data Files

### chrono-data.json (Chronological Navigation)

| Metric | Count | Coverage |
|--------|-------|----------|
| Posts indexed | 1,350 | 100% |
| Years | 8 | 2008-2015 |

All 1,350 existing posts are included in the chronological timeline.

### toc-data.json (Topic Navigation)

| Metric | Count |
|--------|-------|
| Topics | 57 |
| Subtopics | 3 |
| Posts in topics | 338 unique files |
| Topic coverage | 25% of all posts |

**Note**: Not all posts are categorized into topics. The topic structure comes from Section 5 of index.html, which only categorizes certain posts by subject matter.

#### Topic Coverage Breakdown

| Category | Count | Notes |
|----------|-------|-------|
| Posts in topics (.htm, exist) | 338 | Included in toc-data.json |
| Posts in topics (.html, don't exist) | ~100 | Referenced but not in archive |
| Posts NOT in any topic | 1,012 | Only in chronological list |

## index.html Sections

| Section | Description | Post References |
|---------|-------------|-----------------|
| 0 | About Jeremy Tammik | 1 |
| 1 | Contact and Support | 0 |
| 2 | Getting Started | 9 |
| 3 | License | 0 |
| 4 | Disclaimer | 0 |
| 5 | **Topics** (subject-based) | 438 unique (338 exist) |
| 6 | **Chronological** (by date) | 2,077 (1,350 exist) |
| 7 | Footer | 0 |

## Verification

Run the audit script to verify current statistics:

```bash
python scripts/audit_posts.py
```

## History

- **2026-01-05**: Initial statistics documented
  - Fixed chrono-data.json (removed 731 non-existent entries)
  - Fixed toc-data.json extraction (now captures all nested lists)
  - Created audit_posts.py for ongoing verification
