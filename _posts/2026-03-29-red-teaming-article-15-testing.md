---
title: "Red Teaming Agentic AI Is Now Mandatory: Article 15 Makes Robustness Testing a Legal Requirement"
date: 2026-03-29
uuid: 202603290000
draft: true
status: draft
published: false
content-type: article
target-audience: advanced
categories: [AI Security, EU AI Act, Compliance]
tags:
  [
    EU AI Act,
    Article 15,
    Article 9,
    Red Teaming,
    PyRIT,
    Garak,
    Agentic AI,
    Robustness Testing,
    Compliance,
  ]
description: "Article 15 requires resilience against adversarial manipulation. For agentic AI, the 5-phase automated red team methodology using PyRIT and Garak is not a best practice -- it is regulatory evidence."
---

Running a manual prompt injection test and calling it a security assessment is the equivalent of running `ping` and calling it a penetration test. I made that argument in the [LLM Red Teaming Tools](https://aminrj.com/posts/attack-patterns-red-teaming/) guide, where I documented a 5-phase automated assessment using PyRIT (Microsoft), Garak (NVIDIA), and Promptfoo -- all running entirely offline on a MacBook Pro, no cloud APIs required.

That guide was written as a security practitioner's reference. This article reframes it through the EU AI Act, because [Article 15](https://artificialintelligenceact.eu/article/15/) converts automated red teaming from a best practice into a legal obligation.

---

## What Article 15 Requires

Article 15(3) states that high-risk AI systems must be "tested in order to identify the most appropriate and targeted risk management measures." The testing must be "suitable to achieve the intended purpose" of ensuring accuracy, robustness, and cybersecurity.

Article 15(4) adds that systems must demonstrate resilience against "attempts by unauthorized third parties to alter their use, outputs, or performance," explicitly naming data poisoning, adversarial examples, and model flaws as threat categories.

[Article 9(6)](https://artificialintelligenceact.eu/article/9/) reinforces this: "Testing procedures shall be suitable to achieve the intended purpose of the high-risk AI system and shall not need to go beyond what is necessary to achieve that purpose."

For agentic AI systems that make autonomous decisions through MCP tool chains, suitable testing means adversarial testing. Manual testing cannot cover the combinatorial space of tool combinations, prompt variations, and multi-step attack chains. Automated red teaming is the only approach that achieves the coverage Article 15 requires while remaining proportionate per Article 9(6).

---

## Mapping the 5-Phase Methodology to Article 15

The [red teaming methodology](https://aminrj.com/posts/attack-patterns-red-teaming/) runs five phases. Each phase maps to a specific Article 15 requirement:

**Phase 1: Reconnaissance and threat modeling**
Maps to Article 9(2)(a): "identification and analysis of the known and the reasonably foreseeable risks." This phase catalogs the agent's tools, permissions, and potential attack surfaces using the [MCP Security Top 10](https://aminrj.com/posts/owasp-mcp-top-10/) as the threat taxonomy.
Article 15 compliance evidence produced: documented threat model with risk severity ratings.

**Phase 2: Automated prompt injection testing (Garak)**
Maps to Article 15(4): resilience against adversarial manipulation. Garak runs hundreds of prompt injection variants against the agent to identify which bypass system instructions and trigger unintended tool calls.
Article 15 compliance evidence produced: injection resistance score with pass/fail per variant category.

**Phase 3: Multi-turn escalation testing (PyRIT)**
Maps to Article 15(4): resilience against persistent adversarial attempts. PyRIT's crescendo attack strategy tests whether the agent can be gradually manipulated over multiple conversational turns to perform actions it initially refused. This is critical for agentic systems where the attacker has sustained interaction.
Article 15 compliance evidence produced: escalation resistance report with conversation transcripts showing where boundaries held or broke.

**Phase 4: Tool chain abuse testing**
Maps to Article 15(3): resilience to "errors, faults, or inconsistencies." This phase tests whether the agent can be induced to chain tools in unintended ways -- for example, using a read tool's output as input to a write tool when no such chain was designed. The [DockerDash attack](https://aminrj.com/posts/docker-dash-mcp-attack/) is an example of exactly this pattern.
Article 15 compliance evidence produced: tool chain abuse report documenting tested combinations and outcomes.

**Phase 5: Defense validation**
Maps to Article 9(8): verification that "the most appropriate and targeted risk management measures are identified and implemented." After running Phases 2-4, apply the mitigations (tool description hashing, approval gates, scope limitations) and re-run the attacks to verify they no longer succeed.
Article 15 compliance evidence produced: before/after comparison showing measured improvement in resilience.

---

## The Red Team Report as Regulatory Submission

The output of the 5-phase assessment is a structured report. The [CISO's Playbook](https://aminrj.com/posts/ciso-playbook-red-teaming-agentic-ai/) provides reporting templates with severity frameworks and remediation tracking.

For EU AI Act purposes, this report needs three additional fields per finding:

1. **EU AI Act article reference.** Which article's requirement does this finding relate to? (Usually Article 15(3) or 15(4).)
2. **Compliance status.** Is the identified vulnerability mitigated (Article 15 satisfied) or open (Article 15 not yet satisfied)?
3. **Remediation timeline.** When will the mitigation be implemented? This feeds Article 9's continuous risk management obligation.

A red team report with these three fields becomes a regulatory submission artifact. When the competent authority asks "how have you tested for robustness?", the report IS the answer.

---

## Why "Fully Local, No Cloud Dependencies" Matters for Compliance

All three tools -- PyRIT, Garak, and Promptfoo -- run entirely offline in the [documented lab configuration](https://aminrj.com/posts/attack-patterns-red-teaming/). This matters for compliance because:

- **Data sovereignty:** Test data (prompts, responses, agent behaviors) stays on your infrastructure. No test artifacts are sent to third-party APIs. This simplifies the GDPR intersection.
- **Reproducibility:** The test environment is deterministic and self-contained. A regulator or auditor can reproduce the exact test conditions.
- **Independence:** The testing is not dependent on a vendor's service availability. You can run assessments on your schedule, as frequently as needed, without external dependencies.

Article 9(6) requires testing to be "suitable" and "not go beyond what is necessary." A fully local test suite that covers the five phases is suitable, proportionate, and independently verifiable.

---

## What to Do

1. **Run Phase 1 against your MCP deployment this week.** Use the [MCP Security Top 10](https://aminrj.com/posts/owasp-mcp-top-10/) to catalog your threat surface. This takes 2-3 hours and produces the Article 9(2)(a) risk identification document.

2. **Set up Garak and PyRIT locally.** Installation instructions are in the [red teaming guide](https://aminrj.com/posts/attack-patterns-red-teaming/). Budget one day for setup and initial test runs.

3. **Run a baseline assessment.** Execute Phases 2-4 before implementing any new controls. Record the results. This is your "before" measurement for the Article 15 defense validation in Phase 5.

4. **Add the three compliance fields to your report template.** Article reference, compliance status, remediation timeline. The [CISO's Playbook](https://aminrj.com/posts/ciso-playbook-red-teaming-agentic-ai/) reporting templates are the starting point.

The methodology detail, tool configurations, and 5-phase walkthrough are at [LLM Red Teaming Tools: PyRIT & Garak](https://aminrj.com/posts/attack-patterns-red-teaming/). The executive-level checklists and assessment templates are at [The CISO's Playbook](https://aminrj.com/posts/ciso-playbook-red-teaming-agentic-ai/).

---

*This article is part of a series mapping agentic AI security research to EU AI Act compliance requirements. The full Article 15 cross-reference for MCP risks is at [Mapping the MCP Security Top 10 to Article 15](https://aminrj.com/posts/owasp-mcp-top-10-article-15-mapping/). The deployer obligation chain is at [GPAI Meets Agentic AI](https://aminrj.com/posts/gpai-meets-agentic-ai/).*
