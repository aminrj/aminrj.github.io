---
layout: page
title: "HolmesGPT Case Study"
description: "How a customer support agent was compromised through prompt injection, and what it took to contain it."
permalink: /resources/holmesgpt-case-study/
order: 10
---

<style>
  .magnet-hero { text-align: center; padding: 2rem 0 1.5rem; }
  .magnet-hero .magnet-tag { display: inline-block; font-family: var(--font-monospace); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; padding: 4px 12px; border-radius: 4px; background: #e8f5e9; color: #2e7d32; margin-bottom: 1rem; }
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
  <span class="magnet-tag">Case Study</span>
  <h1>HolmesGPT Case Study</h1>
  <p>A customer support agent processes 10,000 conversations daily. It passes standard security reviews. No one tests it for prompt injection. Then a customer message contains embedded instructions that the agent executes, exfiltrating 850 customer records over three days.</p>
  <a href="/assets/pdfs/holmesgpt-case-study.pdf" class="magnet-download-btn" target="_blank">Download PDF →</a>
  <div class="magnet-meta">PDF · 8 pages · Free · No sign-up required</div>
</div>

<div class="magnet-contents">
  <h2>What's Inside</h2>
  <ul>
    <li>
      <strong>The Scenario</strong>
      <div class="magnet-why">HolmesGPT is a customer support agent deployed by a mid-market SaaS company. It processes customer inquiries through a multi-turn conversation, accesses account data through a read-only API, and can escalate to human agents.</div>
    </li>
    <li>
      <strong>The Attack</strong>
      <div class="magnet-why">A customer submits a normal-looking support ticket with embedded instructions. The agent's input processing does not strip or separate the embedded content. Over three days, 850 customer records are exfiltrated.</div>
    </li>
    <li>
      <strong>Detection</strong>
      <div class="magnet-why">Detection was not automated. It was a human noticing an anomaly in a spreadsheet. The monitoring system had no rule that would have caught this pattern.</div>
    </li>
    <li>
      <strong>Containment</strong>
      <div class="magnet-why">The security team took immediate action: agent disabled, credentials rotated, logs preserved, data scope assessed. Containment took 45 minutes.</div>
    </li>
    <li>
      <strong>Response</strong>
      <div class="magnet-why">Short-term: customer notification, regulatory notification, agent redesign, monitoring enhancement. Long-term: input sanitization pipeline, output policy enforcement, adversarial testing program, incident response playbook.</div>
    </li>
    <li>
      <strong>Lessons Learned</strong>
      <div class="magnet-why">What worked: audit logging, kill switch, credential scoping. What failed: input processing, output validation, monitoring, adversarial testing.</div>
    </li>
    <li>
      <strong>Checklist for Your Team</strong>
      <div class="magnet-why">Seven specific controls to assess before deploying AI agents: input processing, output validation, monitoring, adversarial testing, kill switch, audit logging, incident response, and credential scoping.</div>
    </li>
  </ul>
</div>

<div class="magnet-cta-section">
  <p>Need more? Explore all free resources or get the next one delivered.</p>
  <a href="/resources/" class="magnet-download-btn">Browse All Resources →</a>
</div>
