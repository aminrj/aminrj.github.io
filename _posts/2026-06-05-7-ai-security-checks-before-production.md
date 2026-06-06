---
title: 7 AI security checks before production
date: 2026-06-05
uuid: 202606050000
status: published
published: true
content-type: article
target-audience: intermediate
categories: [AI Security, Agentic AI, Production]
tags:
  [
    AI Security,
    Agentic AI,
    LLM,
    OWASP,
    Prompt Injection,
    MCP,
    Security,
    Checklist
  ]
image:
  path: /assets/media/ai-security/ai-security-checklist-production.png
description: If you have one day for an AI security review before launch, run these 7 checks first. They catch the majority of production incidents, and most teams skip at least three of them.
mermaid: false
---

Most AI security checklists have 40+ items. If you are three days from launch and have one afternoon, that list is not the tool you need.

These 7 checks target the controls whose absence appears most frequently in production incident post-mortems. Cisco's 2026 audit found prompt injection vulnerabilities in 73% of audited production AI deployments. The majority of those could have been caught by Check 1 alone.

They will not make your system bulletproof. They will catch the majority of issues that cause incidents. If your system passes all 7, you have a defensible baseline to build from.

![AI security checklist](/assets/media/ai-security/ai-security-checklist-production.png)

## Check 1: Test prompt injection resistance with an automated tool

**What it is:** Run an automated prompt injection test suite against your system before launch.

**What failure looks like:** The model follows instructions injected through user input, tool outputs, or retrieved documents. It overrides its system prompt or triggers unauthorized tool calls. This is still the number one attack vector in the OWASP LLM Top 10 2026.

**How to run it:** Set up [PyRIT](https://github.com/microsoft/PyRIT) (open source, MIT-licensed) and run it against your system endpoint using the built-in HarmBench and AdvBench datasets as a baseline. You need statistical results, an attack success rate across at least 500 variations, not a pass/fail from 10 manual tests. A 3% ASR sounds low and may represent thousands of successful attacks at scale.

**What most teams do instead:** Run 10 to 15 manual prompts, see no bypass, and mark it complete. Manual testing against a probabilistic system has no predictive validity. A model update the day before launch can invalidate every manual test result.

---

## Check 2: Define a tool allowlist, not a denylist

**What it is:** Your agent should only be permitted to call the specific tools required for its defined function. Everything else is blocked by default.

**What failure looks like:** An agent can call any registered tool, with controls only applied after the fact via monitoring. Attackers do not need to exploit code. They manipulate the model into calling a tool that was always available and never should have been accessible.

**How to run it:** List every tool your agent has access to. For each tool, ask whether this agent needs this capability to perform its defined job. If the answer is no, remove the tool from the registry. What remains is your allowlist. Document it and enforce it at the framework layer.

**What most teams do instead:** Register all available tools for convenience and plan to monitor for misuse. Monitoring is not a substitute for a restricted surface area. An agent that cannot call a tool cannot misuse it.

---

## Check 3: Validate every tool input parameter

**What it is:** Check 2 restricted which tools the agent can call. This check restricts what the model can pass into those tools once called. Both controls are necessary. Neither is sufficient alone.

Before any tool call is executed, validate the model-generated parameters against a defined schema.

**What failure looks like:** The model generates a tool call with attacker-influenced parameters. A file path that traverses outside the allowed directory. A database query with injected content. An API call to an unauthorized endpoint. The model did not produce harmful output. The harm is in the parameters it passed to a legitimate tool.

**How to run it:** For each tool in your allowlist, define an explicit parameter schema: allowed types, allowed value ranges, allowed path patterns. Implement server-side validation that rejects any call not conforming to the schema. Log every rejection with the full parameter payload. Those logs are your incident investigation record.

**What most teams do instead:** Trust that the model will generate reasonable parameters because the system prompt describes the intended use. System prompts are advisory to the model. They are not enforced constraints.

---

## Check 4: Issue scope-limited API keys per agent

**What it is:** Each agent gets its own identity with credentials scoped to the minimum permissions required for its defined function. No shared credentials. No broad-access keys.

**What failure looks like:** All agents share a single API key or service account with administrative access. A single successfully manipulated agent gives an attacker full access to every backend covered by that key, across every agent instance running in production.

**How to run it:** For each agent, create a dedicated service identity. Scope its permissions to the specific resources accessed in the agent's defined workflow. Test by attempting operations outside the defined scope. Those calls should fail. Document the scope as part of your deployment record.

**What most teams do instead:** Use a shared admin key because it is faster to set up. Credential scope is your most reliable blast-radius control. When other controls fail, and some will, credential scope determines how much damage is done.

---

## Check 5: Log every agent action with cryptographic signing

**What it is:** Every action your agent takes, every tool call, every parameter, every response, is logged with a tamper-evident signature in a system the agent itself cannot modify.

**What failure looks like:** Agents produce logs, but the logs are stored in a location the agent has write access to, or are stored without integrity protection. Post-incident investigation cannot establish what the agent actually did because the log chain cannot be trusted.

**How to run it:** Three tiers, depending on your infrastructure:

- **Cloud-native (easiest):** If running on AWS, GCP, or Azure, route agent action logs to CloudTrail, GCP Cloud Audit Logs, or Azure Monitor. These services provide integrity protection by default.
- **Self-hosted (medium):** Use an append-only log store (e.g., OpenSearch with index lifecycle management) with HMAC-SHA256 on each entry using a key the agent cannot access.
- **Minimal viable:** At minimum, log to a separate service account with no agent write permissions and verify hashes manually before any investigation relies on the logs.

**What most teams do instead:** Use standard application logging with the assumption that only legitimate processes write to the log store. AI agents create a new threat model for logging. A manipulated agent may be instructed to write misleading entries or overwrite records.

---

## Check 6: Scan MCP servers before installation

**What it is:** Before installing any MCP server, scan it, including its tool descriptions, for adversarial content.

**What failure looks like:** A developer installs an MCP server from a community registry. It passes malware scanning. Its tool descriptions contain embedded instructions that the agent will execute once the descriptions are loaded into its context window. The payload is not code. It is a text string that standard security tooling has no mechanism to flag. As of mid-2026, no dedicated scanning tool exists for MCP tool descriptions. Most teams rely on manual review.

**How to run it:** Review tool descriptions manually for instruction-like language that is not clearly operational documentation. Compute a hash of the tool descriptions at installation and store it. At every future reconnection, recompute the hash and compare. Tool descriptions can change server-side after you install the package.

**What most teams do instead:** Scan for malware and assume the tool descriptions are safe because they are not executable. [The full attack chain this check defends against is documented here.](/posts/2026-05-28-mcp-attack-chain-database-exfiltration/)

---

## Check 7: Validate outputs for sensitive data patterns

**What it is:** Before any agent response reaches the user or an external system, scan it for sensitive data patterns: PII, credentials, internal system references, data that should not leave your environment.

**What failure looks like:** The model includes a user's full account details, another user's information, or internal system credentials in a response. The model did not decide to leak this data. It was responding naturally to its context. No input validation was violated. No prompt injection was detected. The output was simply never checked.

**How to run it:** At minimum, scan every response with a regex for common PII patterns (SSN, credit card numbers, email addresses, phone numbers) and block if matched. Layer on a secondary model call for contextual PII if your system handles health or financial data. For regulated environments, integrate with your existing DLP provider rather than building a custom filter. The filter should run server-side, not in the client.

**What most teams do instead:** Focus security investment on input controls and assume that if the input was clean, the output will be safe. Output validation is the control that catches what input validation missed. It catches an entire class of data leakage that has no corresponding input-side trigger.

---

## What these 7 checks don't cover

These are a triage list. They are not a complete security posture.

They do not cover training data security, model provenance verification, fine-tuning corpora review, RAG knowledge base access controls, infrastructure hardening, agent-to-agent message authentication, NIST AI RMF governance mapping, or regulatory compliance documentation.

Those matter. They come after you have these 7 in place.

If your system passes all 7 checks, you have addressed the controls that appear most frequently in production incident post-mortems. You have a defensible baseline. You do not yet have a complete AI security program.

**Prioritization tip:** If you can only do 3 of the 7, start with Check 1 (prompt injection testing), Check 2 (tool allowlist), and Check 4 (scope-limited credentials). These three alone block the most common attack paths.

---

The full production checklist expands these 7 into 40+ controls with named owners and acceptance criteria, including a PyRIT configuration template for Check 1 and IAM policy templates for Check 4. [Read it here.](/posts/2026-05-23-ai-security-threat-modeling-production/)

---

<div style="background: var(--card-bg-color); border: 1px solid var(--border-color); border-radius: 8px; padding: 1.25rem; margin: 1.5rem 0;">
  <p style="margin: 0 0 0.75rem; font-weight: 600;">Download the full checklist</p>
  <p style="margin: 0 0 0.75rem; font-size: 0.9rem; color: var(--text-muted-color);">The <a href="/resources/predeployment-checklist/">AI Agent Pre-Deployment Security Checklist</a> has 25 controls across 5 families: probabilistic testing, supply chain, tool controls, injection defense, and sign-off. [Download the PDF →](/assets/pdfs/predeployment-checklist.pdf)</p>
  <p style="margin: 0; font-size: 0.85rem; color: var(--text-muted-color);">Also: <a href="/resources/containment-rubric/">Containment Rubric</a> · <a href="/resources/threat-model-checklist/">Threat Modeling Checklist</a></p>
</div>

For weekly AI security coverage, production incidents, framework updates, and what teams are actually missing before launch: [subscribe to the AI Security Intelligence newsletter.](/newsletter/)

---

*Amine Raji, PhD, CISSP. AI/LLM security. [Get in touch](/contact/) for pre-production security reviews.*
