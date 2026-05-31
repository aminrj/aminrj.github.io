# [AI Sec Intel] #13 — Six governments just told you how to secure AI agents. Here's the part that's actually useful.

**Subject options:**
- A (recommended): `[AI Sec Intel] #13 — Six governments agree: your AI security model was built for the wrong problem.`
- B: `[AI Sec Intel] #13 — The first joint agentic AI guidance dropped. The one control that matters is identity.`
- C: `[AI Sec Intel] #13 — Prompt filtering was built for AI that responds. Agents act. Here's what changes.`

**Preview text:** `Five Eyes published the first coordinated agentic AI guidance. Strip away the government language and there's a usable deployment model underneath. Plus: your coding agent now runs from a phone.`

**Subtitle:** `The progressive-autonomy model, the identity-first mandate, and why a regex blocklist turned an AI agent into a remote shell.`

---

Hey 👋,

I've been wiring the permission model for the cybersecurity agent I'm building — the part where the agent goes from "reads threat feeds" to "can actually act on what it finds." The hardest design question isn't capability. It's restraint: how do you let an agent take useful actions without letting a poisoned input turn those same actions against you.

That's exactly the question six national cybersecurity agencies tried to answer on May 1. The framing they landed on matches what I keep arriving at in the lab: don't deploy an agent at full capability and then bolt on guardrails. Start it constrained, earn autonomy as the controls prove out. This issue is the practical read of that guidance — what to actually do with it.

---

## This week in AI security

**Five Eyes published the first joint agentic AI guidance. Skip the preamble — here's the usable part.**

On May 1, six agencies — CISA, NSA, Australia's ASD ACSC, Canada's CCCS, New Zealand's NCSC, and the UK's NCSC — jointly published "Careful Adoption of Agentic AI Services." It's the first coordinated multi-government guidance specifically for agentic systems. Most coverage focused on the five risk categories (privilege, design and configuration, behavioral, structural, accountability). The more useful content is the deployment model underneath.

The core recommendation: don't deploy agents at full autonomy from day one. Start with lower-risk tasks, expand the agent's autonomy only as security controls mature, maintain continuous monitoring of agent behavior and tool usage, and keep meaningful human oversight over high-impact or irreversible actions. It's a maturity model for agency, not a checklist.

> **[GREY CALLOUT — THE FRAMING THAT MATTERS]**
> **The honest admission buried in the government language:** existing frameworks (OWASP LLM Top 10, MITRE ATLAS) were built for LLM vulnerabilities and platform misuse. They were not built for agents that autonomously plan, call APIs, modify files, and escalate privileges without a human in the loop. Prompt filtering and behavioral monitoring were built for AI that *responds*. Agentic AI *acts*. A control that flags an anomaly after the fact is useless when the agent has already made twelve API calls and modified access controls before anyone looked.

> **[AMBER CALLOUT — DO THIS]**
> **Apply the progressive-autonomy model to one agent this week.** Pick an agent currently running at full capability. Write down: what irreversible actions can it take right now without human approval? For each one, ask whether the control maturity actually justifies that autonomy. Where it doesn't, add a human-in-the-loop gate on the irreversible action — not on everything, just the ones you can't undo. That single exercise is the most useful thing in the entire 30-page guidance.

[CISA guidance →](https://www.cisa.gov/resources-tools/resources/careful-adoption-agentic-artificial-intelligence-services) · [CSA practitioner read →](https://labs.cloudsecurityalliance.org/research/csa-research-note-cisa-agentic-ai-guidance-20260503-csa-styl/)

---

**The one control all six agencies agreed on: every agent needs its own cryptographic identity**

If you read nothing else in the guidance, read the identity section. The agencies were direct: each agent must carry a verified, cryptographically anchored identity with short-lived credentials. Not a shared service account. Not an org-level API key. A distinct, continuously authenticated identity per agent.

This is the same gap I covered in Issue #5 — the Grantex audit found 28 of 30 agent projects with zero per-agent identity. Now six governments have made it the single most technically specific recommendation in their joint guidance. The convergence is the signal: identity is the control that everything else depends on. You cannot scope permissions, attribute actions, revoke access, or investigate an incident if you can't tell which agent did what.

> **[AMBER CALLOUT — THE PRACTICAL STEP]**
> **Inventory your agent credentials this week.** For each agent in your environment: does it have its own identity, or does it share one? Are its credentials long-lived or short-lived? Can you revoke one agent's access without breaking the others? If the answer to any of these is wrong, that's your highest-leverage hardening work — ahead of any prompt-injection defense. Identity first, because everything else hangs off it.

[CSA Agentic AI Security Scoping Matrix →](https://cloudsecurityalliance.org/artifacts/agentic-ai-security-scoping-matrix)

---

**Your coding agent now runs from a phone. The attack surface moved with it.**

Anthropic shipped Claude Code to the web and mobile this week — accessible from any browser and from a phone, beyond the terminal for the first time. OpenAI Codex gained the ability to control a locked Mac the same week. The practical implication everyone's celebrating: agents that used to require a laptop physically open now run from anywhere.

The security implication nobody's mentioning: the trust boundary moved. A terminal-based coding agent ran in an environment you controlled — your machine, your network, your monitoring. A browser or phone-based agent runs in an environment you mostly don't. The agent still has the same repository access, the same ability to commit code, the same tool permissions — but now the session originates from a device and network outside your security perimeter.

> **[GREY CALLOUT — WHAT THIS CHANGES]**
> **Convenience and attack surface scale together.** The same feature that lets a developer fix a bug from their phone on the train lets a compromised phone session reach your production repository from an untrusted network. If your coding agents can now run from mobile, your threat model needs to account for sessions originating outside your controlled environment — device compromise, session hijacking, and shoulder-surfing of approval prompts all move from theoretical to relevant.

> **[AMBER CALLOUT — CHECK THIS]**
> **Review what your coding agents can do without re-authentication from a new device.** If a developer's authenticated session can commit to a protected branch, merge a PR, or trigger a deploy from a phone with no step-up auth, that's the gap the new mobile access opened. Require step-up authentication for irreversible or high-impact actions regardless of which device the session runs from.

---

**CVE-2026-2256: a regex blocklist turned an AI agent into a remote shell**

A concrete one worth the pattern lesson. The MS-Agent framework (v1.5.2) had a command injection vulnerability in its Shell tool — the component that lets the agent run OS commands for file management and automation. The framework tried to filter dangerous commands using a regex-based blocklist. Researchers bypassed it with crafted input, turning the agent into an execution proxy: an attacker injects content into a data source the agent consumes (a document, a log, a research input), and the agent constructs and runs the malicious command on the attacker's behalf. No direct shell access required.

> **[GREY CALLOUT — THE PATTERN, NOT THE CVE]**
> **Blocklists fail for agent tools the same way they failed for SQL injection.** A regex that blocks "known dangerous" commands is trying to enumerate badness — and LLM-mediated input generation makes the bypass space effectively infinite. The agent will happily construct a command phrasing the blocklist didn't anticipate. The fix is the same one that fixed SQL injection: don't filter the dangerous inputs, constrain to an allowlist of permitted operations with validated parameters. If your agent has a shell tool, a file tool, or a query tool guarded by a denylist, you have a CVE-2026-2256 waiting to happen.

[CVE-2026-2256 technical breakdown →](https://www.pointguardai.com/ai-security-incidents/shell-game-ms-agent-flaw-lets-hackers-seize-ai-agents-cve-2026-2256)

---

## Tooling worth knowing

- **CSA Agentic AI Security Scoping Matrix** — the practical implementation companion to the CISA guidance. Six dimensions (Identity Context, Data Protection, Audit and Logging, Agent/Foundation Model Controls, Agency Perimeters, Orchestration) that map directly to the controls the guidance describes. If the CISA document tells you *what*, this tells you *at which autonomy level*. Use them together. [cloudsecurityalliance.org →](https://cloudsecurityalliance.org/artifacts/agentic-ai-security-scoping-matrix)
- **mcp-attack-labs** — reproducible lab code for the MCP attacks covered across this newsletter's series, including the tool-poisoning and cross-server patterns. If you're building the kind of allowlist defense CVE-2026-2256 calls for, the labs let you test it against the actual attacks. [github.com/aminrj-labs/mcp-attack-labs →](https://github.com/aminrj-labs/mcp-attack-labs)

---

## One thing to check this week

Take the progressive-autonomy model from the Five Eyes guidance and apply it to your highest-privilege agent. Three questions: (1) What irreversible actions can it take without human approval right now? (2) Does it have its own cryptographic identity with short-lived credentials, or does it share a credential? (3) Are its tool permissions guarded by an allowlist or a denylist? If you answer those three honestly for one agent, you'll have a concrete hardening backlog by end of day — and it'll map cleanly to what six governments just recommended.

---

## What I'm watching

→ **Identity-first as the emerging consensus** — six governments named per-agent cryptographic identity as the most actionable control. The vendor category (Okta for AI Agents, Token Security, others) is forming around it. This is becoming the foundational control everything else assumes.

→ **The mobile coding agent surface** — Claude Code on web/phone and Codex controlling a locked Mac landed the same week. The convenience is real; the trust-boundary shift is unaddressed. Expect the first "agent committed malicious code from a compromised phone session" incident within months.

→ **CISA's "framework era is over" framing** — the guidance implicitly concedes that OWASP LLM Top 10 and ATLAS weren't built for agents that act autonomously. Watch whether the frameworks adapt or whether agent-native standards (like the CSA scoping matrix) take over.

→ **The cybersecurity agent build** — next issue: the permission model in practice, how I implemented progressive autonomy with an allowlist-based tool gate, and what broke when I tested it against the mcp-attack-labs payloads.

---

Questions, pushback, something I missed — reply directly, I read everything.

Cheers,
**Amine**

---

## Beehiiv HTML callouts — paste as Custom HTML blocks

**Grey — the framing that matters (Five Eyes):**
```html
<div style="background:#f5f5f4;border-left:3px solid #a8a29e;padding:12px 16px;border-radius:0 6px 6px 0;font-family:Georgia,serif;font-size:15px;line-height:1.7;color:#1c1917;">
  <b>The honest admission buried in the government language:</b> existing frameworks (OWASP LLM Top 10, MITRE ATLAS) were built for LLM vulnerabilities and platform misuse. They were not built for agents that autonomously plan, call APIs, modify files, and escalate privileges without a human in the loop. Prompt filtering was built for AI that <em>responds</em>. Agentic AI <em>acts</em>. A control that flags an anomaly after the fact is useless when the agent has already made twelve API calls and modified access controls before anyone looked.
</div>
```

**Amber — do this (progressive autonomy):**
```html
<div style="background:#fefce8;border-left:3px solid #ca8a04;padding:12px 16px;border-radius:0 6px 6px 0;font-family:Georgia,serif;font-size:15px;line-height:1.7;color:#1c1917;">
  <b>Apply the progressive-autonomy model to one agent this week.</b> Pick an agent currently running at full capability. Write down: what irreversible actions can it take right now without human approval? For each one, ask whether the control maturity justifies that autonomy. Where it doesn't, add a human-in-the-loop gate on the irreversible action — not on everything, just the ones you can't undo.
</div>
```

**Amber — practical step (identity):**
```html
<div style="background:#fefce8;border-left:3px solid #ca8a04;padding:12px 16px;border-radius:0 6px 6px 0;font-family:Georgia,serif;font-size:15px;line-height:1.7;color:#1c1917;">
  <b>Inventory your agent credentials this week.</b> For each agent: does it have its own identity, or does it share one? Are its credentials long-lived or short-lived? Can you revoke one agent's access without breaking the others? If the answer to any is wrong, that's your highest-leverage hardening work — ahead of any prompt-injection defense. Identity first, because everything else hangs off it.
</div>
```

**Grey — what this changes (mobile agents):**
```html
<div style="background:#f5f5f4;border-left:3px solid #a8a29e;padding:12px 16px;border-radius:0 6px 6px 0;font-family:Georgia,serif;font-size:15px;line-height:1.7;color:#1c1917;">
  <b>Convenience and attack surface scale together.</b> The same feature that lets a developer fix a bug from their phone on the train lets a compromised phone session reach your production repository from an untrusted network. If your coding agents can now run from mobile, your threat model needs to account for sessions originating outside your controlled environment — device compromise, session hijacking, and shoulder-surfing of approval prompts all move from theoretical to relevant.
</div>
```

**Amber — check this (mobile re-auth):**
```html
<div style="background:#fefce8;border-left:3px solid #ca8a04;padding:12px 16px;border-radius:0 6px 6px 0;font-family:Georgia,serif;font-size:15px;line-height:1.7;color:#1c1917;">
  <b>Review what your coding agents can do without re-authentication from a new device.</b> If a developer's authenticated session can commit to a protected branch, merge a PR, or trigger a deploy from a phone with no step-up auth, that's the gap mobile access opened. Require step-up authentication for irreversible or high-impact actions regardless of which device the session runs from.
</div>
```

**Grey — the pattern (CVE-2026-2256):**
```html
<div style="background:#f5f5f4;border-left:3px solid #a8a29e;padding:12px 16px;border-radius:0 6px 6px 0;font-family:Georgia,serif;font-size:15px;line-height:1.7;color:#1c1917;">
  <b>Blocklists fail for agent tools the same way they failed for SQL injection.</b> A regex that blocks "known dangerous" commands is trying to enumerate badness — and LLM-mediated input generation makes the bypass space effectively infinite. The fix is the same one that fixed SQL injection: don't filter the dangerous inputs, constrain to an allowlist of permitted operations with validated parameters. If your agent has a shell, file, or query tool guarded by a denylist, you have a CVE-2026-2256 waiting to happen.
</div>
```
