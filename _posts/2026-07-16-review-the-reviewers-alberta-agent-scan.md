---
title: "Review the Reviewers: The Security Questions Behind Alberta's 466-Million-Line AI Code Scan"
date: 2026-07-16
categories: [AI Security, Agentic AI]
tags: [ai-security, agentic-ai, ai-governance, cloud-security]
description: "Alberta ran roughly 50 AI agents across every repository the province owns. The results are impressive. Here is the security review I would run on the review itself."
image:
  path: /assets/media/ai-security/review-the-reviewers.png
---

Earlier this month, the Government of Alberta became the first government I know of to publish a portfolio-wide AI agent code review with real numbers attached. Roughly 50 Claude Code agents, running Opus and Sonnet models in parallel, scanned 466 million lines of code in about 20 hours. The scan covered every repository the province owns: around 1,280 applications and 3,400 repositories serving all 27 provincial ministries. The team estimates the same review done conventionally would have taken about 6.5 years.

I want to be clear up front: I think this is good work, and publishing it is better work. Most governments sit on decades of unreviewed code and say nothing. Alberta reviewed all of it, fixed a lot of it, and released technical white papers so other governments can copy the approach.

But I run agent deployments against production infrastructure for a living, and the headline numbers are the easy part. What decides whether a deployment like this is safe is the architecture around the agents, and that is exactly what a case study leaves out. So this post is the security review I would run on the review itself: what Alberta has documented, what remains open, and what good answers look like for anyone planning to copy this.

One caveat before we start. The numbers come from Anthropic's case study and the ministry's own statements. They are self-reported by the vendor and the customer. I have no reason to doubt them, but treat them as claims, not audit findings.

I covered the Alberta scan alongside the autonomous-hackbot story in [this week's newsletter](/newsletter/newsletter-issue-20/); this post is the long-form version of the Alberta half.

## What Alberta actually did

The published material describes three workstreams.

**The scan.** Around 50 agents worked autonomously and in parallel across every repository. The pipeline was two-stage: a deterministic rules engine flagged known patterns first, then the agents reviewed those flags and cited the exact file and line for each finding so developers could verify them. The scan surfaced issues that traditional scanners had missed.

**The fixes.** Where the scan found a vulnerability, Claude Code often generated a fix, tested it, and built it. Where a system lacked the tests needed to confirm a patch was safe, the agent wrote the tests first. Where code was too old to patch efficiently, it was rebuilt in a modern language. One subsidy portal, hand-coded in Java about 25 years ago and originally a five-month build, was rebuilt in four to five days. Every patch was reviewed and approved by the ministry's engineers before it shipped.

**The continuous layer.** The ministry built specialized review agents on the Claude Agent SDK that run throughout development: a red-team agent that probes applications from the outside the way an attacker might, a blue-team agent that assesses defenses against an international security standard and writes a remediation plan pointing to exact files, plus agents for code quality and public-facing content. Every application is checked against roughly 95 security controls per pass.

Credit where it is due, because several of the right controls are documented:

- A deterministic prefilter in front of the agents, so the expensive reasoning runs on flagged candidates rather than raw volume
- File-and-line citations on every finding, which makes each result independently verifiable by a human
- Tests written before patches where coverage was missing
- A human review and approval gate on every patch before it shipped

That is a better pipeline shape than most enterprise deployments I have assessed. Now for the questions the public material does not answer.

## The most privileged system in the province

Here is the framing that matters. For those 20 hours, the review fleet was plausibly the most privileged system in Alberta: 50 autonomous workers with read access to every line of code the province runs, including the systems that hold tax records, procurement data, and social services case files. And the fleet's output, a ranked map of every weakness in that estate, is one of the most valuable single artifacts a government can produce. An attacker who steals the findings database gets the benefit of the 20-hour scan without paying for it.

This is not a hypothetical concern. The same month Alberta's case study landed, two bug bounty hunters published the results of their autonomous hackbot: 126 vulnerabilities in five months, with the striking detail that most of their token spend went to keeping the bot authenticated, because the critical bugs sit behind login. Autonomous offense pays its biggest costs for authenticated access. A deployed review fleet is exactly that, pre-assembled.

So the questions below are not criticism of Alberta. They are the questions any security lead will be asked the day they propose the same deployment, and the answers determine whether the copy is safe.

## Seven questions, and what good looks like

### 1. What identity did each agent run under?

Fifty agents can run as fifty identities or as one shared credential cloned fifty times. The difference decides everything downstream: whether you can attribute an action to a specific worker, whether you can revoke one agent without stopping the fleet, and whether your audit logs mean anything at all. Shared credentials across agents are the single most common failure I see in agent deployments.

**What good looks like:** one workload identity per agent worker, short-lived credentials issued at spawn, independent revocation, and the initiating human principal recorded in the delegation chain. If two agents can present the same credential, you can neither attribute nor contain either of them.

### 2. What could the agents reach besides code?

Read access to 3,400 repositories is the stated scope. The real scope is defined by the environment: could the workers reach live source control or a mirror, could they reach the network, could they reach each other? A worker that reads a repository from a snapshot inside an isolated project is a very different risk from a worker holding tokens against the production version control system, where "read-only" still includes cloning everything, enumerating members, and reading CI configuration.

I learned this the uncomfortable way. We gave an SRE agent read-only access across a multi-cluster Kubernetes fleet, on the assumption that observe-level access was the safe rung to start on. It wasn't. Read-only in Kubernetes still means reading every Secret, every service-account token, and every ConfigMap stuffed with connection strings, which is to say the agent had a full data-exfiltration surface before it did anything a human would recognize as "write." The prompt-level guardrails we had bolted on failed in ways that were almost funny. The infrastructure controls, scoped identity, Terraform-managed permissions, deterministic gates, were the only things that held. I put the whole story into a fwd:cloudsec talk this year; the one-line version is that read access is not a security boundary, and Alberta's 3,400 repositories are that same lesson at portfolio scale.

**What good looks like:** agents run against a read-only mirror or snapshot, never live origin. Network egress is denied by default and granted per destination, which in this design means the model endpoint and nothing else. Workers cannot reach each other.

### 3. Where did 466 million lines of government code travel?

Code is data, and government code is sensitive data twice over: the logic itself, and everything embedded in it. Any estate this old and this large contains hardcoded credentials, connection strings, internal hostnames, and API keys scattered through repositories and configs. A full-estate scan moves all of that through an inference pipeline. Which tenancy served the models, what region, what retention applied to prompts and outputs, and whether the provider's data handling was contractually pinned are not procurement trivia. They are the difference between a security review and a bulk export.

**What good looks like:** a dedicated or regionally pinned inference tenancy, contractual zero retention on inputs and outputs, and a secrets sweep that runs before the agent scan so embedded credentials are rotated rather than shipped.

### 4. What happens when the code talks back?

Every repository is untrusted input. Comments, string literals, README files, commit messages, and vendored third-party code all flow into the agent's context, and any of it can carry instructions aimed at the model rather than the compiler. Across 3,400 repositories the question is not whether adversarial text is present, it is what the agent can do when it encounters it. This is where Alberta's citation requirement quietly earns its keep: a finding anchored to a file and line is checkable, so a manipulated agent produces verifiable garbage rather than trusted garbage. But the fix-generation path deserves the same scrutiny, because a poisoned context that shapes a patch is a supply chain attack with government commit access as the prize.

**What good looks like:** treat repository contents as hostile input in the threat model. Constrain the agent's toolset to read and report, require structured output, keep the human patch gate mandatory rather than customary, and diff-review agent-authored changes with the same rigor as an external contributor's first pull request.

### 5. Who guards the findings?

The scan's output is a prioritized inventory of exploitable weaknesses across an entire province, complete with file paths and remediation status. That artifact outlives the scan. It sits somewhere, someone can query it, and it is precisely what an attacker would want first. The same applies to the continuous red-team and blue-team agents, which produce a rolling stream of the same intelligence.

**What good looks like:** the findings store gets crown-jewel treatment: its own access control, encryption, need-to-know scoping, and monitoring. Access to the findings database should be rarer and louder than access to any single system it describes.

### 6. What keeps the red-team agents on the leash?

The continuous layer includes an agent that probes applications from the outside the way an attacker might. That is autonomous offensive tooling running inside government infrastructure, and it needs the controls any human red team operates under: explicit authorization scope, environment separation so probes cannot drift into production systems holding live citizen data, and kill switches that work mid-run. An autonomous prober with a stale scope file is an incident generator.

**What good looks like:** written authorization per target, technical enforcement of that scope (allowlists at the network layer, not instructions in the prompt), separate identities for offensive agents, and telemetry that pages a human when a probe touches anything outside scope.

### 7. Can you replay what the fleet did?

Twenty hours, 50 agents, every repository. If a finding is later disputed, or a repository is later found to contain adversarial content, can the ministry reconstruct exactly what each agent read, decided, and produced? Agent-side logs are not enough, because they sit inside the compromise boundary you are trying to audit. The record has to come from the platform.

**What good looks like:** per-agent, immutable logs sourced from infrastructure telemetry rather than the agents' own output, retained long enough to support incident response, with at least a couple of detection signals derived from that telemetry (per-agent call rates against baseline, first-ever tool combinations, egress volume per worker) rather than from anything the model writes.

## The checklist in one table

| # | Question | What good looks like |
|---|----------|----------------------|
| 1 | What identity per agent? | One workload identity per worker, short-lived, independently revocable, human principal in the chain |
| 2 | What can agents reach? | Read-only mirror, default-deny egress, no worker-to-worker paths |
| 3 | Where does the code travel? | Pinned tenancy and region, zero retention, secrets rotated before the scan |
| 4 | What if the code carries instructions? | Hostile-input threat model, read-and-report toolset, mandatory human patch gate |
| 5 | Who guards the findings? | Crown-jewel controls on the findings store, rare and audited access |
| 6 | What contains the red-team agents? | Enforced scope at the network layer, separate identities, kill switches, out-of-scope alerts |
| 7 | Can you replay the run? | Immutable per-agent logs from platform telemetry, detection signals the model cannot author |

## This will be copied. Copy the right part.

Alberta is hosting an industry day in Edmonton this July to share what it learned, and it plans to scale the approach across the provincial government this fall. Other governments and large enterprises will copy this, and they should. But I can already tell you how the bad copies will go, because I have watched the pattern in enterprise AI adoption for two years: the headline crosses the ocean and the pipeline discipline does not. Someone will pitch "466 million lines in 20 hours" to a steering committee, procure a fleet, point it at live source control with a shared service account, and skip the rules engine, the citations, and the patch gate because those parts slow the demo down.

The scale was never the achievement. The achievement is a pipeline where deterministic tooling runs first, every agent claim is anchored to something a human can check, and nothing ships without a person approving it. That shape is reproducible by any organization at any size. Fifty agents is a budget line. The discipline is the design.

## What I'm reading next

Alberta has published its technical white papers at [thevelocitywhitepapers.com](https://thevelocitywhitepapers.com/), and the seven questions above are the checklist I am taking into them. If the papers answer even four of the seven, they will be the most useful public artifact on agent deployment any government has produced, more useful than the scan numbers themselves. If they answer all seven, every security lead planning an agent rollout should read them before writing a single line of their own design.

If you are planning something similar and want to know where your current agent deployment stands, my free [Agent Security Scorecard](https://scorecard.aminrj.com) checks your setup against the OWASP Agentic Top 10 in about 12 minutes. Question one alone, the identity question, is where most deployments I assess fall over first.

## Sources

- [Anthropic case study: Government of Alberta uses Claude to find and fix cybersecurity vulnerabilities](https://www.anthropic.com/news/alberta-government-claude-cybersecurity)
- [The Velocity White Papers, Government of Alberta](https://thevelocitywhitepapers.com/)
- [Digital Watch coverage of the Alberta review](https://dig.watch/updates/alberta-claude-code-cybersecurity-review)
- [Joseph Thacker and JD: The Bug Bounty Singularity](https://josephthacker.com/hacking/2026/07/01/we-built-a-hackbot.html)
