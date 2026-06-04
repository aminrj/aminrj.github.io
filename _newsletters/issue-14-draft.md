# [AI Sec Intel] #14 — Your coding agent's approval prompt is lying to you.

**Subject options:**
- A (recommended): `[AI Sec Intel] #14 — Your coding agent's approval prompt is lying to you.`
- B: `[AI Sec Intel] #14 — One keypress. Six coding agents. Full RCE. Same root cause.`
- C: `[AI Sec Intel] #14 — "Yes, I trust this folder" is now a remote code execution primitive.`

**Preview text:** `SymJack and TrustFall broke every major AI coding agent this month — Claude Code, Cursor, Gemini, Copilot, Codex. The dialog you click through doesn't say what you're approving. Here's what to do.`

**Subtitle:** `Two disclosures, one architectural flaw: the trust prompt approves more than it shows. Plus the CI/CD variant that needs no human at all.`

---

Hey 👋

If you use an AI coding agent — Claude Code, Cursor, Gemini CLI, Copilot, Codex — this issue is about you specifically. Two disclosures this month showed that the "Yes, I trust this folder" prompt you click through a dozen times a day is approving far more than it tells you. Both turn a cloned repository into remote code execution on your machine. Both work across every major tool. Neither is a bug in any single product — they're the same architectural flaw wearing two disguises.

I spent this week mapping how this connects to the MCP attack chain I published last week. It's the same lesson at a different layer: the danger isn't the model, it's the trust you grant without seeing what you're granting.

---

## This week in AI security

**SymJack: a booby-trapped repo tricks your coding agent into overwriting its own config — then runs attacker code on restart**

Adversa AI's disclosure is the sharpest of the month. The attack: a malicious repository contains an innocent-looking file copy operation. Your AI coding assistant performs the copy as part of normal work. What it's actually doing is following a symlink that overwrites the agent's own configuration file. The next time the agent restarts, it runs the attacker's code with your full user privileges. They confirmed it against six tools: Claude Code, Gemini CLI / Antigravity CLI, Cursor Agent CLI, GitHub Copilot CLI, Grok Build, and OpenAI Codex CLI. Every one was vulnerable.

The detail that makes it dangerous: the approval prompt the developer sees describes a benign file copy. It does not say "this will overwrite my configuration." The user accepts because nothing looks wrong — and accepting is the entire point of using a coding agent. Speed and trust in automation are exactly what the attack exploits.

> **[GREY CALLOUT — THE INSIGHT]**
> **This is one technique against a whole category, not six separate bugs.** SymJack is architectural: every agent that can copy files and read project-scoped configuration is exposed, because the approval prompt describes the *action* (copy a file) and not the *consequence* (overwrite my own config and execute attacker code on restart). The agent is doing exactly what it was told. That's the problem — the instruction looked safe and the prompt didn't reveal otherwise.

> **[AMBER CALLOUT — DO THIS]**
> **Treat external repositories as untrusted code, because that's what they are.** Don't run AI coding agents against repos you didn't author or don't fully trust — especially external pull requests. For any agent that processes outside code, run it in an isolated environment (container, VM, dedicated CI runner with scoped credentials) so a config-overwrite can't reach your real keys. The safe proof-of-concept repos are on Adversa's GitHub if you want to test your own setup.

[SymJack writeup →](https://adversa.ai/blog/the-approval-prompt-is-lying-to-you-symlink-rce-in-five-ai-coding-agents-claude-code-cursor-antigravity-copilot-grok-build/) · [SecurityWeek coverage →](https://www.securityweek.com/symjack-attack-turns-ai-coding-agents-into-supply-chain-attack-delivery-systems/)

---

**TrustFall: one keypress, four CLIs, full RCE — and in CI/CD there's no keypress at all**

The companion disclosure. A cloned repo ships two JSON files (`.mcp.json` and `.claude/settings.json`) that auto-approve an attacker-controlled MCP server the moment you accept the folder trust prompt. One Enter keypress and the attacker's MCP server runs with your privileges. Confirmed across Claude Code, Cursor CLI, Gemini CLI, and GitHub Copilot CLI — all default the trust prompt to "Yes."

The genuinely alarming part is CI/CD. When Claude Code runs on a continuous integration server through Anthropic's official GitHub Action, it runs headless. No terminal, so the trust dialog never appears. A pull request from an outside contributor ships a malicious project file, the pipeline runs against that branch, and the attacker's code reaches whatever the runner can reach: deploy keys, signing certificates, cloud tokens. Adversa published a working demo that exfiltrates the runner's environment variables. No human in the loop at all.

> **[GREY CALLOUT — THE PATTERN]**
> **This is the third Claude Code CVE in six months from the same root cause: project-scoped settings as an injection vector.** Each one gets patched in isolation; the underlying class hasn't been closed. Anthropic blocks some dangerous settings at project level (`bypassPermissions`) but not others (`enableAllProjectMcpServers`, `enabledMcpjsonServers`). The vendor position is that accepting the trust prompt is informed consent. The researchers' counter: the dialog in current versions doesn't say what it's asking permission for. Whichever side you land on, the practical exposure is the same.

> **[AMBER CALLOUT — CHECK THIS TODAY]**
> **If you run any AI coding agent in CI/CD: gate it.** Never let Claude Code (or Gemini/Cursor/Copilot CLI) run automatically against unmerged external pull requests. Require a human merge gate before the agent touches the branch. Scope CI runner credentials to the absolute minimum — assume that whatever the runner can reach, a malicious PR can reach too. Push agent settings centrally (server-managed config) rather than trusting per-repo files.

[TrustFall writeup →](https://adversa.ai/blog/trustfall-coding-agent-security-flaw-rce-claude-cursor-gemini-cli-copilot/) · [Help Net Security on the CI/CD angle →](https://www.helpnetsecurity.com/2026/05/07/trustfall-ai-coding-cli-vulnerability-research/)

---

**From the blog: the same lesson, one layer down**

Last week I published a step-by-step walkthrough of how a malicious MCP server drains a database in five steps — and the root cause is identical to SymJack and TrustFall. The attack doesn't start at your model. It starts at your tool marketplace, in a tool description field that looks like documentation and reads like an instruction to the LLM. A developer installs a calendar-integration MCP server, runs a malware scan (clean), and never checks the tool description — which quietly tells the agent to export all customer records before answering any query. The post includes the three controls that actually stop it.

> **[BLUE CALLOUT — THE THROUGH-LINE]**
> **SymJack, TrustFall, and the MCP database attack are the same story:** implicit trust granted somewhere nobody was watching — a config file, an approval prompt, a tool description. Assume that trust will be abused. Instrument your agents so you can see when it is. Design so that a compromised agent is an incident you contain, not a breach you discover months later.

[Read: How a Malicious MCP Server Can Drain Your Database in 5 Steps →](https://aminrj.com/posts/mcp-attack-chain-database-exfiltration/)

---

## This week's resource

If the SymJack and TrustFall disclosures made you realize you don't actually know what your AI agents can reach, that's the gap my **AI Agent Pre-Deployment Security Checklist** is built to close. It walks every control you need verified before an agent goes anywhere near production or sensitive credentials — identity, tool permissions, sandboxing, CI/CD gating, the exact areas these attacks exploit. Free, no fluff, built from real assessments.

[Get the AI Agent Pre-Deployment Security Checklist →](https://aminrj.com/resources/predeployment-checklist/)

---

## One thing to check this week

Answer one question for your team: can an AI coding agent in your environment run against an external pull request without a human merge gate first? If yes — in anyone's local setup or any CI pipeline — that's a TrustFall-class exposure live right now. The fix is a policy, not a patch: external code gets a human merge before any agent touches it, and CI runners get minimum-scope credentials. That single control neutralizes the most dangerous variant of both attacks this week.

---

## What I'm watching

→ **The "informed consent" boundary** — Anthropic considers post-trust-dialog execution out of scope; researchers argue the dialog doesn't disclose what it authorizes. This definitional fight determines whether the whole class gets fixed or keeps generating CVEs one at a time.

→ **Coding-agent RCE as the 2026 supply-chain vector** — SymJack and TrustFall both turn coding agents into backdoor delivery systems for CI/CD poisoning. This is shaping up to be the supply-chain attack story of the year, and the defaults are the vulnerability.

→ **The headless CI/CD gap** — the trust dialog that "protects" interactive use simply doesn't exist in automation. Every team running coding agents in pipelines has this exposure until they gate it explicitly.

→ **The cybersecurity agent build** — next issue: the allowlist-based tool gate in practice, tested against exactly these config-overwrite and trust-prompt patterns.

---

Questions, pushback, something I missed — reply directly, I read everything.

Cheers,
**Amine**

---

## Beehiiv HTML callouts — paste as Custom HTML blocks

**Grey — the insight (SymJack):**
```html
<div style="background:#f5f5f4;border-left:3px solid #a8a29e;padding:12px 16px;border-radius:0 6px 6px 0;font-family:Georgia,serif;font-size:15px;line-height:1.7;color:#1c1917;">
  <b>This is one technique against a whole category, not six separate bugs.</b> SymJack is architectural: every agent that can copy files and read project-scoped configuration is exposed, because the approval prompt describes the <em>action</em> (copy a file) and not the <em>consequence</em> (overwrite my own config and execute attacker code on restart). The agent is doing exactly what it was told. That's the problem — the instruction looked safe and the prompt didn't reveal otherwise.
</div>
```

**Amber — do this (SymJack):**
```html
<div style="background:#fefce8;border-left:3px solid #ca8a04;padding:12px 16px;border-radius:0 6px 6px 0;font-family:Georgia,serif;font-size:15px;line-height:1.7;color:#1c1917;">
  <b>Treat external repositories as untrusted code, because that's what they are.</b> Don't run AI coding agents against repos you didn't author or don't fully trust — especially external pull requests. For any agent that processes outside code, run it in an isolated environment (container, VM, dedicated CI runner with scoped credentials) so a config-overwrite can't reach your real keys. The safe proof-of-concept repos are on Adversa's GitHub if you want to test your own setup.
</div>
```

**Grey — the pattern (TrustFall):**
```html
<div style="background:#f5f5f4;border-left:3px solid #a8a29e;padding:12px 16px;border-radius:0 6px 6px 0;font-family:Georgia,serif;font-size:15px;line-height:1.7;color:#1c1917;">
  <b>This is the third Claude Code CVE in six months from the same root cause: project-scoped settings as an injection vector.</b> Each one gets patched in isolation; the underlying class hasn't been closed. Anthropic blocks some dangerous settings at project level (bypassPermissions) but not others (enableAllProjectMcpServers, enabledMcpjsonServers). The vendor position is that accepting the trust prompt is informed consent. The researchers' counter: the dialog in current versions doesn't say what it's asking permission for. Whichever side you land on, the practical exposure is the same.
</div>
```

**Amber — check this today (TrustFall):**
```html
<div style="background:#fefce8;border-left:3px solid #ca8a04;padding:12px 16px;border-radius:0 6px 6px 0;font-family:Georgia,serif;font-size:15px;line-height:1.7;color:#1c1917;">
  <b>If you run any AI coding agent in CI/CD: gate it.</b> Never let Claude Code (or Gemini/Cursor/Copilot CLI) run automatically against unmerged external pull requests. Require a human merge gate before the agent touches the branch. Scope CI runner credentials to the absolute minimum — assume that whatever the runner can reach, a malicious PR can reach too. Push agent settings centrally (server-managed config) rather than trusting per-repo files.
</div>
```

**Blue — the through-line (blog tie-in):**
```html
<div style="background:#eff6ff;border-left:3px solid #3b82f6;padding:12px 16px;border-radius:0 6px 6px 0;font-family:Georgia,serif;font-size:15px;line-height:1.7;color:#1c1917;">
  <b>SymJack, TrustFall, and the MCP database attack are the same story:</b> implicit trust granted somewhere nobody was watching — a config file, an approval prompt, a tool description. Assume that trust will be abused. Instrument your agents so you can see when it is. Design so that a compromised agent is an incident you contain, not a breach you discover months later.
</div>
```
