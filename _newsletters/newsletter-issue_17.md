---
title: "Your agents have no idea who they are. Attackers are counting on it."
Subject: "[AI Sec Intel] #17 | Your agents have no idea who they are. Attackers are counting on it."
preview_text: "Identiverse 2026 named agent identity the defining problem of the year. Step Finance lost $27M because its agents could move money without asking. The fix is testable. Here's the test."
subtitle: "Delegation, not impersonation, is now the industry's official design pattern. Two production incidents show exactly what ignoring it costs."
issue: 17
date: 2026-06-27
---

Hey 👋

I spent most of last week on a trail with no signal, which is the only reliable way I know to actually think instead of just reacting to the feed.

What I kept circling back to: almost everything I write about in this newsletter is a symptom. The disease underneath is nearly always the same one. Tool poisoning, prompt injection, the allowlist that betrays you, the supply-chain backdoor: they all do damage in proportion to what the agent was allowed to be and do without anyone being able to say which agent did it. Strip the incidents down to the studs and you keep hitting the same load-bearing wall: we deployed a workforce of autonomous things and never gave them identities, scoped permissions, or a revocation switch.

I've said versions of this before (Issue #5, Issue #13). The difference this week is that the rest of the industry stopped treating it as a nice-to-have. So this issue is less "patch this CVE" and more "here is where the field is going, and here is the test you can run on Monday to find out if you're standing on the right side of it."

For the deeper technical version of how I think about scoping agent permissions, [it's on the aminrj.com blog.](https://aminrj.com/posts/agent-permission-model/)

---

## This week in AI security

**The identity industry just named agent identity the defining problem of 2026.**

Identiverse 2026 wrapped last week and the takeaway was unambiguous: governing non-human identities and AI agents dominated the keynotes, the sessions, and all 200-plus booths on the floor. Ping Identity CEO Andre Durand framed the shift as "actions, not access", moving from static who-are-you access control to continuous what-are-you-doing-right-now decisions. Non-human identities now outnumber humans by a significant margin in the average enterprise, and in cloud-native shops the ratio runs far higher. The same week, Estonia moved to assign digital identities to AI agents so that every agent action traces back to accountability and a human link. Okta, Ping, Token, and Securden all shipped or expanded agent-identity products in the same stretch. When the entire identity sector pivots in one quarter, that's the market pricing in a structural change.

> **The consensus that emerged is worth memorizing, because it's the design pattern you'll be held to: delegation, not impersonation.** An agent should act as itself, with its own identity, carrying a delegated and scoped slice of a human's authority. Never by borrowing the human's credentials wholesale. The moment an agent runs as you, with your token, every action it takes is indistinguishable from your own in the logs, and an injected prompt inherits your entire blast radius. Delegation with a distinct agent identity means you can scope it, attribute it, and revoke it without burning down the human account behind it. If your agents currently authenticate with a shared service account or a human's API key, you're on the impersonation side of this line, and the whole industry just agreed that's the wrong side.

> **Run the cheapest audit there is this week: can you name every agent in your environment, and who owns each one?** Not the service accounts. The agents. Most teams cannot produce this list, and "we don't have an inventory" is the finding. Start one. One row per agent: what it is, which human owns it, what credential it authenticates with, and what it's allowed to touch. The act of filling in that table surfaces the over-privileged and orphaned agents faster than any scanner, because the blanks are the vulnerabilities.

[Forrester's Identiverse recap](https://www.forrester.com/blogs/identiverse-2026-recap-identity-security-for-agentic-ai-dominates/) · [Estonia assigns IDs to agents](https://www.biometricupdate.com/202606/identity-emerges-as-governance-layer-for-agentic-ai)

---

**$27 million walked out the door because the agents could move money without asking.**

If the identity story sounds abstract, here's the concrete version. At Step Finance, a Solana DeFi portfolio manager, attackers compromised executive devices in January. Ordinarily that's a bad day, not a catastrophe. What made it a catastrophe: AI trading agents that held permission to execute large token transfers with no human approval in the path. Once inside, the attackers didn't need to defeat the agents. They just used them. The agents moved 261,000+ SOL, somewhere around $27-30 million, doing exactly what they were designed to do. About $4.7M was recovered. The token fell 97%. The company shut down. The post-incident detail that should sting every team running agents: a large share of DeFi teams were operating with shared API keys, so there was no per-agent identity to scope, throttle, or revoke when it mattered.

> **The agents weren't hacked. They were used, because their permissions had no upper bound and their identity had no human gate on irreversible actions.** This is the lethal-trifecta lesson from last issue, except the exfiltration channel is a money transfer and the loss is final. The lesson isn't "AI agents are dangerous." It's that an autonomous identity with standing authority to take irreversible actions is a privileged account, and we have known how to handle privileged accounts for twenty years. We just stopped applying it the moment the account started calling itself an agent.

> **Find every irreversible or high-consequence action your agents can take unattended (move money, delete data, change access rights, modify production, release confidential data) and put a human approval gate on that specific list.** Not on everything; that kills the utility. Just the actions you can't undo. Token productized exactly this control: a human must biometrically approve high-consequence agent actions. But you don't need a vendor to start. You need a list of irreversible actions and a gate in front of it.

[Step Finance and four other 2026 agent breaches](https://beam.ai/agentic-insights/ai-agent-security-breaches-2026-lessons)

---

**Cline's own post-mortem said the quiet part out loud: an LLM with shell access in CI processing untrusted input is the same as giving every stranger shell access.**

In February, an attacker used a compromised npm publish token to ship a malicious `cline@2.3.0` with a postinstall script. The published payload turned out benign and the window was about eight hours, so the direct impact was limited. The valuable part is what Cline documented in the cleanup. Their AI-powered issue-triage workflow had shell access, processed untrusted issue text from arbitrary GitHub users, and opened a prompt-injection path to code execution on CI runners, which then chained with cache poisoning and token handling gaps. Their own conclusion, stated plainly: giving an LLM shell access in a CI context where it processes untrusted input is functionally equivalent to giving every GitHub user shell access on your runners.

> **This is the identity problem wearing CI/CD clothes.** The triage agent had no scoped identity of its own; it inherited the pipeline's privileges, and the pipeline could reach publish tokens. An agent that reads untrusted input (issues, PRs, tickets, emails) and also holds privileged credentials is the trifecta again, in your build system, where there's no human watching in real time. The honesty of Cline's write-up is the real takeaway: they didn't blame a clever attacker, they named the architecture. Borrowed privilege plus untrusted input plus a credential within reach.

> **Audit one AI-driven automation in your pipeline this week and ask three things: does it process input from people outside your team, does it have shell or tool access, and can it reach a real credential (publish token, deploy key, cloud secret)?** If the answer is yes-yes-yes, that's a Cline-class exposure regardless of whether anything has gone wrong yet. Give the automation its own minimal-scope identity, strip its standing access to publish/deploy credentials, and require a human merge before it runs against outside contributions.

[Cline post-mortem analysis](https://www.penligent.ai/hackinglabs/ai-agents-hacking-in-2026-defending-the-new-execution-boundary/)

---

## Where this is going

A pattern is forming across all three stories, and it's the thing I kept turning over on the trail.

The first era of AI agent security was about the model: jailbreaks, prompt injection, "can we make it say something bad." The era we're entering is about the identity: what the agent is permitted to be, whose authority it carries, and whether you can attribute and revoke its actions. Prompt injection isn't going away (OWASP's June report calls it a permanent architectural flaw, not a patchable bug), so the entire defensive center of gravity is shifting from "stop the agent from being tricked" to "limit what a tricked agent can actually do." That second framing is winnable. The first one isn't, and the field has finally admitted it.

The standards are racing to catch up and none of them have crossed the finish line: SPIFFE, OAuth 2.1 for agent-to-MCP auth, ID-JAG, AIUC-1, and a handful of IETF drafts, all less than a year old or still in progress. The practical read: you don't get to wait for the standard. The control pattern (distinct identity, delegated and scoped authority, short-lived credentials, human gate on irreversible actions, full attribution) is stable even while the protocols settle. Build to the pattern now and swap in the standard later.

---

## From the lab

- **The cybersecurity agent build:** I've been building an agent that goes from "reads threat feeds" to "acts on what it finds," and the entire hard part is exactly this issue's theme: how to grant useful autonomy without granting standing authority a poisoned input can turn against me. The permission model, the allowlist of validated operations, and the human gate on irreversible actions are the spine of it. [Follow the build.](https://aminrj.com/posts/agent-permission-model/)
- **Loop Engineering on Your Own Hardware:** the flip side of standing authority. An autonomous loop that runs unattended on your own GPU. The security section is the part that matters here: what an unsupervised agent can and can't be trusted to verify about its own work. [Read it.](https://aminrj.com/posts/loop-engineering-on-your-own-hardware/)

---

## Tooling worth knowing

- **Agent Security Scorecard:** score your agents against the OWASP Agentic Top 10 (2026) in about 12 minutes. This issue's identity-and-authorization gap (ASI03) is exactly what it probes: per-agent identity, scoped permissions, and revocation. If the "name every agent and its owner" audit above turned up blanks, this is the structured version of the same exercise. [Take the scorecard.](https://scorecard.aminrj.com)
- **AI Agent Pre-Deployment Security Checklist:** the identity and permissions sections map one-to-one onto the controls in this issue: distinct identity, least privilege, human gate on irreversible actions, revocation. Free, built from real assessments. [Get the checklist.](https://aminrj.com/resources/predeployment-checklist/)

---

## One thing to check this week

Pick your single most autonomous agent and answer four questions about it, honestly, in writing:

1. **Identity:** does it have its own credential, or does it run as a shared service account or a human's key?
2. **Scope:** list what it can actually reach. Is that list the minimum it needs, or everything that was convenient?
3. **Irreversible actions:** what can it do that you cannot undo (money, deletion, access changes, production writes, data release)? Is there a human gate on those specific actions?
4. **Revocation:** if this one agent were compromised right now, can you kill its access without breaking everything else?

If any answer is "no" or "I'm not sure," that's not a gap in your prompt-injection defenses. It's a gap in your identity model, and that's the one the whole field just agreed is the real fight. Fix the worst answer for one agent this week. That's the entire job, scoped down to something you can finish before Friday.

I'm working through these exact four questions on my own agent build. [Follow along on the blog.](https://aminrj.com/posts/agent-permission-model/)

---

## What I'm watching

→ **"Actions, not access" as the new model.** The shift from static permissions to continuous, real-time authorization decisions is the direction every major identity vendor just committed to. Watch whether the tooling can actually make those decisions at machine speed, or whether it becomes the bottleneck it was meant to remove.

→ **Delegation vs impersonation hardening into doctrine.** Agents acting as themselves with delegated authority, never borrowing a human's credentials. This is becoming the default design pattern. Expect "our agent runs as a shared service account" to read, by year end, the way "we store passwords in plaintext" reads today.

→ **Standards that aren't finished but already matter.** SPIFFE, OAuth 2.1 for agents, ID-JAG, AIUC-1, IETF drafts. None are final. All are shaping product roadmaps now. The teams that build to the control pattern (not a specific protocol) will swap standards in cleanly; the teams that wait will be retrofitting under pressure.

→ **AI-vs-AI on vulnerability discovery.** FIRST now forecasts 2026 landing near 66,000 CVEs, driven largely by autonomous discovery agents. The share needing urgent patching stays roughly flat, so the real skill is pulling signal from a near-doubling of noise. Triage, not discovery, is the 2026 bottleneck.

→ **The cybersecurity agent build.** Next issue: I'm wiring the delegation-not-impersonation pattern into my own agent (its own identity, scoped tokens, a human gate on the irreversible actions) and testing it against poisoned inputs to see whether the identity boundary actually holds where the prompt-injection defense doesn't.

---

I write the full technical deep-dives on the aminrj.com blog: agent security patterns, lab tests, framework breakdowns. If this newsletter is useful, [that's where the long-form work lives.](https://aminrj.com/)

Questions, pushback, something I missed? Reply directly. I read everything.

Cheers, **Amine**
