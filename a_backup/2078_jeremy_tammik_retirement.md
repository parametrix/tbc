Jeremy's Retirement, Continuation of the Blog, Revit SDK 2026.2
July 25, 2025

By [Pedro Nadal](https://adndevblog.typepad.com/aec/pedro-nadal.html)

* [Jeremy's Retirement and continuation of the Blog](#section1)
* [Revit 2026.2 SDK release](#section2)
* [API additions](#section3)
* [CefSharp Removal](#section4)

**Jeremy's Retirement and continuation of the Blog**

After almost 17 years at the forefront of the Revit developer community, Jeremy Tammik has officially stepped into retirement.

For many in the AEC and developer space, The Building Coder has been more than just a blog — it has been a beacon of clarity, consistency, and generosity. Jeremy’s deep expertise, tireless dedication, and ability to make even the most complex Revit API topics approachable have left a lasting impact on thousands of developers, partners, and colleagues around the world.

Although Jeremy is now enjoying a well-earned retirement, we’re happy to share that he is going to remain as an occasional contributor to the blog. His voice and insights are always welcome, and we look forward to hearing from him again in future posts.

Going forward, the Developer Advocacy and Support team will join the authorship of The Building Coder. While we all know that no single person can truly fill Jeremy’s shoes, we as a team are committed to continuing the blog in the same spirit of openness, technical excellence, and community support that he so thoughtfully fostered.

Thank you, Jeremy, for everything you’ve built — not just in terms of code and content, but in community.

**Revit 2026.2 SDK release**

Alongside the [recent release of Revit 2026.2](https://www.autodesk.com/blogs/aec/2025/07/09/whats-new-in-revit-2026-2-residential-content-and-productivity-enhancements/), which introduced enhancements in residential modeling, content usability, and productivity tools, Autodesk has also published the Revit 2026.6 SDK update.

You can review the full list of Revit improvements in the [official Revit 2026.2 release notes](https://help.autodesk.com/view/RVT/2026/ENU/?guid=RevitReleaseNotes_2026updates_2026_2_html).

The latest Revit SDK version is available for download at: [aps.autodesk.com/developer/overview/revit](https://aps.autodesk.com/developer/overview/revit)  
or direct download link: [Revit 2026.2 SDK](https://autodesk-adn-transfer.s3.us-west-2.amazonaws.com/ADN+Extranet/Revit/REVIT_2026_2_SDK.msi)

**API Additions**

**Add-In Manager: Grouping Add-ins in the UI**

A small but useful improvement has been introduced in the **RevitAddInUtility** API to help better organize your tools inside Revit’s Add-In Manager.

A new optional flag called:

```
RevitAddInManifestSettings.UnifyInAddInManager
```

allows developers to **group multiple AddIn entries into a single line** in both the Add-Ins Manager and Admin Add-Ins Manager UI.

If you have several external commands or applications defined in the same manifest file, enabling this flag can simplify the user interface by presenting them as a single item, avoiding clutter and potential confusion.

**Sample manifest with grouping enabled:**

```
<?xml version="1.0" encoding="utf-8"?>
<RevitAddIns>
  <AddIn Type="DBApplication">
    <Name>SampleApplication</Name>
    <FullClassName>SampleApplication.Application</FullClassName>
    <Assembly>SampleApplication.dll</Assembly>
    <ClientId>C96B32A3-98C6-4B47-99DA-562E64689C6F</ClientId>
    <VendorId>Autodesk</VendorId>
  </AddIn>
  <ManifestSettings>
    <UnifyInAddInManager>True</UnifyInAddInManager>
  </ManifestSettings>
</RevitAddIns>
```

When this setting is enabled (True), users won’t be able to toggle individual commands on/off; the entire group is managed as a single unit.

**MEP API: Resetting Fabrication Assembly Types**

In Revit 2026.2, a change was made to how **FabricationPart** elements are organized within **assembly types**.

Originally, in Revit 2026 RTM, multiple fabrication parts could share the same assembly type based on the similarity of geometry and transformation. However, based on user feedback, the behavior has been reverted: **each FabricationPart now has its own unique assembly type**, as it was in previous versions.

To support this change, a new method has been introduced:

```
FabricationPartType.ResetAssemblyTypes(Document doc)
```

This method allows you to **manually reset all assembly type definitions** for fabrication parts in your model. Use this method during migration workflows or when consistency across fabrication elements is critical.

**CefSharp Removal**

The **CefSharp** dependency has been fully removed from Revit as of the 2026 release. This change was already announced in the initial **Revit 2026 SDK**, but it's worth highlighting again due to its impact on many existing add-ins.

If your add-ins relied on CefSharp to render HTML-based user interfaces within Revit, you may consider migrating to an alternative solution. The recommended approach is to adopt **Microsoft Edge WebView2**, which is actively supported and provides modern capabilities for hosting web content in desktop applications.

Note: Starting with Revit 2026, the required **WebView2 DLLs are already included** in the Revit installation, so no additional runtime installation is needed for end users.