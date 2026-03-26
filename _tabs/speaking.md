---
layout: speaking
title: Speaking
icon: fas fa-microphone-alt
order: 2
permalink: /speaking/
hook: >-
  AI security practitioner with 15+ years in high-stakes environments (banking, defense, aerospace, automotive) —
  now focused exclusively on agentic AI attack surfaces. Every claim I make in front of an audience has been
  reproduced in a local lab first.
---

## About

Amine Raji is an AI security practitioner, independent researcher, and Cloud Cybersecurity Leader at Volvo Cars, where he leads cloud security strategy across a global engineering organisation.

He holds a PhD and CISSP certification, with 15+ years of applied security experience spanning banking, defense, aerospace, and automotive sectors. He now focuses at the intersection of cloud infrastructure and AI security — specifically how agentic architectures, MCP deployments, and LLM-integrated pipelines inherit and amplify cloud misconfigurations into a new class of attack.

His work is empirical: every claim he makes in front of an audience has been reproduced in a local lab first. He writes at [aminrj.com](https://aminrj.com), publishes the *AI Security Intelligence* newsletter, and contributes to the OWASP Agentic Security project.

He speaks to practitioners, security architects, and engineering leaders who are deploying AI into cloud infrastructure and need to understand the attack surface before it becomes an incident.

---

## Talks

<div class="speaking-section">

<div class="speaking-talk-card">
  <div class="speaking-talk-header">
    <span class="speaking-talk-number">1</span>
    <h3 class="speaking-talk-title">Your Cloud Infrastructure Is a Prompt Injection Surface</h3>
  </div>
  <div class="speaking-talk-meta">
    <span class="speaking-talk-badge audience"><i class="fas fa-users"></i> Cloud security engineers, DevSecOps teams, platform architects</span>
    <span class="speaking-talk-badge format"><i class="fas fa-clock"></i> 30–45 min keynote or technical session</span>
  </div>
  <p class="speaking-talk-abstract">CloudTrail events, resource tags, monitoring alerts, and pipeline output all flow through trusted cloud channels into AI agent context windows — bypassing every model-layer defense because they arrive as internal, trusted data. This talk demonstrates that a single crafted CloudTrail entry, a poisoned AWS resource tag, or a compromised runbook indexed into a RAG pipeline can redirect an agent with IAM credentials to take destructive actions against its own infrastructure. The fix isn't in the model — it's in the cloud configuration. Attendees leave with a new threat model for cloud-native AI deployments and five concrete AWS and Azure controls that eliminate the most impactful attack paths.</p>
</div>

<div class="speaking-talk-card">
  <div class="speaking-talk-header">
    <span class="speaking-talk-number">2</span>
    <h3 class="speaking-talk-title">The MCP Attack Surface: What Your Developers Are Installing Right Now</h3>
  </div>
  <div class="speaking-talk-meta">
    <span class="speaking-talk-badge audience"><i class="fas fa-users"></i> Security engineers, AppSec teams, DevSecOps leads</span>
    <span class="speaking-talk-badge format"><i class="fas fa-clock"></i> 30–45 min keynote or technical session</span>
  </div>
  <p class="speaking-talk-abstract">The Model Context Protocol has become the de facto standard for connecting AI agents to tools and data. It has also become the fastest-growing attack surface in enterprise AI deployments. This talk walks through three real attack patterns — tool poisoning, meta-context injection, and cross-server hijacking — with live code demonstrations and direct mappings to documented breaches from 2025–2026. Attendees leave with a concrete threat model and a prioritised list of controls they can implement before their next sprint ends.</p>
</div>

<div class="speaking-talk-card">
  <div class="speaking-talk-header">
    <span class="speaking-talk-number">3</span>
    <h3 class="speaking-talk-title">OWASP Agentic Top 10 in Practice: Real Attack Chains, Real Mitigations</h3>
  </div>
  <div class="speaking-talk-meta">
    <span class="speaking-talk-badge audience"><i class="fas fa-users"></i> Security architects, risk teams, engineering managers</span>
    <span class="speaking-talk-badge format"><i class="fas fa-clock"></i> 40–60 min keynote or workshop</span>
  </div>
  <p class="speaking-talk-abstract">The OWASP Agentic Top 10 exists. Most teams have read the summary. Almost none have mapped it to their actual systems. This talk takes each of the ten risk categories from abstract definition to concrete attack chain — using real incidents, reproducible lab scenarios, and the specific architectural decisions that made each one possible. It closes with a defensive framework grounded in least agency, strong observability, and human-in-the-loop design. Practical, evidence-based, no vendor agenda.</p>
</div>

<div class="speaking-talk-card">
  <div class="speaking-talk-header">
    <span class="speaking-talk-number">4</span>
    <h3 class="speaking-talk-title">Red Teaming AI Agents: A Practitioner's Field Guide</h3>
  </div>
  <div class="speaking-talk-meta">
    <span class="speaking-talk-badge audience"><i class="fas fa-users"></i> Red teamers, penetration testers, security researchers</span>
    <span class="speaking-talk-badge format"><i class="fas fa-clock"></i> 45–60 min technical session</span>
  </div>
  <p class="speaking-talk-abstract">Traditional red teaming methodologies break against agentic AI systems. The attack surface is non-deterministic, execution paths are emergent, and blast radius crosses tool boundaries, memory stores, and inter-agent communication channels simultaneously. This talk presents a structured red teaming methodology for agentic AI — covering goal hijacking, tool chain weaponization, identity spoofing, memory poisoning, and cascading failure induction — built from direct adversarial testing with PyRIT, Promptfoo, and Garak against locally deployed agent architectures.</p>
</div>

<div class="speaking-talk-card">
  <div class="speaking-talk-header">
    <span class="speaking-talk-number">5</span>
    <h3 class="speaking-talk-title">When Agents Delegate: Security Failures in Multi-Agent Systems</h3>
  </div>
  <div class="speaking-talk-meta">
    <span class="speaking-talk-badge audience"><i class="fas fa-users"></i> Platform engineers, AI architects, security teams</span>
    <span class="speaking-talk-badge format"><i class="fas fa-clock"></i> 30–45 min keynote or panel anchor</span>
  </div>
  <p class="speaking-talk-abstract">Single-agent security is hard enough. Multi-agent systems — where agents delegate tasks to other agents, pass credentials through chains, and trust messages without authentication — introduce an entirely different class of failure. This talk examines the trust assumptions embedded in today's agent frameworks, maps them to documented incident patterns, and makes the case for treating inter-agent communication with the same skepticism we apply to untrusted API calls. Includes a live demonstration of an identity spoofing attack across a three-agent pipeline.</p>
</div>

<div class="speaking-talk-card">
  <div class="speaking-talk-header">
    <span class="speaking-talk-number">6</span>
    <h3 class="speaking-talk-title">The State of Agentic AI Security: What 2025 Taught Us and What 2026 Will Demand</h3>
  </div>
  <div class="speaking-talk-meta">
    <span class="speaking-talk-badge audience"><i class="fas fa-users"></i> CISOs, security leaders, technical executives</span>
    <span class="speaking-talk-badge format"><i class="fas fa-clock"></i> 20–30 min keynote, conference opener or closer</span>
  </div>
  <p class="speaking-talk-abstract">2025 was the year AI agents moved from demos to production — and the year the first serious wave of agentic AI incidents landed. Tool poisoning, credential theft via cloud-connected agents, cascading failures triggered by a single poisoned document. This talk synthesises the key lessons from that first year: which threat categories materialised, which mitigations actually worked, and what the arrival of the OWASP Agentic Top 10, EU AI Act enforcement, and NIST CAISI mean for security teams trying to keep pace. Framed for decision-makers, grounded in technical evidence.</p>
</div>

</div>

---

## Published Thinking

- [aminrj.com](https://aminrj.com) — Research and writing on agentic AI security, cloud security, and defensive architectures
- [AI Security Intelligence](https://newsletter.aminrj.com) — Weekly newsletter: threats, vulnerabilities, and defensive innovations in AI security
- [OWASP Agentic Security project](https://owasp.org) — Contributor to the Agentic Security Initiative
