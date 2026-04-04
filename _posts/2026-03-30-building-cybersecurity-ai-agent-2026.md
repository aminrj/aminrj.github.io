---
title: "Building a Cybersecurity AI Agent From Scratch: The Complete 2026 Guide"
date: 2026-03-30
uuid: 202603300000
content-type: article
target-audience: advanced
categories: [AI Security, Agentic AI, Developer Guide]
tags:
  [
    LangGraph,
    MCP,
    Agentic AI,
    Cybersecurity,
    Threat Intelligence,
    Python,
    LLM,
    Security Engineering,
  ]
image:
  path: /assets/media/ai-security/build-a-cybersecurity-ai-agent.png

description: "A complete hands-on guide to building a Security Intelligence Agent using LangGraph and MCP — covering architecture decisions, trade-offs, and working code that performs live threat correlation and CVE analysis. Includes real agent output and lessons from debugging."
mermaid: true
---

# Building a Cybersecurity AI Agent From Scratch: The Complete 2026 Guide

It is 2 AM. An alert fired on your SIEM — a source IP your team has never seen before is hammering port 22 on a perimeter host. You pull the raw log, grep for the IP, and open three browser tabs: Shodan, VirusTotal, and the NVD search. Twenty minutes later you have a half-assembled picture: the IP is known Tor exit node infrastructure, there is a CVE that affects the SSH daemon version on that host, and your logs show seventeen failed auth attempts in the last six hours. You write up the finding. It took a senior analyst thirty minutes to produce something that could have been automated in three.

This guide builds the system that runs that triage automatically.

By the end you will have a working **Security Intelligence Agent** that takes a target — IP address, domain, CVE identifier, or threat actor name — and autonomously fetches current threat intelligence from live sources, correlates indicators with known CVEs from NIST NVD, searches your security logs for matching events, and produces a structured threat assessment report. It runs entirely on your local machine. No data leaves your environment. No API calls to a cloud LLM if you do not want them.

Here is what that looks like against a real CVE — including every tool call the agent made and where it got each piece of information:

```
$ python3 main.py -v CVE-2025-68664

[*] Target:     CVE-2025-68664
[*] Type:       cve
[*] Plan:       threat_intel → cve_lookup → report
[*] Started:    2026-04-04T19:24:17Z

  [prompt] Search for current threat intelligence about: CVE-2025-68664...
  [turn 1] → search_threat_intelligence(query='CVE-2025-68664 exploitation in the wild')
       ↳ CVE-2025-68664 LangChain Serialization Flaw
          https://orca.security/resources/blog/cve-2025-68664-langchain-serialization-flaw/
       ↳ CVE-2025-68664: What It Means for Your Business
          https://integsec.com/blog/cve-2025-68664-langchain-serialization-flaw
       ↳ Nuclear Option: Deep Dive into LangChain Serialization Injection
          https://www.penligent.ai/hackinglabs/nuclear-option-deep-dive-into-langchain-serialization-injection-cve-2025-68664/
  [turn 2] no tool calls — node finished
  [✓] threat_intel          42.3s
  [turn 1] → lookup_cve(cve_id='CVE-2025-68664')
       ↳ CVE-2025-68664 CVSS=9.3 CRITICAL
  [✓] cve_lookup            18.1s
  [✓] report                31.7s

======================================================================
## Threat Assessment Report

**Target:** CVE-2025-68664
**Severity:** CRITICAL

### Executive Summary
CVE-2025-68664 is a critical deserialization vulnerability (CVSS 9.3) in
langchain-core prior to 0.3.29. Public PoC details are disclosed. Attackers
can extract API keys and environment secrets, or execute arbitrary code via
crafted JSON payloads containing the reserved 'lc' key...

### CVE Analysis
| CVE ID | CVSS | Severity | Vector |
| CVE-2025-68664 | 9.3 | CRITICAL | AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N |

### Recommendations
1. Upgrade langchain-core to ≥ 0.3.29 immediately
2. Rotate all API keys exposed to LangChain applications
3. Implement strict input validation rejecting 'lc' key structures
...

[*] Severity:   CRITICAL
[*] Total time: 92.1s
======================================================================
```

In 92 seconds, from a CVE ID, the agent pulled live intelligence from three sources, got the authoritative CVSS score from NIST, identified the patch version, and produced an actionable report. Against a threat actor name, the same pipeline surfaces current TTP reporting and campaign activity from real analyst publications:

```
$ python3 main.py -v "LockBit ransomware"

  [turn 1] → search_threat_intelligence(query='LockBit ransomware TTPs 2026')
       ↳ LockBit Ransomware: From Origins to LockBit 4.0 (Neo) in 2026
          https://www.xactcybersecurity.com/lockbit-ransomware-attack-guide/
       ↳ The State Of Ransomware 2026 - BlackFog
          https://www.blackfog.com/the-state-of-ransomware-2026/
       ↳ LockBit Ransomware: Attack Methods and 2026 Status - CybelAngel
          https://cybelangel.com/blog/lockbit-cybercriminal-guide/

[*] Severity:   HIGH  |  Total time: 196s
```

Every source URL is visible. Every claim in the report traces to a source you can verify. That transparency is not an accident — it is a design requirement, and one of the things this guide spends time on.

We will build this in two stages: first with LangGraph native tools (maximum control, simplest security reasoning), then extend with MCP (Model Context Protocol) — now the dominant standard for connecting agents to external tools, and something you need to understand critically before deploying.

Everything runs locally first. Cloud options are noted throughout.

---

## Part 1 — Why Agents, Why Now, and Why the Basics Matter

### What an LLM Alone Cannot Do

A language model answers questions. It has knowledge up to its training cutoff, it can reason over text you give it, and it produces text output. That is genuinely useful, but it is fundamentally passive. The model cannot fetch a live CVE feed. It cannot query Shodan against a current IP. It cannot compare what it finds against your specific firewall logs from last night.

These limitations are not bugs; they are by design. LLMs are stateless text transformers. The moment you want an LLM to interact with the world — not just describe it — you need an agent.

An agent is a system where an LLM controls an execution loop. The LLM reasons over a problem, decides what action to take, calls a tool (a Python function, an API, a shell command), receives the result, reasons again, decides the next action, and continues until the task is complete. The LLM is the decision-maker. The tools are the hands.

The five properties that make an agentic system different from a simple chatbot are worth memorizing, because they are also the five properties that create a new attack surface — which is exactly what Part 2 of this series demonstrates:

1. **Autonomy** — the agent plans and acts without per-step human approval
2. **Tool use** — the agent calls external APIs, reads files, executes code
3. **Delegation** — the agent can hand off subtasks to other agents
4. **Persistence** — the agent maintains state across turns and sessions via memory
5. **Identity** — the agent acts with credentials and permissions that belong to a real account

None of these is hypothetical. The agent you build in this guide will have all five from the first working version.

### The Real Value Proposition for Security Teams

Before we write any code, let us be specific about what this buys you — and what it does not.

**What it buys you:** The agent performs in under four minutes what takes a junior analyst thirty to sixty minutes when done manually across multiple browser tabs and tool switches. That is: live threat intel gathering, CVE correlation, log pattern matching, and structured report output. For routine triage — an unfamiliar IP in your logs, a newly published CVE that affects software you run, a threat actor name that appeared in a client report — this is exactly the right tool.

**What it does not buy you:** Judgment about your organization's specific risk posture. Knowledge of your architecture beyond what you put in the logs. An understanding of which finding is highest priority in your environment this week. The agent is a first-pass triage tool. It raises the quality floor for the first fifteen minutes of an investigation. A human analyst still owns the decision.

**The transparency advantage:** Unlike a black-box AI assistant that gives you an answer with no provenance, this agent shows its work. Verbose mode (`-v`) exposes every search query, every source URL, every tool call. When the report says "LockBit 5.0 was released in February 2026," you can see that it came from a Broadcom threat report published in January 2026. If the source does not support the claim, you know before you act on it.

### Why LangGraph (and Not Something Else)

The framework landscape in 2026 is noisy. Here is the honest decision matrix:

| Framework | Best for | Avoid if |
|---|---|---|
| **LangGraph** | Complex branching workflows, explicit state control, production debugging | You need something running in 30 minutes with minimal boilerplate |
| **CrewAI** | Role-based multi-agent collaboration, rapid prototyping | You need complex conditional branching or state rollbacks |
| **OpenAI Agents SDK** | Teams fully committed to OpenAI stack, fastest path to production | You want provider flexibility or local/open-source models |
| **PydanticAI** | Type-safe outputs, FastAPI-style ergonomics, 25+ model providers | You need visual debugging tools |
| **AutoGen/AG2** | Multi-agent conversations, research prototyping | Production deployments with strict SLA requirements |

For a security use case you need: conditional routing (if intel mentions CVEs, go look them up; if the target is an IP, search the logs), explicit state management (accumulate findings across multiple tool calls without losing earlier results), reproducible debugging (trace exactly which node fired and what it received), and eventual MCP integration. **LangGraph is the right choice.** Its state machine architecture makes agentic loops predictable, and the audit trail it produces is exactly what security operations require.

> **What about OpenClaw and NemoClaw?**
>
> OpenClaw (246K GitHub stars as of early 2026) is a **personal AI assistant platform** — you write a `SOUL.md` configuration file and get an agent connected to messaging apps with no Python required. It is not a framework for building custom threat intelligence pipelines. OpenClaw shipped with CVE-2026-25253 (critical WebSocket vulnerability), rampant skill poisoning in its ecosystem, and zero security by default. The community building security layers on top of it — SecureClaw, ClawSec, the SlowMist hardening guide — is doing exactly the work that Part 2 of this series covers. The attacks are identical. The scale is just larger.
>
> NemoClaw is NVIDIA's enterprise security layer on top of OpenClaw — announced GTC March 2026, still in early alpha — adding kernel-level sandboxing and policy-based guardrails. Relevant if you want to harden OpenClaw deployments; not relevant to building structured, code-defined agentic workflows.

### The Four Concepts That Make LangGraph Click

**State** is a typed Python dictionary that flows through every step of the graph. Every node reads from it and writes back to it. Updates append rather than replace — nothing is lost. In our agent, the state carries: the original target, threat intel findings, CVE matches, log analysis results, extracted IOCs, and the final report.

**Nodes** are where work happens. Each node is a Python function that takes the current state, does something (calls an API, runs an LLM), and returns an update.

**Edges** decide what happens next. A conditional edge examines the current state and routes to different nodes based on what it finds.

**Tools** are Python functions the LLM can invoke. The LLM sees the tool's name, description, and parameter schema, and decides when to call which. Tool descriptions are processed as instructions — a distinction with significant security implications covered in Part 2.

Here is the complete execution flow:

```
User input (target: IP / domain / CVE / threat actor)
    ↓
[START] → supervisor_node  ← deterministic routing, no LLM
               ↓
    ┌──────────────────────────────────────────────────────┐
    │  threat_intel_node   ← Tavily web search, IOC extract │
    │  cve_lookup_node     ← NIST NVD API                   │
    │  log_analysis_node   ← local JSONL log search         │
    │  report_node         ← LLM synthesis                  │
    └──────────────────────────────────────────────────────┘
    (each node routes back to supervisor after completion)
    ↓
[END] → structured threat assessment + IOC list + SQLite checkpoint
```

The supervisor does not run tools — it routes. Each specialist node has its own tool set. This separation makes the system debuggable and extensible.

---

## Part 2 — The Tech Stack

### The LLM Layer: Three Paths and What They Actually Cost You

The choice of LLM matters more for security workflows than most tutorials acknowledge. Three factors:

**Factor 1: Content filtering.** Cloud LLMs have increasingly aggressive filters on security-adjacent requests. Analyzing an active exploitation chain, reasoning through a brute-force sequence, or interpreting malware behavior will hit refusals at unpredictable points. Not every time, but often enough to break production pipelines. This is not a flaw — safety filtering exists for good reasons. It is a practical constraint. Local open-weight models like Qwen3.5 have no content filtering, which is what makes them operationally viable for security research.

**Factor 2: Data sovereignty.** In any realistic security deployment you are feeding the agent actual log files, internal IP ranges, real CVE data from your environment. Sending that to an external API is a data governance problem — and in regulated industries (banking, defense, automotive), potentially a compliance violation. Local models solve it completely.

**Factor 3: Tool-call reliability.** Smaller models follow single-step instructions well. They struggle with multi-hop reasoning. The supervisor pattern in this guide is specifically designed to compensate: it breaks multi-hop tasks into explicit sequential nodes rather than asking a single model call to plan and execute everything. A 27B model with this architecture outperforms an unstructured agentic loop using a much larger model.

**Path A — Local via Ollama (recommended):**

[Ollama](https://ollama.com) serves an OpenAI-compatible API on `localhost:11434`. No API key, no usage costs, no data leaving your machine.

```bash
ollama pull qwen3.5:27b
```

Not all model variants support tool/function calls — the capability depends on which chat template was compiled into the GGUF. Before committing to a model, test it:

```bash
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"your-model","messages":[{"role":"user","content":"hi"}],
       "tools":[{"type":"function","function":{"name":"t","description":"t",
       "parameters":{"type":"object","properties":{}}}}]}'
# A response with "choices" = tool calls work.
# An error like "does not support tools" = skip this variant.
```

Verified working:

| Model | Size | Tool calls | Notes |
|---|---|---|---|
| `qwen3.5:27b` | 17 GB | ✓ | Used in this guide; strong reasoning |
| `qwen2.5:14b` | 9 GB | ✓ | Good balance; daily workflows |
| `qwen2.5-coder:7b-instruct-q4_K_M` | 4.7 GB | ✓ | Fastest option for demos |
| `qwen3.5:9b-q4_K_M` | 5.6 GB | ✗ | No tool template in this quantization |
| `qwen3.5:35b-a3b-q4_K_M` | 21 GB | ✗ | MoE variant — no tool template |

> **Qwen3.5 thinking mode:** Qwen3.5 models run an extended chain-of-thought before every response by default. This is valuable for complex reasoning tasks but adds 30–90 seconds per node call in structured agentic workflows where the model is just deciding which tool to call. Disable it with `extra_body={"think": False}` in the Ollama request. Do not put this in `model_kwargs` — the key must go through `extra_body` so the OpenAI SDK forwards it as a raw JSON field rather than mapping it to a typed parameter. Getting this wrong produces `TypeError: Completions.create() got an unexpected keyword argument 'think'`.

**Path B — OpenAI:**

`gpt-4o-mini` hits the best cost/performance balance. Content filters will occasionally refuse security-specific prompts; frame defensively ("analyze this for indicators of compromise" rather than "explain how to exploit this").

**Path C — Anthropic:**

`claude-sonnet-4-5` is strong for agentic workflows requiring careful instruction-following. Same filtering caveats as OpenAI.

For all three paths, the LangGraph code is identical. Only `llm_config.py` changes:

```python
# llm_config.py — single place to configure the LLM for all nodes

def get_llm():
    provider = os.getenv("LLM_PROVIDER", "ollama").lower()

    if provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=0)

    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5"), temperature=0)

    # Ollama — disable Qwen3.5 thinking via extra_body
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(
        base_url=os.getenv("LM_STUDIO_BASE_URL", "http://localhost:11434/v1"),
        api_key="ollama",   # any non-empty string
        model=os.getenv("LM_STUDIO_MODEL", "qwen3.5:27b"),
        temperature=0,
        extra_body={"think": False},  # suppresses silent chain-of-thought
    )
```

Centralizing LLM configuration in one file means changing providers requires touching exactly one place. The nodes never import model-specific packages directly.

`temperature=0` is non-negotiable for agents. Non-determinism is useful for creative tasks. For security analysis you need the same routing decision for the same data.

### The Tool Layer: Native vs MCP — With Security Context

**LangChain native tools** (`@tool` decorator) are Python functions that live in the same process as your agent. Simple, fast, easy to audit. Their descriptions are static — written in your code.

**MCP tools** run as separate server processes. Your agent connects to them at runtime via a client-server protocol. Any MCP-compatible client can use them — Claude Desktop, Cursor, your LangGraph agent. This is now the standard tool interoperability layer: donated to the Linux Foundation in December 2025, adopted by OpenAI and Google, 75+ connectors in Claude alone.

What has also become clear is that MCP introduces an attack surface native tools do not have. MCP tool descriptions are served dynamically at runtime — they can change between loads. A compromised MCP server can embed hidden instructions in tool descriptions that the LLM processes as legitimate directives. The ecosystem around OpenClaw's skill marketplace demonstrated this at scale: plugin poisoning was rampant, and it took months to build detection tooling.

This guide builds with native tools first, then shows the MCP migration with security implications explicit. That sequence is the right mental model: understand what you are gaining and what you are accepting.

### Complete Stack

```
LLM:           Ollama / OpenAI / Anthropic (single llm_config.py)
Framework:     LangGraph 1.x (langgraph-checkpoint-sqlite ≥ 3.0.1)
Core libs:     langchain-core ≥ 0.3.29 (minimum patched for CVE-2025-68664)
Tools:         LangChain @tool (native) → FastMCP (MCP server)
Search:        Tavily API (free tier: 1,000 searches/month)
CVE data:      NIST NVD API v2.0 (free; 50 req/30s with key)
Log data:      Local JSONL (swap for SIEM API in production)
State store:   SQLite checkpointer (built into LangGraph)
Observability: LangSmith (optional, free tier)
```

Pin versions explicitly. Both LangGraph and LangChain had critical CVEs in late 2025 (CVE-2025-67644 and CVE-2025-68664) that affect the exact code in this guide.

---

## Part 3 — Environment Setup

```bash
mkdir ~/sec-intel-agent && cd ~/sec-intel-agent
python3 -m venv venv && source venv/bin/activate

pip install \
  "langgraph>=0.2" \
  "langgraph-checkpoint-sqlite>=3.0.1" \
  "langchain-core>=0.3.29" \
  langchain-openai langchain-anthropic langchain-community \
  tavily-python httpx python-dotenv fastmcp mcp langsmith
```

Create `.env`:

```env
LLM_PROVIDER=ollama
LM_STUDIO_BASE_URL=http://localhost:11434/v1
LM_STUDIO_MODEL=qwen3.5:27b

TAVILY_API_KEY=tvly-...
NVD_API_KEY=          # optional — raises rate limit from 5 to 50 req/30s

LOG_FILE_PATH=sample_logs.jsonl

# Optional LangSmith observability
# LANGCHAIN_TRACING_V2=true
# LANGCHAIN_API_KEY=ls__...
# LANGCHAIN_PROJECT=sec-intel-agent
```

**`.env` in `.gitignore` — non-negotiable.** This file contains live API keys. The agent will create a `.gitignore` entry automatically if you use the repo from GitHub. If you are setting up manually, add it yourself before the first commit. API keys committed to git history require key rotation even after removal — the history is permanent on any remote that received the push.

Verify Ollama connectivity and tool support:

```bash
curl http://localhost:11434/v1/models
# Lists available models

# Test tool call support for your chosen model
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen3.5:27b","messages":[{"role":"user","content":"hi"}],
       "tools":[{"type":"function","function":{"name":"t","description":"t",
       "parameters":{"type":"object","properties":{}}}}]}'
```

---

## Part 4 — Building the Agent

### Step 1: Define the State

```python
# state.py
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class SecurityIntelState(TypedDict):
    # Input
    target: str        # IP, domain, CVE ID, or threat actor name
    target_type: str   # "ip" | "domain" | "cve" | "threat_actor"

    # Accumulated findings — add_messages appends rather than replaces
    messages: Annotated[list, add_messages]
    threat_intel: list[dict]   # Tavily search results
    cve_matches: list[dict]    # NVD CVE details
    log_findings: list[dict]   # matched log events
    ioc_list: list[str]        # deduplicated Indicators of Compromise

    # Control flow
    completed_phases: list[str]
    current_phase: str
    error_log: list[str]

    # Output
    report: str
    severity: str   # "critical" | "high" | "medium" | "low" | "info"
```

The `Annotated[list, add_messages]` on `messages` tells LangGraph to append rather than overwrite on each update — this is how conversation history accumulates across nodes without being lost.

### Step 2: Build the Tools

Four tools cover the full triage workflow. Security considerations are inline — they matter, and they are not afterthoughts.

```python
# tools.py
import os, json, re, time
from datetime import datetime
from pathlib import Path
import httpx
from langchain_core.tools import tool

# Path confinement — prevents directory traversal via log_path parameter.
# Resolved once at module load so misconfiguration fails at startup.
_LOG_FILE_PATH = Path(os.getenv("LOG_FILE_PATH", "sample_logs.jsonl")).resolve()
_ALLOWED_LOG_DIR = _LOG_FILE_PATH.parent

@tool
def search_threat_intelligence(query: str) -> str:
    """Search for current threat intelligence about an IP, domain, CVE, or
    threat actor. Returns recent news, advisories, and analyst reports.

    Args:
        query: Target name plus context — e.g.
               "CVE-2024-1234 exploitation in the wild",
               "185.220.101.47 malicious activity 2026"
    """
    query = query.strip()[:500]  # truncate — prevents prompt injection via oversized input
    from tavily import TavilyClient
    results = TavilyClient(api_key=os.getenv("TAVILY_API_KEY")).search(
        query=query, search_depth="advanced", max_results=5, include_answer=True
    )
    findings = [{
        "title": r.get("title", ""),
        "url": r.get("url", ""),
        "content": r.get("content", "")[:500],
        "published_date": r.get("published_date", ""),
        "relevance_score": r.get("score", 0)
    } for r in results.get("results", [])]
    return json.dumps({
        "query": query,
        "answer_summary": results.get("answer", ""),
        "results": findings,
        "retrieved_at": datetime.now(UTC).isoformat()
    }, indent=2)


@tool
def lookup_cve(cve_id: str) -> str:
    """Look up a CVE from the NIST National Vulnerability Database.
    Returns CVSS score, severity, description, and dates.

    Args:
        cve_id: CVE identifier — e.g. CVE-2024-1234
    """
    cve_id = cve_id.upper().strip()
    # Format validation prevents SSRF via crafted IDs interpolated into the URL
    if not re.match(r'^CVE-\d{4}-\d{4,7}$', cve_id):
        return json.dumps({"error": f"Invalid CVE format: {cve_id}"})

    headers = {"User-Agent": "SecurityIntelAgent/1.0"}
    nvd_key = os.getenv("NVD_API_KEY", "").strip()
    if nvd_key:
        headers["apiKey"] = nvd_key

    for attempt in range(3):
        r = httpx.get(
            f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}",
            timeout=15, headers=headers
        )
        if r.status_code == 403:   # NVD returns 403 on rate-limit, not 429
            time.sleep(6); continue
        r.raise_for_status(); break

    vulns = r.json().get("vulnerabilities", [])
    if not vulns:
        return json.dumps({"error": f"{cve_id} not found in NVD"})

    vuln = vulns[0]["cve"]
    description = next(
        (d["value"] for d in vuln.get("descriptions", []) if d["lang"] == "en"),
        "No English description"
    )
    metrics = vuln.get("metrics", {})
    cvss_list = metrics.get("cvssMetricV31") or metrics.get("cvssMetricV30") or []
    cvss = cvss_list[0].get("cvssData", {}) if cvss_list else {}

    return json.dumps({
        "cve_id": cve_id,
        "description": description[:600],
        "cvss_score": cvss.get("baseScore", "N/A"),
        "cvss_severity": cvss.get("baseSeverity", "N/A"),
        "cvss_vector": cvss.get("vectorString", "N/A"),
        "published": vuln.get("published", ""),
    }, indent=2)


@tool
def analyze_logs(target: str, log_path: str = "") -> str:
    """Search security logs for events related to a target.

    Args:
        target: IP address, domain, hash, or username to search for.
        log_path: Optional JSONL log file. Defaults to LOG_FILE_PATH.
                  Do not pass arbitrary paths — path confinement is enforced.
    """
    resolved = Path(log_path).resolve() if log_path else _LOG_FILE_PATH
    if not str(resolved).startswith(str(_ALLOWED_LOG_DIR)):
        return json.dumps({"error": "Access to this path is not permitted."})

    if not resolved.exists():
        _create_sample_logs(str(resolved))

    matches = []
    with open(resolved) as f:
        for line in f:
            if line.strip():
                try:
                    entry = json.loads(line)
                    if target.lower() in json.dumps(entry).lower():
                        matches.append(entry)
                except json.JSONDecodeError:
                    continue

    if not matches:
        return json.dumps({"target": target, "matches": 0,
                           "summary": "No log entries found."})

    event_types = {}
    for m in matches:
        evt = m.get("event_type", "unknown")
        event_types[evt] = event_types.get(evt, 0) + 1

    timestamps = sorted(m.get("timestamp", "") for m in matches if m.get("timestamp"))
    return json.dumps({
        "target": target,
        "total_matches": len(matches),
        "event_type_breakdown": event_types,
        "first_seen": timestamps[0] if timestamps else "unknown",
        "last_seen": timestamps[-1] if timestamps else "unknown",
        "sample_entries": matches[:5],
    }, indent=2)


@tool
def extract_iocs(text: str) -> str:
    """Extract Indicators of Compromise from any text block.
    Pure regex — no network calls. Identifies IPs, domains, SHA256/MD5
    hashes, CVE IDs, and email addresses.

    Args:
        text: Any text — threat reports, log entries, web pages.
    """
    text = text[:50_000]  # cap at 50 KB — prevents memory exhaustion
    iocs = {
        "ips": list(set(re.findall(
            r'\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}'
            r'(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b', text))),
        "domains": list(set(re.findall(
            r'\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)'
            r'+(?:com|net|org|io|co|ru|cn|de|info|biz|gov|mil)\b', text))),
        "sha256_hashes": list(set(re.findall(r'\b[a-fA-F0-9]{64}\b', text))),
        "md5_hashes": list(set(re.findall(r'\b[a-fA-F0-9]{32}\b', text))),
        "cve_ids": list(set(re.findall(r'CVE-\d{4}-\d{4,7}', text, re.IGNORECASE))),
        "emails": list(set(re.findall(
            r'\b[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}\b', text))),
    }
    return json.dumps({"total_iocs_found": sum(len(v) for v in iocs.values()),
                       "iocs": iocs}, indent=2)

ALL_TOOLS = [search_threat_intelligence, lookup_cve, analyze_logs, extract_iocs]
```

### Step 3: Build the Supervisor

The supervisor uses **deterministic conditional logic, not an LLM**. This is a deliberate choice: LLM-based routing adds latency, token cost, and non-determinism to what is purely a control-flow decision. The LLM's reasoning is reserved for tasks that actually require it.

```python
# supervisor.py
from typing import Literal
from langgraph.types import Command
from state import SecurityIntelState

def supervisor_node(state: SecurityIntelState) -> Command[Literal[
    "threat_intel_node", "cve_lookup_node", "log_analysis_node",
    "report_node", "__end__"
]]:
    if state.get("report"):
        return Command(goto="__end__")

    completed = set(state.get("completed_phases", []))
    target_type = state.get("target_type", "unknown")

    # Phase 1: threat intel always runs first
    if "threat_intel" not in completed:
        return Command(goto="threat_intel_node", update={"current_phase": "threat_intel"})

    # Phase 2: CVE lookup if the target is a CVE or if intel mentioned CVEs
    if "cve_lookup" not in completed and (
        target_type == "cve" or
        any("CVE-" in str(r) for r in state.get("threat_intel", []))
    ):
        return Command(goto="cve_lookup_node", update={"current_phase": "cve_lookup"})

    # Phase 3: log analysis for IP and domain targets
    if "log_analysis" not in completed and target_type in ("ip", "domain"):
        return Command(goto="log_analysis_node", update={"current_phase": "log_analysis"})

    return Command(goto="report_node", update={"current_phase": "report"})
```

### Step 4: Build the Analyst Nodes

Each node runs a focused agentic loop: invoke the LLM, execute tool calls, accumulate results, repeat up to `_MAX_TURNS`. The shared `_run_node` function handles this pattern.

```python
# nodes.py (key sections)
_MAX_TURNS = 4  # any legitimate task with these tools completes in ≤3 turns;
                # exceeding 4 indicates a runaway loop or hallucination

def _run_node(state, tools, prompt, phase_name, result_field):
    llm_with_tools = llm.bind_tools(tools)
    messages = list(state["messages"]) + [HumanMessage(content=prompt)]
    results = []

    for _ in range(_MAX_TURNS):
        response = llm_with_tools.invoke(messages)
        messages.append(response)
        if not response.tool_calls:
            break
        for tc in response.tool_calls:
            tool_fn = next((t for t in tools if t.name == tc["name"]), None)
            result = tool_fn.invoke(tc["args"]) if tool_fn else \
                     json.dumps({"error": f"Unknown tool: {tc['name']}"})
            results.append(json.loads(result))
            messages.append(ToolMessage(content=result, tool_call_id=tc["id"]))

    completed = list(state.get("completed_phases", []))
    return {"messages": messages, result_field: results,
            "completed_phases": completed + [phase_name]}
```

The IOC extraction instruction is tailored to what each target type actually produces in search results:

```python
def threat_intel_node(state):
    target_type = state.get("target_type", "unknown")

    if target_type in ("ip", "domain"):
        ioc_instruction = (
            "Then call extract_iocs on the result content to pull out "
            "any embedded IPs, domains, or file hashes."
        )
    elif target_type == "cve":
        ioc_instruction = (
            "Then call extract_iocs if you see CVE IDs, PoC artifact "
            "hashes, or related indicators."
        )
    else:  # threat_actor — narrative blog posts; structured IOCs are rare
        ioc_instruction = (
            "Only call extract_iocs if results contain explicit IPs, "
            "file hashes, or C2 domains. Skip it for narrative reports."
        )
    # ...
```

This matters more than it looks. Without the `threat_actor` guard, the model always calls `extract_iocs` on blog prose and correctly finds nothing — burning a full LLM turn (30–60 seconds at 27B) to confirm that a narrative report about LockBit does not embed IP addresses. The target-type-aware instruction eliminates that wasted turn.

The report node synthesizes everything with a conditional template — sections for phases that did not run are simply omitted rather than filled with "no data available" boilerplate:

```python
def _build_report_prompt(completed: list[str]) -> str:
    """Only include report sections for phases that actually ran."""
    cve_section = _CVE_SECTION if "cve_lookup" in completed else ""
    log_section = _LOG_SECTION if "log_analysis" in completed else ""
    return _REPORT_SYSTEM_PROMPT_BASE.format(
        cve_section=cve_section,
        log_section=log_section,
    ).strip()
```

After the report is generated, `extract_iocs` runs over the report body (not the References section — that would extract citation source URLs as false-positive IOCs) to capture any structured indicators the model derived during synthesis:

```python
# Strip references section before IOC extraction
report_body = re.split(r'###\s+References', report_text, maxsplit=1)[0]
report_iocs = json.loads(extract_iocs.invoke({"text": report_body}))
```

### Step 5: Wire the Graph

```python
# graph.py
import sqlite3
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver

def build_graph(db_path="sec_agent.db"):
    builder = StateGraph(SecurityIntelState)

    builder.add_node("supervisor", supervisor_node)
    builder.add_node("threat_intel_node", threat_intel_node)
    builder.add_node("cve_lookup_node", cve_lookup_node)
    builder.add_node("log_analysis_node", log_analysis_node)
    builder.add_node("report_node", report_node)

    builder.add_edge(START, "supervisor")
    builder.add_edge("threat_intel_node", "supervisor")
    builder.add_edge("cve_lookup_node", "supervisor")
    builder.add_edge("log_analysis_node", "supervisor")
    builder.add_edge("report_node", END)

    conn = sqlite3.connect(db_path, check_same_thread=False)
    return builder.compile(checkpointer=SqliteSaver(conn))

graph = build_graph()
```

### Step 6: The Entry Point

Target type detection handles the classification and rejects inputs that would waste API quota with no useful result:

```python
# main.py (key section)
def detect_target_type(target: str) -> str:
    t = target.strip()
    if re.match(r'^CVE-\d{4}-\d{4,7}$', t, re.IGNORECASE): return "cve"
    if re.match(r'^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$', t):
        # Reject private/reserved ranges — external APIs return nothing useful
        if re.match(r'^(127\.|10\.|172\.(1[6-9]|2\d|3[01])\.|192\.168\.|169\.254\.)', t):
            raise ValueError(f"'{t}' is a private/reserved address.")
        return "ip"
    if re.match(r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$', t):
        return "domain"
    return "threat_actor"
```

---

## Part 5 — Running the Agent: Real Output

### CVE Analysis

```bash
python3 main.py -v CVE-2025-68664
```

```
[*] Target:     CVE-2025-68664
[*] Type:       cve
[*] Plan:       threat_intel → cve_lookup → report
[*] Started:    2026-04-04T19:24:17Z

  [prompt] Search for current threat intelligence about: CVE-2025-68664...
  [turn 1] → search_threat_intelligence(query='CVE-2025-68664 exploitation in the wild')
       ↳ CVE-2025-68664 LangChain Serialization Flaw
          https://orca.security/resources/blog/cve-2025-68664-langchain-serialization-flaw/
       ↳ What It Means for Your Business - IntegSec
          https://integsec.com/blog/cve-2025-68664-langchain-serialization-flaw
       ↳ Nuclear Option: Deep Dive into LangChain Serialization Injection
          https://www.penligent.ai/hackinglabs/nuclear-option-deep-dive...
  [turn 2] no tool calls — node finished
  [✓] threat_intel          42.3s
  [turn 1] → lookup_cve(cve_id='CVE-2025-68664')
       ↳ CVE-2025-68664 CVSS=9.3 CRITICAL
  [✓] cve_lookup            18.1s
  [✓] report                31.7s
======================================================================
## Threat Assessment Report

**Target:** CVE-2025-68664
**Severity:** CRITICAL

### Executive Summary
CVE-2025-68664 is a critical deserialization vulnerability (CVSS 9.3) in
langchain-core prior to 0.3.29. Public PoC details are disclosed, enabling
attackers to extract API keys, environment secrets, and execute arbitrary
code via crafted JSON payloads containing the reserved 'lc' key...

### CVE Analysis
| CVE ID | CVSS | Severity | Vector |
|---|---|---|---|
| CVE-2025-68664 | 9.3 | CRITICAL | AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N |

### Indicators of Compromise
**CVE IDs:** CVE-2025-68664
**Behavioral Indicators:**
- JSON payload: `{"lc": 1, "type": "constructor", "id": ["subprocess", ...]}`
- Unexpected subprocess calls from LangChain application context

### Recommendations
1. Upgrade langchain-core to ≥ 0.3.29 immediately
2. Rotate all API keys exposed to LangChain applications
3. Reject JSON structures containing the 'lc' key at application boundaries
4. Configure IDS rules to detect outbound connections matching PoC patterns
5. Run SCA across all repositories for vulnerable LangChain versions

[*] Severity:   CRITICAL  |  IOCs found: 1  |  Total time: 92.1s
======================================================================
```

### Threat Actor Analysis

```bash
python3 main.py -v "LockBit ransomware"
```

```
[*] Target:     LockBit ransomware
[*] Type:       threat_actor
[*] Plan:       threat_intel → report

  [turn 1] → search_threat_intelligence(query='LockBit ransomware TTPs 2026')
       ↳ LockBit Ransomware: From Origins to LockBit 4.0 (Neo) in 2026
          https://www.xactcybersecurity.com/lockbit-ransomware-attack-guide/
       ↳ The State Of Ransomware 2026 - BlackFog
          https://www.blackfog.com/the-state-of-ransomware-2026/
       ↳ LockBit Ransomware: Attack Methods - CybelAngel
          https://cybelangel.com/blog/lockbit-cybercriminal-guide/
  [turn 2] no tool calls — node finished   ← skipped extract_iocs (narrative sources)
  [✓] threat_intel          73.5s
  [✓] report               111.4s

**Target:** LockBit ransomware  |  **Severity:** HIGH

### Threat Intelligence Findings
- LockBit 5.0 released February 2026, now targeting Windows, Linux, ESXi
- LockBit 4.0 infrastructure disrupted May 2025 (dark web domains hijacked)
- FBI issued $10M reward for administrator Dmitry Khoroshev ("LockBitSupp")
- Primary access: phishing and RDP exploitation

### Indicators of Compromise
*No structured IOCs in current intelligence feeds.*
**Behavioral Indicators:**
- Rapid file encryption across ESXi hypervisor and Linux endpoints
- Double/triple extortion (encryption + leak threats + DDoS threats)
- Dark web leak site communications

[*] Severity:   HIGH  |  IOCs found: 0  |  Total time: 196s
```

"IOCs found: 0" for a threat actor query is **correct**, not a failure. Narrative blog posts about LockBit do not embed IP addresses or file hashes. The agent correctly skips the IOC extraction step (saving one full LLM turn) and honestly reports that structured IOCs were not available in the current intelligence feed. For IP targets, the same pipeline finds embedded indicators in technical advisories.

---

## Part 6 — MCP: Turning Your Tools Into a Shared Protocol

Once your tools are working as native `@tool` functions, migrating to MCP is a small step with significant architectural implications.

```python
# mcp_server.py
from mcp.server.fastmcp import FastMCP
from tools import search_threat_intelligence, lookup_cve, analyze_logs, extract_iocs

mcp = FastMCP("security-intel-tools")

@mcp.tool()
def search_threat_intel(query: str) -> str:
    """Search for current threat intelligence about an IP, domain, CVE, or
    threat actor using live web search."""
    return search_threat_intelligence.invoke({"query": query})

@mcp.tool()
def cve_lookup(cve_id: str) -> str:
    """Look up CVE details from NIST NVD. Returns CVSS score, severity,
    description, and affected software."""
    return lookup_cve.invoke({"cve_id": cve_id})

@mcp.tool()
def log_search(target: str) -> str:
    """Search security logs for events related to a target IP, domain, or hash.
    Uses the configured log file; does not accept arbitrary paths."""
    return analyze_logs.invoke({"target": target})  # log_path omitted intentionally

@mcp.tool()
def ioc_extract(text: str) -> str:
    """Extract Indicators of Compromise from any text block."""
    return extract_iocs.invoke({"text": text})

if __name__ == "__main__":
    mcp.run()  # stdio transport — correct for local/Claude Desktop use
```

Note: `log_search` does not expose the `log_path` parameter. Path confinement is enforced inside `analyze_logs` via `_ALLOWED_LOG_DIR`. An MCP client or a compromised co-installed MCP server cannot direct the tool to read arbitrary files. This is the principle of least exposure applied at the MCP boundary.

Connect to Claude Desktop by adding to `~/.claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "security-intel-tools": {
      "command": "python3",
      "args": ["/absolute/path/to/sec-intel-agent/mcp_server.py"]
    }
  }
}
```

---

## Part 7 — Observability

With `LANGCHAIN_TRACING_V2=true` and `LANGCHAIN_API_KEY` set, every run sends a full trace to [smith.langchain.com](https://smith.langchain.com) automatically — every LLM call, every tool invocation with arguments and results, every node execution, every routing decision.

The `-v` verbose flag provides local observability without LangSmith:

```bash
python3 main.py -v CVE-2025-68664
# Shows every tool call, argument, and truncated result preview in real time
```

Use verbose mode to verify claims against sources before acting on them. If the report says a CVE has a 9.3 CVSS score, you saw the NVD API call in the trace and can confirm it came from `lookup_cve(cve_id='CVE-2025-68664')` → `CVSS=9.3 CRITICAL`.

**LangSmith note:** Traces include full tool arguments. If `analyze_logs` processes logs with PII (usernames, internal IPs), that data appears in LangSmith. Review project access controls before enabling on production data.

---

## Part 8 — Lessons From Building It

These are things the code in every tutorial glosses over. They are things you will hit.

**Not all quantized models support tool calls.** Ollama compiles a specific chat template into each model variant. Some quantized GGUF files do not include the tool-call template. `qwen3.5:9b-q4_K_M` and `qwen3.5:35b-a3b-q4_K_M` both fail with "does not support tools." `qwen3.5:27b` and `qwen2.5:14b` work. Test with a minimal tool call before running the full agent.

**Qwen3.5 thinking mode will silently double your runtime.** The extended chain-of-thought mode is on by default. It adds 30–90 seconds of silent reasoning before every response — invisible in the output, invisible in the logs unless you time it. The fix is `extra_body={"think": False}` in the Ollama request. Put it in the wrong place (`model_kwargs` instead of `extra_body` directly) and you get `TypeError: Completions.create() got an unexpected keyword argument 'think'`. The key goes through `extra_body` because it is an Ollama-specific field the OpenAI SDK does not know about.

**IOC extraction on the full report produces false positives.** If you run the regex extractor over the entire report including the References section, the source citation URLs get extracted as "domains" — you end up with `xactcybersecurity.com` and `blackfog.com` in your IOC list. Strip the References section before running extraction: `re.split(r'###\s+References', report_text)[0]`.

**Narrative search results for threat actors contain no structured IOCs — and that is correct.** The first time the agent returns "IOCs found: 0" for a LockBit query, it looks like a failure. It is not. Blog posts from threat intel vendors do not embed IP addresses or file hashes. The correct response is to skip the extraction call (wasted LLM turn), note the absence in the IOC section, and derive behavioral indicators from the narrative instead. The report saying "no structured IOCs; behavioral indicators: rapid ESXi encryption, double extortion" is more honest and more useful than hallucinating IPs.

**The `log_path` path confinement needs explicit verification on WSL2.** `Path.resolve()` behavior on Windows paths accessed through WSL2 can be unexpected. Test it explicitly: `python3 -c "from tools import _ALLOWED_LOG_DIR; print(_ALLOWED_LOG_DIR)"`. If the printed path is not what you expect, the path confinement check may not be doing what you think.

**The `datetime.utcnow()` deprecation is a warning, not an error — but fix it.** Python 3.12 logs deprecation warnings for `datetime.utcnow()` every time it is called. In an agent that calls it multiple times per run, this creates visual noise that can mask real warnings. Replace with `datetime.now(UTC)` from `from datetime import datetime, UTC`.

---

## Part 9 — Extending the Agent

In order of impact:

**Shodan integration** — `shodan_lookup(ip: str)` via the Shodan API (free tier: 100 queries/day). Returns open ports, running services, geolocation. Add to `threat_intel_node`'s tool list; route there from the supervisor when the target is an IP.

**VirusTotal hash lookup** — `virustotal_lookup(hash: str)` against 70+ AV engines. When `analyze_logs` returns SHA256 hashes, the supervisor can route to a hash analysis node automatically.

**Real SIEM integration** — replace the JSONL reader in `analyze_logs` with an Elasticsearch or Splunk query. The tool interface does not change; only the data source behind it does.

**Alert tools** — `send_slack_alert(message, severity)` or `create_jira_ticket(summary, description)`. Route to an alert node from the supervisor when `severity == "critical"`.

**Cross-session memory** — the SQLite checkpointer saves state per `thread_id`. For semantic recall across sessions ("what did we find about this IP last week"), add ChromaDB as a vector memory store alongside the SQLite checkpointer.

**Per-claim source attribution** — change the report system prompt to require inline citations per bullet point: `"LockBit 5.0 was released in February 2026 [Broadcom]"`. This improves verifiability and makes hallucination detection systematic rather than requiring the analyst to cross-check each claim manually.

---

## Part 10 — What You Actually Built

Let us be precise.

It **does**: autonomously decide which analysis tools to run for a given target, retrieve current threat intelligence from live sources with visible provenance, query the real NIST NVD API, search through local log data for matching indicators, extract structured IOCs from technical content (and correctly report their absence from narrative content), route between analysis phases without human intervention, produce a structured report in under four minutes on local hardware, and persist all state for session resumption.

It **does not**: replace a human analyst. It has no understanding of your organization's specific risk posture, no knowledge of your architecture beyond what you put in the logs, and no judgment about which finding matters most in your context this week. It is a first-pass triage tool — one that raises the quality floor for the first phase of an investigation and hands the analyst a structured starting point rather than a blank page.

The production version — the one that earns trust in a real security operation — requires one additional layer this article has not covered: **security controls on the agent itself.** The same properties that make this agent useful (autonomous tool use, external data ingestion, MCP-based tool sharing) are the properties that make it attackable. A single poisoned CVE description, a malicious entry in your log file, or a compromised MCP package can redirect the agent's actions in ways that are invisible in the output.

That is Part 2: [The Security Intelligence Agent You Just Built Is an Attack Surface](https://aminrj.com/2026/03/mcp-tool-poisoning-osint-agent) — three working exploits against this exact codebase, measured success rates, and the defenses that stop them.

---

## References

1. **LangGraph documentation** — [langchain-ai.github.io/langgraph](https://langchain-ai.github.io/langgraph)
2. **LangGraph 1.0 release notes** (October 2025) — [github.com/langchain-ai/langgraph/releases](https://github.com/langchain-ai/langgraph/releases)
3. **LangChain MCP adapter** — [github.com/langchain-ai/langchain-mcp-adapters](https://github.com/langchain-ai/langchain-mcp-adapters)
4. **Model Context Protocol specification** — [spec.modelcontextprotocol.io](https://spec.modelcontextprotocol.io) — read the Security Considerations section before deploying
5. **FastMCP** — [github.com/jlowin/fastmcp](https://github.com/jlowin/fastmcp)
6. **Ollama** — [ollama.com](https://ollama.com) — local model serving with OpenAI-compatible API
7. **Tavily Search API** — [docs.tavily.com](https://docs.tavily.com) — free tier: 1,000 searches/month
8. **NIST NVD API v2.0** — [nvd.nist.gov/developers/vulnerabilities](https://nvd.nist.gov/developers/vulnerabilities)
9. **LangSmith** — [smith.langchain.com](https://smith.langchain.com) — free tier sufficient for development
10. **CVE-2025-67644** — LangGraph SQLite Checkpoint SQL Injection. Fixed in `langgraph-checkpoint-sqlite` ≥ 3.0.1
11. **CVE-2025-68664 / LangGrinch** — LangChain Core Serialization Injection (CVSS 9.3). Fixed in `langchain-core` ≥ 0.3.29
12. **OWASP Top 10 for Agentic AI Applications 2026** — [genai.owasp.org](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)

---

*Complete code: [ai-cybersecurity-agent repository](https://github.com/aminrj-labs/ai-cybersecurity-agent)*

*Part 2 — [The Security Intelligence Agent You Just Built Is an Attack Surface](https://aminrj.com/2026/03/mcp-tool-poisoning-osint-agent)*

