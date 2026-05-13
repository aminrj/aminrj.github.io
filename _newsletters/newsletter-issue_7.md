---
title: 97% expect an AI agent breach this year
Subject: 97% expect an AI agent breach this year
Preview text: But only 6% of the security budgets cover it
issue: 7
date: 2026-04-08
---

Hey 👋,

This week I started building a cybersecurity AI agent: purpose-built, 100% local, LangGraph + FastMCP + Ollama. The first real decision was framework choice. I evaluated OpenClaw and NVIDIA's NemaClaw and ruled both out: OpenClaw for the obvious reasons (5 critical CVEs in three months, 1,184 confirmed malicious skills in its marketplace), NemaClaw because it's cloud-centric by design and a security research environment needs the opposite.

The [full build guide](aminrj.com/posts/building-cybersecurity-ai-agent-2026/) covers the decision matrix and working code. Next issue: what the threat correlation module actually produces.

While I was building, the field had a busy week.

## THIS WEEK IN AI SECURITY

**97% of enterprises expect a material AI agent security incident this year and only 6% of security budgets cover it.**

Arkose Labs surveyed 300 enterprise leaders. 97% expect a material AI-agent-driven security or fraud incident within 12 months. Nearly half expect one within six months. Security budget allocated to this risk: 6%.

> **Worth noting:** organizations aren't ignoring the risk. They're acknowledging it and deploying anyway. The question isn't whether they think agents are dangerous — it's whether acknowledging danger without funding defense is a posture or just a survey response.

→ [securityboulevard.com](https://securityboulevard.com/2026/04/97-of-enterprises-expect-a-major-ai-agent-security-incident-within-the-year/)

## OpenClaw: 9 CVEs in 4 days, CVSS 9.9 privilege escalation, 1,184 confirmed malicious skills

The velocity is the story. Nine CVEs in four days including a CVSS 9.9, low-privilege tokens escalating to admin with RCE. Censys puts exposed instances at 21,639. Malicious skill count: 1,184 out of 10,700 confirmed.

> **For enterprises where employees have installed OpenClaw connected to corporate SaaS:** that's an unapproved privileged access workstation. Check OAuth grants in your identity provider — you won't find it anywhere else.

The ClawHub number: 11% of marketplace skills confirmed malicious at scale is a supply chain poisoning rate, not an edge case.

→ [OpenClaw secure-deployment guide](aminrj.com/posts/openclaw-secure-deployment/)

## Okta for AI Agents goes GA April 30

This is the first major identity vendor shipping purpose-built agent identity.

Okta for AI Agents provides identity, authentication, and fine-grained authorization for autonomous agents. Every Okta customer is now being asked to evaluate agent identity. Identity is necessary. It's not sufficient, an agent with a properly scoped identity can still be prompt-injected into misusing its legitimate access.

> **Worth tracking:** how Okta handles tool-level scoping for agent-to-agent delegation. The Grantex audit (Issue #5) showed zero projects implement scope narrowing for delegated calls. That's the gap Okta needs to close to matter for multi-agent architectures.

→ details on [okta.com](https://okta.com/newsroom/press-releases/showcase-2026/)

## Four CVEs in CrewAI chain prompt injection to RCE, all in default configurations

Four vulnerabilities in CrewAI's Code Interpreter and default tool configurations create a chain: attacker-controlled input → prompt injection → SSRF → file read → RCE. No additional privileges required. This fires when agents process emails, documents, or web content — which is most of what production agents do.

> **Action:** Audit Code Interpreter configurations and default tool permissions before your next CrewAI deployment. If agents process external content, treat every input as untrusted.

→ More details on [adversa.ai](https://adversa.ai/blog/top-agentic-ai-security-resources-april-2026/) blog.

## Microsoft and Palo Alto both published OWASP Agentic Top 10 implementation guides this week

Two of the three largest security platforms independently publishing OWASP Agentic implementation guidance in the same week signals one thing: the framework is becoming the enterprise compliance baseline. Read both — not for the vendor positioning, but because the gaps between what each covers reveal where the unsolved problems still are.

→ Microsoft [LINK](microsoft.com/en-us/security/blog/2026/03/30/addressing-the-owasp-top-10-risks-in-agentic-ai-with-microsoft-copilot-studio/)
→ Palo Alto: [LINK](paloaltonetworks.com/blog/cloud-security/owasp-agentic-ai-security/)

## Infostealers + agentic AI: the kill chain most teams aren't modeling

_"Flashpoint 2026: 3.3 billion stolen credentials in criminal markets. Mandiant M-Trends 2026: privilege escalation now takes 22 seconds."_

A credential from any of those breaches, reaching an environment where an agent holds OAuth tokens and MCP tool access, gives an attacker a path that looks like normal agent activity. The threat model most teams are missing: "attacker authenticates as the agent using a stolen credential" — not "attacker prompt-injects the agent."

→ Full details in [this guide](aminrj.com/posts/infostealer-agentic-killchain/)

## TOOLING WORTH KNOWING

* **OWASP AI Security Solutions Landscape Q2 2026**: updated vendor capability map against agentic security risks. Useful for comparing what platforms actually cover vs. what they claim. _[owasp.org](genai.owasp.org/resource/ai-security-solutions-landscape-for-agentic-ai-q2-2026/)_
* **Sysdig Falco rules for AI coding agents:** syscall-level detection for Claude Code, Gemini CLI, Codex CLI. Most concrete detection guidance available if AI coding agents run in your CI. [sysdig.com](https://sysdig.com)

## ONE THING TO CHECK THIS WEEK

Search your identity provider's **OAuth grant list for OpenClaw, Moltbot, or Clawdbot**. Then check whether those grants include "read all mail," "manage files," or "access calendar." You won't find employee-installed AI agents in endpoint logs — the identity provider is the only place they're visible.

## WHAT I'M WATCHING

1. Okta's tool-level scoping — whether it addresses delegated agent-to-agent authorization or just top-level identity
2. OpenClaw CVE velocity — nine in four days suggests something structural is being found
3. RSAC behavioral baseline gap — no vendor shipped one; whoever defines normal agent behavior first wins a category
4. TeamPCP — Telnyx confirmed the campaign continues

Questions, pushback, topics — reply directly, I read everything.

Cheers,
Amine
