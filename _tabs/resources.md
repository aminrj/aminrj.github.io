---
layout: page
icon: fas fa-book-open
title: Resources
order: 4
permalink: /resources/
---

<!-- ── Resources page styles ──────────────────────────────────────────────── -->

<style>
  .resources-hero {
    text-align: center;
    padding: 2rem 0 1.5rem;
  }
  .resources-hero h1 {
    font-size: 1.8rem;
    margin-bottom: 0.5rem;
  }
  .resources-hero p {
    color: var(--text-muted-color);
    font-size: 1rem;
    max-width: 600px;
    margin: 0 auto;
  }
  .resources-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
  }
  .resource-card {
    background: var(--card-bg-color);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 1.5rem;
    transition: border-color 0.2s;
  }
  .resource-card:hover {
    border-color: var(--accent-color);
  }
  .resource-card .resource-tag {
    display: inline-block;
    font-family: var(--font-monospace);
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    padding: 2px 8px;
    border-radius: 3px;
    margin-bottom: 0.75rem;
  }
  .resource-card .resource-tag.checklist { background: #e3f2fd; color: #1565c0; }
  .resource-card .resource-tag.rubric { background: #f3e5f5; color: #7b1fa2; }
  .resource-card .resource-tag.case-study { background: #e8f5e9; color: #2e7d32; }
  .resource-card .resource-tag.guide { background: #fff3e0; color: #e65100; }
  .resource-card h3 {
    font-size: 1.1rem;
    margin-bottom: 0.5rem;
  }
  .resource-card p {
    font-size: 0.9rem;
    color: var(--text-muted-color);
    margin-bottom: 1rem;
    line-height: 1.5;
  }
  .resource-card .resource-meta {
    font-family: var(--font-monospace);
    font-size: 0.75rem;
    color: var(--text-muted-color);
    margin-bottom: 0.75rem;
  }
  .resource-btn {
    display: inline-block;
    font-family: var(--font-monospace);
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 6px 14px;
    border-radius: 4px;
    text-decoration: none;
    transition: all 0.2s;
  }
  .resource-btn.primary {
    background: var(--accent-color);
    color: #fff;
  }
  .resource-btn.primary:hover {
    opacity: 0.9;
  }
  .resource-btn.outline {
    border: 1px solid var(--border-color);
    color: var(--text-color);
    background: transparent;
  }
  .resource-btn.outline:hover {
    border-color: var(--accent-color);
    color: var(--accent-color);
  }
  .resource-cta-section {
    text-align: center;
    padding: 2rem 0;
    margin-top: 2rem;
    border-top: 1px solid var(--border-color);
  }
  .resource-cta-section p {
    color: var(--text-muted-color);
    margin-bottom: 1rem;
  }
</style>

<div class="resources-hero">
  <h1>Free AI Security Resources</h1>
  <p>Practitioner-grade checklists, rubrics, and case studies for teams deploying AI agents in production.</p>
</div>

<div class="resources-grid">

  <!-- Field Guide -->
  <div class="resource-card">
    <span class="resource-tag guide">Field Guide</span>
    <h3>AI Agent Security Field Guide</h3>
    <p>20+ pages mapping the OWASP Agentic Top 10 to real attack patterns and production-ready mitigations.</p>
    <div class="resource-meta">PDF · 20+ pages · Free</div>
    <a href="/assets/pdfs/ai-agent-security-field-guide.pdf" class="resource-btn primary" target="_blank">Download →</a>
  </div>

  <!-- Pre-Deployment Checklist -->
  <div class="resource-card">
    <span class="resource-tag checklist">Checklist</span>
    <h3>Agent Pre-Deployment Security Checklist</h3>
    <p>25 controls across 5 families: probabilistic testing, supply chain, tool controls, injection defense, and sign-off.</p>
    <div class="resource-meta">PDF · 5 pages · Free</div>
    <a href="/resources/predeployment-checklist/" class="resource-btn outline">View &amp; Download →</a>
  </div>

  <!-- Threat Model Checklist -->
  <div class="resource-card">
    <span class="resource-tag checklist">Checklist</span>
    <h3>5 Ways AI Breaks Threat Modeling</h3>
    <p>A practical checklist for security teams deploying agentic AI — with what you need to add before you ship.</p>
    <div class="resource-meta">PDF · 6 pages · Free</div>
    <a href="/resources/threat-model-checklist/" class="resource-btn outline">View &amp; Download →</a>
  </div>

  <!-- Identity Readiness Checklist -->
  <div class="resource-card">
    <span class="resource-tag checklist">Checklist</span>
    <h3>AI Agent Identity Readiness Checklist</h3>
    <p>Five dimensions to verify before any AI agent enters production: governance, risk, capability, procurement, operations.</p>
    <div class="resource-meta">PDF · 5 pages · Free</div>
    <a href="/resources/identity-readiness-checklist/" class="resource-btn outline">View &amp; Download →</a>
  </div>

  <!-- Containment Rubric -->
  <div class="resource-card">
    <span class="resource-tag rubric">Rubric</span>
    <h3>AI Agent Containment Rubric</h3>
    <p>Assess your team's ability to contain AI-specific incidents across detection, isolation, response, communication, and improvement.</p>
    <div class="resource-meta">PDF · 5 pages · Free</div>
    <a href="/resources/containment-rubric/" class="resource-btn outline">View &amp; Download →</a>
  </div>

  <!-- HolmesGPT Case Study -->
  <div class="resource-card">
    <span class="resource-tag case-study">Case Study</span>
    <h3>HolmesGPT Case Study</h3>
    <p>How a customer support agent was compromised through prompt injection, and what it took to contain it. Full timeline, detection, and lessons.</p>
    <div class="resource-meta">PDF · 8 pages · Free</div>
    <a href="/resources/holmesgpt-case-study/" class="resource-btn outline">View &amp; Download →</a>
  </div>

</div>

<div class="resource-cta-section">
  <p>Get the next one. Practitioner-grade AI security, no noise.</p>
  <a href="/subscribe/" class="resource-btn primary">Subscribe →</a>
</div>
