---
Subject: MCP servers just tripled. Here's the full attack map.
Preview text: 1,467 exposed servers. 9 of 11 registries poisoned. Memory that spreads across users. The week in MCP security.
Issue: 11
Date: 2026-05-09
---

Hey 👋,

I'm speaking at OWASP Stockholm on May 19 about MCP security over the past six months. Preparing the talk forced me to map the attack surface properly, and what I found is that three separate research teams published findings this week that together cover the ground almost completely. That's the thread.

Issue #10 covered the MCP caller-identity research and the OWASP checklist as a triage tool. This week's findings extend that picture. If you haven't run MCPSec against your MCP configurations yet, the numbers below will change that calculation.

---

## This week in AI security

**Exposed MCP servers have nearly tripled. Attackers are now reaching cloud infrastructure.**

Trend Micro's updated scan, a follow-up to their July 2025 research, found exposed MCP servers have grown from 567 to 1,467. The bigger shift: attackers are no longer limited to accessing data through exposed servers. They're compromising the cloud services hosting them.

The chain: scan for exposed MCP servers, exploit unauthenticated endpoints, find hardcoded cloud credentials (48% of MCP server source code recommends storing secrets in `.env` files or plaintext JSON), then use those credentials to access the underlying cloud provider's API. Trend Micro found CVSS 9.8 vulnerabilities in cloud-specific MCP implementations that bypass security controls and execute unauthorized commands within the cloud environment.

> **The architectural shift:** MCP servers started as a local integration problem. They're now a cloud security problem. An exposed MCP server is a launchpad for full cloud account compromise — data breaches, lateral movement, financial access. The threat model has escalated one level.

> **Action:** Scan your MCP server source code for `.env` references and plaintext credential storage. Any MCP server with cloud provider API keys in its configuration is one exposed endpoint away from a full cloud compromise. Rotate those credentials to short-lived, scoped tokens before anything else.

[Trend Micro research →](https://www.trendmicro.com/vinfo/us/security/news/vulnerabilities-and-exploits/update-on-exposed-mcp-servers-the-threat-widens-to-the-cloud)

---

**The MCP attack taxonomy: four families, one root cause**

With several weeks of MCP CVEs accumulating, it's worth mapping the attack surface properly rather than tracking individual CVEs. The OX Security advisory consolidates this into four families that all derive from one root cause in Anthropic's STDIO transport handling.

**1. Unauthenticated command injection via STDIO config.** Direct path from configuration to execution. Affected: LiteLLM (CVE-2026-30623, patched), LangChain, LangFlow/IBM (no CVE, no patch), LettaAI, LangBot.

**2. Authenticated injection with hardening bypass.** Developers implement allowlists for "python," "npm," "npx." OX found these are bypassable through argument injection or shell metacharacters. Affected: Upsonic (CVE-2026-30625), Flowise (GHSA-c9gw-hvqq-f33r).

**3. Zero-click prompt injection via IDE config.** Attacker-controlled content modifies `.mcp.json` automatically, registering a malicious STDIO server. Only Windsurf required truly zero interaction (CVE-2026-30615). Cursor, VS Code, Claude Code, Gemini CLI are all affected, but Google, Microsoft, and Anthropic classified these as "not a security vulnerability" or "expected behavior."

**4. Malicious marketplace distribution.** OX successfully poisoned 9 out of 11 MCP registries with a test payload. No malware, just a proof of concept that ran a command generating an empty file. The distribution mechanism works.

Anthropic's STDIO transport passes configuration directly to command execution with no manifest validation. Every downstream project inherits this. Anthropic declined to fix it at the protocol level.

> **For OWASP mapping:** Family 1 = ASI02 (Tool Misuse). Family 2 = ASI02 + ASI03 (Authorization Failures). Family 3 = ASI01 (Goal Hijacking via prompt injection). Family 4 = ASI04 (Supply Chain). All four attack the same architectural gap. The OWASP Agentic Top 10 covers the taxonomy — the OX research proves it's not theoretical.

[OX Security advisory →](https://www.ox.security/blog/mcp-supply-chain-advisory-rce-vulnerabilities-across-the-ai-ecosystem/) · [The Register →](https://www.theregister.com/2026/04/16/anthropic_mcp_design_flaw/)

---

**MemoryTrap: Claude Code's memory spreads poisoned entries across sessions and users**

Memory is another attack surface the OX taxonomy doesn't cover. Cisco researcher Idan Habler disclosed CVE-2026-21852 (MemoryTrap) in April 2026: a poisoned `MEMORY.md` file can outlive a session, persist in a shared memory store, and be reloaded by unrelated sessions and users. The attack is straightforward — inject a malicious instruction into an agent's persistent memory, and it gets executed every time Claude Code starts.

Anthropic patched this in v2.1.50, but the vulnerability class is wider than Claude Code. Any agent with persistent memory that accepts externally sourced content without sanitization has the same gap. The mechanism mirrors what the Malice in Agentland paper documented for fine-tuning pipelines: persistent state that bypasses per-session controls and carries attacker-influenced content forward indefinitely.

> **Why this matters beyond Claude Code:** the same vulnerability class applies to any agent with persistent memory — vector database memory stores, session compaction, long-term memory modules. If a memory store accepts externally sourced content and injects it into future contexts without sanitization, it's a MemoryTrap variant waiting to be found. This is ASI04 (Knowledge & Memory Poisoning) in practice.

> **If you run Claude Code in shared environments:** audit what's in the memory store. Any content derived from external sources — web pages, documents, code repositories — is a potential poisoning vector. Clear and re-seed from known-good sources. If you're building agents with persistent memory, sanitize at write time, not just at read time.

[Cisco MemoryTrap disclosure →](https://blogs.cisco.com/ai/identifying-and-remediating-a-persistent-memory-compromise-in-claude-code) · [CVE-2026-21852 →](https://omegamax.co/blog/agent-memory-poisoning-cve-2026)

---

**AI-assisted attacks in 2025-2026: three documented cases**

The Hacker News published a consolidation this week of confirmed AI-assisted attack incidents from 2025-2026.

In July 2025, a single attacker using Claude Code conducted an extortion campaign against 17 organizations over one month — developing malicious code, organizing stolen files, analyzing financial records to calibrate ransom demands, and drafting extortion emails. In December 2025, another individual used Claude Code and ChatGPT to breach the Mexican government, targeting more than 10 agencies and stealing 195 million taxpayer records. In February 2025, three teenagers with no coding background used ChatGPT to build an attack tool that hit Rakuten Mobile's systems about 220,000 times.

> **The pattern across all three:** the AI didn't autonomously decide to attack. A human directed it. The capability uplift is real — tasks that previously required specialized skill (malware development, financial record analysis, large-scale enumeration) are now accessible to anyone who can write a prompt. The threat model isn't rogue AI. It's AI-amplified human attackers at dramatically lower skill thresholds.

[The Hacker News →](https://thehackernews.com/2026/05/2026-year-of-ai-assisted-attacks.html)

---

**48.9% of organizations blind to agent-to-agent traffic**

Salt Security's 1H 2026 State of AI & API Security surveyed 300+ security leaders. The headline number: 48.9% have no visibility into machine-to-machine traffic, which includes agent-to-MCP-server traffic — the exact path the OX Security research showed attackers exploiting.

78.6% report increased executive scrutiny of AI security risks. Only 23.5% find their legacy security tools effective for the current threat landscape.

Your WAF and API gateway inspect North-South traffic. Agent-to-agent and agent-to-MCP traffic is East-West — it never crosses your perimeter. It looks like authenticated internal traffic because it is. Behavioral baselines are the only detection layer that addresses this. No vendor ships one yet.

[Salt Security 1H 2026 report →](https://salt.security/blog/the-era-of-agentic-security-is-here-key-findings-from-the-1h-2026-state-of-ai-and-api-security-report)

---

## Tooling worth knowing

- **MCPSec** — static scanner for MCP configurations. Flags missing authentication, unscoped keys, tool handlers accepting filesystem paths or raw SQL. This is the right first scan to run. [github →](https://github.com/MCPSec/mcpsec)
- **Sentinely** — runtime security gate for AI agents. Scores each action against a behavioral model before execution, fails closed. The closest thing to a behavioral baseline currently available for MCP deployments. [sentinely.ai →](https://sentinely.ai)
- **mcp-attack-labs** — my own reproducible lab code for MCP tool poisoning, rug-pull, and cross-server attacks. If you're preparing security assessments or a talk (hi OWASP Stockholm 👋), this is the fastest path to a live demo. [github →](https://github.com/aminrj-labs/mcp-attack-labs)

---

## One thing to check this week

Run MCPSec against your MCP configs. Check for STDIO transport with unscoped commands, allowlists that can be bypassed, and cloud credentials in the config. Cloud credentials alone — that's an immediate rotation event.

---

## What I'm watching

→ **OWASP Stockholm, May 19** — I'm presenting on the MCP attack surface: tool poisoning, cross-server attacks, rug pulls, the OX four-family taxonomy, and what defenders need to implement before these become your incident. If you're in Stockholm, come say hello.

→ **Anthropic's SDK patch decision** — community and researcher pressure continues. The four-family taxonomy makes it harder to sustain "expected behavior" as the official position. Watching for movement.

→ **Agent governance standards** — Open Agent Passport and pre-action authorization specs are gaining traction. Enterprise AI deployments will eventually require per-agent identity and revocation. Worth tracking before it becomes a compliance requirement.

→ **MCP registries** — 9 of 11 poisoned in OX's test. No registry has published a security response. The supply chain problem precedes the runtime problem.

---

Questions, pushback, something I missed — reply directly, I read everything. If you're attending OWASP Stockholm, reply and I'll make sure we connect.

Amine
https://aminrj.com | https://aminrj.com/subscribe

---

## Beehiiv callout HTML — paste as Custom HTML blocks

**Grey (architectural shift — MCP cloud threat):**

```html
<div style="background:#f5f5f4;border-left:3px solid #a8a29e;padding:12px 16px;border-radius:0 6px 6px 0;font-family:Georgia,serif;font-size:15px;line-height:1.7;color:#1c1917;">
  <b>The architectural shift:</b> MCP servers started as a local integration problem. They're now a cloud security problem. An exposed MCP server is a launchpad for full cloud account compromise — data breaches, lateral movement, financial access. The threat model has escalated one level.
</div>
```

**Amber (action — credential rotation):**

```html
<div style="background:#fefce8;border-left:3px solid #ca8a04;padding:12px 16px;border-radius:0 6px 6px 0;font-family:Georgia,serif;font-size:15px;line-height:1.7;color:#1c1917;">
  <b>Action:</b> Scan your MCP server source code for .env references and plaintext credential storage. Any MCP server with cloud provider API keys in its configuration is one exposed endpoint away from a full cloud compromise. Rotate those credentials to short-lived, scoped tokens before anything else.
</div>
```

**Grey (OWASP taxonomy mapping):**

```html
<div style="background:#f5f5f4;border-left:3px solid #a8a29e;padding:12px 16px;border-radius:0 6px 6px 0;font-family:Georgia,serif;font-size:15px;line-height:1.7;color:#1c1917;">
  <b>For OWASP mapping:</b> Family 1 = ASI02 (Tool Misuse). Family 2 = ASI02 + ASI03 (Authorization Failures). Family 3 = ASI01 (Goal Hijacking via prompt injection). Family 4 = ASI04 (Supply Chain). All four attack the same architectural gap. The OWASP Agentic Top 10 covers the taxonomy — the OX research proves it's not theoretical.
</div>
```

**Grey (MemoryTrap — broader implication):**

```html
<div style="background:#f5f5f4;border-left:3px solid #a8a29e;padding:12px 16px;border-radius:0 6px 6px 0;font-family:Georgia,serif;font-size:15px;line-height:1.7;color:#1c1917;">
  <b>Why this matters beyond Claude Code:</b> the same vulnerability class applies to any agent with persistent memory — vector database memory stores, session compaction, long-term memory modules. If a memory store accepts externally sourced content and injects it into future contexts without sanitization, it's a MemoryTrap variant waiting to be found. This is ASI04 (Knowledge & Memory Poisoning) in practice.
</div>
```

**Amber (MemoryTrap — action):**

```html
<div style="background:#fefce8;border-left:3px solid #ca8a04;padding:12px 16px;border-radius:0 6px 6px 0;font-family:Georgia,serif;font-size:15px;line-height:1.7;color:#1c1917;">
  <b>If you run Claude Code in shared environments:</b> audit what's in the memory store. Any content derived from external sources — web pages, documents, code repositories — is a potential poisoning vector. Clear and re-seed from known-good sources. If you're building agents with persistent memory, sanitize at write time, not just at read time.
</div>
```

**Grey (AI-assisted attacks — framing):**

```html
<div style="background:#f5f5f4;border-left:3px solid #a8a29e;padding:12px 16px;border-radius:0 6px 6px 0;font-family:Georgia,serif;font-size:15px;line-height:1.7;color:#1c1917;">
  <b>The pattern across all three:</b> the AI didn't autonomously decide to attack. A human directed it. The capability uplift is real — tasks that previously required specialized skill (malware development, financial record analysis, large-scale enumeration) are now accessible to anyone who can write a prompt. The threat model isn't rogue AI. It's AI-amplified human attackers at dramatically lower skill thresholds.
</div>
```

**Grey (Salt Security — detection gap):**

```html
<div style="background:#f5f5f4;border-left:3px solid #a8a29e;padding:12px 16px;border-radius:0 6px 6px 0;font-family:Georgia,serif;font-size:15px;line-height:1.7;color:#1c1917;">
  <b>The detection gap:</b> your WAF and API gateway inspect North-South traffic. Agent-to-agent and agent-to-MCP server traffic is East-West — it never crosses your perimeter. It looks like authenticated internal traffic because it is. Behavioral baselines are the only detection layer that addresses this. No vendor ships one yet.
</div>
```
