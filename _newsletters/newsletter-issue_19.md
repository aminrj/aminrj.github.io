---
title: "One polite word bypassed the guardrails. The private repos leaked anyway."
Subject: "[AI Sec Intel] #19 | One polite word bypassed the guardrails. The private repos leaked anyway."
preview_text: "GitHub's agentic workflows leaked private repos to anyone who could open an issue. An AI agent ran a ransomware attack nearly end to end. And Kubernetes ops agents went mainstream. One thread ties all three."
subtitle: "Three incidents, one conclusion: the prompt layer fails politely, and only the infrastructure layer holds. The unit of agent security isn't the prompt. It's the blast radius."
issue: 19
date: 2026-07-13
---

Hey 👋

Some personal news first. I'll be speaking at fwd:cloudsec Europe in London, September 7–8. The talk is called "What We Learned Giving an AI Agent Read Access to Our Whole Kubernetes Fleet," and it's exactly what it sounds like: a production experience report, including the parts that made me wince. If you're going to be there, reply to this email and let's plan to meet.

I mention it now because this week's news reads like the case file for that talk. Three separate stories, and every one of them lands on the same conclusion I reached running an agent against real clusters: the prompt layer will fail, politely and quietly, and the only controls that hold are the ones the model can't talk its way past. This issue is that argument, made three times by three different incidents.

If you want the technical foundation for it, [it's on the blog →](https://aminrj.com/posts/agent-permission-model/)

---

## This week in AI security

### GitLost: one polite word, and the private repos leaked

Noma Security disclosed GitLost on July 7, a flaw in GitHub's new Agentic Workflows. The attack needs zero credentials. The attacker opens an issue in a public repository and hides plain-English instructions in the body. When the org's AI agent processes that issue, it reads the attacker's text as trusted instructions, follows them into the organization's *private* repositories, and leaks the contents publicly. Here's the detail that should end every "we'll prompt our way to safety" conversation: Noma found the model initially refused the malicious request, and adding *one polite word* flipped it to compliance. That's the entire strength of the guardrail, measured to the word. The exposure is every public repo you own, because any of them can carry the payload in an issue or comment.

**Look at what failed and what would have held.** The prompt-level defense, the model's judgment about what it should and shouldn't do, collapsed under a courtesy word. What would have contained the attack is boring infrastructure: an agent identity that simply cannot read private repos while processing public-repo input. Not "shouldn't." *Cannot.* The flaw isn't that the model was gullible. All models are gullible, that's last issue's role-confusion research in production clothes. The flaw is an authorization design where one agent context spans both untrusted input and private data, so the model's gullibility *matters*. Scope it so it doesn't.

**Audit every agent you've granted access to both public-facing input and private resources in the same context.** For GitHub specifically: any org where an agentic workflow can be triggered by public issues or comments while holding read access to private repos is running the GitLost pattern right now. Split the identity. One scoped credential for anything that touches public input, a separate one, never in the same session, for private data. If the platform won't let you split it, that's a risk decision to escalate, in writing, this week.

[Noma's disclosure, summarized →](https://www.rockcybermusings.com/p/weekly-musings-top-10-ai-security-20260703-20260709)

---

### JADEPUFFER: an AI agent ran a ransomware attack nearly end to end

Researchers observed what's being described as the first ransomware attack conducted almost entirely by an autonomous AI agent. JADEPUFFER exploited a vulnerability in Langflow, the popular visual framework for building LLM apps, then worked the kill chain on its own: broke into the network, harvested credentials, and encrypted a company's database. A human pointed it at the target; the agent did substantially everything after that. It's the operational sequel to March's hackerbot-claw supply-chain incident (Issue #16), and it closes the argument about whether attacker-agents are a real threat class. They're now running end-to-end extortion, not just poisoning packages.

**The economics matter more than the novelty.** Ransomware crews were already efficient, but every intrusion consumed skilled operator hours, and operator hours were the scarce resource that rate-limited the whole industry. An agent that runs the intrusion autonomously turns a labor cost into a compute cost, and compute is cheap and parallel. The defensive consequence is the one I keep coming back to: your response clock is now set against a machine. Detection-to-containment windows tuned to human attackers (hours, a workday) are tuned to the wrong adversary. And note the entry point, a vulnerability in an *AI application framework*. Your LLM tooling isn't just an attack surface for prompt injection; it's ordinary vulnerable software that autonomous attackers scan for like anything else.

**Two checks.** First, if you run Langflow anywhere, patch and audit it now, and treat every internet-exposed AI framework (Langflow, Flowise, n8n, Dify, and friends) as tier-one attack surface with the same patching SLA as your edge devices. Second, take your incident-response plan and ask it one question: which steps assume the attacker moves at human speed? Every place your playbook waits for a human to notice, triage, and act is a window an agent-attacker moves through. Automate containment for the highest-confidence detections, credential revocation, network isolation, so at least the first response also happens at machine speed.

[The week's roundup →](https://www.esecurityplanet.com/weekly-roundup/ai-driven-attacks-critical-exploits-and-global-breaches-define-this-week-in-july-2026-in-cybersecurity/)

---

### Agents are operating Kubernetes clusters in production now

The pieces shipped quietly, and this quarter they clicked together. AWS's open-source EKS MCP server hands an agent a real toolbox against a live cluster (list and read resources, pull logs, query metrics, apply manifests), the AWS DevOps Agent went GA as an autonomous on-call engineer, and agentic CloudWatch investigations sift telemetry for root cause on demand. "Self-healing Kubernetes" now literally means an agent that reads your cluster, forms a hypothesis, drafts a fix, and, if you let it, applies it to production.

The mature adopters in this week's writeups aren't treating that as an on/off switch. They're climbing a ladder: **observe** (read-only), then **recommend** (proposes, human applies), then **gated** (applies with explicit approval), then **auto** (applies within policy bounds). Each rung is enforced by deterministic controls: Cedar-based policy gating tool calls at runtime, Kyverno/OPA admission control rejecting non-compliant manifests exactly as it would from a human, and a structured audit trail of trigger, diagnosis, change, approver, outcome. Worth stating soberly: even the sandboxes aren't magic. Unit 42 and BeyondTrust published escapes and network-isolation bypasses against AgentCore's code interpreter this year (since remediated), covering credential-exfiltration and DNS-tunneling paths.

**Two things I'd underline from having run this pattern in production. First, "read-only" is not "harmless."** An agent with fleet-wide read access can read Secrets, service-account tokens, and ConfigMaps full of connection strings. Observe-level access is already a data-exfiltration surface, and it needs scoping (which namespaces, which resource types) just as much as write access does.

**Second, the rung that holds is never the model's judgment. It's the deterministic gate.** Admission control doesn't care how persuasive the injected prompt was; the non-compliant manifest bounces. That's the design principle underneath everything: put the enforcement where the model can't negotiate with it. The sandbox escapes reinforce this rather than undercut it. A per-session microVM is necessary, not sufficient; the credential scope and egress rules around it do the real work.

**If you're deploying (or being asked to deploy) a cluster agent, write down which rung of the ladder it's on and what enforces that rung.** Then check three specifics: the agent's service-account RBAC is scoped to the namespaces and verbs it needs (broad permissions are a release blocker, not a cleanup task); `automountServiceAccountToken: false` anywhere the pod doesn't need API access, with short-lived projected tokens where it does; and egress policy, because network egress is the single highest-impact control on what a compromised agent can leak. If you can't name the rung and the enforcement, the agent is on the "auto" rung by default, whether anyone decided that or not.

[Agentic EKS ops, honestly assessed →](https://cloudnativenow.com/contributed-content/self-healing-kubernetes-gets-real-and-risky-running-ai-agents-on-amazon-eks/) · [The security gaps teams find too late →](https://vector-labs.ai/insights/running-ai-agents-on-kubernetes-the-security-architecture-gaps-most-teams-discover-too-late)

---

## Where this is going

Put the three side by side. GitLost: the model's refusal folded to a polite word, and only authorization scope could have saved the private repos. JADEPUFFER: the attacker is now an agent, so defense has to run at machine speed, which means deterministic automation in the first-response loop, not human judgment. Kubernetes ops: the practitioners furthest along all landed on graduated autonomy, enforced by infrastructure the model can't argue with. Three different corners of the field, one identical conclusion: **the unit of AI agent security is not the prompt, it's the blast radius.** The industry spent 2025 trying to make agents trustworthy. 2026 is about making them *containable*, and accepting that those are different engineering problems with different tools.

This is, not coincidentally, the entire thesis of my fwd:cloudsec talk. We gave an agent read access to a whole Kubernetes fleet and learned in production which controls were real. The prompt-level ones failed in ways that were almost funny; the infrastructure-level ones, scoped non-human identities, Terraform-managed permissions, deterministic gates, held every time it mattered. September 7–8 in London, and the newsletter gets the write-up after.

---

## From the lab

- **fwd:cloudsec Europe, September 7–8, London** — "What We Learned Giving an AI Agent Read Access to Our Whole Kubernetes Fleet." A production experience report: the architecture, the scoping decisions, what broke, and the containment framework we ended up with. If you're attending, reply and let's meet. [Conference details →](https://fwdcloudsec.org/conference/europe/)
- **The agent permission model** — the technical spine under everything in this issue: how I scope what an agent can reach, why the enforcement lives in infrastructure rather than the prompt, and how the human gate on irreversible actions works in practice. [Read it →](https://aminrj.com/posts/agent-permission-model/)

---

## Tooling worth knowing

- **Agent Security Scorecard** — 12 minutes against the OWASP Agentic Top 10 (2026). After this week, pay attention to the identity and authorization sections: the GitLost pattern (one context spanning untrusted input and private data) is exactly what they surface. [Take the scorecard →](https://scorecard.aminrj.com)
- **AI Agent Pre-Deployment Security Checklist** — 25 yes/no controls. The RBAC scoping, token handling, and egress checks map one-to-one onto the Kubernetes hardening in story three. [Get the checklist →](https://aminrj.com/resources/predeployment-checklist/)

---

## One thing to check this week

Run the GitLost test on your own environment. It takes twenty minutes. List every agent or agentic workflow you have (GitHub agents, CI triage bots, support-ticket agents, cluster agents). For each one, two columns: *what untrusted input can reach it* (public issues, external emails, web content, customer tickets, tool output) and *what private resources it can touch in that same context* (private repos, internal docs, secrets, production APIs). Any row with entries in both columns is a GitLost-shaped exposure, and no amount of prompt hardening changes that, because the fix that works is structural: split the identity, or cut one column to zero. One polite word is all that stands between "shouldn't" and "did."

This exact exercise, run against a whole Kubernetes fleet, is the opening of my fwd:cloudsec talk. [The groundwork is on the blog →](https://aminrj.com/posts/agent-permission-model/)

---

## What I'm watching

→ **Agentic CI/CD as the softest target** — GitLost, the Claude Code GitHub Action chain, Cline's post-mortem: the pattern of the quarter is agents in build systems reading strangers' text while holding real credentials. Expect this to be the dominant incident class of H2, because it combines maximum untrusted input with maximum standing privilege and minimum human observation.

→ **Machine-speed extortion** — JADEPUFFER won't stay unique. The playbook is now demonstrated and the marginal cost is compute. Watch for ransomware dwell times collapsing, and for the first insurers and regulators to start asking whether your containment is automated.

→ **The autonomy ladder becoming the audit standard** — observe → recommend → gated → auto, enforced deterministically, is converging from every direction (AWS's learn/enforce modes, the Five Eyes guidance, the K8s field practice). I expect "which rung, and what enforces it" to be a standard auditor question within a year. Get your answer in writing first.

→ **AI frameworks as ordinary attack surface** — Langflow was the JADEPUFFER entry point; exposed MCP servers and OpenClaw instances keep piling up in the scan data. The industry treats LLM tooling as novel; attackers treat it as unpatched software. The attackers are right.

→ **The fwd:cloudsec talk** — final prep over the coming weeks: the containment ladder framework, the NHI scoping architecture, and the honest list of what failed. Subscribers get the full write-up after London, and I'll share the war stories that don't fit in 25 minutes here first.

---

I write the full technical deep-dives on the aminrj.com blog: agent security patterns, lab tests, framework breakdowns. If this newsletter is useful, [that's where the long-form work lives →](https://aminrj.com/).

Questions, pushback, something I missed, reply directly. I read everything.

Cheers, **Amine**
