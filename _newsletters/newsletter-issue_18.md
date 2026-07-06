---
title: "On July 28, MCP changes shape. Three attack surfaces open where your gateway can't see them."
Subject: "[AI Sec Intel] #18 | On July 28, MCP changes shape. Three attack surfaces open where your gateway can't see them."
preview_text: "The new MCP spec goes final July 28 and moves security from the protocol to the endpoint. Plus: new research explains why prompt injection works, and it's not what you think. Here's what to check before the spec ships."
subtitle: "MCP goes stateless on July 28, relocating a whole category of security work from the protocol to the endpoint. Here's what changes, and the four checks to run before it ships."
issue: 18
date: 2026-07-04
---

Hey 👋

There's a date on the calendar that matters more than any single CVE this month: July 28. That's when the MCP 2026-07-28 specification goes final, and it's the biggest structural change to the protocol since it launched. The validation window is already open, Tier-1 SDKs are shipping support now, and the ecosystem starts moving the day it lands.

Here's why I'm leading with it instead of a fresh vulnerability. Most of what I cover in this newsletter is an attack against the current design. This is the design itself changing underneath you, and it quietly relocates a whole category of security work from the protocol layer (where it was handled for you) to the endpoint layer (where it's now your problem). No CVE will be filed for that. It won't show up in a scanner. It's the kind of shift you either prepare for in the next three weeks or inherit as an incident later.

So this issue is a get-ready issue. What's changing, why it matters, and the specific things worth checking before the spec ships. Plus a piece of research that reframes prompt injection in a way that finally explains why none of our filters ever fully work.

If you want the deeper version of how I think about scoping what an agent can reach, [it's on the aminrj.com blog →](https://aminrj.com/posts/agent-permission-model/)

---


## This week in AI security

**MCP goes stateless on July 28. The state doesn't disappear, it moves into the conversation, and three new attack surfaces open where your gateway can't see them.**

Since launch, MCP has been stateful. An agent connects, gets an `Mcp-Session-Id` in the HTTP header, and every request carries it. The model never saw that ID and never touched it, so it could never leak it. The new spec removes the handshake. Now when an agent calls something like `create_browser()`, the server returns a handle *inside the conversation*: `{ "browser_id": "browser-abc123" }`. The model sees it, holds it, and passes it back on every call. Akamai and Backslash both broke down what that opens up, and it comes to three distinct problems.

**Handle hijacking** replaces session hijacking. The handle is now just a string sitting in a chat transcript, a Jira ticket, a Slack paste, a tool response. Whoever can read or plant that string can replay it, unless the server checks the handle against the auth context rather than trusting the handle alone.

**The filesystem scope gap.** The old `Roots` capability, the one structural boundary on what paths an agent could touch, is deprecated. Scope enforcement is now opt-in, built by each server developer, and applied inconsistently.

**IDE HTML rendering.** The new MCP Apps extension (SEP-1865) lets servers ship interactive HTML that renders in a sandboxed iframe *inside your IDE*, right next to your source, your terminal, and every connected server. A fake VS Code auth prompt stops being a curiosity and becomes a credential-harvesting surface.
> **Here's the point worth sitting with: all three are invisible to network and gateway security, by design.** A handle string in a conversation isn't HTTP traffic. Filesystem access on a developer laptop never crosses the gateway. An IDE iframe rendering HTML generates no network signal. Your MCP gateway wasn't built badly. It was built for a different threat model, and the new spec moves the risk to the endpoint, where the gateway can't see. And to be clear, this is good engineering. Stateless scales, and the OAuth 2.1 hardening (mandatory PKCE, audience-bound tokens, `iss` validation per RFC 9207) closes real holes. But the security work that used to live at the session layer now happens on the endpoint only if you decide to put it there.
> **Run these four checks before July 28, while you still have lead time.** One: for each MCP server you run, are handles tied to a specific user, and do they expire? A handle that never expires is a permanent access token. Two: inventory which MCP servers run locally on developer machines, because those are the ones no network tool will ever surface. Three: find which servers can render HTML into the IDE (MCP Apps), and review that HTML the way you'd vet a third-party script on your website. Four: stop assuming your gateway covers MCP, and decide on purpose where your endpoint visibility comes from. None of this means migrating anything yet. It means knowing what you're standing on before the ground moves.

[Akamai's breakdown →](https://www.akamai.com/blog/security-research/new-mcp-specification-security-teams-must-prepare) · [Backslash: three new attack surfaces →](https://www.backslash.security/blog/new-mcp-spec-opens-new-attack-surfaces) · [The official release candidate →](https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/)

---


**New research: prompt injection works because models read *tone*, not role tags. That's why your filters keep failing.**

This is the most clarifying piece of research I've read this year, and it presents at ICML in Seoul on July 6. "Prompt Injection as Role Confusion" (Ye, Cui, Hadfield-Menell) traces injection to a single mechanism. An LLM receives the whole conversation as one stream of text, split by role tags (`user`, `tool`, `think`), and those tags are supposed to be the security boundary. But the model doesn't read role from the tag. It reads role from *how the text sounds*. The researchers built probes that measure how strongly the model internally believes a token belongs to a given role. They found that reasoning-style text registers as the model's own private thoughts even when it's explicitly wrapped in `user` tags. Their attack, **CoT Forgery**, injects fake reasoning that mimics the model's own thinking style, and it takes jailbreak success from near-zero to about 60% across every frontier model tested. The same mechanism explains ordinary agent injection: prepend "User:" to a malicious command buried in a webpage, and the model treats it as a trusted instruction. Across 1,000 exfiltration attempts, attack success rose from 2% to 70% in lockstep with how much role confusion the probe measured, *before a single token was generated*.
> **This is the mechanistic proof of something I keep saying: you cannot filter your way out of prompt injection, because to the model, sounding like a role is indistinguishable from being one.** Every content filter, every "ignore previous instructions" detector, every guardrail that inspects the text is playing a game the architecture already lost. The attacker isn't smuggling a keyword. They're impersonating a *voice*, and the model's own weights treat a convincing caricature of its reasoning as more genuinely its own than its real reasoning. The quieter warning is worse for anyone building shopping or browsing agents. Because role perception is a matter of degree, the mere *tone* of a retrieved page can bleed across the tag boundary and nudge an agent, with no explicit injection at all. An enthusiastic product page can steer a purchasing agent. That's testable at scale, and it's legal.
> **Stop pouring budget into "detect the bad prompt" as your primary defense. Move it to "limit what a fooled agent can do."** Assume the injection will land, because the research says it will. The controls that actually hold sit downstream of the model's confusion: scoped permissions, a human gate on irreversible actions, per-request authorization that doesn't trust the model's read of who's speaking. And if you run reasoning models, treat any externally sourced text that *looks like* structured reasoning as radioactive. That's the exact shape CoT Forgery exploits.

[The paper →](https://arxiv.org/abs/2603.12277) · [Plain-English writeup →](https://www.tomshardware.com/tech-industry/artificial-intelligence/ai-models-handed-over-a-cocaine-recipe-after-being-told-the-user-was-wearing-a-green-shirt)

---


**AWS shipped Continuum, and the interesting part isn't the AI, it's the "graduated trust" dial.**

At its NY Summit on June 17, AWS launched Continuum, an agentic security platform that runs the full vulnerability lifecycle: discover, prioritize by business context, *prove exploitability by building a working exploit in a sandbox*, then propose a validated fix. That validation step is the genuinely novel part, concrete reproducible proof instead of a probabilistic severity score. But the design choice worth your attention is the governance one. Continuum ships in "learn mode" by default, with a human in the loop on every recommendation. Organizations graduate it to "enforce mode" for autonomous remediation *category by category*, only as they build confidence. AWS was blunt about why: the "Mythos moment," where specialized models now find and chain vulnerabilities faster than any human SOC can triage, forcing defenders to operate at machine speed too.
> **This is the whole industry converging on the pattern I've been building toward: you don't grant an agent autonomy, you let it earn autonomy, one bounded category at a time, with the limit enforced by deterministic infrastructure rather than the model's good behavior.** It's the same progressive-autonomy model the Five Eyes guidance landed on (Issue #13), now baked into a shipping product with a trust ladder you climb one rung at a time. The tell: in AWS's own design, the control enforcing each autonomy limit is almost always deterministic infrastructure, not the model choosing to stay in bounds. That's the right instinct. There's a counter-current worth noting, though. AWS's own CTO framed the human in the loop as something to eventually design *out* ("at some point the human becomes an obstacle"). That's the tension of the next two years in one sentence, and where you set that dial is a risk decision, not a convenience one.
> **Whatever tooling you use, adopt the learn-then-enforce dial as your own deployment default.** New agent, or new capability on an existing one, starts supervised. It earns unattended operation on a specific action only after the controls around that action have proven out. Write down which categories your agents are in "enforce mode" for today, and ask whether each one actually earned it or just defaulted there because nobody set the dial.

[AWS Continuum announcement →](https://www.aboutamazon.com/news/aws/aws-summit-nyc-2026-ai-agents) · [Analysis of the trust-ladder design →](https://www.digitalapplied.com/blog/aws-summit-ny-2026-agentcore-continuum-context-agents)

---


## Where this is going

Three stories, one current running under all of them. The MCP spec pushes enforcement to the endpoint. The role-confusion paper proves the model itself can't be the enforcement point. And Continuum's design concedes that the durable control is deterministic infrastructure with a human dial, not the agent's judgment. Put those together and the direction is unmistakable: **security for agents is moving out of the model and into the boundaries around it.** The 2025 instinct was to make the model harder to trick. The 2026 consensus, forming in real time across a research paper, a protocol revision, and a hyperscaler product in the same three weeks, is that you make the *blast radius* smaller and the *authorization* explicit, because the model will be tricked and you plan for it.

That's not a counsel of despair, it's a relief. "Stop the model from ever being fooled" is unwinnable. "Contain what a fooled model can reach, and prove the containment holds" is ordinary security engineering, the kind we've done for decades. The frontier isn't a smarter filter. It's a smaller, provable perimeter.

---


## From the lab

- **The cybersecurity agent build** — this is exactly the perimeter I've been building: an agent that acts on what it finds, with its authority scoped, its irreversible actions gated, and the enforcement living in the infrastructure rather than the prompt. Everything in this issue is a reason that architecture is the right one. [Follow the build →](https://aminrj.com/posts/agent-permission-model/)
- **Loop Engineering on Your Own Hardware** — the self-hosted autonomous loop, and the security section on what an unsupervised agent can and can't be trusted to verify about its own work. The role-confusion paper is the deeper "why" underneath that caution. [Read it →](https://aminrj.com/posts/loop-engineering-on-your-own-hardware/)


---


## Tooling worth knowing

- **Agent Security Scorecard** — score your agents against the OWASP Agentic Top 10 (2026) in about 12 minutes. As the MCP spec pushes enforcement to your side of the line, the identity, authorization, and scoping checks it runs are exactly the controls you now own outright. [Take the scorecard →](https://scorecard.aminrj.com)
- **MCP Server Security Hub (Backslash)** — a free tool to vet MCP servers on security posture. Useful right now for the pre-July-28 inventory: which of your servers run locally, and which can render HTML into the IDE. [Vet your servers →](https://mcp.backslash.security)
- **AI Agent Pre-Deployment Security Checklist** — the scoping, least-privilege, and human-gate controls map directly onto the endpoint work the new spec hands you. Free, built from real assessments. [Get the checklist →](https://aminrj.com/resources/predeployment-checklist/)


---


## One thing to check this week

Build your MCP inventory before July 28. It's the prerequisite for everything else. One row per MCP server your team uses, four columns: (1) local or remote? (local means invisible to network monitoring, so it's your endpoint's job); (2) does it issue handles that are user-bound and time-limited, or handles that work forever for anyone? (3) can it render HTML into the IDE via MCP Apps? (4) is filesystem scope structurally enforced, or just a convention the developer promised to honor? You won't have clean answers for every server, and the blanks *are* the finding. That table turns three weeks of lead time into a concrete backlog, instead of finding out the hard way after the spec ships and the ecosystem moves.

I'm running this exact inventory on my own stack ahead of the deadline. [I'm writing up how on the blog →](https://aminrj.com/posts/agent-permission-model/)

---


## What I'm watching

→ **The endpoint becomes the agent-security battleground** — the MCP spec is the forcing function, but the pattern is bigger: as agents run locally in IDEs and on developer laptops, the network gateway stops being the control point. Expect a wave of endpoint-layer agent-security tooling, and expect the teams still relying on gateway-only visibility to have a blind spot they can't see into.

→ **Role confusion reframes the whole defense conversation** — if injection is a measurable consequence of how the model perceives "who's speaking," the research agenda shifts from better filters to genuine role perception at the architecture level. Watch whether the labs can build models that actually distinguish instruction from data, because until they do, containment is the only real defense.

→ **Graduated trust as the deployment standard** — learn-mode-to-enforce-mode, autonomy earned category by category, is showing up in shipping products now, not just guidance documents. The open question is who controls the dial and how fast they turn it, especially with vendors already framing the human-in-the-loop as friction to remove.

→ **OAuth 2.1 finally mandatory for MCP, and mostly unimplemented** — the new spec makes it non-negotiable, but audits still find most public MCP servers with no auth or long-lived static keys. The gap between "the spec requires it" and "the ecosystem ships it" is the attack surface for the back half of 2026.

→ **The cybersecurity agent build** — next issue: I'm running my own pre-July-28 MCP hardening pass live, per-request handle validation, structural filesystem scope, and an MCP Apps review policy, and reporting what broke and what held when I tested it against the endpoint attack surfaces from this issue.

---


I write the full technical deep-dives on the aminrj.com blog: agent security patterns, lab tests, framework breakdowns. If this newsletter is useful, [that's where the long-form work lives →](https://aminrj.com/).

Questions, pushback, something I missed, reply directly. I read everything.

Cheers, **Amine**
