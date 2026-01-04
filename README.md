# tbc &ndash; The Building Coder blog source

Source and chronological index for [The Building Coder](http://thebuildingcoder.typepad.com) Revit API blog.

The repository hosts all the HTML, CSS and markdown source text for The Building Coder.

It also boasts a complete index of all posts.

## Offline Local Hosting

This fork has been modified for **fully offline local hosting**. All internal Typepad links have been converted to point to local files, allowing you to browse the entire blog archive without an internet connection.

### Changes Made

- **13,500+ internal links** converted from Typepad URLs to local file paths
- **2,066 HTML fragments** wrapped with proper document structure (`<html>`, `<head>`, `<body>`)
- **640+ unavailable resources** (old file downloads, category pages) converted to text with notes
- **CSS fix** for proper code block formatting with preserved indentation
- **Backup** of original files stored in `a_backup/`

### Running Locally

1. Start a local HTTP server from the repository root:
   ```bash
   python -m http.server 9000 --directory .
   ```

2. Open your browser to: http://localhost:9000/a/index.html

3. Browse the complete blog archive offline with all internal links working.

### Original Repository

The original repository is available at: https://github.com/jeremytammik/tbc

Each index entry includes a pointer to both the local source HTML or MD markdown and the official, global, Typepad-hosted blog entry.

You can download this repository to your local system to perform your own global text search or ensure offline access.

Please let me know if you discover any issues with this.

Thank you!

Enjoy.

For more background information, here are two articles on
publishing [The Building Coder source and index on GitHub](http://thebuildingcoder.typepad.com/blog/2016/02/tbc-the-building-coder-source-and-index-on-github.html)
and [hosting The 3D Web Coder source HTML and index on GitHub pages](http://the3dwebcoder.typepad.com/blog/2015/03/hosting-a-node-server-on-heroku-pages-and-3d-web.html#2).


## Author

Jeremy Tammik,
[The Building Coder](http://thebuildingcoder.typepad.com) and
[The 3D Web Coder](http://the3dwebcoder.typepad.com),
[ADN](http://www.autodesk.com/adn)
[Open](http://www.autodesk.com/adnopen),
[Autodesk Inc.](http://www.autodesk.com)

## Offline Hosting Modifications

Modifications for offline hosting by parametrix, January 2026.

## License

This sample is licensed under the terms of the [MIT License](http://opensource.org/licenses/MIT). Please see the [LICENSE](LICENSE) file for full details.

