---
title: "I Build My Lead Magnets Like Software, Not in Canva"
date: 2026-06-29
uuid: 202606290000
status: published
published: true
content-type: article
target-audience: intermediate
categories: [DevOps, Developer Guide, Automation]
tags:
  [
    DevOps,
    Automation,
    Markdown,
    Playwright,
    WeasyPrint,
    PDF,
    Jinja2,
    Static Site
  ]
image:
  path: /assets/media/devops/markdown-to-pdf-pipeline.png
description: One Markdown file produces both a web page and a print-identical PDF. Version-controlled, zero drift between versions, and built around a headless-browser-versus-PDF-library decision I had to defend with actual benchmarks.
mermaid: true
---

I needed branded PDFs to gate behind email signups: the checklist, the guide, the one-pager. The obvious tool was Canva. I opened it, made one, and immediately hit the thing that always kills design tools for me. The moment I wanted the same content as a web page and a PDF, I had two artifacts that would drift apart the instant I edited either one. Fix a typo in the PDF, forget the web version, and now they disagree. Update the web version, re-export the PDF by hand, hope you matched the styling.

So I did what I do with everything else that has a "source" and an "output": I treated it like software. One Markdown file is the source of truth. A build step produces both a web page and a PDF that's pixel-identical to it. Edit the `.md`, rebuild, both outputs update together. No design tool, no drift, fully version-controlled.

Here's the pipeline, the one genuinely contested technical decision in it, and why "build it like software" beats "make it in Canva" for anything you'll maintain over time.

## Why not Canva: single source of truth beats a design tool

The case against Canva isn't that it's bad. It's excellent at what it does. The case is that a design tool makes the artifact the source of truth, and the artifact is the wrong thing to own.

When the design is the source, every output is a manual export, every edit is a manual re-export, and every channel (web, PDF, the email itself) is a separate copy you keep in sync by remembering to. That's fine for a one-off. It's a slow leak for anything you revise, and a lead magnet is something you revise: you tweak the offer, fix a claim, update a stat, rebrand. Each revision is a chance for the copies to diverge.

When the content is the source (a Markdown file with the words and structure, separate from the styling) outputs become a function of the source. Web page and PDF are both renders of the same `.md`. There's exactly one place the content lives, the styling is applied consistently by the build, and "keep them in sync" stops being a task because they're generated from the same input. That's the entire value proposition, and it's the same reason we don't ship compiled binaries as our source code.

It also means the content is diffable and version-controlled. I can see exactly what changed between v1 and v2 of a guide in a git diff. Try that with two Canva exports.

## The pipeline: Markdown to HTML to PDF

Three stages, each a boring, well-understood tool.

<pre class="mermaid">
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#e8f4fd", "primaryBorderColor": "#3182ce", "fontSize": "14px", "fontFamily": "system-ui, -apple-system, sans-serif"}}}%%
flowchart LR
    MD["guide.md<br/>+ YAML frontmatter"] --> J["Jinja2 template"]
    J --> H["guide.html"]
    H --> WEB["Web page"]
    H --> PW["Playwright<br/>headless Chromium"]
    PW --> PDF["guide.pdf<br/>print-identical"]
    CSS["Design tokens (CSS)"] -. "one stylesheet" .-> H
    classDef src fill:#fff4e5,stroke:#d97706,color:#1a202c,stroke-width:1.5px
    classDef step fill:#e8f4fd,stroke:#3182ce,color:#1a202c,stroke-width:1.5px
    classDef out fill:#e6f4ea,stroke:#1e7e34,color:#1a202c,stroke-width:1.5px
    class MD,CSS src
    class J,H,PW step
    class WEB,PDF out
</pre>

**1. Markdown + YAML frontmatter to HTML, via Jinja2.** The source file is content plus a frontmatter block for the variable bits: title, subtitle, accent color, the CTA. A Jinja2 template wraps the rendered Markdown body in the branded HTML shell. Standard, current pattern; nothing exotic, no custom tooling.

```yaml
---
title: "The Pre-Deployment Checklist for Agentic Systems"
subtitle: "Seven checks before you ship"
accent: "#c8553d"      # terracotta
cta: "Get the full course →"
---

## Build-time checks

- [ ] Probabilistic behavior testing
- [ ] Supply-chain verification
...
```

**2. HTML to PDF, via Playwright (headless Chromium).** The same HTML that renders as the web page gets loaded in a headless browser, which then prints it to PDF using its built-in print engine. Because the browser rendering the web page and the browser generating the PDF are the same engine, the two outputs are visually identical by construction. This is the contested choice, and I'll defend it in a second.

**3. Design tokens in CSS** carry the branding (fonts, colors, the print-specific styling) so the look lives in one stylesheet, not baked into each document.

```python
# the whole HTML to PDF step
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"file://{html_path}")
    page.pdf(path=out_pdf, format="A4", print_background=True)
    browser.close()
```

One `make build` runs all three. Edit the Markdown, run it, and `guide.html` and `guide.pdf` both update from the one source.

## The contested decision: Playwright over WeasyPrint

This is the one place an engineer will push back, so let me give the honest version instead of pretending it's clear-cut.

The two real options for HTML-to-PDF in Python are WeasyPrint (parses HTML/CSS directly and writes native PDF primitives, no browser) and Playwright (drives headless Chromium and uses its print engine). The 2026 benchmarks are clear, and they do not uniformly favor Playwright.

File size: WeasyPrint wins, decisively. It produces 50–80% smaller PDFs (roughly 8 KB vs 16 KB on a simple document, 21 KB vs 59–125 KB on a complex one) because it emits native PDF primitives instead of routing through a print engine that embeds extra resources.

Deployment footprint: WeasyPrint wins. Playwright ships about 300 MB of Chromium. WeasyPrint is a comparatively light Python dependency, far easier to put in a small container or a serverless function.

Warm-mode speed: Playwright wins, hugely. With a warm browser pool, Playwright is 15–75× faster (3 ms vs 227 ms simple, 13 ms vs 629 ms complex), because WeasyPrint spawns a fresh process every call with no warm mode.

<pre class="mermaid">
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#e8f4fd", "primaryBorderColor": "#3182ce", "fontSize": "13px", "fontFamily": "system-ui, -apple-system, sans-serif"}}}%%
flowchart TB
    Q{"What matters most<br/>for this document?"} -->|"pixel-identical fidelity,<br/>or JS-rendered charts"| PW["Playwright<br/>(same engine as the web page)"]
    Q -->|"smallest files,<br/>lightest deploy, no JS"| WP["WeasyPrint<br/>(native PDF primitives)"]
    classDef q fill:#fff4e5,stroke:#d97706,color:#1a202c,stroke-width:1.5px
    classDef a fill:#e8f4fd,stroke:#3182ce,color:#1a202c,stroke-width:1.5px
    class Q q
    class PW,WP a
</pre>

So if WeasyPrint makes smaller files and deploys lighter, why did I pick Playwright? Because fidelity mattered more than footprint for this use case, and only one engine guarantees it.

The whole point of my pipeline is that the PDF is pixel-identical to the web page I already see in my browser. WeasyPrint has its own rendering engine; its CSS support is good but not identical to Chromium's, so the web page (rendered in a real browser) and the WeasyPrint PDF can subtly differ in spacing, font rendering, or a modern CSS feature WeasyPrint handles differently. That difference defeats the single-source-of-truth promise: now I have two renderers and I'm back to checking that two outputs agree. With Playwright, the page I preview and the PDF I ship come from the same engine, so they can't disagree. A few extra hundred KB per file is a price I'll pay every time to never have to eyeball-diff a web page against its PDF again.

The honest framing, then: Playwright isn't strictly better, it's the right trade for a branded, fidelity-critical document where the web and print versions must match. If I were generating millions of lightweight invoices server-side with no JavaScript, WeasyPrint would be the correct answer and I'd say so.

## The JavaScript dividing line

There's also a hard technical boundary that can make the decision for you, and it's worth knowing even if you don't hit it: WeasyPrint cannot execute JavaScript.

It parses HTML and CSS and stops there. No browser engine, no JS runtime. So if a document contains anything JS-rendered (a Chart.js graph, a D3 visualization, a Plotly chart, a dynamic table) WeasyPrint renders it blank. Only a real browser engine (Playwright or Puppeteer) runs the script and captures the result.

For my current lead magnets, which are static prose plus CSS, this boundary doesn't bite; WeasyPrint would technically suffice on the JS front. But the moment I want a generated chart in a report (and I will), Playwright is mandatory and WeasyPrint is disqualified. Choosing Playwright up front means the pipeline doesn't need re-architecting the first time a document needs a rendered visual. That's a real consideration for a system you intend to keep, not just a fidelity preference.

(And to dispatch the obvious old option: wkhtmltopdf is dead. It stopped active development in 2023, and the popular `pdfkit` library wraps it. Don't start a new project on it. The choice in 2026 is genuinely Playwright vs WeasyPrint; everything else is a wrapper around one of those ideas or an abandoned engine.)

## Design tokens: branding in one place

The styling is a set of CSS custom properties, design tokens, so the brand lives in one stylesheet and every document inherits it:

```css
:root {
  --font-body: "Fraunces", serif;            /* editorial confidence */
  --font-mono: "JetBrains Mono", monospace;  /* engineering precision */
  --accent: #c8553d;                         /* terracotta */
  --paper: #faf6f0;
}
```

The fonts are deliberate: JetBrains Mono for the code and checklist elements (engineering-document precision) and Fraunces for the prose (editorial warmth), with a terracotta accent so it doesn't read like every other developer PDF. Custom-font loading in Playwright PDFs is well-documented and reliable; the headless browser loads the web fonts exactly as a real browser does, which is another quiet win for the same-engine approach. Even the checkboxes are CSS-drawn rather than image assets, so they stay crisp at any zoom and there's no binary to manage.

Change `--accent` once and every document and both outputs re-skin. That's the design-token payoff: branding is configuration, not a property of each file.

## Parseable control syntax: content stays content

The last principle is the one that keeps the system honest over time: content must never become layout.

The temptation in any templating system is to start sneaking presentation into the source (a raw `<div class="callout">` here, an inline style there) until the Markdown file is half HTML and the single-source-of-truth promise quietly dies. To prevent that, the few structural things a document needs (a callout box, a two-column section, a page break) are expressed as a small, parseable control syntax that the build interprets, not as raw layout the author hand-writes.

```markdown
::: callout
This is content. The ":::" is a parseable directive the build turns
into the branded callout box. The author never writes a class or a div.
:::
```

The author writes meaning ("this is a callout"); the build owns appearance ("here's what a callout looks like"). That separation is what lets me restyle every callout in every document by editing one template, and it's what stops the source files from slowly rotting into HTML. It's the same discipline as keeping logic out of your templates: content files describe what, the build decides how.

## The report variant: LaTeX / DOCX from the same idea

The same architecture extends past lead magnets. For longer, more formal documents (reports, whitepapers) I keep a variant that targets a LaTeX (or DOCX) template instead of HTML/PDF. Same principle: Markdown content as the source, a template that owns the formatting, a build that produces the output. The renderer changes; the discipline doesn't.

This is the real test of whether you built a pipeline or just a one-off script: can you swap the output target without touching the content? If the answer is yes, you've separated content from presentation properly. If you have to edit the source files to change the output format, you've got Canva with extra steps.

## The takeaway

Build lead magnets the way you build software, because that's what they are: a source you'll revise and outputs you'll regenerate. One Markdown file with YAML frontmatter is the source. Jinja2 makes the HTML, Playwright makes a PDF that's pixel-identical to it (fidelity over footprint, a trade I'd defend, not a free win), design tokens carry the brand, and a parseable control syntax keeps content from rotting into layout.

The single concrete payoff: I edit one `.md`, run one command, and both the web page and a print-identical PDF update together, version-controlled, no drift, ever. That's worth more than a Canva file the moment you have to maintain it instead of just make it once, which, for anything behind an email gate that you'll revise as your offer evolves, is always.

---

### References & sources

- Playwright vs WeasyPrint benchmarks, warm speed (15–75×), file size (WeasyPrint 50–80% smaller), no-JS limitation: [PDF4.dev Playwright vs WeasyPrint (2026)](https://pdf4.dev/blog/playwright-vs-weasyprint), [PDF4.dev HTML-to-PDF benchmark 2026](https://pdf4.dev/blog/html-to-pdf-benchmark-2026)
- WeasyPrint cannot execute JavaScript (blank charts); browser engine required for JS-rendered visuals: [Apryse HTML-to-PDF methods](https://apryse.com/blog/html-to-pdf-conversion-methods), [Iron Software 2026 comparison](https://ironsoftware.com/suite/blog/comparison/html-to-pdf-2026-guide/)
- wkhtmltopdf abandoned (2023); pdfkit wraps it: [PDF4.dev generate PDF from HTML](https://pdf4.dev/blog/generate-pdf-from-html-python)
- Jinja2 + Markdown to HTML to PDF and custom-font loading in Playwright: [APITemplate.io Python HTML-to-PDF](https://apitemplate.io/blog/how-to-convert-html-to-pdf-using-python/)

*HTML-to-PDF tooling and benchmarks are current as of mid-2026. The benchmark figures were measured on a specific machine and config; treat them as directional and measure your own documents before optimizing for file size or speed.*

---

*Amine Raji, PhD, CISSP. AI/LLM security, with a weakness for build pipelines.*
