---
title: "The CISO's Playbook: Red Teaming Agentic AI Systems — Checklists, Frameworks, and Assessment Templates"
date: 2026-03-06
uuid: 202603060000
status: draft
content-type: guide
target-audience: executive
categories: [Security, AI, LLM]
tags:
  [
    AI Security,
    CISO,
    Red Team,
    OWASP,
    MITRE ATLAS,
    Agentic AI,
    Risk Assessment,
    Compliance,
    Security Governance,
    Threat Modeling,
  ]
image:
  path: /assets/media/ai-security/ciso-playbook-red-teaming.png
description: "A structured, actionable playbook for security leaders and their teams — checklists, decision matrices, severity frameworks, and ready-to-use templates for assessing the security posture of agentic AI deployments. No case studies. Pure reference material."
---

> _Everything your security team needs to plan, execute, and report on agentic AI red team assessments — in one reference document._

---

## How to Use This Playbook

This playbook is a standalone operational reference. Each section is designed to be used independently:

- **Section 1** frames the strategic risk for executive stakeholders.
- **Sections 2–3** provide pre-assessment preparation checklists.
- **Section 4** is a quick-reference attack pattern catalog with severity and detection data.
- **Section 5** maps all three major frameworks to each other for compliance alignment.
- **Sections 6–8** structure the assessment engagement itself.
- **Sections 9–10** provide ready-to-use reporting and remediation templates.
- **Section 11** is a one-page executive brief for board or leadership presentations.

Print the sections relevant to your current phase. Return to this document at each stage of your assessment program.

---

## 1. Strategic Risk Summary

Agentic AI systems introduce a category of security risk that existing enterprise frameworks do not cover. These systems differ from traditional software — and from basic LLM deployments — in five fundamental ways:

| Property | Security Implication |
|---|---|
| **Autonomous execution** | Agents plan and execute multi-step operations without human approval at each step. A single injected instruction can trigger an entire chain of tool calls. |
| **Tool access** | Agents invoke real tools: databases, APIs, file systems, cloud services. Exploitation produces real-world consequences, not just model outputs. |
| **Delegation** | Multi-agent architectures pass tasks between agents. A compromised orchestrator poisons every downstream agent in the pipeline. |
| **Persistent memory** | Agents retain context across sessions. Poisoned memory today alters behavior in future interactions. |
| **Inherited identity** | Agents operate with the credentials and permissions of the accounts or services they connect to. Compromised agents act with full privilege scope. |

**The business risk**: An agentic AI system with access to production infrastructure, customer data, or internal APIs creates an attack surface that scales with its tool access — not with its code complexity. A single prompt injection can be more damaging than a traditional code-level vulnerability because the blast radius is determined by what the agent can reach, not what the developer intended.

Three industry frameworks now address this risk directly: **OWASP Agentic Top 10** (December 2025), **MITRE ATLAS** (October 2025 update), and the **CSA Agentic AI Red Teaming Guide** (May 2025). This playbook synthesizes all three into a unified assessment methodology.

---

## 2. Pre-Assessment Readiness Checklist

Before initiating a red team engagement, confirm the following items. Each is a prerequisite for a meaningful assessment.

### 2.1 Scope Definition

| # | Item | Status |
|---|---|---|
| 1 | All AI agents in scope are identified with their names, purposes, and deployment environments | ☐ |
| 2 | Each agent's tool access is documented (APIs, databases, file systems, cloud services, messaging) | ☐ |
| 3 | Agent-to-agent communication paths are mapped (which agents can delegate to or receive instructions from) | ☐ |
| 4 | Credential and permission scope for each agent is documented | ☐ |
| 5 | Data flows are mapped: what data enters the agent context (user input, RAG sources, tool outputs, memory) | ☐ |
| 6 | Production vs. staging assessment environment is confirmed (with rollback procedures if production) | ☐ |

### 2.2 Organizational Readiness

| # | Item | Status |
|---|---|---|
| 7 | Executive sponsor identified and rules of engagement signed | ☐ |
| 8 | Incident response team notified of assessment window | ☐ |
| 9 | Legal review completed (especially for assessments involving customer-facing agents) | ☐ |
| 10 | Baseline agent behavior documented (expected tool calls, response patterns, guardrail behaviors) | ☐ |
| 11 | Monitoring and logging confirmed operational for the assessment period | ☐ |
| 12 | Success criteria defined: what constitutes a critical, high, medium, and low finding | ☐ |

### 2.3 Technical Prerequisites

| # | Item | Status |
|---|---|---|
| 13 | Test accounts and credentials provisioned for assessment team | ☐ |
| 14 | Network access to agent endpoints confirmed | ☐ |
| 15 | Ability to inspect agent logs, tool call records, and memory state confirmed | ☐ |
| 16 | Snapshot or rollback capability for agent memory and persistent state | ☐ |
| 17 | Red team tooling installed and validated (PyRIT, Promptfoo, or equivalent) | ☐ |
| 18 | Communication channel established between red team and incident response | ☐ |

---

## 3. Twenty Questions Every Security Team Should Ask

Before any technical assessment, these questions expose architectural risk. If your engineering team cannot answer them clearly, that itself is a finding.

### Agent Architecture

1. **What can each agent do?** — Full inventory of tools, APIs, and system access per agent.
2. **What is the maximum blast radius?** — If an agent is fully compromised, what is the worst-case outcome given its current permissions?
3. **How are agent permissions scoped?** — Are tools limited by least-privilege principles, or does the agent inherit broad service account credentials?
4. **Can agents invoke other agents?** — If yes, is there authorization between them, or does any agent trust instructions from any other agent?
5. **What enters the context window?** — Enumerate every source: user input, system prompts, tool descriptions, RAG documents, tool results, memory, inter-agent messages.

### Data and Trust Boundaries

6. **Where does untrusted data enter the pipeline?** — User inputs, retrieved documents, third-party API responses, uploaded files, email content.
7. **Is there tenant isolation?** — In multi-tenant deployments, can one tenant's data or prompts influence another tenant's agent behavior?
8. **What data can the agent exfiltrate?** — If instructed to, could the agent send internal data to external endpoints via its tools?
9. **Are RAG sources validated?** — Who controls the documents in the retrieval pipeline? Can they be modified by external parties?
10. **Is agent memory tamper-proof?** — Can a user or injected instruction write to persistent memory that affects future sessions?

### Controls and Monitoring

11. **Are tool calls validated before execution?** — Is there a gatekeeper between the model's decision to call a tool and actual execution?
12. **Is there human-in-the-loop for high-risk actions?** — Which operations require human approval? How is this enforced — at the application layer or just the prompt?
13. **Can you reconstruct agent decision chains?** — Given a finding, can you trace back through every prompt, tool call, and intermediate result that led to the action?
14. **What guardrails exist, and how are they implemented?** — Prompt-level instructions, model-level safety filters, application-level validators, or infrastructure-level controls?
15. **Are guardrails tested adversarially?** — Have existing safety controls been tested against known bypass techniques?

### Governance and Compliance

16. **Is AI agent behavior auditable for regulatory purposes?** — Can you produce a complete decision trail for compliance review?
17. **How are AI-specific incidents classified?** — Does your incident response plan distinguish between traditional security incidents and AI-specific incidents (goal hijacking, memory poisoning, cascading failure)?
18. **What is the patching cadence for AI components?** — Model versions, MCP servers, plugins, RAG pipeline dependencies.
19. **Are third-party AI components inventoried?** — MCP servers, plugins, model providers, embedding services, vector databases.
20. **Who owns AI security risk?** — Is there a named individual responsible for AI security posture, or is it distributed across application security, infrastructure, and data teams?

---

## 4. Attack Pattern Quick Reference

This reference catalogs the OWASP Agentic Top 10 attack categories with severity ratings, detection difficulty, exploitability, and priority actions. Use this as the assessment scope baseline.

### Severity and Exploitability Key

- **Severity**: Critical / High / Medium — based on maximum impact when the attack succeeds
- **Detection**: Hard / Medium / Easy — how difficult the attack is to detect with standard monitoring
- **Exploitability**: High / Medium / Low — skill and access required to execute the attack

### ASI01 — Agent Goal Hijacking

| Attribute | Value |
|---|---|
| **Severity** | Critical |
| **Detection** | Hard |
| **Exploitability** | High |
| **MITRE ATLAS** | AML.T0051 (Prompt Injection), AML.T0054 (Jailbreak) |
| **CSA Category** | Goal & Instruction Manipulation |

**What happens**: The agent's intended objective is replaced by an attacker-controlled objective via direct or indirect prompt injection. The agent continues operating normally from the user's perspective but serves the attacker's goals.

**Attack vectors**: Direct prompt injection in user input. Indirect injection via retrieved documents, tool descriptions, API responses, or data labels. Multi-turn escalation (crescendo attacks). Meta-context injection where payload is embedded in environmental data (Docker labels, file metadata, configuration comments).

**Assessment test points**:

- [ ] Inject conflicting instructions in user input and verify the agent follows system prompt
- [ ] Plant instructions in retrievable documents and test whether the agent executes them
- [ ] Test tool descriptions for injected instructions that alter agent behavior
- [ ] Attempt multi-turn escalation: start benign, gradually introduce malicious instructions
- [ ] Test all data sources that enter the context window for injection potential

**Priority remediation**: Input/output filtering at application layer. Instruction hierarchy enforcement. Context isolation between trusted instructions and untrusted data.

---

### ASI02 — Tool Misuse and Exploitation

| Attribute | Value |
|---|---|
| **Severity** | Critical |
| **Detection** | Medium |
| **Exploitability** | High |
| **MITRE ATLAS** | AML.T0056 (Plugin Compromise), AML.T0049 (Exploit Public-Facing App) |
| **CSA Category** | Critical System Interaction |

**What happens**: Legitimate tools are invoked with unauthorized parameters, chained into destructive sequences, or triggered by injected context instead of genuine user intent.

**Attack vectors**: Parameter manipulation in tool calls. Tool chaining to achieve unauthorized objectives (e.g., read → modify → exfiltrate). Shadow tool installation via compromised MCP servers. Implicit tool invocation through conversation context. Exploiting tools that perform destructive actions without confirmation.

**Assessment test points**:

- [ ] Attempt to invoke tools with parameters outside documented ranges
- [ ] Chain multiple tool calls to achieve an objective no single tool should allow
- [ ] Test whether the agent calls tools based on injected context vs. genuine user request
- [ ] Verify destructive tool calls require explicit confirmation
- [ ] Test for path traversal, SQL injection, and command injection through tool parameters

**Priority remediation**: Tool call authorization layer. Parameter validation and sanitization. Allowlists for tool call sequences. Human approval for destructive operations.

---

### ASI03 — Identity and Authorization Failures

| Attribute | Value |
|---|---|
| **Severity** | Critical |
| **Detection** | Hard |
| **Exploitability** | Medium |
| **MITRE ATLAS** | AML.T0049 (Exploit Public-Facing App) |
| **CSA Category** | Authorization & Control Hijacking |

**What happens**: Agents operate with excessive privileges, share credentials between sessions or tenants, accept forged identity claims, or escalate privileges through tool access.

**Assessment test points**:

- [ ] Map the actual permissions each agent holds vs. the minimum required
- [ ] Test whether agents can access resources belonging to other tenants or users
- [ ] Verify that agent credentials are scoped to the minimum necessary tools and actions
- [ ] Attempt privilege escalation through tool chaining (use one tool's output to unlock another)
- [ ] Test whether agents verify identity claims in inter-agent communication

**Priority remediation**: Least-privilege agent credentials. Per-session credential scoping. Inter-agent authentication. Permission boundary enforcement at the infrastructure layer.

---

### ASI04 — Supply Chain Vulnerabilities

| Attribute | Value |
|---|---|
| **Severity** | High |
| **Detection** | Hard |
| **Exploitability** | Medium |
| **MITRE ATLAS** | AML.T0053 (Adversarial ML Supply Chain) |
| **CSA Category** | Supply Chain & Dependency |

**What happens**: Malicious or vulnerable components enter the agent stack — compromised MCP servers, npm packages, model providers, plugins, or embedding services.

**Assessment test points**:

- [ ] Inventory all third-party components: MCP servers, plugins, model APIs, embedding services
- [ ] Verify source integrity and version pinning for all dependencies
- [ ] Test for "rug pull" scenarios: tool behavior change after initial trust establishment
- [ ] Scan MCP server tool descriptions for hidden instructions or obfuscated payloads
- [ ] Verify that supply chain monitoring covers AI-specific components, not just code dependencies

**Priority remediation**: Component inventory and provenance verification. Tool description scanning (mcp-scan or equivalent). Version pinning. Runtime integrity monitoring.

---

### ASI05 — Insecure Output Handling

| Attribute | Value |
|---|---|
| **Severity** | High |
| **Detection** | Medium |
| **Exploitability** | High |
| **MITRE ATLAS** | AML.T0048 (Exfiltration via ML Inference API) |
| **CSA Category** | Critical System Interaction |

**What happens**: Agent outputs are consumed by downstream systems (web applications, databases, other agents) without sanitization, enabling injection attacks, data exfiltration, or cross-system contamination.

**Assessment test points**:

- [ ] Test whether agent output containing code or markup is executed by downstream consumers
- [ ] Verify output sanitization before database insertion, web rendering, or email sending
- [ ] Test for exfiltration via agent output (embedding sensitive data in apparently benign responses)
- [ ] Verify that agents cannot generate outputs that trigger actions in consuming applications

**Priority remediation**: Output sanitization pipeline. Content type enforcement. Structured output schemas. Downstream input validation independent of agent output.

---

### ASI06 — Knowledge and Memory Poisoning

| Attribute | Value |
|---|---|
| **Severity** | High |
| **Detection** | Hard |
| **Exploitability** | Medium |
| **MITRE ATLAS** | AML.T0043 (Craft Adversarial Data) |
| **CSA Category** | Knowledge Base Poisoning, Memory & Context Manipulation |

**What happens**: False or malicious data is planted in RAG sources, vector databases, or persistent agent memory, causing the agent to reason from corrupted knowledge in current and future sessions.

**Assessment test points**:

- [ ] Inject adversarial documents into RAG sources and verify whether the agent retrieves and trusts them
- [ ] Test whether agents can be instructed to write to their own persistent memory
- [ ] Plant contradictory information across knowledge sources and observe agent behavior
- [ ] Verify that knowledge sources have integrity controls and access restrictions
- [ ] Test memory isolation between tenants, users, and sessions

**Priority remediation**: RAG source access control and integrity verification. Memory write authorization. Source attribution in agent reasoning. Memory isolation boundaries.

---

### ASI07 — Insecure Inter-Agent Communication

| Attribute | Value |
|---|---|
| **Severity** | Critical |
| **Detection** | Hard |
| **Exploitability** | Medium |
| **MITRE ATLAS** | AML.T0051 (Prompt Injection) |
| **CSA Category** | Multi-Agent Exploitation |

**What happens**: In multi-agent architectures, agents send unverified messages to each other. A compromised or poisoned agent propagates malicious instructions through the communication fabric.

**Assessment test points**:

- [ ] Test whether agents validate the source and integrity of messages from other agents
- [ ] Inject malicious context into an upstream agent and verify whether downstream agents execute it
- [ ] Test orchestrator manipulation: can modifying the orchestrator's context redirect all sub-agents?
- [ ] Verify that inter-agent communication is logged with full provenance
- [ ] Test trust propagation: does trust in agent A automatically extend to agent A's delegated subtasks?

**Priority remediation**: Inter-agent authentication and message signing. Context sanitization at agent boundaries. Orchestrator hardening. Independent validation of delegated instructions.

---

### ASI08 — Cascading Failures

| Attribute | Value |
|---|---|
| **Severity** | Critical |
| **Detection** | Medium |
| **Exploitability** | Medium |
| **MITRE ATLAS** | AML.T0043 (Craft Adversarial Data), AML.T0051 (Prompt Injection) |
| **CSA Category** | Impact Chain & Blast Radius |

**What happens**: A single point of compromise — one poisoned document, one manipulated tool response, one injected instruction — amplifies through the agent pipeline, affecting multiple agents, systems, and decisions.

**Assessment test points**:

- [ ] Map cascade paths: which single points of failure can affect multiple downstream agents?
- [ ] Inject a poisoned input at the earliest stage and trace how far it propagates
- [ ] Test circuit breakers: does the system halt when anomalous behavior is detected?
- [ ] Verify blast radius containment: are there isolation boundaries between agent domains?
- [ ] Test resource exhaustion: can a crafted input trigger infinite loops or exponential tool calls?

**Priority remediation**: Circuit breakers at agent boundaries. Blast radius analysis and containment zones. Rate limiting on tool calls. Independent validation at each pipeline stage.

---

### ASI09 — Human Trust Exploitation

| Attribute | Value |
|---|---|
| **Severity** | Medium |
| **Detection** | Hard |
| **Exploitability** | High |
| **MITRE ATLAS** | AML.T0052 (Phishing via AI) |
| **CSA Category** | Checker-Out-of-the-Loop |

**What happens**: Users over-trust agent outputs, approve dangerous actions without review, or assume agent-generated content is verified. The agent becomes a social engineering vector.

**Assessment test points**:

- [ ] Test whether users review agent actions before approval or rubber-stamp them
- [ ] Generate intentionally incorrect but plausible outputs and measure user acceptance rate
- [ ] Verify that high-risk actions are flagged with clear risk indicators
- [ ] Test whether the system distinguishes between agent-originated content and verified sources
- [ ] Assess approval workflow fatigue: do users approve more readily after repeated benign requests?

**Priority remediation**: Graduated approval workflows based on action risk. Clear provenance labeling. Mandatory review for irreversible actions. User training on AI trust calibration.

---

### ASI10 — Agent Untraceability

| Attribute | Value |
|---|---|
| **Severity** | High |
| **Detection** | Easy |
| **Exploitability** | N/A (enabler for other attacks) |
| **MITRE ATLAS** | N/A (operational gap) |
| **CSA Category** | Agent Untraceability |

**What happens**: Insufficient logging, missing correlation IDs, or incomplete audit trails prevent reconstruction of what an agent did, why it did it, and what data it accessed. This makes incident response impossible and compliance audits unreliable.

**Assessment test points**:

- [ ] Trigger a multi-step agent action and attempt to reconstruct the full decision chain from logs
- [ ] Verify that every tool call is logged with timestamp, parameters, result, and context
- [ ] Test whether logs capture the full prompt context at each decision point
- [ ] Verify log tamper resistance — can the agent modify its own audit trail?
- [ ] Assess whether logs support regulatory timeline requirements (GDPR 72-hour breach notification, etc.)

**Priority remediation**: Structured logging with correlation IDs. Immutable audit trails. Full context capture at each decision point. Automated anomaly alerting on log patterns.

---

## 5. Framework Cross-Reference Matrix

Use this matrix to align your assessment findings with multiple compliance frameworks simultaneously. Each row is an attack category with its mapping across OWASP, MITRE ATLAS, CSA, and NIST AI RMF.

| Attack Category | OWASP Agentic | MITRE ATLAS | CSA Red Team Guide | NIST AI RMF |
|---|---|---|---|---|
| Goal Hijacking / Prompt Injection | ASI01 | AML.T0051, AML.T0054 | Goal & Instruction Manipulation | GOVERN 1.2, MAP 3.4 |
| Tool Misuse / Exploitation | ASI02 | AML.T0056, AML.T0049 | Critical System Interaction | MANAGE 2.2, MAP 3.5 |
| Identity / Authorization Failure | ASI03 | AML.T0049 | Authorization & Control Hijacking | GOVERN 1.4, MANAGE 4.1 |
| Supply Chain Compromise | ASI04 | AML.T0053 | Supply Chain & Dependency | MAP 3.3, MANAGE 3.1 |
| Insecure Output Handling | ASI05 | AML.T0048 | Critical System Interaction | MANAGE 2.3 |
| Knowledge / Memory Poisoning | ASI06 | AML.T0043 | Knowledge Base Poisoning, Memory & Context Manipulation | MAP 2.3, MANAGE 2.2 |
| Inter-Agent Communication Failure | ASI07 | AML.T0051 | Multi-Agent Exploitation | GOVERN 1.2, MANAGE 4.2 |
| Cascading Failure / Blast Radius | ASI08 | AML.T0043, AML.T0051 | Impact Chain & Blast Radius | MAP 5.1, MANAGE 2.4 |
| Human Trust Exploitation | ASI09 | AML.T0052 | Checker-Out-of-the-Loop | GOVERN 3.2, MAP 3.5 |
| Untraceability / Audit Gaps | ASI10 | — | Agent Untraceability | GOVERN 1.5, MANAGE 4.1 |

### How to Use This Matrix

**For compliance reporting**: Map each finding to the relevant column for the framework your organization reports against. Include the specific technique ID in your finding report.

**For gap analysis**: Walk down each column. If your assessment program does not cover a row, that is an untested risk category.

**For executive communication**: Use the OWASP column as the primary reference (most widely recognized). Use NIST AI RMF for regulated industries.

---

## 6. Five-Phase Assessment Lifecycle

Structure every red team engagement around these five phases. Each phase has defined inputs, activities, and outputs.

### Phase 1 — Reconnaissance and Scope

**Objective**: Map the agent attack surface before testing begins.

| Activity | Output |
|---|---|
| Identify all agents, their purposes, and deployment environments | Agent inventory |
| Document tool access per agent (APIs, databases, services, MCP servers) | Tool access matrix |
| Map data flows: what enters and exits the context window | Data flow diagram |
| Identify agent-to-agent communication paths | Agent interaction map |
| Document credential scope per agent | Permission inventory |
| Establish rules of engagement and communication protocols | Signed ROE document |

**Key deliverable**: Attack surface map showing every entry point, tool, credential, and communication channel in scope.

### Phase 2 — Threat Modeling

**Objective**: Prioritize attack scenarios based on impact and likelihood.

| Activity | Output |
|---|---|
| Map each agent's tool access to potential abuse scenarios | Threat scenario list |
| Identify high-value targets: what data or systems would an attacker want to reach? | Target priority list |
| Cross-reference with Section 4 attack patterns relevant to this architecture | Attack pattern shortlist |
| Assess agent-specific blast radius for each scenario | Blast radius matrix |
| Define success criteria: what constitutes exploitation vs. failed attempt | Assessment criteria |

**Key deliverable**: Prioritized threat model ranking attack scenarios by (blast radius × exploitability × detection difficulty).

### Phase 3 — Attack Execution

**Objective**: Systematically test each prioritized attack scenario.

Use the four-layer testing strategy — execute each layer before escalating to the next:

| Layer | What You Test | Techniques |
|---|---|---|
| **Layer 1: Direct Prompt Attacks** | Model-level resilience to direct injection and jailbreak | Single-turn injection, role-play attacks, encoding bypass, instruction override |
| **Layer 2: Tool and Integration Attacks** | Tool call authorization, parameter validation, tool chaining | Unauthorized parameters, destructive tool calls, tool sequence exploitation, path traversal via tools |
| **Layer 3: Multi-Agent and Pipeline Attacks** | Inter-agent trust, orchestrator security, cascade propagation | Orchestrator manipulation, delegation poisoning, trust chain exploitation, cascading injection |
| **Layer 4: Persistent and Environmental Attacks** | Memory poisoning, RAG contamination, supply chain integrity | Memory injection, RAG document poisoning, MCP tool description manipulation, environmental data injection |

**Key deliverable**: Finding log with exploitation evidence, reproduction steps, and impact classification for each successful attack.

### Phase 4 — Impact Analysis

**Objective**: Classify findings by severity and business impact.

For each finding, assess:

| Dimension | Question to Answer |
|---|---|
| **Confidentiality impact** | What data was accessible or exfiltrated? |
| **Integrity impact** | What data or systems were modified? |
| **Availability impact** | What services were disrupted or degraded? |
| **Blast radius** | How many agents, systems, users, or tenants were affected? |
| **Persistence** | Is the impact temporary (single session) or persistent (affects future sessions)? |
| **Detection gap** | Would this attack be detected by current monitoring within the required response timeline? |

Apply the severity scoring framework in Section 7 to each finding.

**Key deliverable**: Classified finding list with severity scores, business impact assessments, and detection gap analysis.

### Phase 5 — Reporting and Remediation Planning

**Objective**: Deliver actionable findings with clear remediation priorities.

Use the report template in Section 9. Ensure each finding includes:

- Reproduction steps (another engineer can recreate the issue)
- Impact analysis (what happened and what could happen)
- Remediation recommendation (specific, actionable, with priority)
- Framework mapping (OWASP ASI code, MITRE ATLAS technique, CSA category)
- Verification criteria (how to confirm the fix works)

**Key deliverable**: Assessment report using the template in Section 9. Remediation roadmap using the template in Section 10.

---

## 7. Severity Scoring Framework

Use this framework to consistently classify findings across assessments.

### Base Severity

| Level | Criteria | Examples |
|---|---|---|
| **Critical** | Direct data exfiltration, unauthorized system modification, full agent compromise, cross-tenant access | Goal hijacking leading to data exfiltration. Tool misuse enabling infrastructure modification. Cascading failure affecting production systems. |
| **High** | Significant data exposure, privilege escalation, persistent state poisoning, guardrail bypass | Memory poisoning affecting future sessions. Identity spoofing between agents. Supply chain compromise enabling tool manipulation. |
| **Medium** | Limited data exposure, non-persistent manipulation, degraded functionality | Single-session goal diversion. Information disclosure through verbose errors. Partial guardrail bypass with limited impact. |
| **Low** | Minor information disclosure, cosmetic manipulation, theoretical risk without demonstrated exploit | Agent reveals internal tool names. Verbose error messages expose architecture details. Minor prompt leakage with no operational impact. |

### AI-Specific Severity Modifiers

Apply these modifiers to adjust the base severity when AI-specific factors increase or decrease the actual risk.

| Modifier | Condition | Adjustment |
|---|---|---|
| **+1 level** | Attack persists across sessions (memory poisoning, RAG contamination) | Persistent attacks are more dangerous because they affect future users and sessions without re-exploitation |
| **+1 level** | Attack cascades to additional agents or systems | Cascading impact multiplies the blast radius beyond the initial target |
| **+1 level** | Attack is undetectable by current monitoring | An undetectable critical finding is an existential risk |
| **−1 level** | Attack requires specific preconditions unlikely in production | Theoretical attacks with complex prerequisites are lower priority for immediate remediation |
| **−1 level** | Attack impact is contained by existing non-AI controls | Infrastructure-level controls (network segmentation, least privilege) may limit blast radius |

### Severity Decision Tree

```
START: Can the attack exfiltrate data or modify systems?
├── YES → Can it affect multiple tenants, agents, or sessions?
│   ├── YES → CRITICAL
│   └── NO → Does it persist across sessions?
│       ├── YES → CRITICAL (modifier: +1 from High)
│       └── NO → HIGH
└── NO → Can it degrade agent functionality or expose information?
    ├── YES → Is the exposure significant (credentials, PII, architecture)?
    │   ├── YES → HIGH
    │   └── NO → MEDIUM
    └── NO → LOW
```

---

## 8. Tool Selection Decision Matrix

Select assessment tooling based on your environment, team capability, and assessment objectives.

### Primary Tools

| Tool | Best For | Complexity | Multi-Turn | Agent-Specific | Integration |
|---|---|---|---|---|---|
| **PyRIT** (Microsoft) | Automated multi-turn attacks, crescendo/TAP strategies | High | Yes | Partial | Python SDK, Azure-native |
| **Promptfoo** | Broad vulnerability scanning, compliance mapping, CI/CD integration | Medium | Yes | Yes (133 plugins) | YAML config, CLI, CI/CD |
| **Garak** (NVIDIA) | Model-level vulnerability probing, 37+ attack probes | Medium | Limited | Limited | Python, CLI |
| **AgentDojo** (ETH Zurich) | Benchmarking agent task performance under attack | High | Yes | Yes (629 test cases) | Python, research-oriented |
| **mcp-scan** (Invariant Labs) | MCP server tool description scanning for hidden payloads | Low | N/A | Yes | CLI |

### Selection Criteria

| If Your Priority Is... | Recommended Tool(s) |
|---|---|
| Broadest coverage across OWASP/MITRE/NIST | Promptfoo (133 plugins, framework mappings built in) |
| Multi-turn, escalating attacks (crescendo, TAP) | PyRIT (purpose-built for multi-turn orchestration) |
| MCP server supply chain scanning | mcp-scan (lightweight, focused) |
| Model-level safety testing | Garak (37+ specialized probes) |
| CI/CD integration and continuous testing | Promptfoo (native CI/CD support, YAML configuration) |
| Research-grade agent benchmarking | AgentDojo (629 standardized test cases) |
| Air-gapped or restricted environments | PyRIT with local models (supports local LLM targets) |

### Minimum Viable Toolset

For most enterprise assessments, the following combination covers all OWASP ASI categories:

1. **Promptfoo** — Baseline scanning across all ten ASI categories with compliance-mapped reporting
2. **PyRIT** — Deep-dive multi-turn attacks on critical findings from Promptfoo
3. **mcp-scan** — Supply chain scan of all MCP server tool descriptions

This three-tool stack provides automated coverage, targeted exploitation, and supply chain verification.

---

## 9. Assessment Report Template

Use this template structure for all red team assessment reports. Each section is required.

---

### Report Section 1: Executive Summary

| Field | Content |
|---|---|
| **Assessment date** | [Date range] |
| **Scope** | [Agents, systems, and environments tested] |
| **Methodology** | [Frameworks used: OWASP Agentic Top 10, MITRE ATLAS, CSA] |
| **Overall risk rating** | [Critical / High / Medium / Low] |
| **Critical findings** | [Count and one-sentence summary of each] |
| **Key recommendation** | [Single most important action to take] |

---

### Report Section 2: Scope and Methodology

- Agents tested (names, versions, deployment environments)
- Tools and techniques used (reference Section 8)
- Assessment layers completed (reference Section 6, Phase 3)
- Limitations and exclusions
- Rules of engagement summary

---

### Report Section 3: Finding Summary

| # | Finding Title | Severity | OWASP ASI | MITRE ATLAS | Status |
|---|---|---|---|---|---|
| 1 | [Title] | [Critical/High/Medium/Low] | [ASI0X] | [AML.T00XX] | [Open/Mitigated] |
| 2 | [Title] | ... | ... | ... | ... |

---

### Report Section 4: Detailed Findings

For each finding, provide:

```
FINDING: [Title]
SEVERITY: [Critical / High / Medium / Low] (with modifiers applied per Section 7)
FRAMEWORK MAPPING: OWASP [ASI0X] | MITRE ATLAS [AML.T00XX] | CSA [Category]

DESCRIPTION:
[What the vulnerability is.]

REPRODUCTION STEPS:
1. [Step-by-step reproduction that another engineer can follow]
2. [Include exact inputs, tool calls, and expected results]

EVIDENCE:
[Screenshots, logs, tool call records, agent responses]

IMPACT ANALYSIS:
- Confidentiality: [What data was/could be exposed]
- Integrity: [What was/could be modified]
- Availability: [What was/could be disrupted]
- Blast radius: [How far the impact extends]
- Persistence: [Single session / Cross-session / Permanent]

REMEDIATION:
- [Specific, actionable fix]
- [Implementation guidance]
- [Priority: Immediate / Next sprint / Next quarter]

VERIFICATION:
- [How to confirm the fix is effective]
- [Regression test to add to CI/CD]
```

---

### Report Section 5: Risk Matrix

| | Low Exploitability | Medium Exploitability | High Exploitability |
|---|---|---|---|
| **Critical Impact** | High Priority | Critical Priority | Critical Priority |
| **High Impact** | Medium Priority | High Priority | Critical Priority |
| **Medium Impact** | Low Priority | Medium Priority | High Priority |
| **Low Impact** | Informational | Low Priority | Medium Priority |

---

### Report Section 6: Remediation Roadmap

See Section 10 for the full roadmap template.

---

### Report Section 7: Assessment Coverage

| OWASP ASI Category | Tested | Finding Count | Notes |
|---|---|---|---|
| ASI01 — Goal Hijacking | [Yes/No/Partial] | [#] | |
| ASI02 — Tool Misuse | [Yes/No/Partial] | [#] | |
| ASI03 — Identity Failures | [Yes/No/Partial] | [#] | |
| ASI04 — Supply Chain | [Yes/No/Partial] | [#] | |
| ASI05 — Insecure Output | [Yes/No/Partial] | [#] | |
| ASI06 — Memory Poisoning | [Yes/No/Partial] | [#] | |
| ASI07 — Inter-Agent Comms | [Yes/No/Partial] | [#] | |
| ASI08 — Cascading Failures | [Yes/No/Partial] | [#] | |
| ASI09 — Human Trust | [Yes/No/Partial] | [#] | |
| ASI10 — Untraceability | [Yes/No/Partial] | [#] | |

---

### Report Section 8: Appendices

- Full tool call logs
- Agent conversation transcripts
- Configuration files used for automated testing
- Raw Promptfoo/PyRIT output reports

---

## 10. 90-Day Remediation Roadmap Template

Structure remediation in three phases. Each phase builds on the previous one.

### Days 1–30: Critical and Quick Wins

| # | Action | Target | Owner | Deadline | Status |
|---|---|---|---|---|---|
| 1 | Implement tool call authorization layer | All agents | [Name] | Day 7 | ☐ |
| 2 | Scope agent credentials to least privilege | All agents | [Name] | Day 14 | ☐ |
| 3 | Enable structured logging with correlation IDs | All agents | [Name] | Day 14 | ☐ |
| 4 | Deploy input validation on all user-facing agent endpoints | User-facing agents | [Name] | Day 21 | ☐ |
| 5 | Scan all MCP servers for tool description anomalies | MCP infrastructure | [Name] | Day 7 | ☐ |
| 6 | Implement human-in-the-loop for destructive tool operations | Production agents | [Name] | Day 30 | ☐ |

### Days 31–60: Structural Controls

| # | Action | Target | Owner | Deadline | Status |
|---|---|---|---|---|---|
| 7 | Implement inter-agent authentication | Multi-agent pipelines | [Name] | Day 45 | ☐ |
| 8 | Deploy context sanitization at agent boundaries | All agent boundaries | [Name] | Day 45 | ☐ |
| 9 | Implement RAG source integrity verification | RAG pipelines | [Name] | Day 50 | ☐ |
| 10 | Deploy circuit breakers for cascading failure protection | Multi-agent pipelines | [Name] | Day 50 | ☐ |
| 11 | Establish tenant isolation boundaries for memory and context | Multi-tenant agents | [Name] | Day 60 | ☐ |
| 12 | Implement output sanitization pipeline for downstream consumers | All agents with downstream integration | [Name] | Day 60 | ☐ |

### Days 61–90: Governance and Continuous Testing

| # | Action | Target | Owner | Deadline | Status |
|---|---|---|---|---|---|
| 13 | Integrate automated red team testing into CI/CD pipeline | All agent deployments | [Name] | Day 75 | ☐ |
| 14 | Establish AI-specific incident response playbook | Security operations | [Name] | Day 75 | ☐ |
| 15 | Deploy continuous monitoring for anomalous agent behavior | Production agents | [Name] | Day 80 | ☐ |
| 16 | Conduct tabletop exercise using assessment findings | Security + Engineering teams | [Name] | Day 85 | ☐ |
| 17 | Schedule next red team assessment (quarterly cadence) | All agents | [Name] | Day 90 | ☐ |
| 18 | Update AI component inventory and supply chain monitoring | All AI components | [Name] | Day 90 | ☐ |

---

## 11. Executive One-Pager: Agentic AI Security Risk

_This page is designed to be printed and presented to executive leadership or board-level stakeholders in 5 minutes or less._

---

### The Risk

Your organization is deploying AI agents — systems that autonomously plan, execute tasks, access tools, and make decisions. Unlike traditional software, these systems have non-deterministic behavior and an attack surface that scales with their access permissions, not their code complexity.

**A single prompt injection into an AI agent with production access can exfiltrate data, modify systems, and propagate through your entire agent pipeline — all within seconds, all within the agent's legitimate credential scope.**

### The Gap

Your existing security program (penetration testing, code review, WAF, SOC2 controls) was not designed for AI agents. Industry frameworks are now available:

- **OWASP Agentic Top 10** — 10 risk categories specific to autonomous AI systems
- **MITRE ATLAS** — 155 adversarial techniques for AI/ML systems
- **CSA Agentic AI Red Teaming Guide** — 12 threat categories with structured testing methods
- **NIST AI RMF** — Governance framework for AI risk management

### The Ask

| Action | Timeline | Investment |
|---|---|---|
| Conduct first agentic AI red team assessment | 30 days | Assessment team allocation (internal or contracted) |
| Implement critical remediation (tool authorization, credential scoping, logging) | 60 days | Engineering sprint allocation |
| Establish continuous AI security testing in CI/CD | 90 days | Tooling and process integration |
| Quarterly re-assessment cadence | Ongoing | Recurring assessment cycle |

### What Success Looks Like

- Every AI agent has a documented attack surface and threat model.
- Tool calls are authorized, logged, and rate-limited.
- Inter-agent communication is authenticated.
- Red team findings are remediated within SLA, tracked, and verified.
- AI-specific incidents have a dedicated response playbook.
- Assessment coverage spans all ten OWASP ASI categories.

---

## Framework and Tool Reference

### Standards and Frameworks

| Framework | Source | Version/Date | URL |
|---|---|---|---|
| OWASP Agentic Top 10 | OWASP Foundation | December 2025 | [genai.owasp.org](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications/) |
| MITRE ATLAS | MITRE Corporation | October 2025 update | [atlas.mitre.org](https://atlas.mitre.org/) |
| CSA Agentic AI Red Teaming Guide | Cloud Security Alliance | May 2025 | [cloudsecurityalliance.org](https://cloudsecurityalliance.org/artifacts/agentic-ai-red-teaming-guide) |
| NIST AI RMF | NIST | AI 100-1 (2023), AI 600-1 (2024) | [nist.gov](https://www.nist.gov/artificial-intelligence) |

### Assessment Tools

| Tool | Maintainer | License | URL |
|---|---|---|---|
| PyRIT | Microsoft | MIT | [github.com/Azure/PyRIT](https://github.com/Azure/PyRIT) |
| Promptfoo | Promptfoo Inc. | MIT | [promptfoo.dev](https://www.promptfoo.dev/) |
| Garak | NVIDIA | Apache 2.0 | [github.com/NVIDIA/garak](https://github.com/NVIDIA/garak) |
| AgentDojo | ETH Zurich | MIT | [github.com/ethz-spylab/agentdojo](https://github.com/ethz-spylab/agentdojo) |
| mcp-scan | Invariant Labs | MIT | [github.com/invariantlabs-ai/mcp-scan](https://github.com/invariantlabs-ai/mcp-scan) |

---

_This playbook is maintained by [Amine Raji](/) and updated as frameworks and tools evolve. For a hands-on walkthrough of the attack patterns referenced in this guide, see the companion article on [red teaming agentic AI with PyRIT and Promptfoo](/posts/attack-patterns-red-teaming/). For a complimentary assessment of your AI security posture, [schedule a 30-minute review](/consultation/)._
