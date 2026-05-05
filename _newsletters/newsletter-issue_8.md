[AI Sec Intel] #8 — Closed Agent Harness = threat model blind spot
I built a 3-agent coding system this week. First control I added: repo isolation on the write-capable agent.

Hi 👋

This week I built the agent-forge-bootstrap: three agents in sequence: Architect plans, Executor writes code, Reviewer validates and calls pass or fail.

All local: OpenCode + Ollama (qwen3-coder:30b), Discord bot as the human interface.

In one python file (163 lines) that illustrate the multi-agent
orchestration workflow to understand how most recent frameworks function under
the hood.

The engineering problem that took longest to solve: state handoff between agents.
Stateless API calls kept dropping context mid-session. Persistent server communication
via --attach fixed it by keeping the OpenCode process alive across agent turns.

First security control I added: repo isolation on the Executor.
Without it, the agent runs with the full filesystem permissions of its process user.
Give that agent write access to anywhere it wants and you don't have an AI system.
You have an unauthenticated write endpoint.
Full write-up coming shortly.

THIS WEEK IN AI SECURITY
Docker authorization bypass resurfaces — CVSS 8.8 — despite a prior patch
A Docker Engine authorization plugin bypass came back this week. The original patch was incomplete. Affected: Docker Engine prior to 29.3.1, Docker Desktop prior to
4.66.1. If you can reach the Docker API, you can bypass auth plugins entirely and get root-level access to the container host.

Action: Agent containers that mount the Docker socket — common in local dev and CI setups — turn this bypass into a host escape. Update Docker Engine (29.3.1+) and Docker Desktop (4.66.1+), then find exposed containers: docker ps --format ' ' | grep docker.sock
CSO Online →

"Your agent harness, your memory": what closed agent frameworks actually cost you
LangChain published a direct argument for open harnesses: if the framework manages your agent's memory, you've lost visibility into what it remembers, what can be
injected into that memory, and how to force a purge. That matters more than vendor lock-in. OWASP ASI01 and ASI05 both assume you can inspect the memory layer. Closed
harnesses make that assumption wrong.

The deeper issue: This applies to any managed memory service, not just closed competitors. Before deploying any agent with persistent memory: know where it's stored, what can be injected, and how to force a purge. If you can't answer all three, you don't control the context window.
LangChain Blog →

Microsoft: the agentic SOC needs a different security model
Microsoft's security team laid out why current SOC playbooks don't transfer to agent environments. The problem: agents triage at machine speed with no escalation
loop, and a compromised agent's blast radius is larger than a compromised analyst's workstation.
Agents have authorized access to query, modify, and remediate production systems.
No incident driving this, just a framework argument.
But the gaps it names are worth reading before you put any agent into a security operations workflow.

Worth noting: Write out the blast radius of any SOC agent before you deploy it. What can it query, modify, or close without asking a human? If that list doesn't exist in writing, the agent has more access than your threat model covers.
Microsoft Security Blog →

Marimo RCE — update from last issue
Confirmed under active exploitation for credential theft. Patch now if you haven't. BleepingComputer →

TOOLING WORTH KNOWING
Google Chrome Device Bound Session Credentials (DBSC) — Chrome now binds session cookies to the device. Steal the cookie, replay it somewhere else, it fails. Relevant
if any AI application relies on browser-based session management. Verify your users are on a current Chrome version and test that cookie-binding doesn't break your
session flows before rolling it out broadly. BleepingComputer →

EU AI Act compliance layer for Claude Managed Agents (open source) — Compliance integration for Claude-based agents with MCP. Worth reading as a reference
implementation if you're shipping agents under EU AI Act obligations. Just audit what it actually covers before telling anyone you're compliant. docs.geiant.com →

ONE THING TO CHECK THIS WEEK
Look at the write-capable agent in any multi-agent system you run. What filesystem paths can it write to? What environment variables does it inherit. Meaning what
credentials can it read? Can it make outbound network calls without an allow-list? If the answer to any of those is "everything the process user can access," the agent
isn't controlled. It's an unauthenticated write endpoint with a chat interface. This is the first control I added to agent-forge-bootstrap, before any prompt work.

WHAT I'M WATCHING
Docker socket exposure in containerized agents — the CVSS 8.8 auth bypass is back. Agent containers that mount the Docker socket are host escape paths. Audit for
/var/run/docker.sock mounts now, not at the next sprint.

Adobe Reader: four months of exploitation, still no patch. If PDFs enter any AI pipeline — document ingestion, RAG data sources, email parsing — Reader is an active
attack surface. Sandboxed rendering or an alternative parser is the pragmatic fix right now.

Closed harnesses and memory opacity — vendors are shipping managed agent frameworks where memory is a black box. You can't audit retention, can't verify what a prompt
injection could surface from stored context, and OWASP ASI05 guidance assumes you can. Watch for the Agentic Top 10 to address this directly.

EU AI Act enforcement timing — the compliance gap for agentic AI is documented. What's missing is clarity on which autonomous system capabilities trigger Article 9
obligations and when national supervisory authorities will start asking. Q2 is when I'd expect positions to crystallize.

Next week: the full agent-forge-bootstrap write-up: the permission model I built for the Executor and what I learned about harness and memory architecture when the
agent actually has local filesystem access. If you're building multi-agent systems and wondering where to start on security controls, that's the post.

Questions or topics you want covered? Reply to this email.

Cheers,

Amine
