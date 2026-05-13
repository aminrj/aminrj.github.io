---
title: Three attack papers dropped this week. All point to the same architectural flaw.
Subject: Three attack papers dropped this week. All point to the same architectural flaw.
Preview text: 99% guardrail bypass, 95% RAG poisoning, and the one fix that addresses both.
issue: 4
date: 2026-03-16
---

Hey 👋,

Most RAG security discussions focus on the wrong attacker. Insider, APT, compromised pipeline — all real, all valid. But the more common risk is boring: stale documents, outdated policies, contradicted facts that accumulated over months. The adversarial case is just the extreme end of a problem that exists in every large document store. Same architecture, same defenses.

That framing came out of the HN discussion on my RAG poisoning post this week ([41 comments](https://news.ycombinator.com/item?id=47350407)). I ran knowledge base poisoning against a local ChromaDB + LangChain stack - 95% success rate, under 3 minutes, no external GPU, no cloud. Cross-tenant leakage hit 100% on 20 queries with zero sophistication. [Full breakdown](aminrj.com/posts/rag-security-architecture/) with measured defenses. [lab code](github.com/aminrj/rag-security-lab) runs in 10 minutes (`make attack1`).

One finding worth highlighting: the defense layer most teams skip — embedding-level anomaly detection — dropped poisoning success from 95% to 20% on its own, because it catches the clustering signal of coordinated injection that regex and text filters miss entirely.

## THIS WEEK IN AI SECURITY

**AdvJudge-Zero: 99% bypass rate against LLM safety judges**

Palo Alto Unit 42 released research on an automated fuzzer that defeats the ML classifiers most platforms use to catch policy violations before output reaches users. 99% success across models with 70B+ parameters, using low-perplexity input sequences - markdown symbols - that manipulate the classifier's decision logic without touching the underlying model.

> **Worth noting:** This isn't jailbreaking the model - it's bypassing the safety wrapper. Probabilistic safety layers aren't security controls. Structured output schemas and policy engines that operate outside the LLM are the only reliable alternative.

[Unit 42 report →](https://unit42.paloaltonetworks.com/advjudge-zero-automated-fuzzer/)

**HashJack: malicious instructions hidden after the # in a URL**

Cato CTRL documented the first indirect prompt injection that hides instructions in the URL fragment — the text after #. Web servers never see the fragment, so WAFs and IPS miss it entirely. When an AI browser assistant loads the page, the hidden instructions execute. Six scenarios: phishing, data exfiltration, credential theft, misinformation. Perplexity and Microsoft patched. Google: "won't fix, intended behavior."

> **The pattern:** same root cause as DockerDash and the Invariant Labs WhatsApp attack - external data treated as trusted instruction. URL fragments are the newest surface and the most accessible yet: the attacker doesn't need to compromise the site, just craft a link.

[Cato CTRL research →](https://www.catonetworks.com/blog/cato-ctrl-hashjack-first-known-indirect-prompt-injection/)

**Claude Opus 4.6 found 22 Firefox vulnerabilities, wrote 2 working exploits**

Anthropic published a two-week autonomous Firefox security review. 22 vulns found, 14 rated High by Mozilla. The exploit generation test: 350 attempts, 2 working exploits, $4,000 in API credits. Exploits only work in a test environment that removes browser sandboxing.

[Anthropic research →](https://www.anthropic.com/research/partnering-with-mozilla)

**MCP caller identity confusion — 38% of servers unauthenticated at scale**

Researchers quantified what the community suspected: MCP servers frequently share one authorization decision across multiple callers. A compromised agent escalates into other tools via misattributed calls — consistent with Adversa AI's March figure.

> **Fix:** mutual TLS or signed JWTs per caller, fail-closed on unknown callers. This is the Agents Rule of Two in practice — an agent that can't prove which caller is invoking it shouldn't be holding sensitive data access.

[arXiv paper →](https://arxiv.org/abs/2603.07473)

**Confident orgs have 2× the AI incident rate**

Survey of 205 security leaders: most confident orgs had twice the incident rate of less confident peers. 43% report AI making infrastructure changes monthly without oversight. 7% don't track autonomous changes at all.

The more interesting explanation: organizations confident enough to deploy broadly have more surface area to get hit. Whatever the cause, "we feel good about our AI security" is not a leading indicator of actual security posture - it may be a lagging indicator of not yet having checked.

## TOOLING WORTH KNOWING

* **Kvlar** — open-source proxy enforcing YAML policies on every MCP tool call, fails closed by default. Drop it in front of any MCP server without reengineering your harness. [github.com/kvlar-io/kvlar](https://github.com/kvlar-io/kvlar)
* **RankClaw** — scan AI skills/plugins for security risks before installing. Good pre-flight for MCP servers from the ecosystem. [rankclaw.com](https://rankclaw.com)
* **mcp-scan** — Invariant Labs' scanner for malicious tool descriptions. Catches direct poisoning and rug-pull variants at load time. Should be in every MCP deployment's CI. [github →](https://github.com/invariantlabs-ai/mcp-scan)

## ONE THING TO CHECK THIS WEEK

If you're running a RAG system: pull one query a low-privilege user runs and check what documents came back. If classification metadata isn't in the where clause of your vector store query, every user has read access to everything in the collection. Three lines of code fix it. [github.com/aminrj/rag-security-lab](https://github.com/aminrj/rag-security-lab)

**ALSO WORTH YOUR TIME**

* **OWASP LLM08:2025** — Vector and Embedding Weaknesses: the framework entry for RAG attack surface. Pairs well with the lab. [owasp.org](https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/)
* **AI is Eating Security** — Alex Stamos at SnooSec: high-confidence predictions including every company needing to care about 0-days within 6–9 months. [Talk →](https://www.youtube.com/watch?v=ai-eating-security)
* **Cisco State of AI Security 2026:** 83% plan agentic deployment, 29% feel ready. Most useful single number for board conversations. [Cisco blog →](https://blogs.cisco.com/ai/cisco-state-of-ai-security-2026-report)

## WHAT I'M WATCHING

**→ Semantic injection:** 15% residual with all defenses active is the current floor — closing it requires intent classifiers, not regex

**→ AdvJudge-Zero below 70B parameters** — whether the technique holds for smaller deployed models matters more operationally

**→ HashJack toolkits** — technique requires no server compromise; gap between research and commodity exploit is short

**→ MCP caller identity standardization** — arXiv paper will push this onto OWASP's update agenda

If this was useful, forward it to one person on your team working on RAG or agentic deployments. Questions, pushback, topics you want covered — reply directly, I read everything.

Cheers,
Amine
