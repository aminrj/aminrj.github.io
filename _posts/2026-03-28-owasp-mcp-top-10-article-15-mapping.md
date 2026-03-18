---
title: "Mapping the MCP Security Top 10 to EU AI Act Article 15: A Compliance Cross-Reference"
date: 2026-03-28
uuid: 202603280000
draft: true
status: draft
published: false
content-type: article
target-audience: advanced
categories: [AI Security, EU AI Act, Compliance]
tags:
  [
    EU AI Act,
    Article 15,
    MCP,
    OWASP,
    Cybersecurity,
    Agentic AI,
    Compliance,
    Threat Model,
  ]
description: "Each of the 10 MCP-specific security risks maps to a specific Article 15 cybersecurity sub-clause. Here is the cross-reference table that turns a threat model into compliance evidence."
---

[Article 15](https://artificialintelligenceact.eu/article/15/) of the EU AI Act requires high-risk AI systems to achieve "an appropriate level of accuracy, robustness, and cybersecurity." For MCP-connected agentic AI, the cybersecurity requirement in Article 15(4) is the most operationally demanding: systems must be "resilient against attempts by unauthorized third parties to alter their use, outputs, or performance by exploiting system vulnerabilities."

The [MCP Security Top 10](https://aminrj.com/posts/owasp-mcp-top-10/) is a practitioner's threat model that catalogs ten MCP-specific risks with lab-confirmed attack chains, severity ratings, and protocol-level mitigation proposals. It was written as a security reference. But every risk in it maps directly to an Article 15 resilience requirement -- which means addressing the MCP Security Top 10 simultaneously builds the cybersecurity compliance evidence that Article 15 demands.

This article provides the cross-reference.

---

## How Article 15 Structures Cybersecurity Requirements

Article 15 is not a single requirement. It contains four sub-clauses relevant to MCP security:

- **Article 15(1):** High-risk AI systems must achieve an appropriate level of cybersecurity, and this level must be "appropriate in light of the risks."
- **Article 15(3):** Systems must be resilient to "errors, faults, or inconsistencies that may occur within the system or the environment."
- **Article 15(4):** Systems must be resilient against "attempts by unauthorized third parties to alter their use, outputs, or performance by exploiting system vulnerabilities," including data poisoning, adversarial examples, model flaws, and confidentiality attacks.
- **Article 15(5):** Technical solutions must be "appropriate to the relevant circumstances and the risks."

Each sub-clause governs different attack categories. The mapping below assigns each MCP Security Top 10 risk to the most specific sub-clause.

---

## The Cross-Reference Table

| MCP Security Risk | Article 15 sub-clause | Rationale | Hardening control | Lab evidence |
|---|---|---|---|---|
| **MSR-01: Tool Description Poisoning** | Art. 15(4) -- unauthorized third-party exploitation | Attacker embeds hidden instructions in tool descriptions to alter agent behavior | Tool description hash verification, pre-flight scanning | [Tool Poisoning PoC](https://aminrj.com/posts/mcp-tool-poisoning/) |
| **MSR-02: Cross-Server Tool Shadowing** | Art. 15(4) -- unauthorized alteration of use | Malicious server registers tool with same name as trusted server, hijacking calls | Server identity verification, tool namespace isolation | [OWASP Agentic Top 10 in Practice](https://aminrj.com/posts/owasp-agentic-top-10-in-practice/) |
| **MSR-03: Excessive Permission Grants** | Art. 15(1) -- appropriate level of cybersecurity | Tools granted broader permissions than needed, expanding blast radius | Least-privilege tool policies, per-tool permission scoping | [OpenClaw Deployment](https://aminrj.com/posts/openclaw-secure-deployment/) |
| **MSR-04: Insecure Credential Storage** | Art. 15(4) -- confidentiality attacks | API keys and tokens stored in plaintext in MCP server configurations | Credential injection via environment variables, secret manager integration | [MCP's First Year](https://aminrj.com/posts/mcp-security-after-1year/) |
| **MSR-05: Unvalidated Tool Inputs** | Art. 15(3) -- resilience to errors and faults | Agent passes unsanitized user input to tools, enabling injection | Input validation at tool boundary, parameter schema enforcement | [MCP's First Year](https://aminrj.com/posts/mcp-security-after-1year/) (CVE analysis) |
| **MSR-06: Unbounded Resource Consumption** | Art. 15(1) -- appropriate cybersecurity level | Agent enters tool-calling loops, exhausting compute or API quotas | Call rate limiting, loop detection, execution budgets | Architectural control (no specific lab) |
| **MSR-07: Lack of Transport Security** | Art. 15(4) -- confidentiality attacks | MCP stdio transport has no encryption; SSE transport may lack TLS | TLS enforcement for remote servers, transport layer authentication | [MCP's First Year](https://aminrj.com/posts/mcp-security-after-1year/) (scan data) |
| **MSR-08: Insufficient Logging** | Art. 15(1) + Art. 12 -- logging as cybersecurity prerequisite | No structured logging of tool calls, making incident investigation impossible | Structured event logging schema | [EUAI-002](https://aminrj.com/posts/eu-ai-act-logging-agentic-ai/) |
| **MSR-09: Server Identity Spoofing** | Art. 15(4) -- unauthorized third-party alteration | Attacker impersonates trusted MCP server to inject malicious tools | Server certificate pinning, mutual TLS, server registry | [OWASP Agentic Top 10 in Practice](https://aminrj.com/posts/owasp-agentic-top-10-in-practice/) |
| **MSR-10: Supply Chain Compromise** | Art. 15(4) -- exploitation of system vulnerabilities | Attacker compromises an MCP server package or dependency | Dependency pinning, integrity verification, SBOMs | [DockerDash Attack](https://aminrj.com/posts/docker-dash-mcp-attack/) (Threat Model B) |

---

## Reading the Table as Compliance Evidence

A regulator assessing Article 15 compliance will ask three questions:

1. **What threats did you identify?** The MCP Security Top 10 is the answer. It is a documented, risk-specific threat model with severity ratings.

2. **What controls did you implement?** The "Hardening control" column lists the specific technical measure for each threat. Each one is architecturally concrete -- not a policy statement.

3. **How do you know the controls work?** The "Lab evidence" column links to reproducible proof-of-concept attacks that were tested against the controls. This is stronger evidence than a vendor assessment or a configuration audit.

Together, the three columns form a complete Article 15(4) resilience narrative for MCP deployments: identified threats, implemented controls, verified effectiveness.

---

## What This Table Does Not Cover

Article 15 also requires accuracy (15(1)) and robustness (15(3)) beyond cybersecurity. For agentic AI systems, accuracy and robustness testing requires automated red teaming -- which is covered in the [LLM Red Teaming Tools](https://aminrj.com/posts/attack-patterns-red-teaming/) article and will be mapped to Article 15 compliance evidence in a dedicated piece (EUAI-005, scheduled April 20).

The cross-reference between the full OWASP Agentic Top 10 (not MCP-specific) and EU AI Act Articles 9, 12, 14, 15, and 72 will be published as the definitive 10x5 compliance matrix in EUAI-011 (scheduled June 15).

---

## What to Do

1. **Use the table as your Article 15 work plan.** Start from the top. MSR-01 (tool description poisoning) has the most complete lab evidence and the simplest control.

2. **Prioritize by existing lab status.** Six of the ten risks have published, reproducible lab evidence. Start with those -- your compliance evidence is already built.

3. **Document what you implement.** For each row, record: date control was implemented, configuration reference, test results. This becomes your Article 15 compliance file.

The full MCP threat model with protocol-level analysis and spec proposals is at [MCP Security Top 10: A Practitioner's Threat Model](https://aminrj.com/posts/owasp-mcp-top-10/).

---

*This article is part of a series mapping agentic AI security research to EU AI Act compliance requirements. The deployer obligation chain is at [GPAI Meets Agentic AI](https://aminrj.com/posts/gpai-meets-agentic-ai/). The logging architecture for Article 12 is at [EU AI Act Logging Requirements](https://aminrj.com/posts/eu-ai-act-logging-agentic-ai/).*
