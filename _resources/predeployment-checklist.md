---
layout: page
title: "AI Agent Pre-Deployment Security Checklist"
description: "25 controls across five families to verify before any agentic system reaches production."
permalink: /resources/predeployment-checklist/
order: 6
---

<!-- ── Lead magnet page styles ────────────────────────────────────────────── -->

<style>
  .magnet-hero {
    text-align: center;
    padding: 2rem 0 1.5rem;
  }
  .magnet-hero .magnet-tag {
    display: inline-block;
    font-family: var(--font-monospace);
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 4px 12px;
    border-radius: 4px;
    background: #e3f2fd;
    color: #1565c0;
    margin-bottom: 1rem;
  }
  .magnet-hero h1 {
    font-size: 1.8rem;
    margin-bottom: 0.5rem;
  }
  .magnet-hero p {
    color: var(--text-muted-color);
    font-size: 1rem;
    max-width: 600px;
    margin: 0 auto 1.5rem;
    line-height: 1.6;
  }
  .magnet-download-btn {
    display: inline-block;
    font-family: var(--font-monospace);
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 10px 24px;
    border-radius: 6px;
    text-decoration: none;
    background: var(--accent-color);
    color: #fff;
    transition: opacity 0.2s;
  }
  .magnet-download-btn:hover {
    opacity: 0.9;
  }
  .magnet-meta {
    font-family: var(--font-monospace);
    font-size: 0.75rem;
    color: var(--text-muted-color);
    margin-top: 0.75rem;
  }
  .magnet-preview {
    margin: 2rem 0;
    text-align: center;
  }
  .magnet-preview iframe {
    border: 1px solid var(--border-color);
    border-radius: 8px;
    max-width: 100%;
  }
  .magnet-contents {
    margin: 2rem 0;
  }
  .magnet-contents h2 {
    font-size: 1.3rem;
    margin-bottom: 1rem;
  }
  .magnet-contents ul {
    list-style: none;
    padding-left: 0;
  }
  .magnet-contents ul li {
    padding: 0.5rem 0;
    border-bottom: 1px solid var(--border-color);
    font-size: 0.95rem;
    line-height: 1.5;
  }
  .magnet-contents ul li strong {
    color: var(--text-color);
  }
  .magnet-why {
    font-size: 0.85rem;
    color: var(--text-muted-color);
    font-style: italic;
    margin-top: 0.25rem;
  }
  .magnet-cta-section {
    text-align: center;
    padding: 2rem 0;
    margin-top: 2rem;
    border-top: 1px solid var(--border-color);
  }
  .magnet-cta-section p {
    color: var(--text-muted-color);
    margin-bottom: 1rem;
  }
</style>

<div class="magnet-hero">
  <span class="magnet-tag">Checklist</span>
  <h1>AI Agent Pre-Deployment Security Checklist</h1>
  <p>Five control families to verify before any agentic system reaches production. 25 specific controls. Each is a yes or no. If you cannot check it, you have found work to do.</p>
  <a href="/assets/pdfs/predeployment-checklist.pdf" class="magnet-download-btn" target="_blank">Download PDF →</a>
  <div class="magnet-meta">PDF · 5 pages · Free · No sign-up required</div>
</div>

<div class="magnet-contents">
  <h2>What's Inside</h2>
  <ul>
    <li>
      <strong>1. Probabilistic Behavior Testing</strong>
      <div class="magnet-why">You cannot unit-test a distribution with a single pass. Verify the agent behaves within tolerance across repeated, adversarial, and drifted conditions.</div>
    </li>
    <li>
      <strong>2. Training Data and Supply Chain</strong>
      <div class="magnet-why">The data and weights your agent relies on are part of its attack surface. Verify provenance, integrity, and access controls.</div>
    </li>
    <li>
      <strong>3. Agent Tool Controls</strong>
      <div class="magnet-why">Every tool you give an agent expands its blast radius. Minimize permissions, validate inputs, and audit every call.</div>
    </li>
    <li>
      <strong>4. Prompt Injection Defense Layers</strong>
      <div class="magnet-why">Assume injection will be attempted. Defense must hold even if the model is fully compromised.</div>
    </li>
    <li>
      <strong>5. Pre-Ship Sign-Off</strong>
      <div class="magnet-why">This section is not about code. It is about accountability. Someone must own the decision to ship.</div>
    </li>
  </ul>
</div>

<div class="magnet-cta-section">
  <p>Need more? Explore all free resources or get the next one delivered.</p>
  <a href="/resources/" class="magnet-download-btn">Browse All Resources →</a>
</div>
