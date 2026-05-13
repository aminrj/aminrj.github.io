---
title: Trivy compromised. LiteLLM backdoored. Your CI pipeline is the new attack surface.
Subject: Trivy compromised. LiteLLM backdoored. Your CI pipeline is the new attack surface.
Preview text: The payload ran as a systemd service. The Trivy scan still returned green. Nobody noticed.
issue: 6
date: 2026-03-31
---

Hey 👋

I published something this week I didn't expect to write when I started the RAG security series. The EU AI Act's Article 10 requires "appropriate data governance and management practices." I spent some time mapping what that actually means for a retrieval pipeline — and the answer is more specific than the regulation sounds: the embedding anomaly detection layer I measured in the poisoning lab _is_ an Article 10 control. The defense layer most teams skip is also the compliance obligation most teams haven't mapped yet.

While I was writing it, TeamPCP made the same point operationally. They didn't attack any AI model. They attacked Trivy — the vulnerability scanner running in the CI/CD pipeline next to the model — harvested its credentials, and used those to backdoor LiteLLM, the library that proxies API calls to Claude, GPT, Gemini, and every other LLM your agents use. The tools you trust to secure your AI infrastructure became the entry point into it.

That's the thread this week.

_From the lab this week_

**RAG Poisoning meets EU AI Act Article 10 — the compliance angle nobody is mapping**

Article 10 is usually read as a training data obligation. It isn't — or rather, it isn't _only_ that. For RAG systems, the retrieval corpus is operational data that directly determines model output at inference time. If your system touches anything in GPAI Annex III categories (employment decisions, credit assessment, medical triage), Article 10 data governance applies to your vector database, your ingestion pipeline, and your retrieval logic. Not just your training set.

The article maps Article 10(2)'s specific requirements — design choices, data collection, data preparation, dataset relevance — to concrete RAG architecture decisions. The embedding anomaly detection control that reduced poisoning from 95% to 20% in the lab is an Article 10(2)(d) data preparation control. Most teams skip it. Most teams also haven't mapped it as a compliance item. Those are the same gap.

[RAG Poisoning and EU AI Act Article 10 →](https://aminrj.com/posts/rag-poisoning-article-10-data-governance/)

_This week in AI security_

**TeamPCP: the supply chain attack that went through your security scanner to reach your LLM proxy**

The most important AI security incident of the quarter. TeamPCP spent a month cascading through five ecosystems — GitHub Actions, Docker Hub, npm, OpenVSX, PyPI — each stage using credentials stolen from the previous one. The final target: LiteLLM versions 1.82.7 and 1.82.8, which are downloaded 3.4 million times per day and serve as the unified API proxy for Claude, GPT, Gemini, Bedrock, and 100+ other LLM providers.

The payload was three-stage: a credential harvester targeting 50+ secret categories (SSH keys, cloud tokens, Kubernetes secrets, `.env` files), a Kubernetes lateral movement toolkit deploying privileged pods to every cluster node, and a persistent systemd backdoor polling for commands every 50 minutes. Telnyx (telephony SDK, 4.87.1 and 4.87.2) was also compromised on March 27. CVE-2026-33634, CVSS 9.4.

The entry point: Trivy, the vulnerability scanner that LiteLLM used in its own CI pipeline, without version pinning. Trivy was compromised on March 19 via a misconfigured `pull_request_target` workflow. TeamPCP harvested Aqua Security's PAT, then used it to push malicious tags to `trivy-action` and `setup-trivy` — turning trusted version references into credential harvesters for every downstream project that ran them. LiteLLM was one of those projects.

> **The pattern that matters:** TeamPCP exclusively targeted security-adjacent software — the scanner (Trivy), the IaC analyzer (KICS), the LLM proxy (LiteLLM). Tools that run with elevated privileges by design. Compromising them is maximally efficient: the attacker inherits the broad access the organization already granted to the tool. This is SolarWinds applied to the AI ecosystem.

**If you run LiteLLM:** treat any environment that installed 1.82.7 or 1.82.8 as a full credential exposure event. Rotate every secret that was present as an environment variable or config file on that system — not just the LiteLLM API key. Check for `~/.config/sysmon/sysmon.py` and the `sysmon.service` systemd unit as persistence indicators.

**If you run Trivy:** pin to commit SHA, not version tags. Any workflow using `@latest` or a floating version tag gave the attacker a delivery channel.

[Datadog analysis →](https://securitylabs.datadoghq.com/articles/litellm-compromised-pypi-teampcp-supply-chain-campaign/) [Endor Labs: campaign is not over →](https://www.endorlabs.com/learn/teampcp-isnt-done) [Trend Micro payload analysis →](https://www.trendmicro.com/en/research/26/c/inside-litellm-supply-chain-compromise.html)

**Notme.bot — a spec to replace bearer tokens in AI agent authorization**

Last week's Grantex finding (93% of agent projects, zero per-agent identity) raised the problem. This week, a proposed solution appeared on HN: Notme.bot, an open-source specification that replaces bearer tokens with cryptographic provenance for AI agent authorization. Instead of "this token grants access," the model becomes "this agent has verifiable authority delegated from this principal, scoped to these actions, with this audit trail."

It's early-stage and not production-ready, but the direction is right: authorization that can't be exfiltrated and reused because it's not a secret — it's a cryptographic proof.

[notme.bot →](https://notme.bot/)

**GhostDesk: MCP server giving AI agents a full virtual Linux desktop**

A new open-source MCP server that gives AI agents full control of a virtual Linux desktop — keyboard, mouse, screen, applications. The intended use is automation and testing. The security implication is that a compromised agent with GhostDesk access operates like a human with a keyboard: it can interact with any application, bypass session-based controls, and chain actions that no individual tool call would permit.

> **The trend:** agent capabilities are expanding faster than the authorization models governing them. GhostDesk is legitimate tooling. The security question is whether your agent identity and policy layer can constrain what a desktop-capable agent is allowed to do — and right now, almost none of them can.

[github.com/YV17labs/GhostDesk →](https://github.com/YV17labs/GhostDesk)

## Tooling worth knowing

* **Tessera** — 32 OWASP security tests for GPT-4o, Claude, Gemini, and Llama 3. Structured test suite you can run against your own model deployments. [github →](https://github.com/tessera-ops/tessera)
* **pip install --require-hashes** — not a tool, a flag. The TeamPCP LiteLLM compromise would have been caught by any environment using hash-pinned dependencies. [pip docs →](https://pip.pypa.io/en/stable/topics/secure-installs/)
* **StepSecurity Harden Runner** — GitHub Actions hardening that blocks egress to unknown endpoints during CI runs. The Trivy payload exfiltrated to `scan.aquasecurtiy[.]org` — a lookalike domain. Egress controls catch that class of exfiltration. [github →](https://github.com/step-security/harden-runner)

## One thing to check this week

Search every repo and CI workflow for `litellm==1.82.7`, `litellm==1.82.8`, `telnyx==4.87.1`, `telnyx==4.87.2`, `trivy-action` pinned to a tag (not a commit SHA), and `setup-trivy` pinned to a tag. Any match is a credential rotation event, not just a package update. The Endor Labs and Datadog IoC lists have the full set of indicators including the persistence artifacts. [Datadog IoC list →](https://securitylabs.datadoghq.com/articles/litellm-compromised-pypi-teampcp-supply-chain-campaign/)

## What I'm watching

* TeamPCP's next target — Endor Labs assesses the campaign is not over; each stage yields credentials that unlock the next one. PyPI tokens and GitHub PATs from the LiteLLM and Telnyx compromises are now in attacker hands
* LAPSUS$ collaboration — Wiz reported that TeamPCP is now partnering with LAPSUS$; if accurate, the operational scale and extortion component change significantly
* Notme.bot adoption — whether the spec gets traction as OWASP and NIST push concrete agent credential guidance
* EU AI Act August 2 — the Article 10 data governance mapping is one most teams haven't done; the enforcement date is 18 weeks away

If this was useful, forward it to the engineer on your team who manages your CI/CD pipeline. They may not know LiteLLM was in it.

Questions, pushback, topics? Reply directly, I read everything.

Cheers,
Amine
