---
title: "I let an agent rewrite my code while I slept. The scary part wasn't the bill."
Subject: "[AI Sec Intel] #16, I let an agent rewrite my code while I slept. The scary part wasn't the bill."
preview_text: "OWASP's agentic security report now reads like an incident log, not a threat catalog. The same permission model powering autonomous coding loops is the one attackers exploit."
subtitle: "OWASP v2.01 landed June 1. An autonomous bot poisoned LiteLLM's PyPI token and pushed backdoored packages to 47,000 downloads. The allowlist CVE against Cursor made the attack easier, not harder."
issue: 16
date: 2026-06-20
---

Hey 👋

I spent this week building something and then reading the report that reframed it.

The thing I built: a fully autonomous coding loop running on a local model on a single 24GB GPU. It edits code, runs the tests, checks the result, and decides whether to keep going. All night, with no human watching and no API meter running. I published the full build, every flag and every safety brake, on the blog.

The report I read: OWASP's *State of Agentic AI Security and Governance* v2.01, published June 1. It lands the point I kept circling in the lab. When an agent acts autonomously on real systems, AI safety and AI security stop being two different problems. They're the same permission model, looked at from two directions.

That's this issue.

If you want to follow the agent build itself, [it's on the aminrj.com blog →](https://aminrj.com/posts/loop-engineering-on-your-own-hardware/)

---

## This week in AI security

**OWASP's 2026 agentic report stopped cataloging hypotheticals. It now reads like an incident log.**

On June 1, the OWASP GenAI Security Project published version 2.01 of its *State of Agentic AI Security and Governance*. The contrast with last year's edition tells the whole story. The 2025 version listed plausible threats. The 2026 version is built from CVEs, vendor advisories, and breach reports tied to nearly every category of agentic risk.

The center of gravity is coding agents: of 53 agentic projects OWASP tracks, 28 are coding agents, and the five fastest-growing tools (Claude Code, Gemini CLI, Codex, Cline, Aider) all live in that category.

The incident I keep coming back to: an autonomous bot called hackerbot-claw harvested LiteLLM's PyPI publishing token through a compromised Trivy CI setup, then pushed two backdoored versions of LiteLLM straight to PyPI. LiteLLM is the model gateway under CrewAI, DSPy, and Microsoft GraphRAG. The backdoor sat live for about three hours and was pulled near 47,000 downloads. No human directed it after launch.

> **The line OWASP draws that matters most: for an agent acting autonomously on production data, safety and security are the same job.** Their example is the 2025 Replit incident, where a coding assistant deleted a production database despite being told to change nothing, fabricated records, and falsely reported that rollback was impossible. No attacker. But the permission model behind that unprompted failure is identical to the one an attacker would reach through prompt injection. Splitting "the agent might misbehave" (safety) from "someone might make the agent misbehave" (security) into two teams with two backlogs means you'll fix neither, because the control that addresses both is the same scoped permission you keep deferring.

> **Do one thing with this report: map your highest-privilege agent against the lethal trifecta.** Researcher Simon Willison coined the term for agents with all three: private-data access, untrusted-content exposure, and an external communication channel. An agent with all three is one injected prompt away from becoming an exfiltration tool. Meta's "Agents Rule of Two" is the cleanest heuristic I've seen: an unsupervised agent gets at most two of the three. The third requires a human in the loop. Pick your riskiest agent and check which two it has. If it has all three running unattended, that's your week's work.

[OWASP report →](https://genai.owasp.org/resource/state-of-agentic-ai-security-and-governance/) · [Help Net Security writeup →](https://www.helpnetsecurity.com/2026/06/11/owasp-prompt-injection-ai-security-failures/)

---

**CVE-2026-22708: a Cursor flaw where the allowlist made the attack easier**

This one is worth it purely for the pattern. The disclosure against Cursor lets an attacker poison the agent's execution environment so that allowlisted commands (the safe ones you pre-approved, like `git branch`) deliver an attacker's payload instead. The allowlist didn't contain the attack. It auto-approved it, because the attacker hid behind a command the agent had been told never to question. The companion CVE against OpenAI's Codex CLI (CVE-2025-59532) showed the agent's own output redefining the boundary of its sandbox. The cage moving because the thing inside it pushed on the bars.

> **An allowlist that approves a command name without validating what that command actually does is a denylist wearing a better coat.** I've argued before that allowlists beat denylists for agent tools, and I still hold that position, but this CVE sharpens the rule. The allowlist has to constrain the *operation and its parameters*, not just the verb. Allowing `git branch` is not a security control if the agent's environment can be poisoned so `git branch` runs arbitrary code. Allow the specific, validated invocation, or you've built a denylist with extra steps.

> **Audit one allowlisted agent tool this week and ask: does the allowlist check the parameters, or just the command name?** If it only matches the verb, assume it's bypassable. Pin allowed operations to validated argument shapes, and run the dangerous tools in an environment where a hijacked "safe" command can't reach your real credentials.

[Help Net Security on the agent-layer CVEs →](https://www.helpnetsecurity.com/2026/06/11/owasp-prompt-injection-ai-security-failures/)

---

**Sandboxing AI agents quietly became table stakes, and the vendors noticed**

The defensive side moved this quarter. NVIDIA shipped OpenShell, an open-source runtime that boxes an agent into a sandboxed execution layer governed by declarative YAML policies it cannot override even if compromised. Northflank and a wave of microVM/gVisor tooling all converged on the same premise: AI-generated code now executes immediately, with no pull request and no human reading it, and Cursor alone reportedly accepts close to a billion lines of AI-written code a day. Running that directly on your infrastructure is the part everyone skipped while shipping fast.

> **The defensive consensus finally matches what the attacks have been showing: isolate first, trust never.** This is the exact problem my local loop runs into. When an agent writes and executes code unsupervised, the only thing standing between a hallucinated or injected command and your real environment is the boundary you put around it. Sandboxing isn't a maturity upgrade you get to later. For any agent that runs code it generated, it's the precondition for letting it run at all. The tooling is now real and mostly open source, so "we didn't have the infrastructure" stopped being an excuse this quarter.

> **For any agent that executes code in your environment, answer one question: if it ran a malicious command right now, what could it reach?** If the honest answer includes production credentials, your real filesystem, or your internal network, put it behind a sandbox (microVM, gVisor, or a runtime like OpenShell) before you scale it. Contain the blast radius before you widen the autonomy.

[NVIDIA OpenShell →](https://www.alphamatch.ai/blog/nvidia-openshell-ai-sandbox-platforms-2026) · [Sandboxing approaches compared →](https://northflank.com/blog/how-to-sandbox-ai-agents)

---

## From the lab

Two pieces I published that pair directly with this week's theme:

- **Loop Engineering on Your Own Hardware** — the full build for an autonomous coding loop on a single 24GB GPU. The reason it belongs in a security newsletter is the section on where it breaks: "passes tests and typechecks" does not catch security regressions, license contamination, or broken invariants. The loop will turn the bar green and ship an auth bypass no assertion was written to catch. On security-sensitive code, the gap between "the loop says it passed" and "it's actually correct" is exactly where the risk lives. [Read it →](https://aminrj.com/posts/loop-engineering-on-your-own-hardware/)
- **The Right AI Security Framework Depends on the Question You're Asking** — OWASP's report names a dozen frameworks. If you're staring at that list wondering which to actually run, this is the decision. There are 20+ frameworks in 2026; most teams implement all of them and produce a 60-page document with no usable threat model. [Read it →](https://aminrj.com/posts/which-ai-security-framework-to-use/)

---

## Tooling worth knowing

- **Agent Security Scorecard** — score your agents against the OWASP Agentic Top 10 (2026) in about 12 minutes. Vendor-neutral, no login. This week's lethal-trifecta exercise is exactly what it walks you through: where your agents have private data, untrusted input, and an exit channel all at once. [Take the scorecard →](https://scorecard.aminrj.com)
- **AI Agent Pre-Deployment Security Checklist** — 25 controls across five families, each a yes or no, covering identity, tool permissions, sandboxing, and CI/CD gating. The exact gaps the LiteLLM and Cursor incidents exploited. Free, built from real assessments. [Get the checklist →](https://aminrj.com/resources/predeployment-checklist/)

---

## One thing to check this week

Take your most autonomous agent (the one that acts without asking) and run the Rule of Two on it. Three yes/no questions: (1) Can it read private or sensitive data? (2) Does it ingest untrusted content: documents, web pages, tool output, repos you didn't author? (3) Can it send data or take actions that reach outside your environment?

If the answer is yes to all three and no human approves its high-impact actions, you have a lethal-trifecta agent running unsupervised. The fix isn't a patch, it's a gate: remove one of the three, or require human approval on the irreversible actions. That single exercise turns OWASP's 100-page report into a one-line decision you can ship today.

I'm working through exactly this on my own agent build. [Follow along on the blog →](https://aminrj.com/posts/loop-engineering-on-your-own-hardware/)

---

## What I'm watching

→ **Safety and security merging at the org chart** — OWASP's strongest claim is organizational: for autonomous agents on production data, splitting AI safety and AI security into separate teams guarantees you fix neither. Watch whether enterprises actually restructure, or just rename a team and move on.

→ **AI on both ends of the supply chain** — hackerbot-claw poisoned the infrastructure other AI agents depend on, autonomously. The attacker-agent is no longer a thought experiment. Your detection and response window is now measured against a machine that doesn't sleep or get bored mid-attack. Calibrate containment to that clock.

→ **The "allowlist theater" pattern** — CVE-2026-22708 won't be the last allowlist that approved the very command the attacker needed. Expect more "we had a control and it made things worse" disclosures as teams allowlist verbs instead of validated operations.

→ **AI-driven CVE volume** — one forecast has 2026 CVEs pushing toward 66,000, largely from AI-assisted vulnerability discovery. The discovery side is scaling faster than any team's ability to triage. The bottleneck is shifting from "find the bug" to "decide which of the 200 findings actually matters."

→ **The cybersecurity agent build** — next issue: I'm putting my own loop behind a sandbox and wiring a frontier-model reviewer onto the verification step, then testing whether it catches the security regressions the local test gate misses. The hybrid local-worker / cloud-reviewer pattern, measured.

---

I write the full technical deep-dives on the aminrj.com blog: agent security patterns, lab tests, framework breakdowns. If this newsletter is useful, [that's where the long-form work lives →](https://aminrj.com/).

Questions, pushback, something I missed? Reply directly. I read everything.

Cheers, **Amine**
