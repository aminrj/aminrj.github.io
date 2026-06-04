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
    padding: 2.5rem 0 2rem;
  }
  .resources-hero h1 {
    font-size: 2rem;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
  }
  .resources-hero p {
    color: var(--text-muted-color);
    font-size: 1.05rem;
    max-width: 560px;
    margin: 0 auto;
    line-height: 1.6;
  }
  .resources-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.25rem;
    margin: 1.5rem 0 2rem;
  }
  .resource-card {
    background: var(--card-bg-color);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    overflow: hidden;
    transition: border-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
  }
  .resource-card:hover {
    border-color: var(--accent-color);
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
  }
  .resource-card .cover-img {
    width: 100%;
    height: 200px;
    object-fit: contain;
    display: block;
    background: #0f172a;
    padding: 12px;
    box-sizing: border-box;
  }
  .resource-card .card-body {
    padding: 1.1rem 1.25rem 1.25rem;
  }
  .resource-card .resource-tag {
    display: inline-block;
    font-family: var(--font-monospace);
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 3px 10px;
    border-radius: 4px;
    margin-bottom: 0.65rem;
    font-weight: 600;
  }
  .resource-card .resource-tag.checklist { background: #e0f2fe; color: #0369a1; }
  .resource-card .resource-tag.rubric { background: #f3e8ff; color: #7e22ce; }
  .resource-card .resource-tag.guide { background: #fef2f2; color: #b91c1c; }
  .resource-card h3 {
    font-size: 1rem;
    margin-bottom: 0.45rem;
    line-height: 1.35;
    letter-spacing: -0.01em;
  }
  .resource-card p {
    font-size: 0.85rem;
    color: var(--text-muted-color);
    margin-bottom: 0.85rem;
    line-height: 1.55;
  }
  .resource-card .resource-meta {
    font-family: var(--font-monospace);
    font-size: 0.7rem;
    color: var(--text-muted-color);
    margin-bottom: 0.85rem;
    opacity: 0.7;
  }
  .resource-btn {
    display: inline-block;
    font-family: var(--font-monospace);
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 7px 16px;
    border-radius: 5px;
    text-decoration: none;
    transition: all 0.2s;
    font-weight: 500;
  }
  .resource-btn.primary {
    background: var(--accent-color);
    color: #fff;
  }
  .resource-btn.primary:hover {
    opacity: 0.85;
  }
  .resource-cta-section {
    text-align: center;
    padding: 2rem 0;
    margin-top: 1rem;
    border-top: 1px solid var(--border-color);
  }
  .resource-cta-section p {
    color: var(--text-muted-color);
    margin-bottom: 1rem;
    font-size: 0.95rem;
  }
</style>

<div class="resources-hero">
  <h1>Free AI Security Resources</h1>
  <p>Practitioner-grade checklists, rubrics, and field guides for teams deploying AI agents in production.</p>
</div>

<div class="resources-grid">

  <!-- Field Guide -->
  <div class="resource-card">
    <img src="/assets/img/cover-field-guide.svg" alt="AI Agent Security Field Guide cover" class="cover-img">
    <div class="card-body">
      <span class="resource-tag guide">Field Guide</span>
      <h3>AI Agent Security Field Guide</h3>
      <p>20+ pages mapping the OWASP Agentic Top 10 to real attack patterns and production-ready mitigations.</p>
      <div class="resource-meta">PDF · 20+ pages · Free</div>
      <a href="/assets/pdfs/ai-agent-security-field-guide.pdf" class="resource-btn primary" target="_blank">Download →</a>
    </div>
  </div>

  <!-- Pre-Deployment Checklist -->
  <div class="resource-card">
    <img src="/assets/img/cover-predeployment-checklist.svg" alt="Pre-Deployment Security Checklist cover" class="cover-img">
    <div class="card-body">
      <span class="resource-tag checklist">Checklist</span>
      <h3>Agent Pre-Deployment Security Checklist</h3>
      <p>25 controls across 5 families: probabilistic testing, supply chain, tool controls, injection defense, and sign-off.</p>
      <div class="resource-meta">PDF · 5 pages · Free</div>
      <a href="/assets/pdfs/predeployment-checklist.pdf" class="resource-btn primary" target="_blank">Download →</a>
    </div>
  </div>

  <!-- Threat Model Checklist -->
  <div class="resource-card">
    <img src="/assets/img/cover-threat-model-checklist.svg" alt="Threat Modeling Checklist cover" class="cover-img">
    <div class="card-body">
      <span class="resource-tag checklist">Checklist</span>
      <h3>5 Ways AI Breaks Threat Modeling</h3>
      <p>A practical checklist for security teams deploying agentic AI — with what you need to add before you ship.</p>
      <div class="resource-meta">PDF · 6 pages · Free</div>
      <a href="/assets/pdfs/threat-model-checklist.pdf" class="resource-btn primary" target="_blank">Download →</a>
    </div>
  </div>

  <!-- Identity Readiness Checklist -->
  <div class="resource-card">
    <img src="/assets/img/cover-identity-readiness-checklist.svg" alt="Identity Readiness Checklist cover" class="cover-img">
    <div class="card-body">
      <span class="resource-tag checklist">Checklist</span>
      <h3>AI Agent Identity Readiness Checklist</h3>
      <p>Five dimensions to verify before any AI agent enters production: governance, risk, capability, procurement, operations.</p>
      <div class="resource-meta">PDF · 5 pages · Free</div>
      <a href="/assets/pdfs/identity-readiness-checklist.pdf" class="resource-btn primary" target="_blank">Download →</a>
    </div>
  </div>

  <!-- Containment Rubric -->
  <div class="resource-card">
    <img src="/assets/img/cover-containment-rubric.svg" alt="Containment Rubric cover" class="cover-img">
    <div class="card-body">
      <span class="resource-tag rubric">Rubric</span>
      <h3>AI Agent Containment Rubric</h3>
      <p>Assess your team's ability to contain AI-specific incidents across detection, isolation, response, communication, and improvement.</p>
      <div class="resource-meta">PDF · 5 pages · Free</div>
      <a href="/assets/pdfs/containment-rubric.pdf" class="resource-btn primary" target="_blank">Download →</a>
    </div>
  </div>

</div>

<div class="resource-cta-section">
  <p>Get the next one. Practitioner-grade AI security, no noise.</p>
  <a href="/subscribe/" class="resource-btn primary">Subscribe →</a>
</div>
