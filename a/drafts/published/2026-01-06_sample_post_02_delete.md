---
title: "Sample Post Title 02  DELETE"
date: 2026-01-06
categories: [Revit API, Getting Started]
tags: [sample, template, tutorial]
---

### Sample Post Title

This is a sample blog post demonstrating the Markdown format for The Building Coder.

- [Introduction](#2)
- [Code Example](#3)
- [Images](#4)
- [Conclusion](#5)

#### <a name="2"></a> Introduction

Welcome to this sample post. Replace this content with your own article.

You can write paragraphs of text explaining Revit API concepts, share code samples, 
and include images to illustrate your points.

#### <a name="3"></a> Code Example

Here's an example of C# code with syntax highlighting:

```csharp
public Result Execute(
    ExternalCommandData commandData,
    ref string message,
    ElementSet elements)
{
    UIApplication uiapp = commandData.Application;
    UIDocument uidoc = uiapp.ActiveUIDocument;
    Document doc = uidoc.Document;
    
    // Get all walls in the document
    FilteredElementCollector collector 
        = new FilteredElementCollector(doc);
    
    ICollection<Element> walls 
        = collector.OfClass(typeof(Wall)).ToElements();
    
    TaskDialog.Show("Wall Count", 
        $"Found {walls.Count} walls in the document.");
    
    return Result.Succeeded;
}
```

You can also include Python code:

```python
import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

# Get all walls
walls = FilteredElementCollector(doc).OfClass(Wall).ToElements()
print(f"Found {len(walls)} walls")
```

#### <a name="4"></a> Images

Include images from the `img/` folder:

<center>
<img src="img/your_image.png" alt="Description" title="Title" width="500"/>
<p style="font-size: 80%; font-style:italic">Caption describing the image</p>
</center>

#### <a name="5"></a> Conclusion

Summarize your key points here.

For more information, see:
- [The Revit API documentation](https://www.revitapidocs.com)
- [Previous related post](0001_welcome.htm)

Feel free to reach out with questions in the comments!
