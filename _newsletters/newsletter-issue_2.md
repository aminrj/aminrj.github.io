---
title: Claude Code Supply Chain RCE, AI-Powered FortiGate Blitz, Infostealers Now Harvest AI Agent Souls
Subject: Claude Code Supply Chain RCE, AI-Powered FortiGate Blitz, Infostealers Now Harvest AI Agent Souls
Preview text: When your AI coding assistant's config files become an attack vector, a script kiddie with ChatGPT breaches 600 firewalls, and malware evolves to steal your agent's entire identity
issue: 2
date: 2026-03-02
---

Hey there 👋,

Welcome back to Issue #2 of AI Security Intelligence.

I started this newsletter because I found myself struggling to keep up with the mind-boggling speed at which Generative AI, LLMs, and Agentic AI are being embraced across every domain. And the Veracode 2026 report, covered below, confirms it with real-world numbers.

The security side of this adoption is either not taken seriously or not well understood, and the **consequences are far more severe than most people realize**.
Yes, AI and AI Agents seem to work magic. But let's not shoot ourselves in the foot by introducing attack surface with more consequences than we can afford to ignore.

Last week I said the pattern from DockerDash (untrusted context flowing through MCP into unvalidated tool execution) would repeat. **It took exactly seven days**. This week brought three critical Claude Code vulnerabilities exploiting the same trust boundary confusion, the first documented case of *infostealers* targeting AI agent identity files, and Amazon's forensic breakdown of a low-skill attacker using commercial AI to pop 600+ firewalls across 55 countries.

And of course, the **devastating ClawJacked** flaw that let malicious websites hijack local OpenClaw AI agents via WebSocket.

The theme this week is uncomfortable: the tools we're building to make developers faster are also making attackers faster, and the AI agents we're deploying are becoming high-value targets in their own right.

Dense issue. Let's get into it.

## AI Threats & Incidents

**[ClawJacked: Malicious Websites Can Hijack Local OpenClaw AI Agents via WebSocket](https://thehackernews.com/2026/02/clawjacked-flaw-lets-malicious-sites.html)**
_Oasis Security_ disclosed a high-severity vulnerability in OpenClaw's core gateway, codenamed **ClawJacked**, that allows any website to silently take over a locally running AI agent.

_The attack chain:_ malicious JavaScript on a web page opens a WebSocket connection to localhost on the OpenClaw gateway port, brute-forces the gateway password (no rate limiting), registers as a trusted device (auto-approved without user prompt for local connections), and gains complete control over the agent. From there, the attacker can interact with the agent, dump configuration data, enumerate connected nodes, and read application logs.

_The critical design flaw:_ the gateway relaxes several security mechanisms for local connections, including silently approving new device registrations. OpenClaw patched within 24 hours in version 2026.2.25. But the blast radius extends further: reports from Bitsight and NeuralTrust detail how exposed OpenClaw instances can be weaponized through prompt injections embedded in emails or Slack messages processed by the agent. *(OWASP: LLM01 Prompt Injection + LLM03 Supply Chain + LLM06 Excessive Agency)*

> **This is a full-spectrum attack on the agentic AI ecosystem, all in one week.** WebSocket hijacking of the core gateway, log poisoning for indirect prompt injection, a malicious skill marketplace with agent-to-agent social engineering. The Moltbook attack is especially worth studying: an AI agent posing as a legitimate peer on a social network for agents, promoting malicious skills to other agents who trust it by default.

**[Claude Code RCE + API Key Exfiltration via Malicious Repos (CVE-2025-59536, CVE-2026-21852)](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/)**
Check Point Research disclosed three critical vulnerabilities in Anthropic's Claude Code that turn repository configuration files into active attack vectors. The attack is devastatingly simple: an attacker commits a malicious `.claude/settings.json` to a repo, a developer clones and opens it, and Claude Code executes arbitrary commands before the trust dialog even appears. A stolen API key grants access to the entire Workspace: read/write all shared files, upload malicious content, exhaust credits. All three vulnerabilities are patched. *(OWASP: LLM03 Supply Chain + LLM06 Excessive Agency)*

> **This is the AI supply chain version of the classic "malicious .git hooks" attack, but worse.** Traditional git hooks require explicit execution; Claude Code's configuration files execute implicitly because the tool treats them as trusted operational logic.

**[AI-Augmented Threat Actor Breaches 600+ FortiGate Devices Across 55 Countries](https://aws.amazon.com/blogs/security/ai-augmented-threat-actor-accesses-fortigate-devices-at-scale/)**
_Amazon Threat Intelligence_ published a detailed forensic report on a Russian-speaking, financially motivated actor who used multiple commercial GenAI services to compromise 600+ FortiGate devices between January 11 and February 18, 2026. No vulnerabilities were exploited. The campaign succeeded entirely through exposed management ports and weak credentials with single-factor authentication. What makes this significant: the actor had limited technical skills. AI wrote their Python recon scripts, generated step-by-step attack plans from stolen network topologies, parsed and decrypted FortiGate configs, and planned lateral movement into Active Directory and Veeam backup infrastructure (a classic pre-ransomware pattern). **When the actor hit hardened environments, they simply moved on**. *(MITRE ATLAS: AML.T0054 AI-Assisted Techniques)*

> **This is the report that settles the "will AI help attackers?" debate.** Not theoretically, but forensically. Amazon's finding that a low-skill individual achieved the operational scale of a mid-tier APT group through AI augmentation is the clearest evidence yet that GenAI is a force multiplier for offense. **But note also that every single compromise would have been prevented by basic security hygiene**: no exposed management ports, no default credentials, MFA enabled.

**[First-Ever Infostealer Caught Stealing AI Agent Identity: OpenClaw Configuration Exfiltrated](https://thehackernews.com/2026/02/infostealer-steals-openclaw-ai-agent.html)**
_Hudson Rock_ documented the first in-the-wild case of infostealer malware harvesting an AI agent's complete identity. A Vidar variant's broad file-grabbing routine scooped up the victim's `.openclaw` directory, capturing: `openclaw.json` (gateway authentication token, email, workspace path), `device.json` (public and private cryptographic keys for device pairing), and `soul.md` + `MEMORY.md` (the agent's behavioral instructions, daily activity logs, private messages, and calendar data). *(OWASP: LLM02 Sensitive Information Disclosure + LLM03 Supply Chain)*

> **Hudson Rock calls this "the transition from stealing browser credentials to harvesting the souls and identities of personal AI agents."** That's not hyperbole. An OpenClaw identity file doesn't just give you a password; it gives you the agent's entire operational context, behavioral instructions, cryptographic keys, and a memory file that maps the victim's life. This is *identity theft* at a layer that didn't exist 18 months ago.

## Model Security & AI-on-AI Attacks

**[Anthropic Discloses Industrial-Scale Distillation Attacks by DeepSeek, Moonshot AI, and MiniMax](https://www.anthropic.com/news/detecting-and-preventing-distillation-attacks)**
Anthropic published detailed attribution of three distillation campaigns by Chinese AI labs that generated over 16 million exchanges with Claude through ~24,000 fraudulent accounts. DeepSeek (150K+ exchanges) targeted reasoning and censorship-safe alternatives to politically sensitive queries. Moonshot AI (3.4M+ exchanges) targeted agentic reasoning, tool use, computer-use agents, and later attempted to extract and reconstruct Claude's reasoning traces. MiniMax (13M+ exchanges) ran the largest campaign, targeting agentic coding and orchestration. Anthropic detected this while it was still active and watched MiniMax pivot 50% of traffic within 24 hours when a new Claude model dropped.

> **Two things matter here beyond the headline.** First, the operational tradecraft: load-balancing across accounts, mixing extraction traffic with legitimate requests, pivoting to new models within 24 hours of release. This isn't ad hoc, it's **a production-grade data pipeline for systematic capability theft**. Second, the national security angle: Anthropic specifically notes that illicitly distilled models are unlikely to retain safety guardrails.

## MCP & Agent Security

**[30 CVEs in 6 Weeks: MCP's Attack Surface Expands Into Three Distinct Layers](https://dev.to/kai_security_ai/30-cves-later-how-mcps-attack-surface-expanded-into-three-distinct-layers-ihp)**
Kai Security's autonomous scanning agent documented 30 CVEs across the MCP ecosystem between January and February 2026, revealing that the attack surface has expanded beyond the original server-layer exec() injection pattern into three distinct tiers. Layer 1 (43% of CVEs): the familiar exec()/shell injection family. Layer 2 (20%): tooling and infrastructure, including MCP inspectors, scanners, and host applications. Layer 3 (13%): authentication bypass on critical endpoints.

> **The meta-irony of a security scanner having command injection is almost too perfect.** But the real insight is the attack surface migration pattern: server fixes push attackers to tooling, tooling fixes will push them to client applications.

**[Kali Linux Ships Native Claude AI Integration via MCP](https://www.kali.org/blog/kali-llm-claude-desktop/)**
Kali Linux officially documented a native AI-assisted penetration testing workflow integrating Anthropic's Claude via MCP. The architecture: Claude Desktop (macOS/Windows) as the UI, Claude Sonnet 4.5 as the intelligence layer, and a Kali instance running `mcp-kali-server` (a Flask-based API on localhost:5000) as the execution layer.

## Reports & Research

**[Veracode 2026 State of Software Security: AI-Driven Development Outpaces Security](https://www.veracode.com/resources/analyst-reports/state-of-software-security-2026/)**
Veracode's annual report, based on 1.6 million applications generating 141.3 million raw findings, delivers a stark conclusion: "The velocity of development in the AI era makes comprehensive security unattainable." Key numbers: 82% of organizations now harbor security debt (up from 74% last year), 60% carry critical security debt (20% YoY increase), and high-risk vulnerabilities spiked 36% YoY. The report explicitly identifies AI-driven development as a factor: **more code ships faster, but remediation hasn't scaled to match**.

**[CoSAI Releases MCP Security Whitepaper: 12 Threat Categories, ~40 Distinct Threats](https://www.coalitionforsecureai.org/securing-the-ai-agent-revolution-a-practical-guide-to-mcp-security/)**
The Coalition for Secure AI (an OASIS Open Project backed by Anthropic, Google, IBM, Meta, Microsoft, NVIDIA, and others) released a comprehensive MCP security framework. The paper identifies 12 core threat categories spanning nearly 40 distinct threats. Key recommendations: end-to-end agent identity and traceability, least-privilege access for all MCP servers, zero-trust validation for AI outputs, and hardware-based isolation.

**[Cisco Expands AI Defense for the Agentic Era](https://newsroom.cisco.com/c/r/newsroom/en/us/a/y2026/m02/cisco-redefines-security-for-the-agentic-era.html)**
Cisco announced the largest expansion of AI Defense since its January 2025 launch. New capabilities include: **AI BOM** (Bill of Materials) for centralized visibility across AI assets including MCP servers and third-party dependencies; an MCP Catalog for discovering, inventorying, and managing risk across MCP servers and registries; advanced multi-turn algorithmic red teaming for models and agents across multiple languages; and real-time agentic guardrails that monitor for tool poisoning and unauthorized tool use.

## Governance & Compliance Watch

**NIST CAISI RFI: Comment Period Closes March 9**
The NIST AI agent security RFI (docket NIST-2025-0035) closes **March 9, 2026**. If you have operational experience securing agentic systems, especially around MCP, tool-use trust boundaries, or non-human identity management, submit your input.

**Anthropic-Pentagon Standoff Escalates**
Defense Secretary Hegseth declared Anthropic a "supply chain risk to national security" on Friday, restricting military contractors from doing business with the company. The dispute centers on Anthropic's refusal to remove certain safety guardrails from Claude's deployment on classified networks. The precedent matters: it establishes that an AI company's safety posture can be reframed as a supply chain risk.

## Tools & Resources

* **[CoSAI MCP Security Whitepaper](https://github.com/cosai-oasis/ws4-secure-design-agentic-systems/blob/mcp/model-context-protocol-security.md)** — The canonical MCP threat model. 12 threat categories, ~40 distinct threats.
* **[AgentAudit](https://agentaudit.dev)** — A security registry for AI agent packages. 194 packages audited, 118 findings.
* **[Adversa AI MCP Security Top 25](https://adversa.ai/blog/top-mcp-security-resources-february-2026/)** — Curated monthly digest of the most critical MCP security resources.
* **[mcp-kali-server](https://www.kali.org/blog/kali-llm-claude-desktop/)** — Official Kali Linux MCP server package for AI-assisted penetration testing.
* **[Kai Security MCP Scanner](https://mcp.kai-agi.com)** — Autonomous agent that has scanned 560 MCP servers and documented 30 CVEs.

## 💡 My Take

Three observations from this week.

**First, the AI tool supply chain is now a first-class attack surface and we need to talk about it more seriously.** Claude Code's `.claude/settings.json`, MCP's `.mcp.json`, OpenClaw's `.openclaw` directory: these are all config files that live in repos or on developer machines and that now have the power to execute code, redirect API traffic, and compromise entire workspaces.

**Second, we are getting our first empirical evidence of AI-augmented offense at scale.** The Amazon FortiGate report isn't a proof of concept or a red team exercise. It's a forensic analysis of a real campaign where a low-skill actor achieved enterprise-grade operational scale through GenAI.

**Third, AI agent identity is the next credential class that security teams need to protect.** The OpenClaw infostealer case shows that agent config directories containing gateway tokens, cryptographic keys, behavioral instructions, and memory files are now targets for commodity malware.

If I had to boil this week down to one sentence: **AI is simultaneously expanding the attack surface (via tools), amplifying the attacker (via GenAI), and creating entirely new target categories (via agent identity), all faster than the defensive ecosystem is adapting.**

— Amine Raji, PhD

## Wrapping Up

**If you found this useful**, forward it to one colleague who's deploying AI coding tools without auditing their config file trust model. They need this.

**Want the LLM & AI Agent Security Field Guide?** Complete OWASP LLM Top 10, Agentic Top 10, copy-paste detection patterns, and a 14-point security assessment checklist. Reply "field guide" and I'll send it over.

**Questions, comments, feedback?** Reply directly, I read everything.

See you next week.

Cheers,
Amine
