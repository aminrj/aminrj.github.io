---
title: DockerDash MCP Takeover, vLLM CVSS 9.8 RCE, Cisco State of AI Security 2026
Subject: DockerDash MCP Takeover, vLLM CVSS 9.8 RCE, Cisco State of AI Security 2026
Preview text: When image metadata becomes remote code execution, your AI inference servers are pre-auth targets, and Cisco confirms lab attacks have gone live.
issue: 1
date: 2026-02-23
---

Hey there,

Hope you are doing well.

Welcome to Issue #1 of AI Security Intelligence.

I'm building this newsletter because I keep having the same conversation with security engineers and CISOs: *"We're deploying agents, but we don't know what we don't know."*

This is the fix. Every week I curate 40+ AI security sources so you don't have to.
You get the incidents, the CVEs, the framework updates, and the tools—with OWASP and ATLAS mapping so you can immediately translate to your threat models.

This first issue is a dense one. Let's get into it.

## AI Threats & Incidents

**[DockerDash: Two Attack Paths, One AI Supply Chain Crisis](https://noma.security/blog/dockerdash-two-attack-paths-one-ai-supply-chain-crisis/)**
Noma Labs disclosed a critical flaw in Docker's Ask Gordon AI assistant where a single malicious metadata LABEL in a Docker image compromises the entire Docker environment. The attack chain: Gordon AI reads and interprets the malicious instruction → forwards it to the MCP Gateway → which executes it through MCP tools. Zero validation at every stage. Impact is critical RCE in cloud/CLI environments and high-impact data exfiltration (container configs, environment variables, network topology, mounted directories) in Docker Desktop. Docker patched in v4.50.0 with human-in-the-loop confirmation before MCP tool invocation and image URL blocking.

Noma calls this **Meta-Context Injection**—the MCP Gateway cannot distinguish between informational metadata and pre-authorized executable instructions. This is the semantic gap problem applied to tool execution. *(OWASP: LLM01 Prompt Injection + LLM03 Supply Chain + LLM06 Excessive Agency)*

> **The takeaway:** This is the most important AI security disclosure in weeks, not because it's Docker-specific but because the pattern—untrusted context → AI interpretation → MCP forwarding → tool execution with no validation—will repeat across every MCP-enabled tool. If you're building agents with MCP, ask yourself: who validates what the gateway forwards? If the answer is "no one," you have the same vuln class.

**[CVE-2026-22778: Critical vLLM RCE via Malicious Video URL (CVSS 9.8)](https://github.com/advisories/GHSA-4r2x-xpjr-7cvv)**
A chained exploit in vLLM (3M+ monthly downloads) allows unauthenticated RCE by submitting a malicious video link to the API. Stage 1: PIL error messages leak a heap address, reducing ASLR from ~4 billion guesses to ~8. Stage 2: heap overflow in OpenCV/FFmpeg's JPEG2000 decoder overwrites function pointers → arbitrary command execution. Default vLLM installs require no authentication, and even with API keys configured, the exploit works through the invocations route pre-auth. Affects versions 0.8.3 through 0.14.0. **Patch to 0.14.1 immediately.** If you can't patch, disable video model endpoints and restrict API network access. *(OWASP: LLM03 Supply Chain, LLM05 Insecure Output Handling)*

> **The chain here is elegant and terrifying.** A video URL → memory leak → ASLR bypass → heap overflow → RCE. And vLLM is often deployed in GPU clusters meaning one compromised node gives a foothold for lateral movement across your most expensive infrastructure.

**[AI Chat App Leak Exposes 300M Messages from 25M Users](https://www.malwarebytes.com/blog/news/2026/02/ai-chat-app-leak-exposes-300-million-messages-tied-to-25-million-users)**
Chat & Ask AI—a wrapper app using OpenAI, Anthropic, and Google models with 50M+ users—left its Firebase database publicly accessible without authentication. An independent researcher accessed 300 million messages including full chat histories, model selections, and user settings. The root cause is Firebase Security Rules left in public mode. The same researcher found this misconfiguration in 103 of 200 iOS apps scanned. *(OWASP: LLM02 Sensitive Information Disclosure)*

> **The AI model isn't your only attack surface.** This breach had nothing to do with prompt injection or adversarial ML—it was a standard cloud misconfiguration that happened to expose AI conversation data.

## MCP & Agent Security

**[MCP Security Issues Threatening AI Infrastructure (MCP Horror Stories #1)](https://www.docker.com/blog/mcp-security-issues-threatening-ai-infrastructure/)**
Docker launched a blog series documenting real security issues in the MCP ecosystem. Key numbers: OAuth-related vulnerabilities represent the most severe attack class, command injection flaws affect **43% of analyzed MCP servers**, and the mcp-remote package (558K+ downloads) has a supply chain vulnerability affecting hundreds of thousands of developer environments. The post also covers path traversal (22% of servers exhibit file leakage vulnerabilities), unrestricted network access enabling C2 communication, and tool poisoning via malicious descriptions.

> **43% command injection rate across MCP servers.** If you're deploying MCP servers, read the Docker series and run Cisco's new MCP scanner against your setup this week.

**[1Password's SCAM Benchmark: Teaching AI Agents Not to Get Phished](https://1password.com/blog/ai-agent-security-benchmark)**
1Password built SCAM (Security Comprehension and Awareness Measure), an open-source benchmark testing whether AI agents can avoid phishing and credential theft during real tasks. They tested 8 models across 30 scenarios. Baseline results: scores ranged from 35% (Gemini 2.5 Flash) to 92% (Claude Opus 4.6), with **every model committing critical failures** like typing real passwords into phishing pages. Adding a 1,200-word security skill file reduced total critical failures from 287 to 10 across all runs. *(OWASP Agentic: ASI01 Agent Goal Hijack, ASI03 Identity & Privilege Abuse)*

## Reports & Research

**[Cisco State of AI Security 2026 Report](https://blogs.cisco.com/ai/cisco-state-of-ai-security-2026-report)**
Cisco's flagship AI security report dropped this week. The headline: AI vulnerabilities that were lab-only concepts have now materialized in production. Key findings: 83% of organizations planned agentic AI deployment but only 29% felt truly ready to secure it. The report covers prompt injection evolution, AI supply chain fragility, MCP risk surfaces, and adversaries using agents for attack campaigns. Cisco's AI Threat Intelligence team also released **open-source scanners for MCP, A2A, and agentic skill files**—directly relevant given DockerDash.

**[International AI Safety Report 2026](https://internationalaisafetyreport.org/publication/international-ai-safety-report-2026)**
The second International AI Safety Report, led by Yoshua Bengio with 100+ experts from 30+ nations, was published February 3rd. Key findings for practitioners: AI systems now meaningfully assist attackers at several stages of the cyberattack chain, with especially strong evidence for discovering software vulnerabilities. An AI agent placed in the top 5% of teams at a major cybersecurity competition in 2025. Underground marketplaces now sell pre-packaged AI tools lowering the skill threshold for attacks.

**[Wiz AI Cyber Model Arena: Real-World Benchmarks for Offensive AI](https://www.wiz.io/blog/introducing-ai-cyber-model-arena-a-real-world-benchmark-for-agentic-ai-in-cybersec)**
Wiz launched a benchmark of 257 real-world offensive security challenges (zero-days, CVEs, API/web, cloud across AWS/Azure/GCP/K8s) testing 25 agent-model combinations. Top performers: Claude Opus 4.6 with Claude Code, then Gemini 3 Pro with Gemini CLI. All scoring is deterministic (no LLM-as-judge), agents run in isolated Docker containers with no internet access.

## Governance & Compliance Watch

**EU AI Act: Commission Misses Article 6 Guidance Deadline**
The European Commission failed to meet its February 2nd deadline for detailed guidance on Article 6 (high-risk AI systems). This creates uncertainty for compliance planning, but doesn't change the binding deadline: **full high-risk AI obligations take effect August 2, 2026**, with penalties up to €35M or 7% of global turnover.

**NIST CAISI RFI: Comment Period Closing March 9**
The NIST AI agent security RFI (docket NIST-2025-0035) closes **March 9, 2026**. If you have operational experience securing agentic systems, submit your input.

**vLLM Gets a Second Critical RCE: Model Config Execution (GHSA-8fr4-5q9j-m8gm)**
A separate critical vulnerability in vLLM's model config loading allows remote code execution by publishing a benign-looking model whose config.json points to a malicious backend repo via auto_map. Loading the frontend model silently executes the backend's code—even when `trust_remote_code=False`. This is the AI supply chain version of dependency confusion.

## Tools & Resources

* **[Cisco MCP/A2A/Agentic Skill Scanners](https://blogs.cisco.com/ai/cisco-state-of-ai-security-2026-report)** — Open-source tools from Cisco's AI Threat Intelligence team.
* **[1Password/SCAM](https://github.com/1Password/SCAM)** — Open-source benchmark + security skill file for testing AI agent phishing resistance.
* **[KeygraphHQ/shannon](https://github.com/KeygraphHQ/shannon)** — Autonomous AI pentester that actively exploits web vulnerabilities (not just identifies them).
* **[samugit83/redamon](https://github.com/samugit83/redamon)** — AI-powered agentic red team framework. LangGraph-based ReAct agent chaining reconnaissance through exploitation into a Neo4j knowledge graph.
* **[trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config)** — Trail of Bits' opinionated defaults for Claude Code covering sandboxing, permissions, hooks, and MCP servers.

## My Take

Two things stood out to me this week.

**First, the AI security threat surface is splitting into two distinct categories and most teams are only watching one of them.**

**Category one** is traditional security vulnerabilities in AI infrastructure—vLLM's heap overflow, Firebase misconfigurations, model config RCE. These are bugs we know how to reason about even when they appear in new contexts.

**Category two** is genuinely novel—Meta-Context Injection in DockerDash, where the boundary between data and instructions dissolves at the MCP layer. This isn't a memory corruption bug. It's an architectural trust failure in how agents process context. We don't have mature defenses for it yet.

**Second, the 83% vs 29% readiness gap in Cisco's report mirrors every conversation I have with security teams.** Everyone is deploying agents. Almost no one has updated their threat models to account for tool-use, MCP trust boundaries, or non-human identity management. That's the gap this newsletter exists to help close.

If your security program treats AI as "just another application," you're covering category one and blind to category two.

— Amine Raji

## Wrapping Up

**If you found this useful**, forward it to one colleague who's deploying agents without a security playbook. They'll thank you.

**Want a quick-reference cheat sheet?** I built an LLM & AI Agent Security Field Guide covering the complete OWASP LLM Top 10, the Agentic Top 10, copy-paste detection patterns, and a 14-point security assessment checklist. Reply "field guide" and I'll send it over.

**Questions, comments, feedback?** Just reply directly, I read everything.

See you next week.

Cheers,
Amine
