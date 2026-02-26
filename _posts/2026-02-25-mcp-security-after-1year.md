---
title: "MCP's First Year: What 30 CVEs and 500 Server Scans Tell Us About AI's Fastest-Growing Attack Surface"
date: 2026-02-25
uuid: 202602250000
status: draft
content-type: article
target-audience: advanced
categories: [AI Security, LLM]
tags:
  [
    AI Security,
    LLM,
    MCP,
    CVE,
    Attack Surface,
    Tool Poisoning,
    Agentic AI,
    Prompt Injection,
    Supply Chain,
  ]
image:
  path: /assets/media/ai-security/mcp-security-after-one-year.png
description: A practitioner's assessment of MCP security after fifteen months — 30 CVEs, 500 server scans, three architectural attack patterns, and what organizations deploying AI agents need to prioritize now.
---

I've been working in production security for over a decade, across
critical infrastructure, finance, and cloud-native systems.

In that time, I've seen plenty of new technologies ship without adequate
security consideration. But the speed and scale of what's happening with MCP is
something I haven't seen before.

In January 2026, [security researchers disclosed](https://www.endorlabs.com/learn/classic-vulnerabilities-meet-ai-infrastructure-why-mcp-needs-appsec) three vulnerabilities in
Anthropic's Git MCP server, the reference implementation that developers
across the ecosystem had been copying into their own projects.
The bugs were path traversal and argument injection.

Not novel AI attacks. Not sophisticated prompt engineering. The kind of
vulnerabilities that have appeared in the OWASP Top 10 for over a decade.

The developers who copied the official code had been copying the vulnerability
along with it.

That disclosure marked a turning point.
Not because the bugs were unusual, but because of what followed: thirty CVEs in
sixty days, a wave of independent security audits, and a growing body of
evidence that the Model Context Protocol, the USB-C of the agentic AI era, had
been deployed at scale without the security foundations that enterprise software
demands.

This article is a practitioner's assessment of where MCP security stands as of
February 2026, what the data reveals, and what organizations deploying AI agents
need to prioritize now.

---

## A Brief Orientation

For readers encountering MCP for the first time: the Model Context Protocol is
an open standard introduced by Anthropic in November 2024 that defines how AI
assistants connect to external tools and data sources.

It has been adopted by Microsoft, Google, Amazon, OpenAI, and dozens of
development platforms including Cursor, VS Code, Claude Desktop, and GitHub
Copilot.

When you connect an MCP server to an AI assistant, you give the assistant the
ability to call functions, read files, query databases, post messages, execute
code.

MCP servers are the bridge between what the AI _knows_ and what it can _do_.

The architecture looks like this:
![MCP Architecture Overview](/assets/media/ai-security/MCP-security-after-one-year/mcp-architecture-overview.png)
Diagram 1: MCP Architecture Overview

The adoption curve has been steep.
Over ten thousand MCP server repositories were created on GitHub in under a year.

The official registry lists over 518 servers as of this month (Feb. 2026),
growing by dozens each week.

[Cisco's State of AI Security 2026 report](https://blogs.cisco.com/ai/cisco-state-of-ai-security-2026-report) found that 83% of organizations plan to
deploy AI agents into their business functions. Only 29% feel their security
posture is ready for it.

That gap between deployment velocity and security readiness is the story of
MCP's first year.

---

## What the Scans Revealed

An autonomous [security researcher known as Kai](https://dev.to/kai_security_ai/i-scanned-every-server-in-the-official-mcp-registry-heres-what-i-found-4p4m) has been continuously scanning
every server in the official MCP registry since late 2025.
The dataset now covers 535 production endpoints, verified through active probing
rather than passive enumeration.

The findings are sobering.

**38% of servers have no authentication at the MCP protocol level.**
That translates to over 200 servers where any AI agent, or any HTTP client, can
enumerate every available tool and, in many cases, execute them directly.

Among those unprotected servers are CI/CD pipeline triggers, social media
management tools, database query interfaces, and cloud infrastructure controls.

What strikes me about these numbers is not the percentage (authentication
gaps are common in early-stage ecosystems).
It's that the registry has no security requirements for listing.
Any server can appear in the official directory regardless of its security
posture.

The numbers hold up across multiple independent assessments.
Trend Micro identified 492 MCP servers exposed on the public internet with no
client authentication or traffic encryption, collectively providing access to
1,402 tools.

Over 90% offered direct read access to their underlying data sources. 74% were
hosted on major cloud providers.

One particularly telling data point from the Kai dataset: a honeypot server
configured with a tool called `get_aws_credentials(role="admin")` received its
first call within 48 hours of deployment.

No reconnaissance phase. No credential stuffing. An AI agent discovered the tool
and called it 🤯.

![Authentication Gap Across the Registry](/assets/media/ai-security/MCP-security-after-one-year/mcp-authentication.png)
Diagram 2: Authentication Gap Across the Registry

## The CVE Landscape: Old Bugs in New Infrastructure

Between January and February 2026, [security researchers documented](https://dev.to/kai_security_ai/30-cves-later-how-mcps-attack-surface-expanded-into-three-distinct-layers-ihp) 30 CVEs
against MCP servers and related infrastructure. The breakdown tells a story
about the ecosystem's maturity:

- **13 CVEs (43%)** follow the same pattern:
  user-controlled input piped directly into `exec()` or shell commands without
  sanitization. Classical command injection.
  The fix in every case is the same:
  replace `exec()` with `execFile()` and pass arguments as an array.
  The failures are not the same, these span OSINT tools, game engine integrations,
  mobile OS bridges, and data visualization servers.

- **6 CVEs (20%)** target the tooling and infrastructure layer, the inspectors, scanners, and host applications that developers use to _build_ MCP servers.
  This is the layer most organizations don't think to protect.

- **4 CVEs (13%)** involve authentication bypass on critical endpoints.

- **3 CVEs (10%)** affect Anthropic's own reference implementations.

- **2 CVEs (7%)** introduce entirely new vulnerability classes:
  `eval()` injection through data format specifications, and environment variable
  injection that activates on the next server restart rather than immediately.

Two data points stand out:

First, CVE-2026-0755 in a Gemini MCP tool was discovered by Trend Micro's Zero
Day Initiative in July 2025, seven months before publication.
ZDI followed their standard coordinated disclosure process.

The maintainer never responded.

The advisory was eventually published as a zero-day with no patch available.
This is the responsible disclosure framework failing against the realities of an
ecosystem where most servers are maintained by individual developers with no
security process.

Second, the [Endor Labs analysis](https://www.endorlabs.com/learn/classic-vulnerabilities-meet-ai-infrastructure-why-mcp-needs-appsec) of 2,614 MCP implementations found that 82% use
file system operations prone to path traversal, 67% use sensitive APIs related
to code injection, and 34% use APIs susceptible to command injection.

These are not servers with active CVEs.
These are servers with code patterns that make CVEs a matter of time.

The pattern here should be familiar to anyone who's done application security
work.
These aren't exotic AI-native attacks.
They're the same CWE-77 and CWE-22 entries we've been remediating for a decade,
reappearing in infrastructure that's being treated as if it's somehow exempt
from the usual rules.

---

## Three Attack Patterns That Define the Threat Model

The CVE data captures implementation bugs that are important, fixable, and familiar.
But the more significant security challenge in MCP is architectural.

Three attack patterns exploit the way the protocol itself works, not just how
individual servers are coded.

### Pattern 1: Tool Description Injection

Every MCP server exposes its tools to the AI assistant along with a description of what each tool does.
These descriptions are processed by the language model as part of its context.
They are, functionally, instructions.

A malicious MCP server can embed hidden directives inside a tool description.
The user sees "Adds two numbers." The AI sees that, plus a block of additional
instructions telling it to read local configuration files and pass their
contents as a parameter.

The user never sees the hidden text. The AI follows it.

![Authentication Gap Across the Registry](/assets/media/ai-security/MCP-security-after-one-year/mcp-injection-flow.png)
Diagram 3: Tool Description Injection Flow

What makes this different from a standard prompt injection is persistence.
A prompt injection in user input fires once.
A poisoned tool description fires on _every invocation_ of that tool, across every session, until the server is removed.
It is, in effect, a supply-chain attack delivered through metadata.

I find the persistence aspect of this the most operationally concerning.
Organizations that rotate credentials, patch regularly, and monitor for
indicators of compromise have no detection mechanism for a malicious tool
description that's been present since day one.

It doesn't trigger alerts.
It doesn't generate anomalous logs.
It just works, quietly, every time.

### Pattern 2: Cross-Server Poisoning

When multiple MCP servers are connected to the same AI agent, all tools from all
servers are presented in a single flat namespace.

There is no isolation between servers.
There is no concept of per-server permissions.

This means a malicious server can instruct the AI to call tools on any other
connected server.

A poisoned "weather checker" server can direct the AI to read messages from a
legitimate Slack MCP server, query a database through a legitimate PostgreSQL
MCP server, and forward the results to an attacker-controlled endpoint, all
through tool description injection that the user never sees.

In MCP, the risk surface of your entire tool chain is the product of all
connected servers, not the sum.

This pattern was demonstrated in Invariant Labs' [original April 2025 research](https://github.com/invariantlabs-ai/mcp-injection-experiments)
using a WhatsApp MCP server.

[Praetorian's MCPHammer framework](https://github.com/praetorian-inc/MCPHammer),
expanded the demonstration to include Slack integration chaining, where commands
encoded in Slack messages are decoded and executed by a co-installed malicious
local
server.

The AI assistant acts as the unwitting intermediary, passing data between
servers because it was instructed to.

### Pattern 3: Tool Description Mutation (The Rug Pull)

An MCP server presents a benign interface on initial installation.
A code review at install time finds nothing suspicious.
On subsequent loads, the server silently changes its tool descriptions to
include malicious instructions.

This exploits a gap in how MCP clients handle tool metadata.
Clients typically cache tool names, and when a previously-trusted server returns
updated descriptions, the cache trusts the update without alerting the user.

The MCPHammer framework demonstrates this at scale: a management server
can push updated injection text to multiple deployed MCPHammer instances in real
time, silently converting benign servers into malicious ones.

No current MCP client implementation hashes tool descriptions on first load and
alerts on mutation.
The detection mechanism for this attack class does not exist in the deployed
ecosystem.

---

## The Infrastructure Layer Is Not Immune

Perhaps the most concerning finding from the February 2026 CVE wave is that the
attacks have moved beyond individual servers into the foundational
infrastructure.

**The SDK itself leaks data.** `CVE-2026-25536` affects the official MCP
TypeScript SDK (versions up to 1.25.3). When a single `McpServer` instance
handles multiple client connections, a common configuration in stateless
deployments, JSON-RPC message ID collisions cause responses to route to the
\*wrong client.

Client A receives Client B's data. No attack is required. No authentication
bypass is needed. The vulnerability is in how the SDK manages concurrent
connections. Any multi-tenant MCP deployment running an affected version is
potentially leaking data between clients right now.

The SDK finding is the one that changed my thinking about MCP risk
assessment. You can audit every server, review every tool description,
and enforce every access control, and still leak data between clients
because of a concurrency bug in the library everything is built on.

This is infrastructure risk, not application risk, and most organizations are
not assessing it at that layer.

**The development tools are attack surfaces.** `CVE-2026-23744` affects MCPJam
Inspector, a platform for building and testing MCP servers. Versions through
1.4.2 expose an unauthenticated HTTP endpoint that can install arbitrary MCP
servers, and the service listens on `0.0.0.0` by default.

A crafted request from anywhere on the network installs a server and executes
code. These tools run in developer environments with access to source code,
credentials, and build pipelines.

**The security scanners have their own vulnerabilities.** `CVE-2025-66401` affects
MCP Watch, a scanner designed to audit MCP servers for security issues.
It contains a command injection in its `cloneRepo()` method. The tool
organizations reach for to assess MCP security can itself be exploited.

![Authentication Gap Across the Registry](/assets/media/ai-security/MCP-security-after-one-year/MCP-three-attack-layers.png)
Diagram 4: MCP's Three Attack Layers

---

## What Organizations Should Prioritize

The good news is that most of the controls needed are not novel. MCP's security
challenges are largely the result of deploying a new protocol without applying
the practices the industry already knows how to implement.

Five measures deserve immediate attention:

**1. Inventory every MCP server in your environment.** This sounds basic because it is.
Every developer running Claude Desktop, Cursor, or a VS Code extension with MCP
support likely has servers installed. Most organizations have no visibility
into what those servers are, what tools they expose, or what permissions they
hold. You cannot secure what you have not inventoried.

**2. Scan tool descriptions before loading any server.** Invariant Labs released `mcp-scan`
alongside their original research. It detects suspicious patterns in tool
description metadata before a server is connected to an agent. This single step
addresses the entire tool poisoning attack class at install time.

**3. Enforce human approval for sensitive operations.** The MCP specification states that
human confirmation SHOULD be required before tools execute file reads, network
requests, or data mutations. Most client implementations skip this. Enabling it
introduces friction. That friction is the control.

**4. Hash tool descriptions at first load and alert on any change.** If a tool's description
mutates between sessions, that is either a rug pull or an unauthorized update.
Either way, it warrants investigation. This is a straightforward integrity
check that no major MCP client currently implements by default^w

**5. Restrict network egress from MCP server processes.** If a compromised server cannot
make outbound HTTP requests, the exfiltration step in every attack chain
documented above fails silently. Run MCP servers in sandboxed environments with
no outbound internet access beyond their intended scope.

---

## Looking Forward

The MCP specification itself has been evolving.
The June 2025 update introduced the StreamableHTTP transport and improvements to
the authorization model.
The draft security best practices document addresses confused deputy attacks,
scope management, and sandboxing recommendations. These are positive steps.

But specification improvements only matter if the deployed ecosystem adopts them.
The 10,000+ MCP servers already in production were not built against these
updated guidelines.
The 38% without authentication were not built with any security guidelines at all.
Closing the gap between what the spec recommends and what the ecosystem does is
now the central challenge.

For security teams, the practical question is not whether MCP introduces risk,
it clearly does.
The question is whether your organization can deploy AI agents with the
visibility, controls, and response capability to manage that risk at the speed
the technology is moving.

Thirty CVEs in sixty days suggests the answer, for most organizations, is not
yet.

---

_This analysis draws on published research from Endor Labs, Trend Micro,
Praetorian, Invariant Labs, Cisco, and the ongoing MCP registry scanning
project. All sources are linked in-text or available through the organizations
referenced._

_For weekly threat intelligence on agentic AI security, subscribe to [AI Security Intelligence](https://aisecurityintelligence.beehiiv.com)._
