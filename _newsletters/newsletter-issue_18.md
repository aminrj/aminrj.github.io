---
title: "On July 28, MCP changes shape"
Subject: "[AI Sec Intel] #18 | On July 28, MCP changes shape. Three attack surfaces open where your gateway can't see them."
preview_text: "The new MCP spec goes final July 28 and moves security from the protocol to the endpoint. Plus: new research explains why prompt injection works, and it's not what you think."
subtitle: "MCP goes stateless on July 28, moving security work from the protocol to the endpoint. Here's what changes and what to check before it ships."
issue: 18
date: 2026-07-04
---

Hey

There's a date on the calendar that matters more than any single CVE this month: July 28. That's when the MCP 2026-07-28 specification goes final. It's the biggest structural change to the protocol since it launched. Validation is already open, Tier-1 SDKs are shipping support, and the ecosystem starts moving the day it lands.

I'm leading with it instead of a fresh vulnerability because most of what I cover here is an attack against the current design. This is the design itself changing, and it quietly moves a whole category of security work from the protocol layer to the endpoint layer. No CVE will be filed for that. It won't show up in a scanner. You either prepare in the next three weeks or inherit it as an incident later.

This is a get-ready issue. What's changing, why it matters, and what to check before the spec ships. Plus a piece of research that reframes prompt injection in a way that explains why none of our filters ever fully work.

If you want the deeper version of how I think about scoping what an agent can reach, [it's on the blog →](https://aminrj.com/posts/agent-permission-model/)

---

## This week in AI security

### MCP goes stateless on July 28

Since launch, MCP has been stateful. An agent connects, gets an `Mcp-Session-Id` in the HTTP header, and every request carries it. The model never saw that ID, so it could never leak it. The new spec removes the handshake. Now when an agent calls `create_browser()`, the server returns a handle inside the conversation: `{ "browser_id": "browser-abc123" }`. The model sees it, holds it, and passes it back on every call.

Akamai and Backslash both broke down what that opens up. Three problems.

**Handle hijacking** replaces session hijacking. The handle is now just a string in a chat transcript, a Jira ticket, a Slack paste, a tool response. Whoever can read or plant that string can replay it, unless the server checks the handle against the auth context rather than trusting the handle alone.

**The filesystem scope gap.** The old `Roots` capability is deprecated. Scope enforcement is now opt-in, built by each server developer, and applied inconsistently.

**IDE HTML rendering.** The new MCP Apps extension (SEP-1865) lets servers ship interactive HTML that renders in a sandboxed iframe inside your IDE. A fake VS Code auth prompt stops being a curiosity and becomes a credential-harvesting surface.

All three are invisible to network and gateway security. A handle string in a conversation isn't HTTP traffic. Filesystem access on a developer laptop never crosses the gateway. An IDE iframe rendering HTML generates no network signal. Your MCP gateway wasn't built badly. It was built for a different threat model.

This is good engineering. Stateless scales, and the OAuth 2.1 hardening (mandatory PKCE, audience-bound tokens, `iss` validation per RFC 9207) closes real holes. But the security work that used to live at the session layer now happens on the endpoint only if you decide to put it there.

**Run these four checks before July 28.** One: for each MCP server you run, are handles tied to a specific user, and do they expire? A handle that never expires is a permanent access token. Two: inventory which MCP servers run locally on developer machines, because those are the ones no network tool will ever surface. Three: find which servers can render HTML into the IDE (MCP Apps), and review that HTML the way you'd vet a third-party script. Four: stop assuming your gateway covers MCP, and decide on purpose where your endpoint visibility comes from.

[Akamai →](https://www.akamai.com/blog/security-research/new-mcp-specification-security-teams-must-prepare) · [Backslash →](https://www.backslash.security/blog/new-mcp-spec-opens-new-attack-surfaces) · [Release candidate →](https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/)

---

### Prompt injection works because models read tone, not role tags

This is the most clarifying piece of research I've read this year. "Prompt Injection as Role Confusion" (Ye, Cui, Hadfield-Menell) traces injection to a single mechanism. An LLM receives the whole conversation as one stream of text, split by role tags (`user`, `tool`, `think`), and those tags are supposed to be the security boundary. But the model doesn't read role from the tag. It reads role from how the text sounds.

The researchers built probes that measure how strongly the model internally believes a token belongs to a given role. They found that reasoning-style text registers as the model's own private thoughts even when it's explicitly wrapped in `user` tags. Their attack, **CoT Forgery**, injects fake reasoning that mimics the model's own thinking style, and it takes jailbreak success from near-zero to about 60% across every frontier model tested.

The same mechanism explains ordinary agent injection. Prepend "User:" to a malicious command buried in a webpage and the model treats it as a trusted instruction. Across 1,000 exfiltration attempts, attack success rose from 2% to 70% in lockstep with how much role confusion the probe measured.

You cannot filter your way out of prompt injection, because to the model, sounding like a role is indistinguishable from being one. Every content filter, every guardrail that inspects the text is playing a game the architecture already lost. The attacker isn't smuggling a keyword. They're impersonating a voice, and the model's own weights treat a convincing caricature of its reasoning as more genuinely its own than its real reasoning.

An enthusiastic product page can steer a purchasing agent, with no explicit injection at all. Testable at scale. Legal too.

**Stop pouring budget into "detect the bad prompt" as your primary defense. Move it to "limit what a fooled agent can do."** Assume the injection will land. The controls that actually hold sit downstream: scoped permissions, a human gate on irreversible actions, per-request authorization that doesn't trust the model's read of who's speaking. If you run reasoning models, treat any externally sourced text that looks like structured reasoning as radioactive.

[The paper →](https://arxiv.org/abs/2603.12277)

---

### AWS shipped Continuum, and the interesting part isn't the AI

At its NY Summit on June 17, AWS launched Continuum, an agentic security platform that runs the full vulnerability lifecycle: discover, prioritize by business context, prove exploitability by building a working exploit in a sandbox, then propose a validated fix. The validation step is the genuinely novel part, concrete reproducible proof instead of a probabilistic severity score.

But the design choice worth your attention is the governance one. Continuum ships in "learn mode" by default, with a human in the loop on every recommendation. Organizations graduate it to "enforce mode" for autonomous remediation category by category, only as they build confidence. AWS was blunt about why: specialized models now find and chain vulnerabilities faster than any human SOC can triage, forcing defenders to operate at machine speed too.

This is the whole industry converging on one pattern: you don't grant an agent autonomy, you let it earn autonomy, one bounded category at a time, with the limit enforced by deterministic infrastructure rather than the model's good behavior. It's the same progressive-autonomy model the Five Eyes guidance landed on (Issue #13), now baked into a shipping product. The tell: in AWS's own design, the control enforcing each autonomy limit is almost always deterministic infrastructure, not the model choosing to stay in bounds.

AWS's own CTO framed the human in the loop as something to eventually design out: "At some point the human becomes an obstacle." Where you set that dial is a risk decision, not a convenience one.

**Whatever tooling you use, adopt the learn-then-enforce dial as your deployment default.** New agent, or new capability, starts supervised. It earns unattended operation on a specific action only after the controls around that action have proven out. Write down which categories your agents are in "enforce mode" for today, and ask whether each one actually earned it or just defaulted there because nobody set the dial.

[AWS Continuum announcement →](https://www.aboutamazon.com/news/aws/aws-summit-nyc-2026-ai-agents) · [Analysis →](https://www.digitalapplied.com/blog/aws-summit-ny-2026-agentcore-continuum-context-agents)

---

## Where this is going

Three stories, one current. The MCP spec pushes enforcement to the endpoint. The role-confusion paper proves the model itself can't be the enforcement point. Continuum's design concedes that the durable control is deterministic infrastructure with a human dial, not the agent's judgment. Put those together and the direction is clear: security for agents is moving out of the model and into the boundaries around it.

The 2025 instinct was to make the model harder to trick. The 2026 consensus is that you make the blast radius smaller and the authorization explicit, because the model will be tricked and you plan for it.

"Stop the model from ever being fooled" is unwinnable. "Contain what a fooled model can reach, and prove the containment holds" is ordinary security engineering. The frontier isn't a smarter filter. It's a smaller, provable perimeter.

---

## From the lab

- **Loop Engineering on Your Own Hardware** — the self-hosted autonomous loop, with a security section on what an unsupervised agent can and can't be trusted to verify about its own work. The role-confusion paper is the deeper "why" underneath that caution. [Read it →](https://aminrj.com/posts/loop-engineering-on-your-own-hardware/)

---

## Tooling worth knowing

- **Agent Security Scorecard** — score your agents against the OWASP Agentic Top 10 (2026) in about 12 minutes. [Take the scorecard →](https://scorecard.aminrj.com)
- **MCP Server Security Hub (Backslash)** — a free tool to vet MCP servers on security posture. [Vet your servers →](https://mcp.backslash.security)
- **AI Agent Pre-Deployment Security Checklist** — free, built from real assessments. [Get the checklist →](https://aminrj.com/resources/predeployment-checklist/)

---

## One thing to check this week

Build your MCP inventory before July 28. One row per MCP server your team uses, four columns: (1) local or remote? (2) do handles expire and are they user-bound? (3) can it render HTML into the IDE? (4) is filesystem scope structurally enforced or just a convention? You won't have clean answers for every server, and the blanks are the finding. That table turns three weeks of lead time into a concrete backlog.

I'm running this exact inventory on my own stack ahead of the deadline. [I'm writing up how on the blog →](https://aminrj.com/posts/agent-permission-model/)

---

## What I'm watching

→ **The endpoint becomes the agent-security battleground** — as agents run locally in IDEs and on developer laptops, the network gateway stops being the control point. Expect a wave of endpoint-layer agent-security tooling.

→ **Role confusion reframes the defense conversation** — if injection is a measurable consequence of how the model perceives "who's speaking," the research agenda shifts from better filters to genuine role perception at the architecture level.

→ **Graduated trust as the deployment standard** — learn-mode-to-enforce-mode, autonomy earned category by category, is showing up in shipping products now. The open question is who controls the dial and how fast they turn it.

→ **OAuth 2.1 finally mandatory for MCP, and mostly unimplemented** — the new spec makes it non-negotiable, but audits still find most public MCP servers with no auth or long-lived static keys. The gap between "the spec requires it" and "the ecosystem ships it" is the attack surface for the back half of 2026.

→ **The cybersecurity agent build** — next issue: I'm running my own pre-July-28 MCP hardening pass live, per-request handle validation, structural filesystem scope, and an MCP Apps review policy, and reporting what broke and what held.

---

I write the full technical deep-dives on the aminrj.com blog. If this newsletter is useful, [that's where the long-form work lives →](https://aminrj.com/).

Questions, pushback, something I missed, reply directly. I read everything.

Cheers, **Amine**
