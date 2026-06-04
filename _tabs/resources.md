---
layout: page
icon: fas fa-book-open
title: Resources
order: 4
permalink: /resources/
---

<!-- ── Resources page styles ──────────────────────────────────────────────── -->

<!-- Import lead-magnet fonts for the resources page -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;600;700&family=Newsreader:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">

<style>
  /* ── Tokens matching the lead-magnet brand ──────────────────────────── */
  :root {
    --rm-paper:   #FAF8F4;
    --rm-ink:     #1A1A1A;
    --rm-soft:    #5A5A5A;
    --rm-rule:    #D8D4CE;
    --rm-accent:  #C8553D;
    --rm-accent-ink: #9E3F2C;
  }

  /* ── Hero ───────────────────────────────────────────────────────────── */
  .resources-hero {
    text-align: center;
    padding: 3rem 0 2.5rem;
  }
  .resources-hero h1 {
    font-family: 'Fraunces', Georgia, serif;
    font-weight: 700;
    font-size: 2.2rem;
    color: var(--rm-ink);
    margin-bottom: 0.6rem;
    letter-spacing: -0.02em;
    line-height: 1.15;
  }
  .resources-hero p {
    font-family: 'Newsreader', Georgia, serif;
    font-size: 1.05rem;
    color: var(--rm-soft);
    max-width: 540px;
    margin: 0 auto;
    line-height: 1.6;
  }

  /* ── Grid ───────────────────────────────────────────────────────────── */
  .resources-grid {
    display: grid !important;
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 1.5rem !important;
    margin: 1.5rem 0 2.5rem !important;
  }
  @media (max-width: 768px) {
    .resources-grid {
      grid-template-columns: 1fr !important;
    }
  }
  .resources-grid > * {
    width: 100% !important;
    max-width: 100% !important;
  }

  /* ── Card wrapper (clickable) ──────────────────────────────────────── */
  .resource-card-link {
    text-decoration: none;
    color: var(--rm-ink);
    display: block;
  }

  /* ── Card ───────────────────────────────────────────────────────────── */
  .resource-card {
    background: var(--rm-paper) !important;
    border: 1px solid var(--rm-rule);
    padding: 1.75rem 1.75rem 1.5rem;
    transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.15s ease;
    display: flex;
    flex-direction: column;
    cursor: pointer;
    color: var(--rm-ink);
  }
  .resource-card:hover {
    border-color: var(--rm-accent);
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    transform: translateY(-2px);
  }
  .resource-card h3 {
    color: var(--rm-ink);
  }
  .resource-card .desc {
    color: var(--rm-soft);
  }

  /* ── Type badge ─────────────────────────────────────────────────────── */
  .resource-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--rm-accent);
    margin-bottom: 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  .resource-badge::before {
    content: '';
    display: inline-block;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--rm-accent);
    flex-shrink: 0;
  }
  .resource-badge.rubric { color: #7E22CE; }
  .resource-badge.rubric::before { background: #7E22CE; }

  /* ── Title ──────────────────────────────────────────────────────────── */
  .resource-card h3 {
    font-family: 'Fraunces', Georgia, serif;
    font-weight: 700;
    font-size: 1.2rem;
    color: var(--rm-ink);
    line-height: 1.25;
    margin-bottom: 0.55rem;
    letter-spacing: -0.01em;
  }

  /* ── Description ────────────────────────────────────────────────────── */
  .resource-card .desc {
    font-family: 'Newsreader', Georgia, serif;
    font-size: 0.88rem;
    color: var(--rm-soft);
    line-height: 1.55;
    margin-bottom: 1rem;
    flex: 1;
  }

  /* ── Meta ───────────────────────────────────────────────────────────── */
  .resource-meta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    color: var(--rm-soft);
    opacity: 0.6;
    margin-bottom: 1.1rem;
    letter-spacing: 0.02em;
  }

  /* ── Download link ──────────────────────────────────────────────────── */
  .resource-download {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--rm-accent);
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    transition: gap 0.15s ease, color 0.15s ease;
  }
  .resource-download:hover {
    gap: 0.7rem;
    color: var(--rm-accent-ink);
  }
  .resource-download .arrow {
    transition: transform 0.15s ease;
  }
  .resource-download:hover .arrow {
    transform: translateX(2px);
  }

  /* ── CTA section ────────────────────────────────────────────────────── */
  .resource-cta-section {
    text-align: center;
    padding: 2.5rem 0 1rem;
  }
  .resource-cta-section p {
    font-family: 'Newsreader', Georgia, serif;
    font-size: 0.95rem;
    color: var(--rm-soft);
    margin-bottom: 1rem;
  }
  .resource-cta-section a {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--rm-paper);
    background: var(--rm-accent);
    text-decoration: none;
    padding: 9px 22px;
    border-radius: 4px;
    transition: background 0.15s ease;
  }
  .resource-cta-section a:hover {
    background: var(--rm-accent-ink);
  }
</style>

<div class="resources-hero">
  <h1>Free AI Security Resources</h1>
  <p>Practitioner-grade checklists, rubrics, and field guides for teams deploying AI agents in production.</p>
</div>

<div class="resources-grid">

  <!-- Field Guide -->
  <a href="/resources/field-guide/" class="resource-card-link">
    <div class="resource-card">
      <div class="resource-badge">Field Guide</div>
      <h3>AI Agent Security Field Guide</h3>
      <p class="desc">20+ pages mapping the OWASP Agentic Top 10 to real attack patterns and production-ready mitigations.</p>
      <div class="resource-meta">PDF · 20+ pages · Free</div>
      <a href="/assets/pdfs/ai-agent-security-field-guide.pdf" class="resource-download" target="_blank" onclick="event.stopPropagation()">Download<span class="arrow">→</span></a>
    </div>
  </a>

  <!-- Pre-Deployment Checklist -->
  <a href="/resources/predeployment-checklist/" class="resource-card-link">
    <div class="resource-card">
      <div class="resource-badge">Checklist</div>
      <h3>Agent Pre-Deployment Security Checklist</h3>
      <p class="desc">25 controls across 5 families: probabilistic testing, supply chain, tool controls, injection defense, and sign-off.</p>
      <div class="resource-meta">PDF · 5 pages · Free</div>
      <a href="/assets/pdfs/predeployment-checklist.pdf" class="resource-download" target="_blank" onclick="event.stopPropagation()">Download<span class="arrow">→</span></a>
    </div>
  </a>

  <!-- Threat Model Checklist -->
  <a href="/resources/threat-model-checklist/" class="resource-card-link">
    <div class="resource-card">
      <div class="resource-badge">Checklist</div>
      <h3>5 Ways AI Breaks Threat Modeling</h3>
      <p class="desc">A practical checklist for security teams deploying agentic AI — with what you need to add before you ship.</p>
      <div class="resource-meta">PDF · 6 pages · Free</div>
      <a href="/assets/pdfs/threat-model-checklist.pdf" class="resource-download" target="_blank" onclick="event.stopPropagation()">Download<span class="arrow">→</span></a>
    </div>
  </a>

  <!-- Identity Readiness Checklist -->
  <a href="/resources/identity-readiness-checklist/" class="resource-card-link">
    <div class="resource-card">
      <div class="resource-badge">Checklist</div>
      <h3>AI Agent Identity Readiness Checklist</h3>
      <p class="desc">Five dimensions to verify before any AI agent enters production: governance, risk, capability, procurement, operations.</p>
      <div class="resource-meta">PDF · 5 pages · Free</div>
      <a href="/assets/pdfs/identity-readiness-checklist.pdf" class="resource-download" target="_blank" onclick="event.stopPropagation()">Download<span class="arrow">→</span></a>
    </div>
  </a>

  <!-- Containment Rubric -->
  <a href="/resources/containment-rubric/" class="resource-card-link">
    <div class="resource-card">
      <div class="resource-badge rubric">Rubric</div>
      <h3>AI Agent Containment Rubric</h3>
      <p class="desc">Assess your team's ability to contain AI-specific incidents across detection, isolation, response, communication, and improvement.</p>
      <div class="resource-meta">PDF · 5 pages · Free</div>
      <a href="/assets/pdfs/containment-rubric.pdf" class="resource-download" target="_blank" onclick="event.stopPropagation()">Download<span class="arrow">→</span></a>
    </div>
  </a>

</div>

<div class="resource-cta-section">
  <p>Get the next one. Practitioner-grade AI security, no noise.</p>
  <a href="/subscribe/" class="resource-btn primary">Subscribe →</a>
</div>
