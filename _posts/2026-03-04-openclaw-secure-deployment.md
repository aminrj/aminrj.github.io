---
title: "How I Deployed OpenClaw as an AI Security Researcher: A Practitioner's Guide"
description: A hands-on guide to deploying OpenClaw as an AI-powered research assistant while controlling the blast radius — architecture decisions, Docker hardening, tool policies, and lessons from the ClawHavoc supply chain attack.
date: 2026-03-04
categories:
  - AI Security
  - Cloud Native
tags:
  - OpenClaw
  - AI Security
  - Docker
  - LLM
  - Supply Chain
  - Prompt Injection
  - MCP
image:
  path: /assets/media/ai-security/openclaw-secure-deployment-guide.png
---

_A hands-on guide to deploying OpenClaw as your AI-powered research assistant while controlling the blast radius. Built from real operational experience and the latest community security research._

**Amine Raji** · AI Security Consultant · Molntek  
March 2026

---

## Why This Guide Exists

OpenClaw is one of the most powerful open-source AI agent platforms available today. It can execute shell commands, control browsers, read and write files, manage calendars, send messages — and it does all of this through the messaging apps you already use. That power is exactly why security professionals should care about it, and exactly why deploying it carelessly is dangerous.

I started using OpenClaw as my AI security research assistant — automating daily briefings, curating threat intelligence, tracking publications in the AI security space, and managing content workflows. I interact with it through Discord, use Ollama for local models, Claude for deep reasoning, and Obsidian to persist everything important.

This guide documents how I set it up, the security decisions I made along the way, and what I learned from the community's hard-won experience — including the ClawHavoc supply chain attack that compromised roughly 20% of skills on ClawHub, nine disclosed CVEs (three with public exploit code), and over 135,000 OpenClaw instances found exposed to the public internet with insecure defaults.

The goal is practical: help you get the productivity benefits of an always-on AI agent without creating new attack surfaces in your infrastructure.

---

## Understanding What You're Deploying

Before hardening anything, you need to understand what OpenClaw actually is from a security perspective. This is not a chatbot. This is a privileged local service with persistence, autonomous execution, and broad system access.

### The Architecture in Security Terms

OpenClaw runs as a long-lived Node.js process called the **Gateway** — a WebSocket control plane that sits between your messaging channels (Discord, Telegram, WhatsApp, etc.) and the AI model backend (Anthropic, OpenAI, Ollama). The Gateway manages sessions, routes messages, executes tool calls, and maintains persistent memory as Markdown files on disk.

The key architectural components from a security standpoint are:

**Gateway (Control Plane):** WebSocket server on `ws://127.0.0.1:18789` by default. Anyone who can authenticate to this endpoint has operator-level control — configuration changes, tool policy modifications, sandbox overrides, credential access. This is your crown jewel.

**Channels (Attack Surface Inbound):** Discord, Telegram, WhatsApp, Slack — each channel is a potential ingress point. Messages arriving through these channels get processed by the LLM, which can trigger tool calls.

**Tools (Execution Surface):** Shell execution, file operations, browser automation, web fetching, cron scheduling, and more. The exec tool is the highest-risk capability — it runs commands with whatever permissions the OpenClaw process has.

**Skills (Supply Chain):** Plugin-style packages from ClawHub that extend capabilities. These are code that runs in the context of your agent, with all its permissions.

**Memory & Sessions:** Persistent Markdown files under `~/.openclaw/` containing conversation history, learned preferences, and session state. Memory contents are injected into the LLM's system prompt — making memory poisoning a real attack vector.

### The Threat Model

The OpenClaw project documents a clear threat model: **personal assistant security, one trusted operator boundary per gateway.** This is not a multi-tenant platform. If multiple people can message your bot, they all share the same delegated tool authority.

The real-world threats break into three categories:

**1. Prompt Injection via Inbound Messages:** Anyone who can message your bot can attempt to manipulate it via prompt injection. If your agent has tool access, a successful injection can chain into file reads, command execution, or data exfiltration. This risk is amplified by OpenClaw's persistent memory. In other words, a single successful injection can plant instructions that persist across sessions.

**2. Supply Chain Poisoning (ClawHub Skills):** The ClawHavoc campaign demonstrated this at scale. Attackers registered as ClawHub developers and uploaded over 1,184 malicious skills disguised as productivity tools. These skills contained everything from infostealers targeting API keys and SSH credentials to reverse shell backdoors granting full remote access. The campaign specifically targeted macOS users running OpenClaw on always-on machines.

**3. Infrastructure Exposure:** Shodan scans have found tens of thousands of OpenClaw instances exposed to the public internet. Over 93% of those had authentication bypasses. CVE-2026-25253 (CVSS 8.8) demonstrated that even localhost-bound deployments could be compromised through WebSocket origin validation failures — a malicious webpage could silently connect to the local gateway, steal the auth token, and execute arbitrary commands.

---

## My Setup: Architecture and Design Decisions

Here is the architecture I use for AI security research. The key principle is **separation of concerns with controlled blast radius**.

### Infrastructure Layer

**Docker Desktop** serves as the containment boundary. OpenClaw runs in a Docker container with explicit volume mounts, network restrictions, and a non-root user. This is the single most impactful security improvement you can make.

**Ollama** runs separately on the host, serving local models for tasks that don't require frontier intelligence — daily digest curation, initial scoring, routine classification. The models I use for these tasks are smaller (7B-class) and cost nothing to run, but they are also more susceptible to prompt injection, which is why I pair them with strict tool policies.

**Claude** (via Anthropic API) handles deep reasoning tasks, analysis, long-form synthesis, complex decision-making. The stronger model's instruction-following capability provides an additional layer of defense against injection attempts in high-stakes workflows.

**Obsidian** vault (tracked with git) is the final destination for all research outputs. OpenClaw writes to a designated workspace directory; a cron job syncs approved outputs to the Obsidian vault. The agent never has direct write access to the vault itself.

### Channel Architecture (Discord)

I use Discord as my primary interface, with a deliberate channel-per-task architecture. Each Discord channel routes to a specific agent configuration with different model backends and tool policies. This is not just organizational, it is a security boundary.

**#daily-briefing**: Uses Ollama (local model), minimal tool access (web search only, no exec), generates my morning AI security briefing from RSS feeds and curated sources. This channel processes a high volume of untrusted external content, so it gets the most restrictive tool policy.

**#research-deep**: Uses Claude (Anthropic API), broader tool access (file read/write within workspace, web search), handles deep analysis of papers, reports, and incident write-ups. Higher trust because the inputs are curated, but still sandboxed.

**#content-production**: Uses Claude, file read/write access to content workspace, no exec. Helps draft blog posts, newsletter sections, and course materials based on research outputs.

**#maintenance**: Uses Ollama, exec access within sandbox only, handles backup scripts, health checks, and system monitoring. Restricted to pre-approved command patterns.

The critical design choice here is that **no single channel has both broad external content ingestion AND execution capabilities.** The channel that reads untrusted RSS content cannot execute commands. The channel that can execute commands does not process untrusted external content. This breaks the prompt injection kill chain.

---

## Step-by-Step Hardening Guide

### Step 0: Pre-Installation Security Decisions

Before installing anything, make these decisions:

**Dedicated machine or VM.** Do not run OpenClaw on your primary workstation. Use a dedicated VPS, a spare machine, or at minimum a VM. If the agent gets compromised, you want a kill switch you can physically reach, and you want the blast radius contained to a disposable environment.

**Dedicated user account.** Create a purpose-built OS user for OpenClaw. This user should not have sudo access, should not have your SSH keys, and should not have access to your personal files.

**Dedicated credentials.** Create separate API keys, bot tokens, and service accounts specifically for OpenClaw. Use scoped tokens with minimum required permissions. Never reuse your personal API keys.

### Step 1: Docker-Based Deployment

Container isolation is the foundation. Here is a hardened Docker Compose configuration:

```yaml
# docker-compose.yml — hardened OpenClaw deployment
version: "3.8"
services:
  openclaw:
    image: node:20-slim
    user: "1000:1000"
    security_opt:
      - no-new-privileges:true
    read_only: true
    cap_drop:
      - ALL
    tmpfs:
      - /tmp:rw,noexec,nosuid,size=64M
    volumes:
      - ./openclaw-config:/home/openclaw/.openclaw:rw
      - ./workspace:/workspace:rw
      # DO NOT mount your home directory
      # DO NOT mount the Docker socket
    ports:
      - "127.0.0.1:18789:18789" # Bind to localhost ONLY
    environment:
      - NODE_ENV=production
    restart: unless-stopped
    working_dir: /home/openclaw
    command: ["npx", "openclaw", "start"]
```

Key points about this configuration: the `read_only: true` flag makes the root filesystem immutable, so a compromised agent cannot modify system binaries. The `no-new-privileges` flag prevents privilege escalation. Binding port 18789 to `127.0.0.1` ensures the gateway is never directly reachable from the network. Never mount the Docker socket into the container — that grants full host control.

### Step 2: Gateway Authentication and Network Lockdown

The gateway is the control plane. Lock it down immediately:

```bash
# Generate a strong auth token
openssl rand -hex 32

# Set it in your config
openclaw config set gateway.auth.mode token
openclaw config set gateway.auth.token "YOUR_GENERATED_TOKEN"

# Bind to loopback only
openclaw config set gateway.bind loopback
openclaw config set gateway.mode local
```

Never expose the gateway to the public internet directly. If you need remote access, use Tailscale or an SSH tunnel — never port forwarding.

### Step 3: DM Policy and Channel Access Control

Control who can talk to your bot. The default `pairing` mode is a good start, it requires a verification code before any new user can interact.
For maximum control, use an explicit allowlist:

```json
{
  "channels": {
    "discord": {
      "enabled": true,
      "dm": {
        "dmPolicy": "allowlist"
      },
      "guilds": {
        "YOUR_GUILD_ID": {
          "requireMention": true,
          "channels": {
            "BRIEFING_CHANNEL_ID": { "allow": true, "requireMention": true },
            "RESEARCH_CHANNEL_ID": { "allow": true, "requireMention": true },
            "CONTENT_CHANNEL_ID": { "allow": true, "requireMention": true },
            "MAINTENANCE_CHANNEL_ID": { "allow": true, "requireMention": true }
          }
        }
      }
    }
  }
}
```

The `requireMention` setting is essential for guild channels. Without it, the bot processes every message in the channel, dramatically increasing the injection surface. With mention gating, the bot only activates when explicitly addressed.

### Step 4: DM Session Isolation

If anyone beyond you can DM the bot, session isolation prevents cross-user data leakage:

```bash
openclaw config set session.dmScope per-channel-peer
```

The default `main` scope means all DMs share one session — environment variables, conversation history, and any loaded context bleed across users.
The `per-channel-peer` scope isolates each sender into their own session.
This is the setting that, when misconfigured, led to the real-world credential leakage incidents documented by Giskard's security research.

### Step 5: Sandbox Configuration

Enable sandboxing for all non-main sessions at minimum.
For maximum security, enable it globally:

```bash
# Enable sandbox for all sessions
openclaw config set agents.defaults.sandbox.mode all

# Restrict sandbox network (no outbound internet from sandbox)
openclaw config set agents.defaults.sandbox.docker.network none

# Restrict workspace access
openclaw config set agents.defaults.sandbox.workspaceAccess read
```

Understand the exec tool's fail-closed behavior: if `sandbox.mode` is off and `exec.host` is set to `sandbox`, exec now fails rather than silently falling back to running on the gateway host.
This is the correct behavior, but you need to know it exists.

### Step 6: Tool Policy (Least Privilege)

This is where most deployments fail. OpenClaw ships with broad default tool access. Apply a restrictive baseline and selectively re-enable:

```json
{
  "tools": {
    "profile": "messaging",
    "deny": [
      "group:automation",
      "group:runtime",
      "group:fs",
      "sessions_spawn",
      "sessions_send"
    ],
    "fs": { "workspaceOnly": true },
    "exec": {
      "security": "deny",
      "ask": "always"
    },
    "elevated": { "enabled": false }
  }
}
```

For my per-channel agent configurations, I layer additional tool permissions on top of this restrictive baseline. The briefing agent gets `web_search` only. The research agent gets `fs.read` + `web_search`. The maintenance agent gets `exec` within sandbox with `ask: always`. No agent gets unrestricted exec.

### Step 7: Model Selection (Security Implications)

Model choice is a security decision, not just a performance one.
The official OpenClaw documentation explicitly warns that weaker and older models are significantly more susceptible to prompt injection and tool misuse.

For any agent with tool access, use the strongest available instruction-hardened model. In my setup:

- **Channels processing untrusted content** (briefings, RSS ingestion): Even though I use Ollama's local models here for cost, these channels have the most restrictive tool policies precisely because smaller models are more easily manipulated.
- **Channels with tool access** (research, maintenance): Claude Sonnet or Opus through the Anthropic API. The cost is worth the instruction-following reliability when execution capabilities are on the table.

For Ollama specifically, use at minimum a 7B+ parameter model with 64K+ context length. Models below this threshold have poor instruction following and small context windows that make injection easier.
The Ollama documentation recommends Qwen 3.5 27B or GLM 4.7 Flash for tool-capable agents.

### Step 8: Credential Hygiene

Assume anything the agent can see might eventually leak through logs, memory, screenshots, or tool traces.

```bash
# Set strict file permissions
chmod 700 ~/.openclaw
chmod 600 ~/.openclaw/openclaw.json
chmod 600 ~/.openclaw/credentials/*/creds.json
```

Store API keys in environment variables or a secrets file, not directly in the JSON config.
Use scoped, read-only tokens wherever possible.
Create dedicated "agent" credentials that are intentionally limited, separate from your personal accounts.
Rotate credentials on a schedule (monthly at minimum, immediately after any suspected compromise).

If your model provider supports spending limits, set them. A compromised agent running expensive API calls can cause real financial damage.

### Step 9: Skill Installation Safety

After ClawHavoc, treat every skill installation like downloading an unknown executable.

**Before installing any skill:**

1. Check the author's GitHub account age and activity: ClawHavoc attackers used accounts less than a week old
2. Read the SKILL.md source code completely: look for suspicious prerequisites, install scripts, or encoded payloads
3. Check for typosquatting: verify the exact package name character by character
4. Look for community reviews and download counts
5. Be especially suspicious of skills in high-value categories (crypto wallets, auto-updaters, Google Workspace tools): these were the primary ClawHavoc targets
6. Run `openclaw security audit --deep` before and after installation

**Use community scanning tools:**

- **Clawdex** (from Koi Security): Scans skills against a database of known malicious packages
- **clawvet**: A 6-pass CLI scanner that checks SKILL.md files for reverse shells, credential theft patterns, obfuscation, prompt injection, and more
- **mcp-scan** (from Invariant Labs): Scans MCP tool descriptions for hidden injection instructions

**Never** copy-paste terminal commands from a skill's prerequisites section. This is the exact social engineering vector ClawHavoc exploited, fake prerequisite installations that actually deployed Atomic macOS Stealer or keyloggers.

### Step 10: Monitoring, Logging, and Incident Response

Enable comprehensive logging. Without logs, you cannot investigate incidents:

```bash
# Enable debug logging for agent activity
openclaw config set AGENT_LOG_LEVEL DEBUG
```

Session transcripts are stored under `~/.openclaw/agents/<agentId>/sessions/*.jsonl`. Review these periodically for unexpected tool calls, credential access patterns, or cross-session information leakage.

Run the security audit regularly, especially after config changes:

```bash
openclaw security audit --deep
openclaw doctor  # surfaces risky/misconfigured DM policies
```

**If you suspect compromise:**

1. **Contain immediately.** Stop the gateway (`openclaw gateway stop` or kill the process). Don't try to "clean" it.
2. **Rotate everything.** API keys, bot tokens, OAuth credentials, session tokens. Assume all credentials the agent could access are burned.
3. **Audit logs.** Check session transcripts, tool call history, and any exfiltration indicators.
4. **Rebuild from clean state.** Don't try to patch a compromised installation. Restore from backup or rebuild.

---

## Operational Workflows: What I Actually Use OpenClaw For

### Daily AI Security Briefing (Automated)

My morning briefing workflow runs on a cron schedule:

1. **RSS Aggregation:** CommaFeed (self-hosted) aggregates feeds from Lakera AI, Invariant Labs, Trail of Bits, OWASP, CSA, and other AI security sources
2. **OpenClaw Curation (#daily-briefing channel):** The local model (via Ollama) scores and summarizes new items, filtering for relevance to agentic AI security, MCP, prompt injection, and supply chain risks
3. **Output to Obsidian workspace:** Curated digest is written to a designated markdown file in the workspace directory
4. **Sync to vault:** A cron job moves approved outputs to my Obsidian vault

The critical security design: this workflow processes untrusted external content (RSS feeds, web articles) but has no execution capability. The worst case for a prompt injection in this channel is a polluted summary, not command execution.

### Research Deep Dives

When I need to analyze a new paper, incident report, or vulnerability disclosure:

1. I drop the link or document into `#research-deep`
2. Claude (via API) reads, summarizes, and maps findings to relevant frameworks (OWASP Agentic Top 10, MITRE ATLAS)
3. Outputs go to workspace for review
4. After my review, approved outputs feed into blog posts, newsletter content, or course materials

### Backup and Maintenance (Scheduled)

The `#maintenance` channel handles scheduled tasks:

- Obsidian vault git commits and pushes
- Build the initial QMD embedding index for all .md files in the vault and set up a nightly cron job to rebuild/update the index
- Workspace cleanup
- Health checks on dependent services
- Log rotation

All exec operations require explicit approval via the `ask: always` setting. I review and approve each command before execution.

---

## Mapping to OWASP Agentic Top 10

For my course students and fellow security professionals, here is how OpenClaw's attack surfaces map to the framework:

| OWASP Code | Risk                               | OpenClaw Manifestation                                                              | Mitigation Applied                                                           |
| ---------- | ---------------------------------- | ----------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| ASI01      | Agent Goal Hijacking               | Prompt injection via Discord messages or ingested content redirects agent behavior  | Channel separation, mention gating, restricted tool policies per channel     |
| ASI02      | Tool Misuse & Exploitation         | Malicious skill descriptions weaponize exec/browser/file tools                      | Tool deny lists, sandbox mode, skill vetting, mcp-scan                       |
| ASI03      | Identity & Authorization Failures  | Default `main` session scope leaks credentials across users                         | `per-channel-peer` session isolation, dedicated agent credentials            |
| ASI04      | Knowledge & Memory Poisoning       | Persistent memory stores injected instructions that trigger in future sessions      | Periodic memory review, workspace-only file access, clean rebuild procedures |
| ASI06      | Rogue Agent Behavior               | ClawHavoc skills masquerading as legitimate tools                                   | Clawdex scanning, clawvet pre-install checks, no auto-updater skills         |
| ASI07      | Sensitive Information Disclosure   | Session transcripts and memory files readable by any process with filesystem access | Strict file permissions (700/600), dedicated OS user, Docker isolation       |
| ASI08      | Insecure Agent-Agent Communication | Multi-agent setups where one agent can steer another's tool calls                   | Separate gateways per trust boundary, no shared agents for untrusted users   |
| ASI09      | Human-Agent Trust Exploitation     | Agent outputs presented as authoritative — user acts on hallucinated data           | Human review layer on all outputs before action, never auto-publish          |
| ASI10      | Insufficient Logging & Monitoring  | Default logging insufficient for incident investigation                             | DEBUG log level, session transcript review, periodic security audits         |

---

## Common Mistakes and How to Avoid Them

**Mistake: Running OpenClaw on your primary machine.** An agent compromise gives attackers access to everything you have: SSH keys, password manager vaults, browser sessions, personal files. Use a dedicated, disposable environment.

**Mistake: Using `dmPolicy: open`.** This lets anyone message your bot. Combined with tool access, it is effectively an open remote code execution endpoint. Use `pairing` or `allowlist` exclusively.

**Mistake: Mounting your home directory into the container.** Convenience is the enemy of security here. Mount only the specific directories the agent needs, with appropriate read/write restrictions.

**Mistake: Installing skills without review.** After ClawHavoc, the only safe approach is manual verification of every skill before installation. Automated scanning tools help, but they catch patterns, novel attacks will bypass them.

**Mistake: Using the same model for everything.** Match model strength to task risk. Cheap local models for low-risk summarization. Frontier models for anything involving tool execution. This is not about capability, it is about prompt injection resistance.

**Mistake: Forgetting that memory is an attack vector.** OpenClaw's persistent memory injects stored content into the system prompt. A single successful injection that writes to memory creates a persistent backdoor that fires on every subsequent interaction. Review memory contents periodically and have a clean rebuild procedure.

**Mistake: Trusting the gateway is safe because it is on localhost.** CVE-2026-25253 proved this wrong. A malicious webpage in your browser could exploit WebSocket origin validation to hijack a localhost gateway. Keep your OpenClaw version current and the auth token strong.

---

## Security Checklist — Quick Reference

Use this checklist when setting up a new OpenClaw deployment or auditing an existing one:

**Infrastructure:**

- [ ] Dedicated machine/VM/container — not your primary workstation
- [ ] Dedicated OS user with no sudo access
- [ ] Docker deployment with `no-new-privileges`, `read_only`, `cap_drop: ALL`
- [ ] Gateway bound to `127.0.0.1` only
- [ ] No Docker socket mounted in container
- [ ] Latest OpenClaw version (check: `openclaw --version`, must be ≥ 2026.2.26)

**Authentication & Access:**

- [ ] Strong gateway auth token (32+ random hex characters)
- [ ] `dmPolicy: pairing` or `allowlist` on all channels
- [ ] `requireMention: true` on all guild/group channels
- [ ] `session.dmScope: per-channel-peer` for any multi-user scenario

**Tool Policy:**

- [ ] Restrictive base profile (`messaging` or custom)
- [ ] `exec.security: deny` or `exec.ask: always`
- [ ] `elevated.enabled: false`
- [ ] `fs.workspaceOnly: true`
- [ ] Sandbox mode enabled (`agents.defaults.sandbox.mode: all`)
- [ ] Per-channel/per-agent tool allow lists (not global broad access)

**Credentials & Secrets:**

- [ ] Dedicated agent API keys (not personal keys)
- [ ] File permissions: `chmod 700 ~/.openclaw`, `chmod 600` on configs and credentials
- [ ] Provider spending limits configured
- [ ] Credential rotation schedule (monthly minimum)
- [ ] No secrets stored in agent memory or conversation history

**Supply Chain:**

- [ ] Every skill reviewed before installation
- [ ] Clawdex or clawvet scanning enabled
- [ ] No auto-updater skills installed
- [ ] ClawHub skill source code verified against known malicious patterns

**Monitoring:**

- [ ] `openclaw security audit --deep` run after every config change
- [ ] `openclaw doctor` run periodically
- [ ] Session transcript review schedule established
- [ ] Incident response procedure documented (contain → rotate → audit → rebuild)

---

## Final Thoughts

OpenClaw represents the cutting edge of what personal AI agents can do — and by extension, the cutting edge of what can go wrong. The ClawHavoc campaign, the exposed instances, and the CVE disclosures are not edge cases. They are the predictable consequences of deploying powerful autonomous systems without security-first design.

The approach I have documented here is not theoretical. It is what I run daily to stay current on AI security research while maintaining the operational discipline that my background in security demands. The core principle is simple: **treat your AI agent like a junior employee with root access.** Give it the minimum permissions it needs, verify its work, and always have a way to shut it down.

The future of personal AI is agentic. The question is not whether you will use tools like OpenClaw, but whether you will use them securely. I hope this guide helps you make the right choice.

---

_This guide will be maintained and updated as OpenClaw evolves. For the latest AI security research, subscribe to the AI Security Intelligence newsletter at Beehiiv or follow Molntek on LinkedIn._

_Feedback and corrections welcome — this is a practitioner's guide, not a finished product._
