---
title: "466 million lines reviewed in 20 hours. Both offense and defense just went machine-tempo."
Subject: "[AI Sec Intel] #20 | 466 million lines reviewed in 20 hours. Offense and defense both went machine-tempo."
preview_text: "Alberta reviewed 466M lines of code with 50 Claude agents in 20 hours. Two hackers shipped a profitable autonomous hackbot. And agent identity became something you can buy. One thread ties all three."
subtitle: "A government ran 50 agents across its whole code estate. Two part-time hackers shipped a profitable hackbot. Agent identity became a product category. The common thread: the credential is the target."
issue: 20
date: 2026-07-16
---

Hey 👋

This is issue #20, and it has a single theme: deploying and integrating AI agents with production cloud infrastructure without handing over the keys. It's the subject of my talk at fwd:cloudsec Europe in London this September, "What We Learned Giving an AI Agent Read Access to Our Whole Kubernetes Fleet," so expect this thread to keep running over the next few issues.

Three stories this week, and they fit together better than usual. Autonomous defense and autonomous offense both published real numbers in the same seven days, and the identity layer they both depend on finally became something you can put on a purchase order. A Canadian province ran the largest agent code review I've seen documented anywhere. Two part-time hackers ran the first profitable autonomous hackbot I've seen with receipts. And two vendors turned agent identity into a product category. Put them side by side and you get a fairly complete picture of where this is heading.

If you want the deeper version of how I think about scoping what an agent can reach, [it's on the blog →](https://aminrj.com/posts/agent-permission-model/)

---

## This week in AI security

### A government ran 50 agents over its entire codebase. The results are public. The architecture isn't.

The Government of Alberta's Ministry of Technology and Innovation ran roughly 50 Claude Code agents in parallel, on Opus and Sonnet, across every repository the province owns: 466 million lines of code, about 1,280 applications, 3,400 repositories serving all 27 provincial ministries. The full review took around 20 hours. The team estimates the same work done the old way would have taken about 6.5 years.

The pipeline is the interesting part. It ran in two stages. A deterministic rules engine flagged known patterns first, then the agents reviewed those flags and cited the exact file and line for every finding, so developers could verify each one. The scan surfaced issues traditional scanners had missed, generated fixes and missing tests, and the ministry has since built red-team and blue-team review agents on the Claude Agent SDK that check applications against roughly 95 security controls per pass. Next on their list: consolidating 185 legacy applications into 16. They're hosting an industry day in Edmonton this month and plan to scale the approach across the provincial government from the autumn.

As far as I can tell, this is the first time a government has published a portfolio-wide agent code review with real numbers attached, and the shape of the pipeline teaches as much as the scale does. Deterministic prefilter in front, agents behind it, every finding anchored to a checkable file and line, humans confirming. That is the right architecture, and it matches what this newsletter has argued all year. But notice what the write-up leaves out: what identity each of those 50 agents ran under, what they could write to, where their output could travel, and how the generated fixes were gated into production. A fleet of agents holding read access to a government's entire code estate is a genuine achievement and a concentrated target at the same time. The second story is about who's shopping for exactly that.

If you're planning your own version, copy the shape before the scale. Run the agents against a read-only mirror of your repositories, never live origin. Give each agent worker its own identity so you can attribute and revoke individually. Require file-and-line citations so every finding is checkable, and route generated fixes through your normal PR review rather than around it. And write the containment architecture down before the pilot, because you will be asked to scale it the day the first results land.

[Anthropic case study →](https://www.anthropic.com/news/alberta-government-claude-cybersecurity)

---

### The bug bounty singularity is an infrastructure story, not a model story

Joseph Thacker (rez0) and JD (xssdoctor) built an autonomous hackbot out of Claude Code skills for recon, fuzzing, and deep application analysis. In five months it found 126 vulnerabilities, 88 of them High or Critical, with roughly 89% confirmed real once programs accepted them or closed them as duplicates. Largest single bounty so far: $15,000. Two design details stand out. A separate validation bot, built only to disprove findings, cut false positives from 80% down to 60%. And the biggest capability jump came from keeping the bot logged into a real browser on a physical machine, because the critical bugs are simply unreachable when you're logged out. At one point most of their token spend was going to authentication alone.

That last detail is the whole map. The expensive part of autonomous offense is authenticated access, because that is where the criticals live. Now look at your production agents: they hold standing authenticated sessions into your cloud accounts, your SaaS, your internal APIs. To an attacker, a deployed agent is authentication that's already solved. Alberta's 50 reviewers, your SRE agent, your triage bot, each one is a bundle of exactly the access the hackbot spent most of its budget trying to earn.

So treat agent credentials and sessions as the target asset, because that's what they are. Inventory every internet-reachable agent and MCP endpoint you own and assume automated recon is already hitting it. Shorten token lifetimes, bind sessions to origin where the platform lets you, and alert on agent-session reuse from a new location. And steal the disprover pattern while you're at it: if you run agents that triage or review anything, add a second agent whose only job is to break the first one's findings. It cut their false positives by a quarter for essentially free.

[The Bug Bounty Singularity →](https://josephthacker.com/hacking/2026/07/01/we-built-a-hackbot.html)

---

### Agent identity just became a product category. Buy delegation, not impersonation.

Two identity vendors shipped agent-identity messaging in the same week. Teleport introduced an Agentic Identity Framework that governs AI agents as first-class identities with cryptographic credentials instead of shared API keys or blanket access. authentik is positioning its self-hosted platform around managing human and machine identities together, with policies that evaluate context before granting access, whether the caller is a person or an agent.

The market just confirmed what the incident data has been saying all year: impersonation is the wrong model. An agent running on a human's credentials breaks attribution, breaks revocation, and makes least privilege impossible. Delegation is the model that works. The agent gets its own identity, scoped to its declared toolset, with the human principal recorded in the delegation chain. Vendors shipping this removes the last excuse for shared keys. One caution, though: buying an identity product scopes nothing by itself. The policy work is still yours.

So the rule is one identity per agent instance. Not per team, not per application. Scope it to the tools and namespaces the agent actually needs, keep revocation independent so you can kill one agent without breaking its neighbors, and retire every shared API key an agent touches. If two agents can present the same credential, you can neither attribute nor contain either of them. I'm publishing a reference Terraform module for exactly this kind of non-human identity scoping alongside the London talk.

[Teleport →](https://goteleport.com) · [authentik →](https://goauthentik.io)

---

## Where this is going

Put the three side by side. Alberta showed that autonomous defense at portfolio scale is real, published, and shaped correctly: deterministic gate in front, agents behind, humans confirming. The hackbot showed that autonomous offense is now cheap and profitable, and that its single largest cost is getting authenticated. The identity vendors showed that the fix, per-agent scoped identity, is now something you can buy rather than build.

The thread running through all three is the credential. Alberta's write-up is silent on it. The hackbot spent most of its budget acquiring it. The vendors just made it purchasable. Offense and defense are both operating at machine speed now, and the thing that decides who wins a given exchange is no longer how clever the prompt was. It's whether the standing access an agent holds is scoped, attributable, and revocable, or whether it's a shared key with a long life and no owner.

That's the whole argument for the London talk, and it's why I keep circling back to it. We spent 2025 trying to make agents trustworthy. 2026 is about making the access they carry small enough to lose safely.

---

## From the lab

Two recent pieces that pair directly with this week's news:

- **The Enterprise AI Harness Everyone Is Building Has No Security Layer** sits next to both the Alberta pipeline and Andy Gill's survey of open-source security research harnesses (stage-specific prompts, strict context budgets, structured artifact exchange between stages). The harness pattern is winning. In most implementations, the security layer still isn't in it. [My post →](https://aminrj.com/posts/enterprise-ai-harness-no-security-layer/) · [Andy's survey →](https://blog.zsec.uk/harnessing-harnesses/)
- **When Infostealers Meet Agentic AI** is the hackbot's auth economics seen from the other side. If authenticated access is the expensive part of offense, a stolen agent session is the discount. This is the kill chain when the credential is stolen rather than earned. [Read it →](https://aminrj.com/posts/infostealer-agentic-killchain/)

And the announcement: I'm speaking at **fwd:cloudsec Europe in London, September 7–8**. The talk is an experience report on running an SRE agent with read access across a multi-cluster Kubernetes fleet, why read-only turned out not to be a security boundary, and the containment ladder we ended up with. Alberta makes it timely. Portfolio-scale agent deployments aren't hypothetical anymore, and the containment questions are the ones nobody publishes. If you'll be there, reply and let's meet.

---

## Tooling worth knowing

- **harness-kit** by Andy Gill (ZephrFish): a template implementing a recon → hunt → validate → trace → report pipeline with model routing that saves the expensive models for validation. A solid skeleton for defensive review pipelines too, with the caveat above. [GitHub →](https://github.com/ZephrFish/harness-kit)
- **darknet-mcp-server** by Orhan Yildrim: 66 tools across 16 dark web and threat intelligence sources behind a single MCP server (HIBP, IntelligenceX, OTX, AbuseIPDB, the abuse.ch suite, and more). Genuinely useful for SOC agents, and also a concentration risk worth naming out loud: one server piping 16 sources of untrusted text into your agent's context. Wrap it, don't trust it. [GitHub →](https://github.com/badchars/darknet-mcp-server)
- **Agent Security Scorecard**: my free self-assessment against the OWASP Agentic Top 10, about 12 minutes, no login. This issue's identity story maps straight onto the ASI03 items it checks. [Score your agents →](https://scorecard.aminrj.com)
- **AI Agent Pre-Deployment Security Checklist**: the companion checklist for anything agent-shaped heading to production. [Get the checklist →](https://aminrj.com/resources/predeployment-checklist/)

---

## One thing to check this week

Pull the credential list for your most capable production agent and ask three questions of each entry. Is it unique to this agent? Does it expire in hours rather than months? Can you revoke it without breaking anything else? Every "no" is a finding. Fix them in this order: eliminate shared credentials first, shorten lifetimes second, separate revocation paths third. And if you can't produce the credential list at all, that's the finding.

---

## What I'm watching

→ **Detection below the prompt.** Aaron Phifer added a behavioral layer to Triagewall, his self-hosted IDS triage tool, built on statistical process control over the raw Suricata stream: per-host alert-rate spikes and first-ever signature triggers. Neither signal depends on alert text, so prompt injection has nothing to grab. The pattern generalizes to production agents: derive detection from telemetry the model never authors (per-agent API call rates, first-ever tool combinations, egress per session), sourced from cloud audit logs rather than the agent's own logs. [Triagewall on behavioral baselining →](https://triagewall.io/posts/behavioral-baselining)

→ **Knossos**, Praetorian's deception engine, learns your real cloud environment's style (naming, tags, CIDR allocation, IAM patterns) and procedurally generates decoy AWS environments pre-seeded with attack paths, shipped as Terraform and watched through EventBridge. Two reasons I care: deception finally scales to machine-tempo attacks, and the three isolation layers walling off the decoys (network isolation, IAM permission boundaries, SCPs) are the same containment stack your production agents should be sitting inside. [Praetorian →](https://www.praetorian.com/blog/knossos-decoy-environments/)

→ **khaos-c2**, a post-exploitation framework that routes C2 traffic through Microsoft Teams, GitHub Gist, DNS-over-HTTPS, and SMB named pipes. A reminder that an egress allowlist of "trusted SaaS" is not a boundary. Egress has to be a capability you grant per agent and per destination. [GitHub →](https://github.com/28Zaaky/khaos-c2)

→ **The CloudTrail Lake to CloudWatch migration mess.** Aidan Steele documents roughly 8-hour event delays, no centralization by default, and missing enrichment. Your agent forensics depend on this pipeline. Learn its gaps before an incident, not during one.

→ **Alberta's industry day and autumn scale-up.** They're sharing findings with other governments in Edmonton this month. If the containment architecture behind those 50 agents gets published, that document will matter more than the scan results did. Watch for copycat deployments that copy the scale without the pipeline discipline.

→ **Next issue:** the containment ladder in full, ahead of London. Scoped read-only capability, per-agent identity, egress as a capability grant, and human gates on writes. The Alberta deployment is the perfect case to walk it against.

Several of this week's finds came via Clint Gibler's tl;dr sec #337, worth your inbox if it isn't there already.

---

I write the full technical deep-dives on the aminrj.com blog: agent security patterns, lab tests, framework breakdowns. If this newsletter is useful, [that's where the long-form work lives →](https://aminrj.com/).

Questions, pushback, something I missed, reply directly. I read everything.

Cheers, **Amine**
