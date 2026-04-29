---
Subject: No caller auth on most MCP servers. CVE-2026-35616 actively exploited. The checklist that closes both gaps.
Preview text: New research confirms MCP servers trust every request by default. Here's what to do before it becomes someone else's exploit.
Issue: 10
Date: 2026-04-29
---

Hey 👋,

I've been building a cybersecurity AI agent locally — a 35B model running fully air-gapped on consumer hardware, no external API calls, no data leaving the machine. The hardest part isn't the model. It's the permission model. When you wire an agent to real tools — filesystem, shell, APIs — the first question that needs an answer is: who is allowed to call what, and how do you know it's who you think it is?

That question turns out to be the most important unanswered question in the MCP ecosystem right now. New research this week confirmed it.

---

## THIS WEEK IN AI SECURITY

**Most MCP servers trust every caller. New research documents exactly what that enables.**

A large-scale analysis published on arXiv this week examined how MCP servers handle caller identity in production deployments. The finding: most don't. Requests are accepted and executed regardless of origin — no mutual TLS, no signed tokens, no per-caller access controls. Any process that can reach the server can invoke any tool it exposes.

The dangerous part isn't a single server being misconfigured. It's how this propagates in multi-agent systems. When agents chain calls across multiple MCP servers, a compromised agent in the chain can impersonate any other agent downstream. The blast radius of a prompt injection or credential theft isn't bounded by the compromised agent's own permissions — it's bounded by whatever the farthest MCP server in the chain will execute for any request that arrives looking legitimate.

<div style="background:#fefce8;border-left:3px solid #ca8a04;padding:12px 16px;border-radius:0 6px 6px 0;font-family:Georgia,serif;font-size:15px;line-height:1.7;color:#1c1917;">
  <b>Immediate check:</b> For every MCP server in your environment — ask whether it verifies who is calling it, or trusts any request that arrives on the right port. If it's the latter, add mutual TLS or a signed token requirement before connecting it to any agent with real permissions. An unauthenticated MCP server in a multi-agent chain is a lateral movement path, not just a misconfiguration.
</div>

[arXiv research →](https://arxiv.org/abs/2603.07473)

---

**FortiClient EMS zero-day — CVE-2026-35616, exploited in the wild now**

A critical vulnerability in Fortinet's Endpoint Management Server is under active exploitation. Fortinet issued emergency hotfixes. The exploitation window is open.

FortiClient EMS matters here because endpoint management servers sit at the center of managed infrastructure — compromise gives an attacker admin-equivalent access across enrolled endpoints. That's the same network position your agent services, MCP backends, and orchestration layers run on. A compromised EMS gives an attacker a direct, credentialed path to everything the agents can reach. Patch the EMS first. Then check what agent APIs are reachable from that network position.

[BleepingComputer →](https://www.bleepingcomputer.com/news/security/new-fortinet-forticlient-ems-flaw-cve-2026-35616-exploited-in-attacks/)

---

**OWASP LLM AI Governance Checklist: the fastest triage tool available right now**

OWASP published a practical governance checklist for LLM and agentic deployments, mapped directly to the failure patterns seen in Q1 2026 incidents. It covers four controls that address the majority of the documented attack surface: scoped API keys, per-agent identity, revocation paths, and audit trails.

It's not a research paper. It's an audit instrument. If you're trying to prioritize hardening work and don't know where to start, run this checklist against your current deployment. Most teams will find gaps in under an hour.

[OWASP via CSO →](https://www.csoonline.com/article/3493126/genai-security-als-checkliste.html)

---

## TOOLING WORTH KNOWING

- **Sentinely** — runtime security gate for AI agents. Scores each action against a behavioral model before execution: prompt injection, memory poisoning, intent drift, multi-agent manipulation. Fails closed. Designed to deploy in staging without requiring harness rewrites. Right tool if you need runtime visibility now and can't wait for protocol-level fixes. [sentinely.ai →](https://sentinely.ai)

- **MCPSec** — open-source static scanner for MCP configurations. Flags missing authentication, unscoped API keys, and tool handlers that accept filesystem paths or raw SQL. Run it against every MCP config you own. The caller identity research published this week shows exactly what an unscanned config enables. [github →](https://github.com/pfrederiksen/mcpsec)

---

## ONE THING TO CHECK THIS WEEK

Run MCPSec against every MCP configuration in your environment — local development, CI pipelines, and any cloud-hosted endpoints. Specifically: missing caller authentication, tool handlers that accept filesystem paths, unscoped keys attached to agent identities. The arXiv paper published this week documents what those gaps enable in a multi-agent chain. This is not a "schedule for next sprint" finding — it's a lateral movement path that exists right now in most MCP deployments.

---

## WHAT I'M WATCHING

→ Anthropic and the MCP SDK fix — a protocol-level change (manifest-only execution, command allowlists) still hasn't shipped. The design decision stands. Whether community pressure moves it is the open question.

→ The behavioral baseline gap — authenticated sources account for 99% of attack attempts against agent environments (Salt Security, 1H 2026). No vendor ships a behavioral baseline. Detection is the missing layer. Someone will build it.

→ Agent governance standards — Open Agent Passport and pre-action authorization specs are gaining traction. Enterprise AI deployments will eventually require per-agent identity and revocation. Worth tracking before it becomes a compliance requirement.

→ The cybersecurity agent build — next issue: the Executor permission model, what the memory architecture looks like with real filesystem access, and the first results from running a local 35B model as the agent backbone.

---

Questions, pushback, something I missed — reply directly, I read everything.

Amine
https://aminrj.com | https://aminrj.com/subscribe

---

## BEEHIIV HTML — paste as Custom HTML blocks

**Amber (action — Caller Identity):**
```html
<div style="background:#fefce8;border-left:3px solid #ca8a04;padding:12px 16px;border-radius:0 6px 6px 0;font-family:Georgia,serif;font-size:15px;line-height:1.7;color:#1c1917;">
  <b>Immediate check:</b> For every MCP server in your environment — ask whether it verifies who is calling it, or trusts any request that arrives on the right port. If it's the latter, add mutual TLS or a signed token requirement before connecting it to any agent with real permissions. An unauthenticated MCP server in a multi-agent chain is a lateral movement path, not just a misconfiguration.
</div>
```
