  ---
  Subject: 8 agent exploits in Q1. 200,000 vulnerable MCP servers. Anthropic won't fix the protocol.

  Preview text: A persistent context window is a persistent attack surface. Eight production incidents this quarter prove it.

  ---
  👋

  The state handoff problem I covered last issue is an engineering problem. The one underneath it is a security problem.

  This week I've been in the memory layer of agent harnesses — what happens to context when the agent process stays alive across turns, and how that changes the
   threat model. Once you keep a process alive, the context window is no longer transient. It's a store. Whatever gets written into it — a malicious tool
  output, a poisoned document from the Executor's context — persists until something forces a purge. If you don't control what the agent remembers, you don't
  control what it'll do three turns from now.

  OWASP documented eight real incidents this quarter where that failure mode played out in production. The pattern holds across all eight.

  ---
  FROM THE LAB

  Qwen3.6 on 24GB VRAM: Benchmark, Config, and Every Mistake → — llama.cpp at 101 tok/s on an RTX 3090. 1.4× faster than Ollama, 2× the context via KV cache
  quantization. The config if you're running local inference for agent testing.

  ---
  THIS WEEK IN AI SECURITY

  MCP RCE: 200,000 vulnerable instances, Anthropic declined to fix it at the protocol level

  OX Security documented an architectural flaw in Anthropic's MCP SDK that enables arbitrary command execution on any system running a vulnerable
  implementation. User input flows directly into STDIO MCP configuration with no sanitization. Ten CVEs were assigned: CVE-2026-30623 (LiteLLM), CVE-2026-30615
  (Windsurf), CVE-2026-30624 (Agent Zero), and six others across GPT Researcher, Fay Framework, Langchain-Chatchat, and DocsGPT. OX confirmed exploitation on
  six live production platforms.

  Scale: 150M+ downloads, 7,000+ publicly exposed servers, up to 200,000 vulnerable instances.

  Anthropic's response: they declined to implement a protocol-level fix. Sanitization is the developer's problem.

  <div style="background:#fefce8;border-left:3px solid #ca8a04;padding:12px 16px;border-radius:0 6px 6px
  0;font-family:Georgia,serif;font-size:15px;line-height:1.7;color:#1c1917;">
    <b>If you run MCP:</b> Block public internet access to your MCP services and treat all external configuration as untrusted input. Run servers in sandboxes.
  Anthropic has explicitly placed sanitization responsibility on developers — the protocol won't do it.
  </div>

  OX Security → | CSO Online →

  ---
  OWASP GenAI Exploit Round-up: 8 incidents, Q1 2026

  OWASP's GenAI Security Project published their Q1 report on April 14. Eight documented incidents, all production systems.

  The list: Flowise CVE-2025-59528 with 12,000–15,000 exposed instances under active exploitation; a Mexico government breach where attackers used Claude and
  ChatGPT to automate recon and exfiltrate 150 GB of tax and voter data; a Mercor/LiteLLM supply chain compromise; GrafanaGhost — an indirect prompt injection
  that forced enterprise data exfiltration; and four others including Vertex AI privilege abuse and a Meta internal data leak.

  OWASP's read on the pattern: attackers stopped targeting model outputs. They went after agent identities, orchestration layers, and supply chains. The memory
  and state layer — where persistent context lives — is where the blast radius lands.

  OWASP GenAI →

  ---
  Nginx UI auth bypass — CVE-2026-33032, actively exploited

  An authentication bypass in Nginx UI is being exploited in the wild. No credentials required to take over the server. Many MCP backends sit behind Nginx. A
  compromised web layer gives an attacker a direct path to agent tooling. Patch or isolate. Check your MCP backend's network exposure while you're at it.

  BleepingComputer →

  ---
  TOOLING WORTH KNOWING

  Kvlar — open-source firewall for MCP tool calls. Sits between the agent and the tool, evaluates each call against YAML policies, fails closed on no match.
  Allow/deny/require-human-approve per action. The pre-action authorization layer the MCP protocol didn't build in. github.com/kvlar-io/kvlar →

  AWS IAM patterns for agents — AWS published least-privilege IAM patterns tied to agent identities for MCP-connected deployments. Short-lived credentials,
  deterministic policies, continuous permissions audits. If your agents touch AWS resources, this is the reference. AWS Security Blog →

  ---
  ONE THING TO CHECK THIS WEEK

  Rotate and scope every API key used by an AI agent. Replace long-lived, unscoped keys with per-agent least-privilege tokens or short-lived federation tokens.
  A community audit found 93% of agent projects use unscoped keys. The MCP RCE above makes credential exposure the immediate outcome of a successful exploit —
  scoped keys are the difference between "agent compromised" and "everything the agent could reach is compromised."

  ---
  WHAT I'M WATCHING

  → Flowise CVE-2025-59528 — 12–15K instances exposed, active exploitation confirmed by the OWASP Q1 report. If Flowise is in any pipeline you run, this is not
  a "patch next sprint" situation.

  → Anthropic Glasswing and vuln discovery economics — AI-assisted zero-day discovery narrows the window between discovery and weaponization. That changes
  attacker economics in ways not yet priced into most threat models. CSO Online →

  → TeamPCP supply chain wave — Trivy → LiteLLM → Telnyx. Attackers are chaining CI/CD compromises into LLM ecosystems. Scanner binaries are sensitive
  infrastructure. Treat them that way.

  → ACE benchmark — when you can price the cost to exploit a model, threat-informed defense becomes quantifiable. Worth tracking as economic measures start
  driving model selection. fabraix.com →

  ---
  Next week: the full agent-forge-bootstrap write-up. The permission model I built for the Executor, what broke before I had it, and what the memory
  architecture looks like when the agent has real filesystem access. If you're building multi-agent systems, that's the post.

  Questions or topics? Reply to this email.

  Amine
  <https://aminrj.com> | <https://aminrj.com/subscribe>
