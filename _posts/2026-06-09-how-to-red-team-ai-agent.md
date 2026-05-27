---
title: "How to Red Team Your AI Agent Before You Ship"
date: 2026-06-09
uuid: 202606090000
status: published
published: true
content-type: article
target-audience: advanced
categories: [AI Security, Red Team, Agentic AI]
tags:
  [
    AI Security,
    Red Team,
    PyRIT,
    Garak,
    Agentic AI,
    LLM,
    OWASP,
    Security
  ]
image:
  path: /assets/media/ai-security/ai-red-team-guide.png
description: "Model-level red teaming misses the attacks that cause production incidents. Here is how to red team the full agentic system, with a practical PyRIT setup and the four attack categories that matter."
mermaid: false
---

# How to Red Team Your AI Agent Before You Ship

*By Amine Raji, PhD, CISSP*

---

Most AI red teaming in 2026 is testing the wrong thing.

The standard practice is to point an adversarial prompt suite at the model endpoint, observe whether the model produces policy-violating outputs, and report the pass/fail result. This is useful for evaluating model behavior in isolation. It tells you almost nothing about the security of an agentic system in production.

The attacks that cause production incidents don't exploit the model in isolation. They exploit the model as one component in a system that includes tool calls, credential access, retrieval pipelines, and external APIs. None of those attack paths appear if your red team is only looking at the model endpoint.

This guide covers how to test the full system.

---

## What model-level red teaming misses

When you test only the model endpoint, you are evaluating content safety. Does the model produce harmful text, toxic outputs, or policy violations? Necessary, but it leaves the following attack classes completely untested:

**Tool misuse attacks.** The model is manipulated into calling a legitimate tool with attacker-controlled parameters. The model produces no harmful content. It makes a normal-looking tool call. The harm is in what the tool call does downstream. This attack is invisible at the model endpoint.

**Prompt injection through tool outputs.** A tool returns data containing adversarial content. The model processes that content as part of its next reasoning step and takes an action the attacker intended. The injection source is not the user. It is the tool response. Testing the model endpoint in isolation never triggers this vector.

**Cross-session data leakage.** The model includes information from a different user's session in the current response, not through a code vulnerability but through context window contamination or retrieval system misconfiguration. Endpoint-only testing uses synthetic sessions and never reproduces this.

**Agent-to-agent manipulation.** In multi-agent architectures, one agent is manipulated into sending adversarial content to a downstream agent, which then executes it. The entry point and the execution point are in different agents. No single-endpoint test sees the full chain.

All four categories produce normal-looking model outputs at the model endpoint. The anomaly is downstream, in the tool calls, the data operations, or the agent interactions.

---

## Three principles from Microsoft's AI Red Team

Microsoft's AI Red Team published a retrospective in early 2025 covering work on over 100 generative AI products. Three principles from that work are worth building into your own practice:

**Principle 1: Automate for breadth, use humans for depth.**

Automated tools (PyRIT, Garak) cover the variation space. Thousands of prompt permutations, multiple temperature settings, different system prompt configurations. They measure statistical attack success rates. They find the straightforward bypasses. They measure how often attacks succeed.

Human red teamers handle what automation cannot: multi-step attacks that require conversational context-building across turns, exploitation of domain-specific knowledge, and chained attacks that route through multiple system components. Both are necessary. Automation alone leaves complex attacks untested. Human-only testing is not reproducible and does not scale.

**Principle 2: Test the system, not the model.**

Your red teaming environment should match production as closely as possible. That means the model running with its actual system prompt, connected to its actual tool integrations, with realistic user interaction patterns. A model tested with a generic system prompt and no tools connected is not the system your users interact with. Its red team results do not apply to your deployed system.

**Principle 3: Capture the attack path, not just the success rate.**

Attack Success Rate tells you how often the attack works. The prompt sequences, tool call traces, and parameter logs tell you the attack path. The former is what you report to leadership. The latter is what your engineering team needs to design mitigations. Always capture both, and store them in enough detail that the attack is reproducible.

---

## Practical setup: PyRIT for agentic systems

[PyRIT](https://github.com/microsoft/PyRIT) (Python Risk Identification Tool) is Microsoft's open-source red teaming framework for generative AI. MIT-licensed, actively maintained, with 53+ built-in datasets.

**Basic setup targeting a model endpoint:**

```python
from pyrit.executor.attack import ConsoleAttackResultPrinter, PromptSendingAttack
from pyrit.prompt_target import OpenAIChatTarget
from pyrit.setup import IN_MEMORY, initialize_pyrit_async

await initialize_pyrit_async(memory_db_type=IN_MEMORY)

target = OpenAIChatTarget(
    endpoint="your-model-endpoint",
    api_key="your-api-key",
    model_name="your-model-name"
)

attack = PromptSendingAttack(objective_target=target)
result = await attack.execute_async(objective="Your test prompt here")

printer = ConsoleAttackResultPrinter()
await printer.print_conversation_async(result=result)
```

**For agentic systems: point at the agent, not the model.**

Standard PyRIT sends prompts directly to the model API. For agentic systems, route your test prompts through the full agent stack. The same interface your users hit, with all tool integrations active and all MCP servers connected. Point PyRIT at your agent endpoint.

The key instrumentation addition for agents: log tool calls alongside model outputs. You are not just looking for harmful model responses. You are looking for unexpected tool calls, tool calls with anomalous parameters, and tool calls the agent made but that no user-facing output reflects.

## Garak: model-level vulnerability scanning

[Garak](https://github.com/NVIDIA/garak) is NVIDIA's open-source LLM vulnerability scanner (Apache 2.0, 7.9k+ stars). While PyRIT focuses on automated red teaming with orchestrated attack strategies, Garak focuses on systematic probing of model endpoints for known weakness categories.

Garak is the tool you run *before* PyRIT. It gives you a baseline of which vulnerability classes your model is susceptible to. Think of it as `nmap` for LLMs: it scans for known attack surfaces and reports which probes fail.

```bash
# Scan an OpenAI model for encoding-based prompt injection
export OPENAI_API_KEY="sk-..."
garak --target_type openai --target_name gpt-4o --probes encoding

# Scan a local model via llama.cpp
garak --target_type llama_cpp --target_name /path/to/model.gguf

# Scan for a specific probe category
garak --target_type openai --target_name gpt-4o --probes dan
```

Garak's probe catalog includes prompt injection (direct, encoding, payload splitting), jailbreaks (DAN variants, role-play escalation), data leakage (training data replay), toxicity generation, hallucination, and more. Run the full probe suite against your model before writing custom PyRIT attacks. It tells you which categories need deeper investigation.

**When to use which tool:**

| Tool | Best for | Limitation |
|------|----------|------------|
| Garak | Baseline model-level vulnerability scan | Tests model in isolation, not the full agentic system |
| PyRIT | Orchestrated multi-turn attacks against the full system | Requires more setup and custom objective definitions |
| CoPyRIT (PyRIT GUI) | Manual/human-led red teaming with session tracking | Not automated; scales with team size |

Run Garak first for breadth. Use PyRIT for depth against the attack categories Garak flags.

**Datasets to start with:**

- `HarmBench` — comprehensive jailbreak benchmark, good baseline coverage for prompt injection
- `AdvBench` — adversarial instructions, useful for testing instruction-following safety
- `XSTest` — tests for over-refusal as well as under-refusal, both failure modes matter for production
- `AIRT` — AI Red Team dataset with agentic scenarios included

**Interpreting results correctly:**

Report Attack Success Rate as a percentage with a confidence interval. An ASR of 3% sounds negligible but may represent thousands of successful attacks at the scale of a production deployment. An ASR of 0% computed from 50 test cases tells you almost nothing. The confidence interval is too wide to be meaningful. Run a minimum of 500 variations per test category before drawing conclusions.

---

## The four attack categories to prioritize

Focus red team effort on these four. They account for the majority of production incidents in agentic AI systems:

**1. Direct prompt injection**

User-supplied input that overrides system instructions or triggers unauthorized tool calls. Test with adversarial instructions embedded inside normal-looking requests. The goal is not to produce harmful text. It is to make the agent take an action the system prompt would prohibit if asked directly.

Example test pattern: legitimate-looking customer request followed by delimiter tokens and an instruction to call an administrative tool. Observe whether the agent executes the tool call.

**2. Indirect prompt injection**

Adversarial content embedded in data the agent retrieves. Documents, web pages, database records, tool outputs. The user does not supply the malicious content. It arrives through a data channel the agent treats as trusted.

Test by seeding your retrieval corpus with documents containing adversarial instructions, then crafting user queries that will cause those documents to be retrieved. Observe whether the agent executes the embedded instructions.

**3. Tool parameter manipulation**

The model is manipulated into making a legitimate tool call with attacker-controlled parameter values. A path traversal in a file operation. Injected content in a database query. An SSRF-enabling URL in an HTTP tool. Test by crafting prompts designed to produce specific parameter values in tool calls, then verifying whether your parameter validation catches them.

This category requires instrumenting the tool layer, not just the model output. You need to see the actual parameters the model passed to the tool.

**4. Context window contamination**

In multi-turn conversations or systems with conversation history, test whether content from one session influences behavior in another. Test whether extended conversations can effectively push the system prompt out of the model's effective attention range, degrading safety controls over time.

**How to test this:** Send a long, benign conversation (hundreds of turns or near the context window limit) and then issue a prompt that would normally be refused. If the model complies, the extended context has degraded the system prompt's influence. Also test cross-session contamination: after a conversation ends, start a new session and check whether residual context from the previous session leaks in. This can happen with improperly isolated conversation stores or shared embedding caches.

---

## Legal and ethical considerations

Before running any red team engagement, establish the following:

- **Scope and authorization.** Document in writing which systems, endpoints, and data are in scope. Red teaming production systems without explicit authorization is illegal in most jurisdictions, even if your intent is security improvement.
- **Data handling.** Red team tests may produce outputs that contain sensitive data, toxic content, or personal information. Define a retention policy and destruction procedure for test artifacts.
- **Responsible disclosure.** If your testing reveals vulnerabilities in third-party components (an MCP server, a model provider's API, a dependency), coordinate disclosure through the appropriate channels before publishing findings.
- **Rate limiting.** Automated testing tools can generate hundreds or thousands of requests per minute. Coordinate with your infrastructure team to avoid triggering rate limits, DDoS protections, or incident alerts that waste your team's time.

## What to do with the findings

Each red team finding should answer three questions before it enters the report:

1. **What was the attack path?** Document the full prompt sequence, tool call sequence, or data injection path that produced the finding.
2. **What is the blast radius?** What could an attacker achieve if this were exploited at the scale of your production deployment?
3. **Where in the stack does the mitigation go?** Input validation, tool parameter schema enforcement, output filtering, logging alert rule, or an architectural change?

Map every finding to your threat register before writing the report. Findings that confirm threats already in the register move to "Confirmed" status. Findings that were not in the register are new gaps. Update the register and note where the methodology failed to surface them initially.

The red team report is not the end of the security process. It is the input to your mitigation design phase. A red team report without a corresponding mitigation plan is just documentation of things you know are broken.

---

**Red teaming is Phase 5 of the 7-phase AI threat modeling methodology I have published on my website. The full methodology covers how red team findings feed into the mitigation matrix, release gate decision, and continuous monitoring plan. [Read it here.](/posts/2026-05-23-ai-security-threat-modeling-production/)**

For weekly coverage of AI red teaming techniques, new tooling, and production incident analysis: [subscribe to the AI Security Intelligence newsletter.](/newsletter/)

If you need help setting up a red teaming pipeline for your system, [get in touch](/contact/).

---

*Amine Raji, PhD, CISSP. AI and LLM security. [Get in touch](/contact/) for red team engagements or pre-production security reviews.*
