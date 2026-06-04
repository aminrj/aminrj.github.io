---
title: "Your coding agent's approval prompt is lying to you."
Subject: "[AI Sec Intel] #14 — Your coding agent's approval prompt is lying to you."
preview_text: "SymJack and TrustFall broke every major AI coding agent this month — Claude Code, Cursor, Gemini, Copilot, Codex. The dialog you click through doesn't say what you're approving. Here's what to do."
issue: 14
date: 2026-06-04
---

Hey 👋,

If you use an AI coding agent — Claude Code, Cursor, Gemini CLI, Copilot, Codex — this issue is about you specifically. Two disclosures this month showed that the "Yes, I trust this folder" prompt you click through a dozen times a day is approving far more than it tells you. Each one turns a cloned repository into remote code execution on your machine. Neither is a bug in any single product. They're the same architectural flaw in two different disguises.

I spent this week mapping how this connects to the MCP attack chain I published last week. Same lesson at a different layer. The danger isn't the model, it's the trust you grant without seeing what you're granting.

If you want to follow along with the agent build itself, [check out the aminrj.com blog →](https://aminrj.com/). I'm publishing the full series there.

---

## This week in AI security

**SymJack: a booby-trapped repo tricks your coding agent into overwriting its own config, then runs attacker code on restart**

Adversa AI's disclosure is the sharpest of the month. A malicious repository contains an innocent-looking file copy operation. Your AI coding assistant performs the copy as part of normal work. What it's actually doing is following a symlink that overwrites the agent's own configuration file. The next time the agent restarts, it runs the attacker's code with your full user privileges. Confirmed across six tools: Claude Code, Gemini CLI / Antigravity CLI, Cursor Agent CLI, GitHub Copilot CLI, Grok Build, and OpenAI Codex CLI. Every one was vulnerable.

The approval prompt the developer sees describes a benign file copy. It does not say "this will overwrite my configuration." The user accepts because nothing looks wrong. That's the entire point of using a coding agent. Speed and trust in automation are exactly what the attack exploits.

> **This is one technique against a whole category, not six separate bugs.** SymJack is architectural: every agent that can copy files and read project-scoped configuration is exposed, because the approval prompt describes the *action* (copy a file) and not the *consequence* (overwrite my own config and execute attacker code on restart). The agent does exactly what it was told. That's the problem. The instruction looked safe and the prompt didn't reveal otherwise.

> **Treat external repositories as untrusted code, because that's what they are.** Don't run AI coding agents against repos you didn't author or don't fully trust. Especially external pull requests. For any agent that processes outside code, run it in an isolated environment (container, VM, dedicated CI runner with scoped credentials) so a config-overwrite can't reach your real keys. The safe proof-of-concept repos are on Adversa's GitHub if you want to test your own setup.

[SymJack writeup →](https://adversa.ai/blog/the-approval-prompt-is-lying-to-you-symlink-rce-in-five-ai-coding-agents-claude-code-cursor-antigravity-copilot-grok-build/) · [SecurityWeek coverage →](https://www.securityweek.com/symjack-attack-turns-ai-coding-agents-into-supply-chain-attack-delivery-systems/)

---

**TrustFall: one keypress, four CLIs, full RCE — in CI/CD there's no keypress at all**

The companion disclosure. A cloned repo ships two JSON files (`.mcp.json` and `.claude/settings.json`) that auto-approve an attacker-controlled MCP server the moment you accept the folder trust prompt. One Enter keypress and the attacker's MCP server runs with your privileges. Confirmed across Claude Code, Cursor CLI, Gemini CLI, and GitHub Copilot CLI. All default the trust prompt to "Yes."

The real problem is CI/CD. When Claude Code runs on a continuous integration server through Anthropic's official GitHub Action, it runs headless. No terminal, so the trust dialog never appears. A pull request from an outside contributor ships a malicious project file, the pipeline runs against that branch, and the attacker's code reaches whatever the runner can reach: deploy keys, signing certificates, cloud tokens. Adversa published a working demo that exfiltrates the runner's environment variables. No human in the loop.

> **This is the third Claude Code CVE in six months from the same root cause: project-scoped settings as an injection vector.** Each one gets patched in isolation. The underlying class hasn't been closed. Anthropic blocks some dangerous settings at project level (`bypassPermissions`) but not others (`enableAllProjectMcpServers`, `enabledMcpjsonServers`, `permissions.allow`). The vendor position is that accepting the trust prompt is informed consent. The researchers' counter: the dialog in current versions doesn't say what it's asking permission for. Whichever side you land on, the practical exposure is the same.

> **If you run any AI coding agent in CI/CD: gate it.** Never let Claude Code (or Gemini/Cursor/Copilot CLI) run automatically against unmerged external pull requests. Require a human merge gate before the agent touches the branch. Scope CI runner credentials to the absolute minimum. Assume that whatever the runner can reach, a malicious PR can reach too. Push agent settings centrally (server-managed config) rather than trusting per-repo files.

[TrustFall writeup →](https://adversa.ai/blog/trustfall-coding-agent-security-flaw-rce-claude-cursor-gemini-cli-copilot/) · [Help Net Security on the CI/CD angle →](https://www.helpnetsecurity.com/2026/05/07/trustfall-ai-coding-cli-vulnerability-research/)

---

**From the blog: the same lesson, one layer down**

Last week I published a step-by-step walkthrough of how a malicious MCP server drains a database in five steps. The root cause is identical to SymJack and TrustFall. The attack doesn't start at your model. It starts at your tool marketplace, in a tool description field that looks like documentation and reads like an instruction to the LLM. A developer installs a calendar-integration MCP server, runs a malware scan (clean), and never checks the tool description. That description quietly tells the agent to export all customer records before answering any query. The post includes the three controls that actually stop it.

> **SymJack, TrustFall, and the MCP database attack are the same story:** implicit trust granted somewhere nobody was watching. A config file, an approval prompt, a tool description. Assume that trust will be abused. Instrument your agents so you can see when it is. Design so that a compromised agent is an incident you contain, not a breach you discover months later.

[Read: How a Malicious MCP Server Can Drain Your Database in 5 Steps →](https://aminrj.com/posts/mcp-attack-chain-database-exfiltration/)

---

## Tooling worth knowing

- **AI Agent Pre-Deployment Security Checklist** — walks every control you need verified before an agent goes anywhere near production or sensitive credentials: identity, tool permissions, sandboxing, CI/CD gating, the exact areas SymJack and TrustFall exploit. Free, no fluff, built from real assessments. [aminrj.com/resources/predeployment-checklist →](https://aminrj.com/resources/predeployment-checklist/)
- **Adversa AI PoC repos** — safe proof-of-concept repositories for testing your own setup against SymJack and TrustFall. Test your agents against these before trusting any external code. [Adversa AI GitHub →](https://adversa.ai/blog/the-approval-prompt-is-lying-to-you-symlink-rce-in-five-ai-coding-agents-claude-code-cursor-antigravity-copilot-grok-build/)

---

## One thing to check this week

Answer one question for your team: can an AI coding agent in your environment run against an external pull request without a human merge gate first? If yes — in anyone's local setup or any CI pipeline — that's a TrustFall-class exposure. The fix is a policy, not a patch. External code gets a human merge before any agent touches it, and CI runners get minimum-scope credentials. That single control neutralizes the most dangerous variant of both attacks this week.

I'm working through these exact questions in my own agent build. [Follow along on the aminrj.com blog →](https://aminrj.com/)

---

## What I'm watching

→ **The "informed consent" boundary** — Anthropic considers post-trust-dialog execution out of scope; researchers argue the dialog doesn't disclose what it authorizes. This definitional fight determines whether the whole class gets fixed or keeps generating CVEs one at a time.

→ **Coding-agent RCE as the 2026 supply-chain vector** — SymJack and TrustFall both turn coding agents into backdoor delivery systems for CI/CD poisoning. This is shaping up to be the supply-chain attack story of the year. The defaults are the vulnerability.

→ **The headless CI/CD gap** — the trust dialog that "protects" interactive use simply doesn't exist in automation. Every team running coding agents in pipelines has this exposure until they gate it explicitly.

→ **The cybersecurity agent build** — next issue: the allowlist-based tool gate in practice, tested against exactly these config-overwrite and trust-prompt patterns. [Read the first post in the series →](https://aminrj.com/)

---

I'm writing in depth about all of this on the aminrj.com blog. Agent security patterns, lab tests, framework breakdowns. If this newsletter is useful, [the blog is where the full technical deep-dives live →](https://aminrj.com/).

Questions, pushback, something I missed — reply directly, I read everything.

Cheers,
**Amine**
