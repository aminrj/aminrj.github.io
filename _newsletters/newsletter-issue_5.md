---
title: 28 out of 30 agent projects. Zero per-agent identity. Zero revocation.
Subject: 28 out of 30 agent projects. Zero per-agent identity. Zero revocation.
Preview text: The .env file is not an identity system. The ecosystem just forgot. Plus a CVSS 9.8 with no patch.
issue: 5
date: 2026-03-24
---

Hey 👋

I spent most of this week building a threat model for MCP deployments — mapping 10 MCP-specific risks to OWASP categories, with lab-confirmed attack chains for each. Midway through, I kept hitting the same wall: most of the risks I was documenting don't require a sophisticated attack. They require a credential. A shared API key sitting in a `.env` file, with no scope, no expiry, and no per-agent identity.

Then the Grantex audit landed on HN. 30 popular open-source agent projects, 500k+ GitHub stars combined. 28 out of 30 rely exclusively on environment-variable API keys. Zero have per-agent cryptographic identity. Zero have per-agent revocation. It's not a niche problem — it's the default configuration across the entire ecosystem.

That's the thread through everything this week.

**From the lab this week**

**MCP Security Top 10: my own threat model, lab-confirmed**

I published a 30-minute deep dive mapping 10 MCP-specific security risks to the OWASP LLM Top 10 categories they belong to. The framing I kept coming back to: in a standard LLM app, the developer controls what context the model receives. In MCP, a third party does — and the user approved them once, weeks ago, and forgot about it.

The three things the article establishes: (1) MCP's trust model is fundamentally different from a standard API integration. (2) The flat tool namespace — where every connected server's descriptions coexist in one LLM context — is a novel attack surface with no direct OWASP equivalent. (3) The rug pull lives in a runtime API response (`tools/list`), which bypasses every static analysis tool that catches a malicious package. Every attack in the article is lab-confirmed and reproducible from the [mcp-attack-labs repo](https://github.com/aminrj-labs/mcp-attack-labs).

[MCP Security Top 10 →](https://aminrj.com/posts/owasp-mcp-top-10/)

**Something I didn't expect to write this week: the EU AI Act angle**

On March 13, the Council of the EU published the delegated regulation under Article 92 of the AI Act — the enforcement mechanism for GPAI model evaluation. It takes effect August 2, the same date GPAI obligations become enforceable. While working through the compliance implications for MCP deployments, I realized most engineering teams haven't processed a specific fact: if your agent calls Claude, GPT, or Gemini through an API or MCP server, you are a downstream deployer under Article 26. The provider's compliance obligations don't substitute for yours — they're parallel, and the regulatory chain runs through your architecture. The MCP layer makes this substantially harder than a standard API integration because you don't fully control what instructions third-party server authors send to the model.

I wrote it up as a 17-minute practical mapping — which obligations apply at which position in the GPAI supply chain, and what your architecture decisions look like from a compliance standpoint before August 2.

[GPAI Meets Agentic AI →](https://aminrj.com/posts/gpai-meets-agentic-ai/)

**Also published: the RAG defenses companion post**

The practical follow-up to the RAG poisoning research from last week. Three pipeline-specific defenses (embedding anomaly detection, access-controlled retrieval, prompt structure hardening) measured against a live attack suite. Short, dense, ends with a results table. If you ran the lab from Issue #4, this is what to implement next.

[RAG Stack Security: Defenses That Stop Real Attacks →](https://aminrj.com/posts/RAG-mitigation-strategies/)

**This week in AI security**

**93% of agent projects use unscoped API keys — 0% have per-agent identity**

Grantex Research audited 30 popular open-source agent projects across six authorization dimensions. 93% rely exclusively on env-var API keys. 0% assign cryptographically verifiable per-agent identity. 100% have no per-agent revocation — rotating one agent's access requires rotating all of them. In frameworks like CrewAI and AutoGen, when one agent delegates to another, the child either inherits the parent's full credentials or gets its own independent key. No project implements scope narrowing for delegated access.

> **The incident response problem:** your SIEM currently cannot tell you which agent performed which action. When something goes wrong, you have a series of API calls with the same credential as every other agent in the system. Attribution is impossible without per-agent identity — and no popular framework ships it.

**Action:** Inventory every agent in your stack. Replace any shared or org-level key with short-lived, scoped credentials — per-agent tokens with audience binding and a TTL. Highest-leverage single change before any other hardening work.

[Grantex report (HN) →](https://news.ycombinator.com/item?id=47388873) [Full report →](https://grantex.dev/report/state-of-agent-security-2026)

**CVE-2026-2256: prompt injection → OS command execution in ms-agent. CVSS 9.8. No patch.**

CERT/CC advisory VU#431821. ModelScope's ms-agent Shell tool calls `subprocess.run(shell=True)` on input that can be influenced by external content — a document the agent is summarizing, code it's analyzing, a web page it fetched. The denylist defense (`check_safe()`) is bypassable through command obfuscation. Successful exploitation runs with the process's full OS privileges: data exfiltration, file modification, persistence, lateral movement. No vendor statement, no patch at time of writing.

> **The pattern:** check_safe() is a regex denylist. Denylists for shell commands don't hold — there are always equivalent syntaxes. The only defensible pattern is an allowlist of permitted commands, or eliminating shell access entirely.

**If you run ms-agent:** disable the Shell tool now. No patch exists. Run the process with minimal OS privileges and sandbox syscalls. If you can't do that immediately, take it offline.

[CERT/CC advisory VU#431821 →](https://kb.cert.org/vuls/id/431821)

**Fine-tuning on interaction logs? 2% data poisoning embeds backdoors that all current defenses miss**

arXiv:2510.05159 (Malice in Agentland) is getting renewed attention as more teams fine-tune agents on production interaction data. The finding: poisoning 2% of collected interaction traces embeds a trigger-based backdoor with over 80% success rate. Llama-Firewall, Granite Guardian, and weight-based Watch the Weights detection all failed to catch it. The backdoor doesn't degrade normal task performance, so it passes standard evals.

> **If you fine-tune on interaction logs:** audit and provenance your training traces before the next run. Any trace that includes externally sourced content is potentially tainted.

[arXiv:2510.05159 →](https://arxiv.org/abs/2510.05159)

## TOOLING WORTH KNOWING

* **Kvlar** — open-source proxy enforcing YAML policies on every MCP tool call, fails closed by default. Most immediately useful for deny-by-default on shell and database tools. [github →](https://github.com/kvlar-io/kvlar)
* **mcp-scan** — Invariant Labs' scanner for malicious tool descriptions. Catches direct poisoning and rug-pull variants at server load time. [github →](https://github.com/invariantlabs-ai/mcp-scan)
* **OWASP NHI Top 10** — Non-Human Identity framework. If the Grantex findings describe your stack, this is the right starting framework for fixing it. [owasp.org →](https://owasp.org/www-project-non-human-identities-top-10/)

## ONE THING TO CHECK THIS WEEK

For each agent in your stack: what credential does it use? Is it shared with any other agent? What breaks if you rotate it? If the answers are "org API key," "yes," and "everything" — you have the Grantex finding in your own environment. The Nango guide published this week has the clearest breakdown of which auth pattern applies per integration type. [nango.dev →](https://nango.dev/blog/guide-to-secure-ai-agent-api-authentication)

## WHAT I'M WATCHING

* CVE-2026-2256 weaponization timeline — CVSS 9.8, no patch, CERT/CC advisory public. This gets picked up by exploit kits fast
* Fine-tuning pipeline security — Malice in Agentland shows all current defenses fail; this is an open research problem
* EU AI Act August 2 enforcement — the March 13 GPAI delegated regulation made abstract obligations concrete
* Agent identity standards — the Grantex findings will push OWASP Agentic Top 10 and NIST CAISI toward concrete per-agent credential guidance

If this was useful, forward it to the engineer on your team who last deployed an agent. Odds are they used an env file and moved on.

Questions, pushback, topics — reply directly, I read everything.

Cheers,
Amine
