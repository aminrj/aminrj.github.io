# AI Security in Production: A Practitioner's Guide to Threat Modeling Before You Ship

*Last updated: May 2026*

> The 2026 reality: 80%+ of enterprises have AI agents in production. Less than 15% had full security review before deployment. This guide is for the gap between those two numbers.

---

## TL;DR

If you are deciding whether your AI project is safe to ship to production, this article gives you:

- **The 5 frameworks that actually matter** in 2026 (MAESTRO, STRIDE-AI, NIST AI RMF, MITRE ATLAS, ISO 42001) and when to use each
- **A 7-phase methodology** for assessing AI projects before production — adapted from Microsoft's red team practice, Optiv's MAESTRO consulting work, and what works in the lab
- **What deliverables look like** at the end of a real AI threat modeling exercise — the artifacts, not the theory
- **How the Big Four consultancies (Deloitte, KPMG, EY, PwC) actually run these engagements** — their differentiators, costs, and what they produce
- **A complete pre-production checklist** mapping OWASP LLM Top 10 + OWASP Agentic Top 10 controls to team ownership

Read time: 35 minutes. If you only have 5: jump to [the methodology](#part-3-a-7-phase-methodology-for-ai-threat-modeling-in-production) and [the checklist](#part-7-the-pre-production-checklist).

---

## Part 1: Why AI threat modeling is different (and why most teams get it wrong)

Traditional threat modeling was built for deterministic systems. You map data flows, identify trust boundaries, enumerate threats against components with stable behavior, and design controls that hold under known inputs. STRIDE works because a SQL query injection either succeeds or fails the same way every time.

AI systems break this model in five specific ways:

**1. Probabilistic outputs replace deterministic logic.** An LLM that refuses a harmful prompt today may accept the same prompt tomorrow with a different temperature setting or system message. Microsoft's AI Red Team, after testing 100+ generative AI products, explicitly notes that the non-deterministic nature of AI models means coverage requires automation and statistical evaluation — manual testing cannot scale to the variation space.

**2. The attack surface includes the training data.** Data poisoning, model inversion, membership inference — none of these have analogs in traditional software security. They target the *learning* process, not the *execution*.

**3. Agents take actions, not just produce output.** When an AI system can call tools, query APIs, modify files, send emails, and chain operations, it becomes a new class of insider threat. The 2025 Stanford AI Index Report noted AI-related incidents in business increased over 56% year over year. Almost all of the high-severity ones involved agentic systems, not standalone models.

**4. Prompt injection is the SQL injection of LLM systems — and there is no equivalent fix.** Parameterized queries solved SQL injection at the parsing layer. Prompt injection cannot be solved at the parsing layer because the model has no parser separating instructions from data. The 2026 OWASP LLM Top 10 still ranks prompt injection as #1, and the production incident data confirms why.

**5. Supply chain extends beyond code.** A traditional supply chain audit covers source code, dependencies, and build artifacts. An AI supply chain covers all of that *plus* training datasets, model weights, fine-tuning corpora, embedding stores, MCP servers, agent skill marketplaces, and prompt template libraries. A single poisoned dataset cascades into every downstream model trained on it.

### The consequence: traditional methodologies are necessary but insufficient

This is why every credible 2026 AI security framework — Google's SAIF, Microsoft's AI Risk Assessment, NIST AI RMF, CSA's MAESTRO — explicitly states the same thing: existing security practice is the *foundation*, but AI introduces threats that require a new analytical layer on top.

HiddenLayer's 2025 AI Threat Landscape Report found that 61% of organizations deploying AI lack a dedicated security strategy. Forrester's 2026 enterprise survey found that of organizations who *have* deployed agentic AI in production, only 14.4% completed a full security review before going live. The gap between perceived risk and applied controls is the largest in enterprise security right now.

---

## Part 2: The 5 frameworks that actually matter in 2026

There are now over 20 frameworks claiming to address AI security. Most are vendor marketing layered on top of one of five real foundations. These are the five worth knowing:

### MAESTRO — for agentic AI systems

**What it is.** Multi-Agent Environment, Security, Threat, Risk, and Outcome. Developed by Ken Huang at Cloud Security Alliance, released February 2025, now the de facto standard for threat modeling autonomous AI agents.

**Why it matters.** It's the only major framework purpose-built for agentic AI. The 7-layer reference architecture decomposes agent systems into discrete attack surfaces:

1. **Foundation Models** — the underlying LLMs (Claude, GPT, Gemini, Llama)
2. **Data Operations** — embeddings, vector stores, RAG corpora
3. **Agent Frameworks** — LangGraph, CrewAI, AutoGen, Semantic Kernel
4. **Deployment Infrastructure** — Kubernetes, container orchestration, serverless
5. **Evaluation & Observability** — telemetry, logging, behavioral baselines
6. **Security & Compliance** — a vertical cross-cutting layer
7. **Agent Ecosystem** — marketplaces, A2A and MCP protocols, third-party tools

**How to apply it.** Map your system to the 7 layers, identify threats per layer using the published threat landscapes, then analyze cross-layer attack paths. The most dangerous attack chains start at Layer 1 and cascade through to Layer 7 (e.g., a manipulated foundation model output triggers a tool call that exfiltrates data through a poisoned marketplace skill).

**Where it falls short.** MAESTRO is a conceptual framework, not a runtime tool. Teams that have read the paper but not built it into CI/CD report the gap honestly: knowing the seven layers doesn't help if your SAST scanner can't see prompt injection chains. CSA published a follow-up in February 2026 on operationalizing MAESTRO in CI/CD pipelines — worth reading alongside the original.

**When to use it.** Any system using agents, MCP, or multi-step autonomous workflows. This is the default for 2026 agentic deployments.

### STRIDE-AI — for generative AI in regulated environments

**What it is.** A formal adaptation of Microsoft's STRIDE methodology to AI systems, published on arXiv in May 2026 (arXiv:2605.17163). The framework defines a six-phase assessment lifecycle and reinterprets the six STRIDE categories for AI:

- **Spoofing** → identity confusion in multi-agent systems
- **Tampering** → statistical contamination of training data
- **Repudiation** → opacity in AI decision provenance
- **Information disclosure** → model inversion, training data extraction
- **Denial of service** → unbounded consumption, resource exhaustion
- **Elevation of privilege** → jailbreaking, prompt injection bypassing safety controls

**Why it matters.** It bridges the gap between high-level risk standards (NIST AI RMF) and technical vulnerability taxonomies (OWASP LLM Top 10). For organizations that already use STRIDE in their SDL, STRIDE-AI is the lowest-friction path to AI threat modeling.

**Where it falls short.** Less developed than MAESTRO for agentic systems. STRIDE-AI focuses on single-model deployments and doesn't yet have the cross-layer analysis that agents require.

**When to use it.** Regulated industries (finance, healthcare, defense) where your existing security process is STRIDE-based and adding a parallel methodology would create governance fragmentation.

### NIST AI RMF + Agentic Profile — for governance and compliance

**What it is.** The NIST AI Risk Management Framework (AI RMF 1.0, January 2023) provides four functions: GOVERN, MAP, MEASURE, MANAGE. The 2024 Generative AI Profile (NIST AI 600-1) extended it with 13 GAI-specific risks (confabulation, CBRN information, prompt injection, etc.) and 400+ actions. In April 2026, NIST released a concept note for a Critical Infrastructure Profile, and the CSA Labs published a draft Agentic AI Profile addressing the gap left by previous versions.

**Why it matters.** It's the de facto governance vocabulary for AI risk in the US, with broad adoption across federal agencies, financial institutions, and major technology organizations. The EU AI Act explicitly references NIST AI RMF alignment as demonstrating state-of-the-art mitigations. Demonstrating RMF adoption is now a prerequisite for federal AI procurement under Executive Order 14110.

**Where it falls short.** NIST AI RMF is a governance framework, not a threat modeling methodology. It tells you *what to govern* (the four functions) but not *how to identify threats* (you still need MAESTRO, STRIDE-AI, or MITRE ATLAS for that). Treat it as the umbrella, not the operational tool.

**When to use it.** Any organization that needs to demonstrate AI governance to regulators, customers, or boards. Most enterprises in 2026 need RMF alignment regardless of whether they use it for actual threat modeling.

### MITRE ATLAS — for adversarial threat mapping

**What it is.** Adversarial Threat Landscape for Artificial-Intelligence Systems. Maintained by MITRE Corporation, the same team behind ATT&CK. As of the v5.4.0 update (February 2026), it covers 16 tactics, 84+ techniques, 32 mitigations, and 42 documented real-world case studies.

**Why it matters.** ATLAS is to AI what ATT&CK is to traditional infrastructure: a structured catalog of *how attackers actually do this*, grounded in published incidents. The 2026 updates added significant agentic AI coverage including AI Agent Tools (AML.T0061) and the SesameOp case study (AML.CS0042) documenting a backdoor leveraging the OpenAI Assistants API for command and control.

**Where it falls short.** ATLAS describes threats, not mitigations or methodology. You use it to validate that your threat model covers known attack patterns — not to drive the modeling exercise itself.

**When to use it.** Always, as a coverage check. After completing a MAESTRO or STRIDE-AI threat model, verify that you've addressed every ATLAS technique that applies to your architecture. If you can't map your threat coverage to ATLAS techniques, you have gaps.

### ISO/IEC 42001 — for management systems

**What it is.** Published December 2023, ISO 42001 is the first international standard for AI management systems (AIMS). Built on the same high-level structure as ISO 27001 (information security) and ISO 9001 (quality), with AI-specific additions covering AI roles (provider, deployer, user, partner), AI risk assessment, AI system impact assessment, and AI lifecycle controls.

**Why it matters.** It's the closest thing to a "complete operating system" for AI governance. As of early 2026, it's voluntary but rapidly becoming the de facto operating system for AI compliance globally. KPMG was the first Big Four firm to claim ISO 42001 certification. The EU AI Act references 42001-aligned management systems as one acceptable path to demonstrating compliance with high-risk system requirements.

**Where it falls short.** Certification is expensive (typical 12–18 month implementation, $200K–$500K for mid-market companies including external auditor fees). It also doesn't tell you what threats exist — it tells you how to manage them once identified.

**When to use it.** Enterprises selling AI products to regulated buyers (financial services, healthcare, government, defense). The certification is increasingly required to close enterprise deals. If you already have ISO 27001, you're approximately 40% of the way to 42001 — the management system structure is identical.

### The framework stack in practice

These five frameworks don't compete. In practice, mature AI security programs use them as a stack:

```
┌────────────────────────────────────────────────────────────┐
│ ISO 42001 — Management System / Operating Model            │
│ ┌──────────────────────────────────────────────────────┐   │
│ │ NIST AI RMF — Governance Functions (GOVERN/MAP/      │   │
│ │ MEASURE/MANAGE)                                      │   │
│ │ ┌────────────────────────────────────────────────┐   │   │
│ │ │ MAESTRO or STRIDE-AI — Threat Modeling          │   │   │
│ │ │ Methodology (the actual analytical work)        │   │   │
│ │ │ ┌──────────────────────────────────────────┐    │   │   │
│ │ │ │ MITRE ATLAS — Adversarial Threat Mapping │    │   │   │
│ │ │ │ (coverage validation)                    │    │   │   │
│ │ │ │ ┌────────────────────────────────────┐   │    │   │   │
│ │ │ │ │ OWASP LLM Top 10 / Agentic Top 10  │   │    │   │   │
│ │ │ │ │ (specific control catalog)         │   │    │   │   │
│ │ │ │ └────────────────────────────────────┘   │    │   │   │
│ │ │ └──────────────────────────────────────────┘    │   │   │
│ │ └────────────────────────────────────────────────┘   │   │
│ └──────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────┘
```

You pick the framework that matches the question being asked. Board asking "are we governing AI risk properly?" → NIST AI RMF and ISO 42001. Security architect asking "what could go wrong with this agent before we ship?" → MAESTRO. Red team asking "have we covered the known attack techniques?" → MITRE ATLAS.

---

## Part 3: A 7-phase methodology for AI threat modeling in production

The following methodology synthesizes Microsoft's AI Red Team operational practice (from their work on 100+ generative AI products), Optiv's MAESTRO consulting methodology, CSA's MAESTRO operationalization guidance, and what consistently produces useful output in practice. It assumes you already have a functioning information security program — if you don't, start there.

### Phase 1 — Scope & business context (1–2 days)

Before any technical analysis, establish the answers to four questions:

1. **What business outcome is this AI system supposed to produce?** Revenue generation, cost reduction, customer experience, internal productivity. The business outcome determines acceptable risk thresholds.
2. **What is the blast radius if it fails?** Reputational harm, regulatory exposure, direct financial loss, safety implications.
3. **Who has authority to approve the deployment?** Identify the accountable executive — without explicit ownership, threat modeling produces findings nobody acts on.
4. **What's the deployment timeline pressure?** Realistic vs. aspirational. If the answer is "Friday no matter what," the threat model needs to be a triage exercise focused on critical-only findings, not comprehensive analysis.

**Deliverable:** a 1-page scoping document signed by the accountable executive. This becomes the reference point for every prioritization decision downstream.

### Phase 2 — Asset inventory & decomposition (2–4 days)

Decompose the AI system using MAESTRO's 7-layer model. For each layer, document:

- **Layer 1 (Foundation Models):** which models, hosted where, accessed how, with what authentication
- **Layer 2 (Data Operations):** training corpora, fine-tuning data, RAG knowledge bases, vector stores, embedding pipelines
- **Layer 3 (Agent Frameworks):** LangGraph, CrewAI, AutoGen, Semantic Kernel, custom orchestration; tool registration patterns
- **Layer 4 (Deployment Infrastructure):** Kubernetes clusters, container images, serverless functions, secrets management
- **Layer 5 (Evaluation & Observability):** what is logged, where, retention period, who can read it
- **Layer 6 (Security & Compliance):** existing controls already in place
- **Layer 7 (Agent Ecosystem):** MCP servers used, marketplace skills installed, A2A protocols, external tools

**Deliverable:** an asset inventory mapped to the 7 layers, with each asset tagged for criticality. Microsoft's Cloud Adoption Framework recommends an automated AI asset inventory — manual inventories drift quickly in agentic environments. CSA Labs published a parallel piece in April 2026 noting that "Unknown AI assets, or AI assets that aren't tracked for compliance with organizational AI policy, create security risks that bad actors can exploit."

### Phase 3 — Threat identification (3–5 days)

For each layer, identify threats using both top-down and bottom-up approaches.

**Top-down: framework-driven.** Walk through the MAESTRO layer-specific threat landscapes and the OWASP Agentic Top 10. For each documented threat pattern, ask "does this apply to our architecture?" If yes, document it as a candidate finding.

**Bottom-up: asset-centric.** A May 2025 arXiv paper by Microsoft researchers (arXiv:2505.06315) argues for an asset-centric methodology specifically because top-down framework-driven approaches miss compositional attacks that emerge from how assets connect. For each critical asset identified in Phase 2, ask "what would compromise of this asset enable?" and trace the attack paths backward.

The cross-layer analysis is where most threat models in 2026 break down. The most dangerous attack chains start at one layer and cascade through several others. Example chain from documented 2026 incidents:

1. Layer 7 (Ecosystem) — A malicious MCP server is installed via marketplace
2. Layer 3 (Agent Framework) — The agent loads the server's tool descriptions into its context
3. Layer 1 (Foundation Model) — The model follows the malicious instructions embedded in tool descriptions
4. Layer 4 (Infrastructure) — The agent executes a tool with cloud credentials
5. Layer 2 (Data) — The cloud credentials enable database exfiltration

Document the chain, not just the endpoints. The mitigation for the chain may exist at a different layer than where the attack starts.

**Deliverable:** a threat register containing each identified threat with: source asset, attack vector, prerequisites, blast radius, MAESTRO layer mapping, MITRE ATLAS technique mapping where applicable, and OWASP LLM/Agentic Top 10 category.

### Phase 4 — Risk evaluation (2–3 days)

For each threat in the register, assess:

- **Likelihood:** based on attacker capability required, prerequisites, and public exploit availability
- **Impact:** based on the business outcome and blast radius from Phase 1
- **Existing controls:** what already mitigates this in your current architecture
- **Residual risk:** likelihood × impact, accounting for existing controls

Use a 5×5 matrix or whatever your enterprise risk management framework already uses. Resist creating an AI-specific risk scoring scheme — it creates governance fragmentation and slows down approval workflows.

**Deliverable:** the threat register augmented with risk scores and existing control mappings. This is the input for the prioritization and remediation phases.

### Phase 5 — Red team validation (1–3 weeks, parallel to Phase 4)

For high-risk findings, validate empirically. Microsoft's AI Red Team, after working on 100+ products, identified three principles worth adopting:

1. **Automate to cover scale; keep humans for judgment.** Use PyRIT (or commercial equivalents like Microsoft's AI Red Teaming Agent in Foundry, Adversa AI's red teaming tools, or Garak) for the breadth coverage. Use human red teamers for the nuanced, multi-step attacks that require domain expertise.

2. **Test the system, not the model.** Model-level red teaming (testing for hateful/sexual/violent content) misses the attack paths that matter in agentic systems. The dangerous attacks combine prompt manipulation with tool misuse with credential abuse — none of those are visible if you only test the model endpoint.

3. **Capture the prompt sequences, not just the success rate.** Attack Success Rate (ASR) tells you the outcome. The prompt sequences tell you the attack path. The latter is what you need for remediation; the former is what you report to leadership.

**Tools that work in 2026:**
- **PyRIT** (Microsoft, open source, MIT-licensed) — 53+ datasets including AIRT, HarmBench, AdvBench, XSTest
- **Garak** (NVIDIA, open source) — probe-based red teaming, well-suited to CI/CD integration
- **Microsoft AI Red Teaming Agent** (Azure Foundry, generally available) — managed PyRIT with reporting
- **Promptfoo** — declarative test suites for LLM applications
- **Repello AI** — commercial, OWASP LLM Top 10 coverage

For agentic systems specifically: standard PyRIT and Garak miss agentic risks. You need to test the full agent loop including tool calls, not just the model endpoint.

**Deliverable:** a red team report with empirical findings, mapped back to the threat register. Findings that the red team validated move to "Confirmed" status. Findings that the red team could not validate move to "Theoretical" status with a note on testing limitations.

### Phase 6 — Mitigation design & control mapping (1–2 weeks)

For each high-priority threat (theoretical or confirmed), design mitigations. Sort mitigations into three categories:

**Preventive controls.** Block the threat from occurring. Examples: input validation on tool parameters, allowlist for permitted commands, scope-limited API keys per agent, hash verification on MCP tool descriptions before loading.

**Detective controls.** Detect the threat when it occurs. Examples: behavioral baselines on agent tool-call patterns, anomaly detection on embedding cluster patterns, audit logging on all agent actions with cryptographic signing.

**Responsive controls.** Reduce blast radius when the threat occurs. Examples: rollback mechanisms (Veeam-style backup of model weights, vector stores, and agent configurations), kill switches that disable specific agents, credential rotation triggered by anomaly detection.

Each mitigation should be:
- Mapped to a specific MAESTRO layer
- Mapped to a specific OWASP control
- Assigned to a single accountable owner
- Estimated in implementation effort (developer-days)
- Given a clear acceptance criterion (how do we know it works)

**Deliverable:** a mitigation matrix linking each threat to its mitigations, with ownership, effort, and acceptance criteria. This is the artifact your project team will work from for the next sprint or two.

### Phase 7 — Release gate decision & continuous monitoring plan (1–2 days)

Convert the threat model into a release gate. Three possible outcomes:

1. **GO** — All critical findings have implemented mitigations validated by red team. Acceptance criteria met. Continuous monitoring plan documented. Production deployment approved.

2. **GO WITH CONDITIONS** — Critical findings mitigated. Some high findings have compensating controls but not full mitigations. Production deployment approved with specific monitoring requirements and a 30/60/90-day re-assessment.

3. **NO-GO** — Critical findings without acceptable mitigation. Compensating controls insufficient. Deployment blocked pending architectural changes.

The continuous monitoring plan is what differentiates a real threat model from a one-time exercise. Specify:
- Which threats require runtime monitoring
- What signals indicate the threat is materializing
- Who responds, in what time window, with what authority
- How often the threat model is re-evaluated (quarterly minimum for production AI systems; monthly for agentic systems with frequent capability changes)

**Deliverable:** the release gate decision document, the continuous monitoring runbook, and the re-assessment schedule. These three documents together constitute the production-readiness package.

---

## Part 4: What the Big Four consultancies actually produce

Enterprises that don't have in-house AI security capability typically engage one of the Big Four consultancies, a specialized AI security firm, or a regional integrator. The 2026 market has segmented clearly. Here's what each segment actually delivers:

### Deloitte — Trustworthy AI Framework + ISO 42001

Deloitte's AI practice integrates strategy advisory with broader technology and operational capabilities. Their **Trustworthy AI framework** is the anchor for AI governance and responsible AI work, with strong integration across audit, risk, and digital transformation practices.

**What they actually deliver:**
- AI maturity assessment against the Trustworthy AI framework
- ISO 42001 readiness assessment and certification support
- Risk-based AI inventory and classification
- Policies, procedures, and operating model design
- Integration with existing GRC platforms

**Where they excel:** Regulated industries where AI deployment requires regulatory alignment. The integration with their audit and risk practices is unique and useful for enterprises that need defensible governance documentation.

**Typical engagement:** 3–6 months, $400K–$2M depending on scope. Output is heavy on policy, governance documentation, and management system design.

### KPMG — Trusted AI 10-pillar framework

KPMG is the only Big Four firm to publish a formally numbered 10-pillar AI framework. They were also the first to claim ISO 42001 certification for their own operations.

**What they actually deliver:**
- AI risk assessment against the 10-pillar framework
- ISO 42001 implementation and certification
- AI governance committee design and charter
- Third-party AI risk assessment (vendor due diligence)
- Audit-ready evidence packages

**Where they excel:** Companies that want a numbered, defensible framework they can show to regulators or audit committees. The 10-pillar framework provides a clear scoring artifact at the end of an engagement.

**Typical engagement:** 4–8 months, $300K–$1.5M. Output is heavily certification-oriented.

### EY — Sovereign and regulated-industry AI

EY differentiated in 2026 by going all-in on NVIDIA with on-prem Dell AI Factory deployments, positioning themselves as the firm for sovereign and regulated-industry AI where data residency, sovereignty, and on-premises operation matter.

**What they actually deliver:**
- AI governance frameworks for highly regulated industries (financial services, defense, healthcare, government)
- On-premises AI infrastructure design and deployment
- Compliance mapping against EU AI Act, GDPR, sector-specific regulations
- AI control implementation and monitoring

**Where they excel:** EU operations with high-risk AI Act exposure, defense contractors, government agencies. Their sovereign AI positioning is specific and well-suited to the regulated segment.

**Typical engagement:** 6–18 months for full deployments, $500K–$10M+. Output combines governance with actual infrastructure deployment.

### PwC — AI risk assurance + ChatPwC

PwC's AI practice emphasizes AI risk assurance and audit-readiness, with an internal ChatPwC platform that they leverage for client engagements.

**What they actually deliver:**
- AI risk and assurance reviews
- Internal audit of AI systems against established frameworks
- AI governance maturity assessments
- Compliance mapping and gap analysis

**Where they excel:** Companies needing third-party assurance for their AI controls, particularly for boards or audit committees. The audit DNA is genuine.

**Typical engagement:** 2–4 months, $200K–$800K. Output is assurance-focused.

### What the Big Four don't do well

A few honest observations about engaging the Big Four for AI security work:

- **Hands-on red teaming.** None of the Big Four field deep AI red teaming capability comparable to Microsoft's AI Red Team or specialist firms like Adversa AI, Repello AI, or HiddenLayer. If you need actual attack validation, you'll need a specialist on top of or instead of the Big Four.
- **Custom MCP and agent framework security.** The Big Four are framework-strong and implementation-weak. Engagements heavy on attack chain analysis and exploit reproduction go better with specialist firms that publish research (Cato CTRL, OX Security, Invariant Labs).
- **Speed.** Big Four engagements run on 6–18 month timelines. If you need a production-readiness assessment in 4 weeks before a launch, a boutique or in-house team will move faster.

### Specialist AI security firms worth knowing in 2026

For engagements where the Big Four isn't the right fit:

- **Adversa AI** (red teaming, MCP security research, monthly digest)
- **Repello AI** (LLM pentesting, OWASP coverage)
- **HiddenLayer** (AI threat intelligence, model security)
- **Lakera** (LLM application security, Gandalf training platform)
- **Robust Intelligence** (model security and validation, acquired by Cisco)
- **Protect AI** (ML security platform, model scanning)
- **Cato CTRL** (threat research, HashJack disclosure)
- **OX Security** (supply chain security including MCP architectural research)

A typical specialist engagement runs 4–12 weeks at $80K–$400K and produces an empirical attack validation report with reproducible findings — the artifact the Big Four governance work usually lacks.

---

## Part 5: What the deliverables actually look like

Here's what you should expect at the end of a production AI threat modeling engagement, regardless of who runs it:

### 1. Executive summary (1 page)

A non-technical summary covering: number of findings by severity, the top 3–5 risks the executive needs to know about, the recommendation (GO / GO WITH CONDITIONS / NO-GO), and the resource requirement for remediation. This is the only document most executives read. Make it count.

### 2. Asset inventory (5–20 pages)

The MAESTRO 7-layer decomposition of the system. Every model, every dataset, every tool, every credential, every dependency. This is the foundation document that everything else references.

### 3. Threat register (10–50 pages)

The complete list of identified threats, each containing:
- Threat ID (e.g., T-2026-042)
- Title and description
- Source asset and attack vector
- Prerequisites
- MAESTRO layer mapping
- MITRE ATLAS technique mapping (where applicable)
- OWASP LLM Top 10 / Agentic Top 10 mapping
- Existing controls
- Residual risk score (likelihood × impact)
- Status (Theoretical / Confirmed by red team / Mitigated)
- Owner

### 4. Red team report (10–30 pages)

For each high-priority threat that was validated empirically:
- Attack scenario and methodology
- Tools used (PyRIT, Garak, custom)
- Attack Success Rate and confidence interval
- Prompt sequences and tool call traces (the actual attack paths, not just summaries)
- Reproduction steps
- Defensive observations

### 5. Mitigation matrix (5–20 pages)

For each threat requiring action:
- Threat ID
- Mitigation type (preventive / detective / responsive)
- Specific control (with reference to OWASP, NIST, or internal framework)
- Owner
- Implementation effort
- Acceptance criteria
- Dependencies

### 6. Release gate decision (2–3 pages)

The formal GO / GO WITH CONDITIONS / NO-GO decision, signed by the accountable executive identified in Phase 1. Includes the rationale and any conditions attached.

### 7. Continuous monitoring runbook (5–10 pages)

The plan for what happens after deployment:
- Monitoring signals and detection logic
- Response procedures by signal type
- Roles and escalation paths
- Re-assessment schedule
- Triggers for re-running the threat model (new agent capabilities, new tool integrations, model upgrades, new regulatory requirements)

---

## Part 6: The tools that actually work in 2026

A short list of what's worth knowing, sorted by category:

### Open-source threat modeling tools

- **STRIDE-GPT** (github.com/mrwadams/stride-gpt) — AI-powered STRIDE threat modeling, supports Claude 4, GPT-5 series, GitHub Enterprise
- **MAESTRO** (github.com/CloudSecurityAlliance/MAESTRO) — CSA's tool implementing the 7-layer model with AI-powered threat identification
- **PyRIT** (github.com/Azure/PyRIT) — Microsoft's open-source red teaming framework
- **Garak** (github.com/leondz/garak) — NVIDIA's LLM vulnerability scanner
- **mcp-scan** (github.com/invariantlabs-ai/mcp-scan) — Invariant Labs' MCP tool description scanner

### Commercial threat modeling platforms

- **IriusRisk** — has MAESTRO integration for agentic AI threat modeling
- **Devici** — Chris Romeo's threat modeling platform with AI capabilities
- **Apiiro** — graph-powered AI threat modeling integrated into SDLC
- **Microsoft Threat Modeling Tool** + the AI/ML guidance — works if you're a Microsoft shop already

### AI-specific security platforms

- **Microsoft AI Red Teaming Agent** (Azure Foundry) — managed PyRIT with reporting
- **Adversa AI Red Teaming Platform** — commercial red teaming with continuous coverage
- **Lakera Guard** — runtime LLM application firewall
- **Protect AI Radar** — ML model security scanning
- **HiddenLayer** — AI threat intelligence and model integrity

### Runtime monitoring

- **Sysdig Falco rules for AI coding agents** — syscall-level detection for Claude Code, Gemini CLI, Codex CLI
- **Sentinely** — runtime security gate scoring each agent action against a behavioral model
- **StepSecurity Harden Runner** — GitHub Actions hardening, blocks egress to unknown endpoints

---

## Part 7: The pre-production checklist

Use this checklist as the final gate before any AI project ships. Each item should have a named owner and evidence of completion before production approval.

### Foundation Model Layer

- [ ] Model provenance documented (source, version, hash, license)
- [ ] Model SBOM produced and reviewed
- [ ] Model evaluated against OWASP LLM Top 10 categories
- [ ] Prompt injection resistance tested with PyRIT or equivalent
- [ ] Jailbreak resistance tested with documented bypass attempts
- [ ] Output validation in place for sensitive data patterns
- [ ] Rate limiting configured
- [ ] Cost / consumption monitoring with alerting thresholds

### Data Operations Layer

- [ ] Training data provenance documented
- [ ] Fine-tuning corpora reviewed for poisoning resistance
- [ ] RAG knowledge base access control verified (tenant isolation)
- [ ] Vector store anomaly detection enabled
- [ ] Embedding pipeline sanitization (HTML, markdown, hidden tokens)
- [ ] Data classification metadata enforced in retrieval queries
- [ ] PII detection on ingestion
- [ ] Backup and rollback procedures tested

### Agent Framework Layer

- [ ] Framework version pinned (CrewAI ≥ patched, Semantic Kernel ≥ 1.39.4 Python / ≥ 1.71.0 .NET)
- [ ] `[KernelFunction]` and equivalent tool registrations audited
- [ ] AutoInvoke disabled on agents with sensitive access
- [ ] Tool allowlist defined (not denylist)
- [ ] Parameter validation on every tool input
- [ ] Tool execution sandboxing (Docker, seccomp, namespaces)
- [ ] Per-agent identity with cryptographically verifiable credentials
- [ ] Agent-to-agent message authentication

### MCP / Tool Ecosystem

- [ ] MCP server inventory complete (no shadow MCP)
- [ ] mcp-scan run before any new server installation
- [ ] Tool descriptions hash-verified at every reconnection
- [ ] No MCP server has shell execution unless strictly required
- [ ] No MCP server has cloud credentials in plaintext configuration
- [ ] Marketplace skills reviewed and signed before installation
- [ ] MCP gateway in place if you have multiple servers
- [ ] Per-caller authentication (mTLS or signed JWT) on all MCP servers

### Deployment Infrastructure

- [ ] Container images scanned and signed
- [ ] Secrets management externalized (no .env files in production)
- [ ] Kubernetes RBAC scoped to minimum required permissions
- [ ] Network egress allowlist enforced
- [ ] Resource limits set (CPU, memory, network)
- [ ] Backup and rollback procedures tested
- [ ] Disaster recovery plan documented

### Evaluation & Observability

- [ ] All agent actions logged with cryptographic signing
- [ ] Log retention meets regulatory requirements
- [ ] Behavioral baseline defined (or explicit acknowledgment that no baseline exists)
- [ ] Anomaly detection in place for tool call patterns
- [ ] Alerting on safety filter triggers
- [ ] Incident response runbook tested
- [ ] Re-assessment schedule documented

### Security & Compliance

- [ ] NIST AI RMF mapping completed
- [ ] OWASP Top 10 coverage validated
- [ ] MITRE ATLAS coverage validated
- [ ] EU AI Act risk category determined (if EU operations)
- [ ] ISO 42001 alignment documented (if pursuing certification)
- [ ] Data Protection Impact Assessment completed (if processing personal data)
- [ ] Acceptable use policy published
- [ ] User-facing transparency documentation published

---

## Part 8: What to read next

For going deeper on specific topics covered here, ordered by usefulness:

**Primary frameworks (read first):**
- CSA MAESTRO whitepaper — [cloudsecurityalliance.org/blog/2025/02/06/agentic-ai-threat-modeling-framework-maestro](https://cloudsecurityalliance.org/blog/2025/02/06/agentic-ai-threat-modeling-framework-maestro)
- NIST AI RMF + GAI Profile — [nist.gov/itl/ai-risk-management-framework](https://www.nist.gov/itl/ai-risk-management-framework)
- MITRE ATLAS — [atlas.mitre.org](https://atlas.mitre.org)
- OWASP Top 10 for LLM Applications 2025 — [genai.owasp.org](https://genai.owasp.org)
- OWASP Top 10 for Agentic Applications 2026 — [genai.owasp.org](https://genai.owasp.org)

**Operational practice (read second):**
- Microsoft AI Red Team — "Lessons from red teaming 100+ generative AI products" — [microsoft.com](https://www.microsoft.com/en-us/security/blog/2025/01/13/3-takeaways-from-red-teaming-100-generative-ai-products/)
- CSA MAESTRO operationalization in CI/CD — [cloudsecurityalliance.org/blog/2026/02/11/applying-maestro-to-real-world-agentic-ai-threat-models-from-framework-to-ci-cd-pipeline](https://cloudsecurityalliance.org/blog/2026/02/11/applying-maestro-to-real-world-agentic-ai-threat-models-from-framework-to-ci-cd-pipeline)
- Microsoft Threat Modeling AI/ML Systems and Dependencies — [learn.microsoft.com/en-us/security/engineering/threat-modeling-aiml](https://learn.microsoft.com/en-us/security/engineering/threat-modeling-aiml)
- Google SAIF — [safety.google/cybersecurity-advancements/saif](https://safety.google/cybersecurity-advancements/saif)

**Recent research papers (read third):**
- STRIDE-AI (arXiv:2605.17163) — formal STRIDE adaptation for AI
- Asset-Centric Threat Modeling for AI (arXiv:2505.06315) — bottom-up methodology
- MCPShield (arXiv:2604.05969) — formal MCP security framework
- MCP-38 (arXiv:2603.18063) — 38-category MCP threat taxonomy

**Reference implementations:**
- mcp-attack-labs (lab code reproducing real MCP attacks) — [github.com/aminrj-labs/mcp-attack-labs](https://github.com/aminrj-labs/mcp-attack-labs)
- SAFE-MCP (MITRE ATT&CK-style TTP catalog for MCP) — [safemcp.org](https://www.safemcp.org)
- MAESTRO tool — [github.com/CloudSecurityAlliance/MAESTRO](https://github.com/CloudSecurityAlliance/MAESTRO)
- STRIDE-GPT — [github.com/mrwadams/stride-gpt](https://github.com/mrwadams/stride-gpt)

---

## Closing thoughts

The honest assessment of where the AI security field is in May 2026: the frameworks are mature enough, the tools exist, the methodologies work. What's missing is operational practice. Most organizations have read the MAESTRO paper, nodded along, then deployed agents without running a single PyRIT scan or completing a single threat register.

The gap between "we understand AI security" and "we ship secure AI" is the most exploitable surface in the enterprise right now.

If you're deciding whether your AI project is safe to ship to production, the question is not whether you've read the right framework. The question is whether you can produce all seven deliverables from Part 5 — with a named owner on every finding and acceptance criteria on every mitigation — before the launch date.

If you can, ship. If you can't, you don't have a threat model. You have a wish list.

---

*This article will be maintained as the field evolves. The 2026 update cycle has accelerated: most AI security guidance from before October 2025 is now obsolete. Always check publication dates on AI security research — the half-life is now under 6 months.*
