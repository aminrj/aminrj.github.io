---
title: "GPAI Meets Agentic AI: Why Your MCP Deployment Triggers EU AI Act Obligations"
date: 2026-03-23
uuid: 202603230000
draft: true
status: draft
published: false
content-type: article
target-audience: advanced
categories: [AI Security, EU AI Act, Compliance]
tags:
  [
    EU AI Act,
    GPAI,
    MCP,
    Agentic AI,
    Article 26,
    Article 53,
    Deployer Obligations,
    Compliance,
    AI Governance,
  ]
description: "The March 13 delegated regulation on GPAI model evaluation made abstract obligations enforceable. If your agentic AI calls Claude or GPT through MCP, you are a downstream deployer -- and the regulatory chain extends to your architecture."
---

> EUAI-001 | EU AI Act Series | Target: 3600 words
> STATUS: DRAFT STRUCTURE -- DO NOT PUBLISH

---

## Article Structure and Research Directives

### Opening hook (300 words)

Lead with the **March 13, 2026 delegated regulation** published by the Council of the EU. This regulation establishes procedural rules under Article 92 for how the Commission will evaluate GPAI models, including API and source code access requirements, limitation periods, and fine imposition rules. It takes effect August 2, 2026.

**Source to reference:**
- Search: "Council EU delegated regulation GPAI evaluation March 2026" for the press release
- The regulation covers Article 92(1), (2), (3)
- Cite by name, summarize operational impact, do not quote at length

**Framing:** "Last week, abstract GPAI obligations became enforceable evaluation procedures. If your agentic AI calls Claude or GPT through MCP, you are a downstream deployer, and the regulatory chain now extends to your architecture."

---

### Section 1: The GPAI obligation chain (800 words)

**What to cover:** Article 53 (GPAI provider obligations), Article 55 (systemic risk additional obligations), Article 26 (deployer obligations). The chain: GPAI provider builds model -> deployer integrates into agent -> agent calls tools via MCP -> tools produce outputs affecting users.

**Where to find it:**
- EU AI Act full text: Articles 53, 55, 26
- AI Act Explorer at artificialintelligenceact.eu (article-by-article commentary with recitals)
- The AI Act Service Desk Q&A on deployer obligations: ai-act-service-desk.ec.europa.eu

**Breach-prevention angle:** Most teams assume GPAI compliance is the model provider's problem. Show that deployer obligations under Article 26 include:
- Verifying the provider published adequate documentation (Article 53(1)(b))
- Using the model in accordance with its intended purpose
- Monitoring outputs
- Maintaining human oversight

If the provider is under Commission evaluation, the deployer's deployment architecture may need to produce evidence of proper use.

**Diagram directive:** Draw the obligation chain as a flow:
Provider (Art. 53) -> Model API -> Deployer (Art. 26) -> Agent orchestrator -> MCP server -> Tool -> Output -> User
Annotate each link with the specific Article that governs it.

---

### Section 2: Why MCP makes this different from a standard API call (600 words)

**What to cover:** In MCP, tool descriptions are controlled by third-party servers, tool execution happens in the agent's context, and the agent can chain tools autonomously. The deployer's compliance surface is larger than a REST API call.

**Reuse from published work:**
- [MCP Security Top 10](https://aminrj.com/posts/owasp-mcp-top-10/) -- the observation that "in MCP, a third party controls what context the model receives"
- The tool description trust analysis from that article

**Regulatory source:** Article 26(5) -- deployers must monitor AI system performance and report serious incidents. For agentic systems, "monitoring" means logging tool calls, not just API responses.

**Breach-prevention scenario:** An MCP server updates its tool descriptions to include a hidden instruction. The agent follows it, exfiltrates data. This is simultaneously a security incident AND a compliance failure: the deployer failed to monitor (Article 26) and failed to maintain human oversight (Article 14). The tool description scanning demonstrated in [MCP Tool Poisoning PoC](https://aminrj.com/posts/mcp-tool-poisoning/) serves dual purpose: security control AND compliance evidence.

---

### Section 3: Four deployer obligations for agentic MCP systems (1200 words)

Four subsections, each one obligation with a concrete engineering control:

**3.1: Article 26(1) -- Appropriate technical and organizational measures**
- Map to: MCP server allow-listing, tool description validation, network egress control
- Reference: Docker Compose configurations from [OpenClaw deployment guide](https://aminrj.com/posts/openclaw-secure-deployment/)

**3.2: Article 26(5) -- Monitor operation and report serious incidents**
- Map to: Structured logging of every tool call (input/output/timestamp/model decision rationale)
- Bridge to: EUAI-002 (logging schema article, publishes March 30)

**3.3: Article 26(6) -- Keep automatically generated logs**
- Map to: Immutable log retention, 6-month minimum per Article 19
- Reference the GDPR data minimization tension (log metadata, not full content)

**3.4: Article 14/26 -- Human oversight**
- Map to: Approval gates for high-risk tool calls
- Bridge to: Human Oversight article (EUAI-017/013 on calendar)
- Reference the "breakglass" concept

**Breach-prevention synthesis:** Each obligation maps to a control that independently prevents a real attack:
- Art. 26(1) = tool description scanning stops poisoning
- Art. 26(5) = monitoring catches anomalous tool chains
- Art. 26(6) = logs enable forensic reconstruction
- Art. 14 = human gates stop autonomous exfiltration

The compliance framework IS the security architecture.

---

### Section 4: Reference architecture diagram (400 words)

Text-based architecture diagram showing an MCP deployment with compliance controls at each point. Annotate with EU AI Act articles.

**Reuse:** mcp-attack-labs Docker Compose structure as baseline. Add compliance controls as sidecars/middleware.

---

### Closing: What to do this week (300 words)

Three concrete actions:

1. Inventory which GPAI models your agents call. Verify the provider has published Article 53 documentation.
2. Implement tool description scanning as a pre-flight check (reference mcp-scan tooling).
3. Start structured logging of tool calls now -- the schema can be refined, but the data collection cannot be retroactively applied.

---

## Cross-references to include

- [MCP Security Top 10](https://aminrj.com/posts/owasp-mcp-top-10/)
- [MCP Tool Poisoning PoC](https://aminrj.com/posts/mcp-tool-poisoning/)
- [Attacking Docker Desktop via MCP](https://aminrj.com/posts/docker-dash-mcp-attack/)
- [OpenClaw Secure Deployment](https://aminrj.com/posts/openclaw-secure-deployment/)
- EUAI-002 (forward reference, publishes March 30)

## Lab reuse

mcp-attack-labs repo + OpenClaw Docker Compose. No new lab needed -- this is a framing piece connecting existing technical work to the regulatory chain.
