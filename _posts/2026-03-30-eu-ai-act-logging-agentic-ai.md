---
title: "EU AI Act Logging Requirements for Agentic AI: The Article 12 Schema No One Has Written"
date: 2026-03-30
uuid: 202603300000
draft: true
status: draft
published: false
content-type: article
target-audience: advanced
categories: [AI Security, EU AI Act, Compliance]
tags:
  [
    EU AI Act,
    Article 12,
    Article 19,
    Logging,
    Agentic AI,
    MCP,
    Observability,
    OpenTelemetry,
    Compliance,
  ]
description: "Article 12 requires automatically generated logs. Article 19 requires 6-month retention. No technical standard exists for what those logs should contain for agentic AI. Here is the schema, the architecture, and the cost model."
---

> EUAI-002 | EU AI Act Series | Target: 3800 words
> STATUS: DRAFT STRUCTURE -- DO NOT PUBLISH

---

## Article Structure and Research Directives

### Opening hook (300 words)

Lead with the community signal: "The language is unambiguous about what must be logged, yet it says nothing about how."

**Source to reference:**
- Article 12(1)-(4) full text (logging capabilities)
- Article 19 (log retention -- 6-month minimum)
- Recitals 63-64 for legislative intent
- ISO/IEC DIS 24970 (AI system logging) -- confirm still in draft as of March 2026
- CEN-CENELEC harmonized standards status -- confirm not ready

**Framing:** "Article 12 says your high-risk AI system must have 'automatic recording of events (logs).' For an LLM chatbot, that is straightforward. For an agentic system that chains 15 MCP tool calls per task, logging is an architecture problem -- and there is no standard to follow."

---

### Section 1: What Article 12 and 19 actually require (600 words)

**Key requirements to extract from the text:**
- (a) Logs must be automatically generated, not manually curated
- (b) Logs must enable monitoring with respect to risks
- (c) Logs must enable post-market monitoring (Article 72 link)
- (d) Retention: at least 6 months (Article 19(1))
- (e) Logs must be "appropriate to the intended purpose"

**Where to find it:**
- Article 12 full text at artificialintelligenceact.eu
- Article 19 full text
- AI Act Service Desk Q&A on logging requirements
- Verify: ISO/IEC DIS 24970 status at iso.org

**The standard gap:** CEN-CENELEC harmonized standards will not be ready before August 2. Engineering teams must define their own schema. This article fills that gap.

**Breach-prevention angle:** Compliance-grade logging IS incident-response-grade logging. The schema built for Article 12 is the same schema a SOC uses for forensic reconstruction. Build once, satisfy both.

---

### Section 2: The agentic AI logging schema (1200 words -- core deliverable)

Define a JSON schema for agentic AI events. Six event types, each with field definitions, rationale, and the Article it satisfies.

**Event types:**

**2.1 Agent session start/end**
- Fields: session_id, model_id, model_version, agent_config_hash, timestamp, user_id (anonymized)
- Satisfies: Article 12(1) "identification of the version of the system"

**2.2 Tool call**
- Fields: session_id, tool_name, server_id, tool_description_hash, input_params (sanitized), output (truncated), latency_ms, model_decision_rationale
- Satisfies: Article 12(2) "monitoring of the operation"
- This is the core agentic action log. It captures what no standard LLM log captures.

**2.3 Human oversight event**
- Fields: session_id, oversight_pattern, proposed_action, decision, human_id, timestamp
- Satisfies: Article 14 compliance evidence
- Links to the human oversight patterns article

**2.4 Model output**
- Fields: session_id, prompt_hash, completion_hash, output_classification, confidence_score, tokens_used
- Satisfies: Article 50 transparency, Article 72 post-market monitoring

**2.5 Anomaly detection**
- Fields: session_id, anomaly_type, severity, affected_tool, detection_method, auto_response
- Satisfies: Article 9 ongoing risk monitoring

**2.6 Incident report trigger**
- Fields: session_id, incident_type, severity, affected_users_count, evidence_snapshot_id
- Satisfies: Article 73 serious incident reporting (2-10 day notification windows)

**Where to find schema patterns:**
- OpenTelemetry gen-ai semantic conventions (search "opentelemetry gen-ai semantic conventions") -- defines LLM span attributes but not tool calls or oversight events. Your schema extends them.
- OpenTelemetry Collector configuration documentation

**GDPR tension resolution:**
- Article 12 wants maximum logging. GDPR Article 5(1)(c) wants data minimization.
- Resolution: log metadata (tool name, parameters, hashes) not full content. Anonymize user IDs. Hash prompt/completion content for integrity verification without storing plaintext.
- Reference: EDPB guidance on AI systems and data protection

---

### Section 3: Architecture patterns (800 words)

Three patterns with trade-offs:

**3.1 Sidecar logger (recommended for MCP)**
- Deploy logging proxy between agent and MCP server
- Intercepts all tool calls, generates structured events, ships to aggregator
- Does not modify agent or server code
- **Lab reuse:** Add mcp-log-proxy container to existing mcp-attack-labs Docker Compose
- Breach-prevention: sidecar doubles as monitoring/anomaly detection point

**3.2 Agent-native logging**
- Instrument the agent framework (LangChain, CrewAI, custom) to emit events
- **Lab reuse:** Your Python agent in mcp-attack-labs already has a tool-calling loop. Show where to insert event emission (pseudocode diff)
- Trade-off: requires code changes to every agent

**3.3 Gateway logging**
- MCP gateway for multi-agent deployments. Central logging.
- Reference emerging solutions (Peta, Entro, Tetrate) without endorsing
- Trade-off: single point of failure, added latency

---

### Section 4: Retention, integrity, and cost model (600 words)

**Retention:**
- 6 months minimum (Article 19)
- Financial services: consider 5-7 years (MiFID II intersection)
- Healthcare: sector-specific retention requirements

**Integrity:**
- Options: append-only storage, cryptographic chaining, Sigstore-style attestation
- Breach-prevention: cryptographic chaining prevents attackers from covering tracks

**Cost model:**
- Assumptions: 100 tool calls/day, 2KB/event = ~6MB/month/agent
- At 6-month retention: ~36MB/agent
- At 1000 agents: ~36GB (storage is cheap)
- The expensive part: query infrastructure for incident investigation (OpenSearch/Loki)

---

### Closing (300 words)

Three actions:
1. Deploy sidecar logger on your most critical MCP server this week. Start with tool_call events only.
2. Set retention to 6 months. Use append-only storage.
3. Generate a sample Article 72 monitoring report from one week of data -- validates that your schema produces useful compliance output.

---

## Cross-references to include

- [MCP Security Top 10](https://aminrj.com/posts/owasp-mcp-top-10/) (the threat model this logging schema monitors for)
- [MCP Tool Poisoning PoC](https://aminrj.com/posts/mcp-tool-poisoning/) (the attack that tool_call logging detects)
- [GPAI Meets Agentic AI](https://aminrj.com/posts/gpai-meets-agentic-ai/) (EUAI-001 -- deployer obligation to maintain logs)
- Forward reference to EUAI-006 (AI Observability / Article 72, scheduled May 4)

## New deliverable

JSON schema definition -- publish as a GitHub gist alongside the article (aminrj-labs).

## Lab reuse

mcp-attack-labs Docker Compose (sidecar pattern) + Python agent (instrumentation diff).
