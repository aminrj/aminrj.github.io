---
title: "MCP Tool Poisoning Is an EU AI Act Violation -- Here Is Which Articles It Breaks"
date: 2026-03-24
uuid: 202603240000
draft: true
status: draft
published: false
content-type: article
target-audience: advanced
categories: [AI Security, EU AI Act, Compliance]
tags:
  [
    EU AI Act,
    MCP,
    Tool Poisoning,
    Article 15,
    Article 9,
    Agentic AI,
    Compliance,
    Prompt Injection,
  ]
description: "The MCP tool poisoning attack demonstrated in our local proof-of-concept is not just a security vulnerability -- it is a direct violation of EU AI Act Articles 9 and 15. Here is the mapping."
---

The MCP tool poisoning attack works by embedding hidden instructions in MCP tool descriptions. A capable model reads them, follows them silently, and exfiltrates data while returning a normal-looking response to the user. I [demonstrated this attack fully offline](https://aminrj.com/posts/mcp-tool-poisoning/) using LM Studio and a custom Python agent earlier this year. The lab code is open source, the exploit is reproducible in under two minutes, and the attack requires zero sophistication from the attacker.

That article covered the security implications. This one covers what the same attack means under the EU AI Act -- because tool poisoning does not just break your system, it breaks at least three regulatory obligations.

---

## Article 15(4): Resilience Against Exploitation

Article 15(4) of the [EU AI Act](https://artificialintelligenceact.eu/article/15/) requires high-risk AI systems to be "resilient against attempts by unauthorized third parties to alter their use, outputs, or performance by exploiting system vulnerabilities."

Tool poisoning is a textbook case. The attacker alters the system's behavior by exploiting a vulnerability in the MCP protocol: tool descriptions are implicitly trusted by the model. The hidden instruction changes the agent's output (it exfiltrates files instead of performing the requested task) and the attacker is an unauthorized third party (the poisoned MCP server operator).

An MCP deployment vulnerable to tool poisoning fails Article 15(4) on its own terms. The regulation does not require novel attack research to identify this -- the vulnerability class is [documented](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks), [catalogued by OWASP](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/), and [reproducible with open-source tooling](https://aminrj.com/posts/mcp-tool-poisoning/).

**The control that satisfies Article 15(4):** Tool description scanning and hash verification before execution. In the [proof-of-concept lab](https://aminrj.com/posts/mcp-tool-poisoning/), this is implemented as a pre-flight check: before the agent calls any tool, it hashes the tool description and compares it against a known-good baseline. If the description has changed, the call is blocked. This is a sub-millisecond operation that prevents the entire attack chain.

---

## Article 9(2)(b): Risk Identification

Article 9 establishes the [risk management system](https://artificialintelligenceact.eu/article/9/) that providers of high-risk AI systems must implement. Article 9(2)(b) requires "estimation and evaluation of the risks that may emerge when the high-risk AI system is used in accordance with its intended purpose and under conditions of reasonably foreseeable misuse."

Tool poisoning is a reasonably foreseeable risk of any MCP deployment. The attack does not require the user to do anything unusual -- it occurs during normal operation when the agent reads a tool description that has been modified. An organization that deploys MCP-connected agents without identifying tool poisoning in its risk assessment has failed Article 9(2)(b).

**The evidence that satisfies Article 9(2)(b):** A documented risk assessment that includes tool description manipulation as a threat vector, with the severity, likelihood, and mitigation status recorded. The [MCP Security Top 10](https://aminrj.com/posts/owasp-mcp-top-10/) provides the threat taxonomy. The tool poisoning lab provides the attack evidence. The pre-flight hash check provides the mitigation evidence. Together, these three artifacts form a complete Article 9 risk record for this specific threat.

---

## Article 26(5): Deployer Monitoring Obligation

If you are deploying (not providing) an agentic AI system that uses MCP, [Article 26(5)](https://artificialintelligenceact.eu/article/26/) requires you to "monitor the operation of the high-risk AI system on the basis of the instructions of use."

In the tool poisoning scenario, the agent silently diverted from its intended behavior and the user saw a normal-looking response. There was no monitoring in place that would have caught the diversion. The deployer was unaware the attack occurred. This is an Article 26(5) monitoring failure.

**The control that satisfies Article 26(5):** Structured logging of every tool call with input parameters, output content, and the model's decision rationale. When the agent calls an unexpected tool or passes unexpected parameters, the log entry becomes the detection signal. This logging architecture is the subject of a [dedicated article in this series](https://aminrj.com/posts/eu-ai-act-logging-agentic-ai/).

---

## Mapping: Attack Step to Article to Control

| Attack step | Article violated | Required control | Lab status |
|---|---|---|---|
| Poisoned tool description loaded | Art. 15(4) -- resilience against exploitation | Tool description hash verification | [Demonstrated](https://aminrj.com/posts/mcp-tool-poisoning/) |
| Agent follows hidden instruction | Art. 14 -- human oversight | Approval gate for sensitive tool calls | Covered in CISO Playbook |
| File exfiltrated silently | Art. 26(5) -- deployer monitoring | Structured tool call logging | Schema in [EUAI-002](https://aminrj.com/posts/eu-ai-act-logging-agentic-ai/) |
| User sees normal response | Art. 50 -- transparency | Output provenance metadata | Planned (EUAI-007) |
| No risk assessment existed | Art. 9(2)(b) -- risk identification | Documented threat model | [MCP Security Top 10](https://aminrj.com/posts/owasp-mcp-top-10/) |

---

## What to Do

If you operate MCP-connected agents that could fall under Annex III high-risk classification:

1. **Run the lab.** Clone [mcp-attack-labs](https://github.com/aminrj-labs/mcp-attack-labs) and reproduce the tool poisoning attack against your own configuration. If the attack succeeds, you have an Article 15(4) gap.

2. **Add tool description hashing.** The pre-flight check is the minimum viable control. It adds sub-millisecond latency and blocks the most documented MCP attack vector.

3. **Document the risk.** Add tool description manipulation to your Article 9 risk register. Reference the OWASP Agentic Security Initiatives [ASI02 (Tool Misuse & Exploitation)](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/) as the risk category.

4. **Start logging tool calls.** Even before you have a full Article 12 schema, logging tool name + input hash + output hash + timestamp for every call gives you forensic capability and Article 26(5) monitoring evidence.

The full deployer obligation chain is covered in [GPAI Meets Agentic AI](https://aminrj.com/posts/gpai-meets-agentic-ai/). The logging architecture is in [EU AI Act Logging Requirements](https://aminrj.com/posts/eu-ai-act-logging-agentic-ai/).

---

*This article is part of a series mapping agentic AI security research to EU AI Act compliance requirements. The technical proof-of-concept is at [MCP Security: Tool Poisoning & Prompt Injection](https://aminrj.com/posts/mcp-tool-poisoning/). The complete MCP threat model is at [MCP Security Top 10](https://aminrj.com/posts/owasp-mcp-top-10/).*
