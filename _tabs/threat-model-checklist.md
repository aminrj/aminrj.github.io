---
layout: page
title: "5 Ways AI Breaks Threat Modeling"
description: "A practical checklist for security teams deploying agentic AI — with what you need to add before you ship."
permalink: /resources/threat-model-checklist/
order: 7
---

<style>
  .magnet-hero { text-align: center; padding: 2rem 0 1.5rem; }
  .magnet-hero .magnet-tag { display: inline-block; font-family: var(--font-monospace); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; padding: 4px 12px; border-radius: 4px; background: #e3f2fd; color: #1565c0; margin-bottom: 1rem; }
  .magnet-hero h1 { font-size: 1.8rem; margin-bottom: 0.5rem; }
  .magnet-hero p { color: var(--text-muted-color); font-size: 1rem; max-width: 600px; margin: 0 auto 1.5rem; line-height: 1.6; }
  .magnet-download-btn { display: inline-block; font-family: var(--font-monospace); font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; padding: 10px 24px; border-radius: 6px; text-decoration: none; background: var(--accent-color); color: #fff; transition: opacity 0.2s; }
  .magnet-download-btn:hover { opacity: 0.9; }
  .magnet-meta { font-family: var(--font-monospace); font-size: 0.75rem; color: var(--text-muted-color); margin-top: 0.75rem; }
  .magnet-contents { margin: 2rem 0; }
  .magnet-contents h2 { font-size: 1.3rem; margin-bottom: 1rem; }
  .magnet-contents ul { list-style: none; padding-left: 0; }
  .magnet-contents ul li { padding: 0.5rem 0; border-bottom: 1px solid var(--border-color); font-size: 0.95rem; line-height: 1.5; }
  .magnet-contents ul li strong { color: var(--text-color); }
  .magnet-why { font-size: 0.85rem; color: var(--text-muted-color); font-style: italic; margin-top: 0.25rem; }
  .magnet-cta-section { text-align: center; padding: 2rem 0; margin-top: 2rem; border-top: 1px solid var(--border-color); }
  .magnet-cta-section p { color: var(--text-muted-color); margin-bottom: 1rem; }
</style>

<div class="magnet-hero">
  <span class="magnet-tag">Checklist</span>
  <h1>5 Ways AI Breaks Threat Modeling</h1>
  <p>Most engineering teams deploying AI in 2026 already have a security process. That process was not designed for AI. Here are the five specific ways, with what you need to add before you ship.</p>
  <a href="/assets/pdfs/threat-model-checklist.pdf" class="magnet-download-btn" target="_blank">Download PDF →</a>
  <div class="magnet-meta">PDF · 6 pages · Free · No sign-up required</div>
</div>

<div class="magnet-contents">
  <h2>What's Inside</h2>
  <ul>
    <li>
      <strong>1. Outputs Are Probabilistic, Not Deterministic</strong>
      <div class="magnet-why">You cannot unit-test a distribution with a single pass. Your test suite has no predictive power over behavior it did not observe.</div>
    </li>
    <li>
      <strong>2. The Attack Surface Includes Training Data</strong>
      <div class="magnet-why">You can audit source code and dependencies. You cannot audit a learning process that has already concluded.</div>
    </li>
    <li>
      <strong>3. Agents Take Actions, Not Just Produce Output</strong>
      <div class="magnet-why">A standalone LLM producing harmful text is a content moderation problem. An agent acting on that text is an operational security problem.</div>
    </li>
    <li>
      <strong>4. Prompt Injection Has No Equivalent Fix</strong>
      <div class="magnet-why">SQL injection was solved at the parser. Parameterized queries tell the database: this is code, this is data. Language models have no parser.</div>
    </li>
    <li>
      <strong>5. The Supply Chain Extends Beyond Code</strong>
      <div class="magnet-why">Traditional supply chain security has a defined scope: source code, dependencies, build artifacts, container images. AI adds datasets, model weights, MCP servers, and skill marketplaces.</div>
    </li>
    <li>
      <strong>6. What This Means for Your Process</strong>
      <div class="magnet-why">None of this means STRIDE is wrong. It means STRIDE is not sufficient.</div>
    </li>
  </ul>
</div>

<div class="magnet-cta-section">
  <p>Need more? Explore all free resources or get the next one delivered.</p>
  <a href="/resources/" class="magnet-download-btn">Browse All Resources →</a>
</div>
