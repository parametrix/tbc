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

- [OpenAI o3 and o4-mini](https://youtu.be/sq8GBPUb3rk) impress coders and scientists.
  Open AI Codex coding agent runs locally: [tweet](https://x.com/sama/status/1912558495997784441).
  Here's the quick low-down of 03 and 04mini by Dan Shipper:
  - It's agentic. Someone at OpenAI referred to o3 as deep research-lite to me, and that's exactly what it is. Set it to do a task, and come back in 30 seconds or three minutes and get a thorough answer. It can use tools like web search, code interpreter, reminders, and memory in a loop so you can have it code complex features, answer tricky research queries over long documents, or even build you a course that it reminds you to take every day.
  - It's fast. Speed is a dimension of intelligence. Maybe your model can unify physics, but if it doesn't happen in this lifetime I don't care. In my testing, o3 was consistently faster than Anthropic's and Google's frontline reasoning models (3.7
  Sonnet and Gemini 2.5 Pro, respectively) on this dimension. It feels smooth.
  - It's very smart. I don't have access to benchmarks as of this writing, but I fed it expert-level Sudoku problems and it solved them on the first try. Gemini 2.5 Pro and 3.7 Sonnet both failed.
  - It busts some old Chat GPT limitations. Because it's agentic, the old rules don't apply. You don't have to be as wary of web search because it doesn't summarize the first spam blog post it finds in a Google search. You can give it many files and expect coherent, complete answers —I had it read an entire book and outline it, for example. When you use it for coding it will automatically do multiple searches through the web to find up-to-date documentation, which cuts down errors a lot.
  Basically, it makes ChatGPT way more useful.
  - It's not as socially awkward as 01, and it's not a try-hard like 3.7 Sonnet. I found myself coding with it a lot this weekend, and I really liked it. It understands what you mean and does what it's told to at high quality. It doesn't plow ahead and try to build the Taj Mahal when you tell it to fix a bug, like Sonnet does. It also seems a little more vibe-y than other o-series models. It's more fun to talk to; not as good a writer as GPT 4.5 (RIP) or Sonnet 3.5, but still good.

- Super interesting statistical news on global AI development: [AI Index 2025: State of AI in 10 Charts](https://hai.stanford.edu/news/ai-index-2025-state-of-ai-in-10-charts)

- An interesting short article explaining how to handle challenges using AI for complex app coding: [Vibe coding considered harmful, Lego code instead](https://sundaylettersfromsam.substack.com/p/vibe-coding-considered-harmful-lego).

- A [prompting guide for GPT-4.1 models](https://platform.openai.com/docs/guides/text?api-mode=responses#prompting-gpt-4-1-models).
  While the cookbook has the best and most comprehensive guidance for prompting this model, here are a few best practices to keep in mind.
  - Building agentic workflows
  - Using long context
  - Prompting for chain of thought
  - Instruction following

- Demystifying the #! (shebang): Kernel Adventures
  https://crocidb.com/post/kernel-adventures/demystifying-the-shebang/

- Wall: attach top/base, no API?
  https://forums.autodesk.com/t5/revit-api-forum/wall-attach-top-base-no-api/m-p/13427160#M84749
  Wall.AddAttachment Method
  https://revapidocs.com/2026.htm?id=bef619ea-dede-2795-d767-04a464a997f0.htm
  https://www.revitapidocs.com/2026/bef619ea-dede-2795-d767-04a464a997f0.htm


twitter:

AEC, BIM and even Revit API AI usage growing widespread and useful, trends, challenges, agentic, MCP, VS Code and Codex for @AutodeskRevit #RevitAPI @AutodeskAPS #BIM @DynamoBIM https://thebuildingcoder.typepad.com/blog/2025/04/revit-api-agents-mcp-copilot-and-codex.html

AI is growing more widespread and useful in the AEC, BIM and even Revit API arena
&ndash; Global AI statistics and charts
&ndash; AI challenges for complex app coding
&ndash; What is agentic AI?
&ndash; MCP gaining traction
&ndash; MCP server for Fusion
&ndash; Revit MCP
&ndash; GPT prompting guide
&ndash; OpenAI o3, o4-mini and Codex
&ndash; M$ AI packages, VS Code and Codex
&ndash; Codex analyses Revit add-in
&ndash; Gemini ranks high
&ndash; Chef generates and launches full stack
&ndash; DeepWiki analyses all GitHub repos
&ndash; MarkItDown converts anything to MD
&ndash; Postmortem of a startup
&ndash; Demystifying shebang...

linkedin:

AEC, BIM and even Revit API AI usage growing widespread and useful, trends, challenges, agentic, MCP, VS Code and Codex for #RevitAPI

https://thebuildingcoder.typepad.com/blog/2025/04/revit-api-agents-mcp-copilot-and-codex.html

- Global AI statistics and charts
- AI challenges for complex app coding
- What is agentic AI?
- MCP gaining traction
- MCP server for Fusion
- Revit MCP
- GPT prompting guide
- OpenAI o3, o4-mini and Codex
- M$ AI packages, VS Code and Codex
- Codex analyses Revit add-in
- Gemini ranks high
- Chef generates and launches full stack
- DeepWiki analyses all GitHub repos
- MarkItDown converts anything to MD
- Postmortem of a startup
- Demystifying shebang...

#BIM #DynamoBIM #AutodeskAPS #Revit #API #IFC #SDK #Autodesk #AEC #adsk

the [Revit API discussion forum](http://forums.autodesk.com/t5/revit-api-forum/bd-p/160) thread

<center>
<img src="img/" alt="" title="" width="600"/>
<p style="font-size: 80%; font-style:italic"></p>
<a href="img/.gif"><p style="font-size: 80%; font-style:italic">Click for animation</p></a>
</center>

-->

### Revit API Agents, MCP, Copilot and Codex

We live in exciting times, and AI is growing more widespread and useful in the AEC, BIM and even Revit API arena.

I have used GitHub Copilot in VS Code for Revit API add-in coding and installed OpenAI Codex myself.

A long list of topics, many of them just short pointers, ranging through trends and statistics, agentic AI, MCP, new models and technologies,

- [Global AI statistics and charts](#2)
- [AI challenges for complex app coding](#3)
- [What is agentic AI?](#4)
- [MCP gaining traction](#5)
- [MCP server for Fusion](#6)
- [Revit MCP](#7)
- [GPT prompting guide](#8)
- [OpenAI o3, o4-mini and Codex](#9)
- [M$ AI packages, VS Code and Codex](#10)
- [Codex analyses Revit add-in](#11)
- [Gemini ranks high](#12)
- [Chef generates and launches full stack](#13)
- [DeepWiki analyses all GitHub repos](#14)
- [MarkItDown converts anything to MD](#15)
- [Postmortem of a startup](#16)
- [Demystifying shebang](#17)

####<a name="2"></a> Global AI Statistics and Charts

I found
the [AI Index 2025: State of AI in 10 Charts](https://hai.stanford.edu/news/ai-index-2025-state-of-ai-in-10-charts) presents
some very interesting statistical news on global AI development and trends.

####<a name="3"></a> AI Challenges for Complex App Coding

Looking critically at AI usage is also vital, like this article explaining how to handle challenges using AI for complex app coding:
[Vibe coding considered harmful, Lego code instead](https://sundaylettersfromsam.substack.com/p/vibe-coding-considered-harmful-lego).

####<a name="4"></a> What is Agentic AI?

A nice comparison of generative versus agentic AI is presented answering
[Wait, what is agentic AI?](https://stackoverflow.blog/2025/04/17/wait-what-is-agentic-ai/?utm_source=braze&utm_medium=email&utm_campaign=the-overflow-newsletter&lid=1saaj6iiq6rt):

> Simply put: Generative AI creates content; agentic AI solves problems on a user’s behalf.

- Agentic AI is focused on making decisions, not generating content.
- Rather than responding to human prompts like generative AI systems do, agentic AI systems are set to work toward specific goals like maximizing efficiency, boosting customer satisfaction, or increasing sales.
- AI agents can carry out complex sequences of tasks in furtherance of their goals.

####<a name="5"></a> MCP Gaining Traction

The MCP (Model Context Protocol) adoption is gaining significant traction, and it’s increasingly being integrated with A2A (Agent-to-Agent) communication, cf., MCP measured in GitHub stars and A2A interaction:

<center>
<img src="img/2025-04-22_mcp_github_stars.png" alt="MCP GitHub stars" title="MCP GitHub stars" width="600"/> <!-- 1922 -->
</center>

<center>
<img src="img/2025-04-22_a2a_interaction.png" alt="A2A interaction" title="A2A interaction" width="600"/> <!-- 1832 -->
</center>

####<a name="6"></a> MCP Server for Fusion

A Fusion user has implemented an MCP server for Fusion using the M$ Semantic Workbench:

- [Semantic Workbench](https://github.com/microsoft/semanticworkbench)
- [MCP servers](https://github.com/microsoft/semanticworkbench/tree/main/mcp-servers)
- [Fusion MCP server](https://github.com/microsoft/semanticworkbench/tree/main/mcp-servers/mcp-server-fusion)

Semantic Workbench is a versatile tool designed to help prototype intelligent assistants quickly.
It supports the creation of new assistants or the integration of existing ones, all within a cohesive interface.
The workbench provides a user-friendly UI for creating conversations with one or more assistants, configuring settings, and exposing various behaviours.

The Semantic Workbench is composed of three main components:

- Workbench Service (Python): The backend service that handles core functionalities.
- Workbench App (React/Typescript): The frontend web user interface for interacting with workbench and assistants.
- Assistant Services (Python, C#, etc.): any number of assistant services that implement the service protocols/APIs, developed using any framework and programming language of your choice.

Designed to be agnostic of any agent framework, language, or platform, the Semantic Workbench facilitates experimentation, development, testing, and measurement of agent behaviors and workflows. Assistants integrate with the workbench via a RESTful API, allowing for flexibility and broad applicability in various development environments.  The Fusion MCP server can work seamlessly with the Claude MCP client.  We can simply ask Claude to generate 3D models, and it does so automatically in Fusion by utilizing these MCP tools.  The MCP client can utilise basic tools to create 3D models. Its capabilities can be expanded by developing additional tools and providing comprehensive Python API documentation as a resource for the MCP server. The fusion server available is open source and can be simply setup on the machine.  The different MCPs are implemented by different independent engineers, e.g., the Fusion one is by a Fusion user! Great to see the potential power of MCP for such a complex UI as Fusion. MCP achieves things that otherwise would have taken months of learning for a newbie. This may remove the learning curve for using any of the design software in this space and thus anyone can move to any other software as well. Looks like one of the reasons for sticking to one software is taken away for good. This essentially commoditises all CAD software. Given the goal of MCP of becoming something of a "natural language USB for software", the need for traditional UX diminishes for a large proportion of users. Will this also hold true for power users?

####<a name="7"></a> Revit MCP

The [revit-mcp GitHub organisation](https://github.com/revit-mcp) provides
a framework that implements the MCP protocol based on Autodesk Revit software.
It enables AI conversation clients compatible with the MCP protocol to drive Revit.
Example and the three main project components:

- [ColorSplash](https://youtu.be/mUJGSjQHBm8) example
- [revit-mcp](https://github.com/revit-mcp/revit-mcp): Connects with AI conversation clients. Responsible for providing executable functions to the AI conversation client and communicating with Revit.
- [revit-mcp-plugin](https://github.com/revit-mcp/revit-mcp-plugin): This is a Revit plugin used to receive AI commands, load command sets, and execute specific functions.
- [revit-mcp-commandset](https://github.com/revit-mcp/revit-mcp-commandset): Command sets are actual executable commands wrapped based on Revit external events. Developers can add functionality to the command set or customize their own work sets.

####<a name="8"></a> GPT Prompting Guide

You may find
the [prompting guide for GPT-4.1 models](https://platform.openai.com/docs/guides/text?api-mode=responses#prompting-gpt-4-1-models) useful.
While the cookbook provides a comprehensive guidance for prompting this model, this guide shares a few best practices to keep in mind in the following areas:

- Building agentic workflows
- Using long context
- Prompting for chain of thought
- Instruction following

####<a name="9"></a> OpenAI o3, o4-mini and Codex

[OpenAI o3 and o4-mini](https://youtu.be/sq8GBPUb3rk) impress coders and scientists.
Open AI Codex coding agent runs locally: [tweet](https://x.com/sama/status/1912558495997784441).
Here's the quick low-down of 03 and 04mini by Dan Shipper:

- It's agentic. Someone at OpenAI referred to o3 as deep research-lite to me, and that's exactly what it is. Set it to do a task, and come back in 30 seconds or three minutes and get a thorough answer. It can use tools like web search, code interpreter, reminders, and memory in a loop so you can have it code complex features, answer tricky research queries over long documents, or even build you a course that it reminds you to take every day.
- It's fast. Speed is a dimension of intelligence. Maybe your model can unify physics, but if it doesn't happen in this lifetime I don't care. In my testing, o3 was consistently faster than Anthropic's and Google's frontline reasoning models (3.7 Sonnet and Gemini 2.5 Pro, respectively) on this dimension. It feels smooth.
- It's very smart. I don't have access to benchmarks as of this writing, but I fed it expert-level Sudoku problems and it solved them on the first try. Gemini 2.5 Pro and 3.7 Sonnet both failed.
- It busts some old Chat GPT limitations. Because it's agentic, the old rules don't apply. You don't have to be as wary of web search because it doesn't summarize the first spam blog post it finds in a Google search. You can give it many files and expect coherent, complete answers —I had it read an entire book and outline it, for example. When you use it for coding it will automatically do multiple searches through the web to find up-to-date documentation, which cuts down errors a lot.

Basically, it makes ChatGPT way more useful.

- It's not as socially awkward as 01, and it's not a try-hard like 3.7 Sonnet. I found myself coding with it a lot this weekend, and I really liked it. It understands what you mean and does what it's told to at high quality. It doesn't plow ahead and try to build the Taj Mahal when you tell it to fix a bug, like Sonnet does. It also seems a little more vibe-y than other o-series models. It's more fun to talk to; not as good a writer as GPT 4.5 (RIP) or Sonnet 3.5, but still good.

####<a name="10"></a> M$ AI Packages, VS Code and Codex

Roman [@Nice3point](https://t.me/nice3point) Karpovich ([LinkedIn](https://www.linkedin.com/in/nice3point/)), aka Роман Карпович,
principal contributor and maintainer of RevitLookup,
[commented on the last post](https://www.linkedin.com/feed/update/urn:li:activity:7318574255611236353?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7318574255611236353%2C7318581431536959489%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287318581431536959489%2Curn%3Ali%3Aactivity%3A7318574255611236353%29)
discussing [intersection result, LLM for IFC and more AI](https://thebuildingcoder.typepad.com/blog/2025/04/intersection-result-llm-for-ifc-and-more-ai.html),
saying:

Microsoft has already prepared great packages for AI, and they can already be used in C#, with just a couple of lines of code:

- [Artificial intelligence in .NET](https://learn.microsoft.com/en-us/dotnet/core/extensions/artificial-intelligence?tabs=dotnet-cli)
- [Build a Model Context Protocol (MCP) server in C#](https://devblogs.microsoft.com/dotnet/build-a-model-context-protocol-mcp-server-in-csharp/)

####<a name="11"></a> Codex Analyses Revit Add-In

In the past weeks, I installed Visual Studio Code on MacOS, with GitHub Copilot integrated, and used that for some Revit API work with impressive results.

I installed OpenAI Codex and asked it to explain the purpose of my current Revit API code WIP.
I provided one single prompt, six words:

- "please explain what this application does"

Here is the answer it provided right out of the box:

This is a small C# /.NET add‑in for Autodesk Revit (a “Revit plug‑in”) whose goal is to let you take an existing plumbing (or HVAC) distribution network in your model—pipes, fittings (elbows, tees, reducers, etc.) and even ducts—and make a full copy of it, displaced to one side. Under the hood it does four main things:

- Ribbon integration
  &ndash; On startup, it adds an “HVAC System Tools” tab with buttons for
    - “Find Root Node” (identify the “start” of any piping system)
    - “Duplicate Pipe System”
    - “Duplicate Duct System”
    - (There is also a “Rolling Offset” command for auto‑calculating and inserting a two‑pipe offset with 45° bends.)

- Graph‑based network traversal
  &ndash; Before duplicating, it walks your existing system and builds a little graph of “nodes” (every pipe segment or fitting) and their “connectors” (endpoints), capturing for each:
    - Its element id and type (pipe vs. fitting vs. duct)
    - Its geometric transform (location, orientation, rotation)
    - All the connector points (and which other element they’re linked to)
    - Any important parameters (diameter, width/height, family parameters on reducers, etc.)

- Duplication at offset
  &ndash; In a single TransactionGroup it:
    - Starts a transaction and creates a copy of every pipe/duct segment at a fixed offset (e.g. +30 ft in X) using the same system type, level, curve endpoints and size parameters.
    - Places new family instances for each fitting at the corresponding translated origin, applies the same symbol, size parameters and re‑rotates them so their connector axes line up.
    - Commits that transaction.

- Re‑connecting the network
  &ndash; In a second transaction it revisits every new node, finds on each its closest connector on a neighboring new element (using a tiny distance‑threshold test) and calls the Revit API “ConnectTo” to wire them back up in exactly the same topology as the original.

Beyond pure duplication, there are also commands to:

- Find and report the “root” element of any PipingSystem (CmdRootFinder + PipeSystemRootFinder).
- Analyze/traverse a piping system and export its graph to disk (PipingSystemAnalyzer → text file).
- Re‑create a piping system from that file (PipeSystemRecreator).
- Compute and insert a two‑pipe rolling offset (CmdRollingOffset), optionally with real fittings or just a model line.

All of this is built on small data classes &ndash; NodeData, ConnectorData, ParamData &ndash; to snapshot each element’s geometry, connectivity and parameters, plus a few utility routines (in Util.cs) to find connectors, compare points, and manage the various Revit API quirks.

####<a name="12"></a> Gemini Ranks High

Currently Gemini is ahead as "best AI", even in the [OpenAI listing](https://x.com/SaiNemani1/status/1915737273787707809/photo/1).

####<a name="13"></a> Chef Generates and Launches Full Stack

[Chef](https://chef.convex.dev/) by Convex generates full‑stack apps and launches them in realtime.

####<a name="14"></a> DeepWiki Analyses All GitHub Repos

[DeepWiki](https://deepwiki.com/) indexes
and documents all GitHub repos:
Cognition, maker of [Devin](https://devin.ai/),
recently announced DeepWiki as a free encyclopeadia of all GitHub repos.
You can replace any public GitHub repo url with:

- [https://deepwiki.com/org/repo](#14)

That will produce a remarkably accurate Wikipedia-like description of the library as well as a Devin-backed chatbot on how to use it.

####<a name="15"></a> MarkItDown Converts Anything to MD

For more limited document analysis, Microsoft released
[MarkItDown](https://github.com/microsoft/markitdown),
an MCP-integrated LLM tool to convert anything to Markdown.

####<a name="16"></a> Postmortem of a Startup

Are you thinking of starting up something yourself?
In that case, you might discover some useful hints up front in
[a postmortem of a startup](https://buildwithtract.com/?lid=hqbe3uwdig4y).

####<a name="17"></a> Demystifying Shebang

Finally, for Unix aficionados, this article discussed an interesting topic that is completely unrelated to AI,
[demystifying the \#\! (shebang)](https://crocidb.com/post/kernel-adventures/demystifying-the-shebang/)

