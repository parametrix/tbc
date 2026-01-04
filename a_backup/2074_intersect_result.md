<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<link rel="stylesheet" type="text/css" href="bc.css">

<!--
https://prismjs.com
<pre><code class="language-cs">
-->
<link href="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/themes/prism.min.css" rel="stylesheet" />
<script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-core.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
<style> code[class*=language-], pre[class*=language-] { font-size : 90%; } </style>

</head>

<!--

- IntersectionResult parameter getter throws an InvalidOperationException
  https://forums.autodesk.com/t5/revit-api-forum/intersectionresult-parameter-getter-throws-an/m-p/13400449#M84547

- New training approach? *Iterated Distillation and Amplification (IDA)* - a scalable and efficient alignment strategy for general superintelligence using iterative self-improvement... to surpass the intelligence of whoever is training it, i.e., humans: [Cogito v1 Preview -- Introducing IDA as a path to general superintelligence](https://www.deepcogito.com/research/cogito-v1-preview).

- A scientific paper on [Artificial Intelligence for Software Architecture: Literature Review and the Road Ahead](https://arxiv.org/abs/2504.04334).

- Here is a nice [6-minute dystopian charade of vibe coding video](https://youtu.be/JeNS1ZNHQs8).

- The Slow Collapse of Critical Thinking in OSINT due to AI
  https://www.dutchosintguy.com/post/the-slow-collapse-of-critical-thinking-in-osint-due-to-ai
  Open-source intelligence
  https://en.wikipedia.org/wiki/Open-source_intelligence

- OpenAI GPT 4.1 + mini + nano for developers: https://x.com/OpenAI/status/1911824315194192187 (edited)

- Dmytro Vakulenko
  https://dmytro-prototypes.net/
  Freelance Software Developer | Azure, .NET, Python, Typescript, AI | Transforming ideas into innovative and evolutionary solutions
  https://www.linkedin.com/in/ACoAAAirTFIB2JAw2fqoQYvyf0VqS_AaPvUHf3k
  I've been following your work for years and have noticed lately your interest in showcasing unique LLM integrations into CAD/BIM products.
  I wanted to share a couple of projects I’ve been developing, and I'm curious if they might resonate with you:
  1) Open-Source LLM Integration for AutoCAD:
  This project focuses on generating AutoCAD scripts through an iterative process that continues looping until the script is fully compilable/fixed.
  A standout feature is the use of reflection to provide additional insights about classes and methods—truly the “cherry on the top of the cake.”
  https://www.linkedin.com/posts/dmytro-vakulenko-software_scripture-demo-llm-based-autocad-automation-activity-7248239069292294144-pj2i
  2) LLM Querying (and Editing) Data in IFC Files:
  In this project, the chatbot not only retrieves information from IFC files but also generates and executes Python code to interact with them dynamically, tailoring responses in real time based on the data.
  https://www.linkedin.com/posts/dmytro-vakulenko-software_innovation-ifc-ai-agent-variables-activity-7285951367746080768-DIlr
  (and my other posts)
  I would be honored if you could take a look and share your thoughts.
  Your perspective would be invaluable, and I’m excited about the potential to contribute to the ongoing discussion surrounding LLM integrations in the CAD/CAE space.
  Thank you very much for your time and consideration.
  Best regards,
  Dmytro

- A2A
  Google announced the [A2A agent-to-agent protocol](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/) including support for MCP.

  developers.googleblog.comdevelopers.googleblog.com
  Announcing the Agent2Agent Protocol (A2A)- Google Developers Blog
  Explore A2A, Google's new open protocol empowering developers to build interoperable AI solutions. (364 kB)
  https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/
  [A2A is also included in Visual Studio](https://code.visualstudio.com/blogs/2025/04/07/agentMode.
  Agent mode is great for scenarios where:
  Your task involves multiple steps. The agent edits code, runs terminal commands, monitors for errors, and iterates to resolve any issues that arise.
  You are unsure about the scope of the changes. The agent automatically determines the relevant files and context.
  Your task requires interaction with external apps or data. The agent integrates with MCP servers and VS Code extensions.

twitter:

@AutodeskRevit #RevitAPI curve intersection, LLM interaction with AutoCAD and IFC, GPT 4.1, mini, nano and more AI-related news @AutodeskAPS #BIM @DynamoBIM https://thebuildingcoder.typepad.com/blog/2025/04/intersection-result-llm-for-ifc-and-more-ai.html

Revit API curve intersection, LLMs interaction with AutoCAD and IFC, and more AI-related news
&ndash; IntersectionResult properties
&ndash; LLM interaction with AutoCAD and IFC
&ndash; AI literature and roadmap
&ndash; Vibe coding parody
&ndash; Collapse of critical thinking
&ndash; IDA iterated distillation and amplification training
&ndash; A2A agent-to-agent protocol
&ndash; OpenAI GPT 4.1 + mini + nano...

linkedin:

#RevitAPI curve intersection, LLM interaction with AutoCAD and IFC, GPT 4.1, mini, nano and more AI-related news

https://thebuildingcoder.typepad.com/blog/2025/04/intersection-result-llm-for-ifc-and-more-ai.html

- IntersectionResult properties
- LLM interaction with AutoCAD and IFC
- AI literature and roadmap
- Vibe coding parody
- Collapse of critical thinking
- IDA iterated distillation and amplification training
- A2A agent-to-agent protocol
- OpenAI GPT 4.1 + mini + nano...

#BIM #DynamoBIM #AutodeskAPS #Revit #API #IFC #SDK #Autodesk #AEC #adsk

the [Revit API discussion forum](http://forums.autodesk.com/t5/revit-api-forum/bd-p/160) thread

<center>
<img src="img/" alt="" title="" width="600"/>
<p style="font-size: 80%; font-style:italic"></p>
<a href="img/.gif"><p style="font-size: 80%; font-style:italic">Click for animation</p></a>
</center>

-->

### Intersection Result, LLM for IFC and More AI

Today, we highlight one pure Revit API related topic, LLMs interacting with AutoCAD and IFC, and lots more AI-related news snippets:

- [IntersectionResult properties](#2)
- [LLM interaction with AutoCAD and IFC](#3)
- [AI literature and roadmap](#4)
- [Vibe coding parody](#5)
- [Collapse of critical thinking](#6)
- [IDA iterated distillation and amplification training](#7)
- [A2A agent-to-agent protocol](#8)
- [OpenAI GPT 4.1 + mini + nano](#9)

####<a name="2"></a> IntersectionResult Properties

The Revit API  [Curve Intersect method](https://www.revitapidocs.com/2026/570fb842-cac3-83f5-1ab9-621e55186ead.htm) sports
some quirks that prompted explanations in the past.
Another one is discussed in the explanation
why [IntersectionResult parameter getter throws an InvalidOperationException](https://forums.autodesk.com/t5/revit-api-forum/intersectionresult-parameter-getter-throws-an/m-p/13400449#M84547):

**Question:** I check the intersection of 2 line elements.
I know for a fact that these 2 lines intersect:

<pre><code class="language-cs">SetComparisonResult result = line1.Intersect(line2, out resultArray);</code></pre>

It's all nice and fine at this point, since the result and resultArray are not null.
I can get the IntersectionResult out of the IntersectionResultArray for example by:

<pre><code class="language-cs">IntersectionResult intResult = resultArray.get_Item(0);</code></pre>

I'm intersected in the [IntersectionResult.Parameter property](https://apidocs.co/apps/revit/2024/5ca02b0e-289a-f1ef-7ce2-8b3f175fe402.htm#).
When I try to read the value of this parameter, an InvalidOperationException is thrown.
Checking the Parameter property documentation, it claims that it happens when it has not been set yet "Thrown in the getter when this property has not been set by the method providing the result."
Checking this Parameter property in the debugger reveals that it's not the only one failing.
`Distance`, `EdgeObject`, `EdgeParameter` and `Parameter` all fail with `InvalidOperationException`.
This issue occurred to me in a C# addin in all current version versions (22-25).
For testing purposes, I created the following Python script that you can paste into RevitPytonShell.
It results is the same error across all versions.

<pre><code class="language-py">results = clr.Reference[DB.IntersectionResultArray]()

t = DB.Transaction(doc, "Line Creation")
t.Start()

lineV = DB.Line.CreateBound(DB.XYZ(0,0,0), DB.XYZ(0,10,0))
lineH = DB.Line.CreateBound(DB.XYZ(-5,5,0), DB.XYZ(5,5,0))

doc.Create.NewDetailCurve(uidoc.ActiveView, lineV)
doc.Create.NewDetailCurve(uidoc.ActiveView, lineH)

result = lineV.Intersect(lineH, results)

intResult = results.get_Item(0)
# For example this works
print("XYZPoint: {}".format(intResult.XYZPoint))
# But the following all fail
print("Distance: {}".format(intResult.Distance))
print("EdgeObject: {}".format(intResult.EdgeObject))
print("EdgeParameter: {}".format(intResult.EdgeParameter))
print("Parameter: {}".format(intResult.Parameter))

t.Commit()</code></pre>

Even outside of a Transaction (since Line creation and Line.Intersect does not require that), the results are the same:

<pre><code class="language-py">results = clr.Reference[DB.IntersectionResultArray]()

lineV = DB.Line.CreateBound(DB.XYZ(0,0,0), DB.XYZ(0,10,0))
lineH = DB.Line.CreateBound(DB.XYZ(-5,5,0), DB.XYZ(5,5,0))
result = lineV.Intersect(lineH, results)

intResult = results.get_Item(0)
# For example this works
print("XYZPoint: {}".format(intResult.XYZPoint))
# But the following all fail
print("Distance: {}".format(intResult.Distance))
print("EdgeObject: {}".format(intResult.EdgeObject))
print("EdgeParameter: {}".format(intResult.EdgeParameter))
print("Parameter: {}".format(intResult.Parameter))</code></pre>

**Answer:**
The `Curve.Intersect` method does not set the IntersectionResult Parameter property.
Look at the [Curve.Intersect documentation](https://apidocs.co/apps/revit/2026/51961478-fb36-e00b-2d1b-7db27b0a09e6.htm#) to
see which properties are set and what they mean.
The IntersectionResult `Parameter` and `Distance` properties are both set by the `Curve.Project` method.
IntersectionResult is used to return results for several different geometric methods.


####<a name="3"></a> LLM Interaction with AutoCAD and IFC

[Dmytro Vakulenko](https://dmytro-prototypes.net/) shared two AI- though not directly Revit-related projects that may be of interest here,
an [AutoCAD LLM integration](https://www.linkedin.com/posts/dmytro-vakulenko-software_scripture-demo-llm-based-autocad-automation-activity-7248239069292294144-pj2i) and
an [IFC AI agent](https://www.linkedin.com/posts/dmytro-vakulenko-software_ifc-ai-agent-demo-httpsifcaiagentazurewebsitesnet-activity-7268254935761182721-Gft0?utm_source=share).

The first is [Scripture](https://github.com/dimitrovakulenko/Scripture),
an open-source LLM Integration for AutoCAD:
It generates AutoCAD scripts on the fly in an iterative process that continues looping until the script is fully compiled and all errors fixed.
A standout feature is the use of reflection to provide additional insights about classes and methods &ndash; truly the “cherry on the top of the cake.”

- [1-minute demo video](https://youtu.be/7I88PcwZQQk)
- [Scripture GitHub repository](https://github.com/dimitrovakulenko/Scripture)

<center>
<img src="img/dv_scripture.png" alt="Scripture" title="Scripture" width="800"/> <!-- 1200 -->
</center>

Further, the [IFC AI Agent](https://ifc-ai-agent.dmytro-prototypes.net/login) is
an LLM querying and editing data in IFC Files:
In this project, the chatbot not only retrieves information from IFC files but also generates and executes Python code to interact with them dynamically, tailoring responses in real time based on the data.
A decades-old concept reimagined for modern AI!
working with large-scale IFC files &ndash; often gigabytes in size &ndash; poses a challenge: LLMs often can’t fit results into their limited-size context.
The latest innovation in IFC AI Agent addresses this with variables &ndash; a simple yet powerful concept that’s been at the core of software development for decades.

Here’s how it works:

- The AI Agent has a bucket of variables it knows by name.
- For variables with simple values, it knows their exact content.
- When variables holding large datasets, it intelligently works with samples to maintain efficiency while keeping calculations precise.

This approach brings smart data management to AI, enabling seamless interactions with large-scale IFC files.

- [1-minute video](https://youtu.be/fFPVTTtDyTw)
- [IFC AI Agent to try out yourself](https://ifc-ai-agent.dmytro-prototypes.net/login)

For example, ask questions like "List all windows with their dimensions", or ask to modify, e.g., "Move all walls on the ground floor in (1,1,0) direction by 1000 units."  This is an ongoing chat. You can also ask how your data was received, modified, or request further details.

Dmytro also [shares](https://www.linkedin.com/posts/dmytro-vakulenko-software_github-dimitrovakulenkosimpleifcaiagentwithgraphrag-activity-7287741565437898752-Aey9)
the [simple IFC AI agent with GraphRAG](https://github.com/dimitrovakulenko/simpleIfcAIAgentWithGraphRAG) project,
a minimalistic project designed to showcase a simple AI agent that extracts data from an IFC file stored in a graph database (Neo4j). The project demonstrates the integration of AI, IFC file processing, and graph-based data storage and retrieval using modern tools such as Neo4j, LangGraph, and Azure GPT.

Many thanks to Dmytro for pointing these out!

####<a name="4"></a> AI Literature and Roadmap

Looking at the future of AI-driven software architecture, here is a scientific paper
on [Artificial Intelligence for Software Architecture: Literature Review and the Road Ahead](https://arxiv.org/abs/2504.04334).

####<a name="5"></a> Vibe Coding Parody

For an example of how not to approach such a task, you may enjoy
this [6-minute dystopian parody of vibe coding video](https://youtu.be/JeNS1ZNHQs8).

####<a name="6"></a> Collapse of Critical Thinking

In a more serious vein, one can already start observing
[the slow collapse of critical thinking in OSINT due to AI](https://www.dutchosintguy.com/post/the-slow-collapse-of-critical-thinking-in-osint-due-to-ai).
In case you wonder &ndash; as I did &ndash; about the acronym, it stands
for [open-source intelligence](https://en.wikipedia.org/wiki/Open-source_intelligence).

####<a name="7"></a> IDA Iterated Distillation and Amplification Training

A new LLM training approach aims to provide a scalable and efficient alignment strategy for general superintelligence using iterative self-improvement in order to surpass the intelligence of whoever is training it, e.g., us human beings:
[Cogito v1 preview &ndash; introducing IDA as a path to general superintelligence](https://www.deepcogito.com/research/cogito-v1-preview).

####<a name="8"></a> A2A Agent-to-Agent Protocol

Last week, Google announced the [A2A agent-to-agent protocol](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)
an open protocol for building interoperable AI solutions including support for MCP.
[A2A is also included in Visual Studio](https://code.visualstudio.com/blogs/2025/04/07/agentMode).
Agent mode is intended for scenarios where:

- Your task involves multiple steps. The agent edits code, runs terminal commands, monitors for errors, and iterates to resolve any issues that arise.
- You are unsure about the scope of the changes. The agent automatically determines the relevant files and context.
- Your task requires interaction with external apps or data. The agent integrates with MCP servers and VS Code extensions.

####<a name="9"></a> OpenAI GPT 4.1 + Mini + Nano

Finally, just yesterday, OpenAI announced
[GPT 4.1 + mini + nano for developers](https://x.com/OpenAI/status/1911824315194192187).
