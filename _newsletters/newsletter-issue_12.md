---
title: "Claude Mythos, SAFE-MCP, MCPShield: the week the research caught up with the threat."
Subject: "Claude Mythos, SAFE-MCP, MCPShield: the week the research caught up with the threat."
preview_text: "Claude Mythos found thousands of zero-days in 20 hours. Three new MCP research papers landed. And no existing defense covers the full attack surface."
issue: 12
date: 2026-05-20
---

Hey 👋,

Last night I spoke at OWASP Stockholm's Epicenter event. About 40 practitioners showed up. Linus Lagerhjelm from Builders opened with how they've deployed AI agents across their organization securely. I followed with the MCP security threat model: tool poisoning, cross-server attacks, the architectural RCE findings, what defenders need to implement before the next incident.

The discussion afterwards was the best part. The question that kept coming back — from people running agents in production financial and healthcare systems — wasn't "can we prevent these attacks." It was "how do we know when we've been hit." No behavioral baseline. No standard audit trail. Agents acting with legitimate credentials, on trusted tools, following instructions that came from untrusted content they processed upstream. Traditional controls need to be adapted.

That gap — the one between detection and response — is exactly what three new research papers published this month converge on.

---

## From the research front

**SAFE-MCP: the MITRE ATT&CK equivalent for MCP is live and worth adopting now**

If you haven't seen SAFE-MCP yet, check that this week. Built by Frederick Kautz (TestifySec) with community contributors, SAFE-MCP is an open-source TTP catalog for MCP environments. The Linux Foundation and OpenID Foundation have adopted it. It's structured like MITRE ATT&CK but specific to the agent-tool orchestration layer. 14 tactic categories, 80+ techniques, each with mitigation and detection guidance. From Initial Access to Impact, covering MCP hosts, clients, servers, LLMs, and tool/resource surfaces.

Technique examples that will be familiar from previous issues: SAFE-T1001 (Tool Poisoning), SAFE-T1102 (Prompt Injection), OAuth token theft and replay, capability chaining (combining individually benign tool calls to achieve an unauthorized outcome), rug-pull via `tools/list` mutation, memory poisoning across sessions.

For red teams, it's a structured reference for designing MCP-specific test cases. Defenders get technique-by-technique links to MITRE ATT&CK equivalents, so you can map coverage to existing controls instead of starting from scratch. Compliance folks get a vocabulary for documenting MCP threat coverage that existing frameworks don't have.

> **Why this matters now and not later:** the OWASP Agentic Top 10 covers what can go wrong. SAFE-MCP covers *how* attackers achieve it — the specific mechanics at the protocol level. For anyone building a threat model or running a red team exercise against an MCP deployment, these are complementary tools. Start with OWASP ASI codes to prioritize risk categories, then use SAFE-MCP techniques to design the actual test cases.

[safemcp.org →](https://www.safemcp.org)
[github.com/safe-agentic-framework/safe-mcp →](https://github.com/safe-agentic-framework/safe-mcp)

**MCPShield (arXiv:2604.05969): formal framework with one uncomfortable finding — no existing defense provides complete coverage**

Published April 7, this is the most rigorous academic work on MCP security to date. The headline contribution: a hierarchical threat taxonomy with 7 categories, 23 distinct attack vectors organized across four attack surfaces, grounded in empirical analysis of 177,000+ registered MCP tools. The uncomfortable finding: they evaluated 12 existing defense mechanisms against the taxonomy and concluded that none provides complete coverage.

The four attack surfaces the taxonomy organizes around: tool invocation (the request/response chain), context injection (how untrusted content enters the LLM context), cross-boundary communication (trust model failures between agent, server, and host), and supply chain (compromised tools, malicious registries). Their reference architecture — MCPShield — integrates capability-based access control, cryptographic tool attestation, information flow tracking, and runtime policy enforcement as the minimum viable defense stack.

If you followed the OX Security architectural RCE from Issue #11, this finding on tool attestation will be familiar: signed tool manifests would prevent malicious STDIO configurations from being trusted without verification. This is the protocol-level fix Anthropic declined to implement. The academic community is now formalizing it as a required control.

> **The gap MCPShield quantifies:** action-capable tools went from 27% to 65% of the MCP ecosystem between late 2024 and early 2026. That shift from "read data" to "change state" is the attack surface expansion no single existing defense covers end-to-end. Behavioral baselining, cross-session drift detection, and fleet-scale tool description fingerprinting are all identified as open research problems — not solved by any current tool.

[arXiv:2604.05969 →](https://arxiv.org/abs/2604.05969)

**MCP-38 (arXiv:2603.18063): 38 threat categories derived from examining every line of the MCP spec**

A March 2026 paper takes a different approach. Instead of building top-down from observed attacks, it examined every normative element of the MCP specification and derived 38 threat categories from the protocol design itself. Tool discovery, invocation, transport selection, multi-server routing — each examined as a potential attack surface.

The result covers attack patterns that appear in no existing framework because they're specific to MCP's protocol-layer trust model: compositional multi-tool attack paths (where individually permitted calls chain into unauthorized outcomes), transport-selection downgrade attacks, and multi-server routing manipulation. The paper maps these to STRIDE and OWASP categories where possible, and identifies the gaps where no existing framework applies.

This is the paper to read before designing MCP security controls — not because it tells you what to build, but because it tells you where the spec itself creates attack surface that implementation-level defenses can't address.

[arXiv:2603.18063 →](https://arxiv.org/abs/2603.18063)

## This week in AI security

**Claude Mythos: thousands of zero-days, 20-hour exploit window, 99% still unpatched**

Anthropic dropped news on April 7: Claude Mythos Preview autonomously discovered thousands of previously unknown vulnerabilities across every major OS and web browser — including flaws that survived decades of review. 181 working Firefox exploits in one benchmark. A 27-year-old OpenBSD flaw. A 20-gadget ROP chain against FreeBSD developed without human direction. The UK's AISI independently confirmed Mythos is the first AI model to complete an end-to-end simulated 32-step network attack and solve 73% of expert-level CTF challenges.

The number that changes everything: time-to-exploit collapsed from 2.3 years in 2018 to 20 hours in 2026, according to the Zero Day Clock project. Each patch disclosure under Project Glasswing — Anthropic's coordinated program with about 40 vendors — also signals to attackers where to look. The average remediation time for high/critical CVEs is still 74 days. That gap is now an active exploit window.

Over 99% of Mythos-discovered vulnerabilities remain unpatched — not because they're obscure, but because the volume is overwhelming coordinated disclosure infrastructure.

I wrote a longer analysis on what comes after discovery — the validation crisis that most Mythos commentary is missing. [Read it here →](https://aminrj.com/posts/ai-security-validation-crisis/)

> **The economics, not the capability:** Mythos matters because it changes the cost of vulnerability discovery. Finding bugs and writing working exploits are becoming cheaper and less dependent on scarce human expertise. Attackers who previously needed a specialist team now need a model and a task. What's slower to change is the defender side: patch cycles, disclosure coordination, remediation capacity. That asymmetry is the risk.

> **Posture change:** if your vulnerability management program runs on periodic scans and CVSS-scored ticket queues, the Mythos disclosure is the moment to start moving toward continuous monitoring with risk-based prioritization. Patch cycles measured in days, not weeks. Each new Glasswing disclosure is a signal — to you and to attackers simultaneously.

[AISI evaluation →](https://www.aisi.gov.uk/blog/our-evaluation-of-claude-mythos-previews-cyber-capabilities)
[TechRadar analysis →](https://www.techradar.com/pro/claude-mythos-turns-years-of-security-research-into-20-hour-ai-exploits)

**CVSS 10.0: Semantic Kernel's accidental tool exposure turned prompts into host RCE. Patched. The pattern isn't.**

Microsoft published the research on May 7. Two vulnerabilities in Semantic Kernel — the open-source AI orchestration framework powering Copilot integrations — turned a crafted prompt into host-level code execution.

CVE-2026-26030 (Python SDK, patched in ≥1.39.4): the In-Memory Vector Store's filter passed a user-controlled parameter directly to `eval()`. A prompt injection reached `eval()` and executed arbitrary code. Microsoft's demo: a hotel-finder agent, one prompt, `calc.exe` running on the server.

CVE-2026-25592 (CVSS 10.0, .NET SDK, patched in ≥1.71.0): `DownloadFileAsync`, a file-transfer helper, was accidentally tagged `[KernelFunction]` and made callable by the AI model. A prompt injection wrote attacker-controlled content to the Windows Startup folder.

Both patched. The `[KernelFunction]` pattern is not.

> **The accidental exposure class:** any function tagged as LLM-callable is a security boundary. CVE-2026-25592 happened because a developer convenience became an LLM-callable tool with no path validation. This pattern exists in any framework where tool registration is automatic or convention-based. Audit every tagged function for path, URL, or query parameters — those are your injection sinks.

> **If you use Semantic Kernel:** upgrade Python SDK to ≥1.39.4 and .NET SDK to ≥1.71.0. Disable `AutoInvokeKernelFunctions` on any agent with disk, shell, or production data access. Microsoft packaged the vulnerable hotel-finder agent as a CTF challenge — worth running in a sandbox before your next security training session.

[Microsoft security blog →](https://www.microsoft.com/en-us/security/blog/2026/05/07/prompts-become-shells-rce-vulnerabilities-ai-agent-frameworks/)

**ShareLeak + PipeLeak: Microsoft patched. Salesforce patched the URL channel. The email path still works.**

Capsule Security published research on two indirect prompt injection vulnerabilities hitting production enterprise agents. CVE-2026-21520 (ShareLeak, CVSS 7.5): a crafted SharePoint form payload injected a fake system-role message into a Copilot Studio agent, directing it to query SharePoint Lists for customer data and send it via Outlook to an attacker-controlled email. No privileges required. Microsoft's safety mechanisms flagged the attack as suspicious. The data exfiltrated anyway. Patched January 15, CVE assigned.

PipeLeak hit Salesforce Agentforce through Web-to-Lead forms. Structurally identical. No CVE assigned by Salesforce. The URL exfil path was patched. According to Capsule's research, the email channel remains exploitable. Salesforce's recommended mitigation: human-in-the-loop. Capsule's response: "If the human should approve every single operation, it's not really an agent."

Both attacks exploited the same configuration: untrusted input, sensitive data access, and outbound communication. That configuration is also what makes agents useful. It cannot be patched out of the design.

> **The patch closes one syntax. The architecture remains.** Any Copilot Studio agent triggered by untrusted external input with access to SharePoint data and Outlook is exposed to injection variants. Defense requires governance-plane enforcement at the action layer — not model-layer safety filters that can be overridden by a sufficiently crafted payload. ShareLeak proved that even when the safety filter fires, the action can still execute.

> **If you run Copilot Studio:** the exposure window for ShareLeak was November 24, 2025 → January 15, 2026. Audit agents triggered by SharePoint forms for IoCs in that window. For PipeLeak: if your Agentforce agents process untrusted form input and can send email, the attack path exists. No CVE, no patch, no official advisory.

[Dark Reading →](https://www.darkreading.com/cloud-security/microsoft-salesforce-patch-ai-agent-data-leak-flaws) · [VentureBeat deep-dive →](https://venturebeat.com/security/microsoft-salesforce-copilot-agentforce-prompt-injection-cve-agent-remediation-playbook)

## Tooling worth knowing

- **SAFE-MCP** — 14-tactic, 80+ technique TTP catalog for MCP environments, structured like MITRE ATT&CK. Adopted by the Linux Foundation and OpenID Foundation. Use this when designing red team test cases or mapping MCP threat coverage to existing controls. [safemcp.org →](https://www.safemcp.org)

- **MCP Pitfall Lab** (from Adversa AI's May MCP digest) — a six-class pitfall taxonomy (P1–P6) for MCP developers, with a static analyzer that catches four classes automatically (F1=1.0). Practical complement to MCPShield's formal framework: the taxonomy describes the mistakes, the analyzer catches them. [Adversa AI May MCP digest →](https://adversa.ai/blog/top-mcp-security-resources-may-2026/)

- **Semantic Kernel CTF** — Microsoft packaged the vulnerable hotel-finder agent from the CVE-2026-26030 research as a hands-on challenge. Worth running if you're preparing agent security assessments. [Microsoft security blog →](https://www.microsoft.com/en-us/security/blog/2026/05/07/prompts-become-shells-rce-vulnerabilities-ai-agent-frameworks/)

- **mcp-attack-labs** — lab code for all the attacks covered in this newsletter's MCP series, updated with the OX Security four-family taxonomy. Runs locally. [github.com/aminrj-labs/mcp-attack-labs →](https://github.com/aminrj-labs/mcp-attack-labs)

## One thing to check this week

If SAFE-MCP is new to you: spend 20 minutes on the technique table. Filter for techniques tagged "Execution" and "Credential Access" — those are the two tactic categories most likely to produce an incident you don't detect until later. For each technique, ask whether your current MCP deployment has a detection mechanism or a prevention control. Most teams will find gaps in both columns. That's your hardening backlog.

## What I'm watching

→ **The behavioral baseline problem** — every conversation at OWASP Stockholm came back to the same gap: no standard way to define normal agent behavior. MCPShield, SAFE-MCP, and the MCP-38 taxonomy all identify this as an open problem. The first team to ship a practical baseline standard wins a category.

→ **Project Glasswing patch wave** — about 40 vendors have early Mythos findings. Each patch disclosure doubles as a reverse-engineering signal to attackers. Watch for exploitation clusters around disclosure dates.

→ **PipeLeak email channel** — no CVE, no patch, no advisory from Salesforce. Active attack path in one of the most widely deployed enterprise agent platforms.

→ **SAFE-MCP adoption** — adopted by the Linux Foundation and OpenID Foundation. If this becomes a compliance reference the way ATT&CK did, MCP threat modeling shifts from optional to expected. Worth getting ahead of.

If you were at OWASP Stockholm last night — thanks for the conversation. The question about production system detection is the one I'm taking back to the lab.

Questions, pushback, topics — reply directly, I read everything.

Cheers,
**Amine**
