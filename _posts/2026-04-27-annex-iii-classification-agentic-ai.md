---
title: "Annex III Classification Decision Tree for Agentic AI: Is Your Agent High-Risk?"
date: 2026-04-27
uuid: 202604270000
draft: true
status: draft
published: false
content-type: article
target-audience: advanced
categories: [AI Security, EU AI Act, Compliance]
tags:
  [
    EU AI Act,
    Annex III,
    Article 6,
    High-Risk Classification,
    Agentic AI,
    Risk Assessment,
    Compliance,
    AI Governance,
  ]
description: "The Commission missed its February deadline for Article 6 guidance. Until it arrives, engineering teams need a practical decision framework for classifying agentic AI systems against Annex III -- here is one with 20+ worked examples."
---

> EUAI-017 | EU AI Act Series | Target: 4000 words
> STATUS: DRAFT STRUCTURE -- DO NOT PUBLISH

---

## Article Structure and Research Directives

### Opening hook (300 words)

The Commission was supposed to publish Article 6 high-risk classification guidelines by February 2, 2026. They are overdue. Engineering teams cannot wait -- they need to classify their systems now to determine whether full conformity assessment is required by August 2.

**Source to reference:**
- Article 6(5): "The Commission shall, by 2 February 2026, provide guidelines specifying the practical implementation of this Article"
- Full text at artificialintelligenceact.eu
- Verify current status: search "EU AI Act Article 6 guidelines 2026" for any publication since March 1

**Framing:** "Is my system high-risk?" is the most-asked developer question in every EU AI Act community forum. The answer determines whether you need full conformity assessment (Articles 9-15, 17) or a lighter compliance posture. For agentic AI systems that chain autonomous decisions, the classification is not obvious.

---

### Section 1: How Article 6 classification works (600 words)

**What to cover:**
- Article 6(1): Systems listed in Annex III are high-risk
- Article 6(2): The derogation -- a system in Annex III is NOT high-risk if it does not pose "a significant risk of harm to the health, safety, or fundamental rights of natural persons"
- Article 6(3): Conditions for the derogation (performs narrow procedural task, improves result of previously completed human activity, is preparatory, does not influence decision without proper human review)

**Where to find it:**
- Article 6 full text with recitals 46-49
- AI Act Service Desk interpretive Q&A on Article 6

**Breach-prevention angle:** Misclassification is the single most dangerous compliance error. Classify too low: you skip conformity assessment and face penalties. Classify too high: you spend months on unnecessary compliance work. The decision tree eliminates guesswork.

---

### Section 2: The 8 Annex III categories that matter for agentic AI (800 words)

Walk through each Annex III category and assess whether agentic AI systems typically fall within it:

**Annex III categories to analyze:**
1. Biometric identification (category 1) -- does your agent process biometric data?
2. Critical infrastructure (category 2) -- does your agent manage infrastructure components?
3. Education and vocational training (category 3) -- does your agent assess learners?
4. Employment (category 4) -- does your agent screen, evaluate, or manage workers?
5. Essential services access (category 5) -- does your agent make credit, insurance, or benefits decisions?
6. Law enforcement (category 6) -- does your agent assess risk profiles?
7. Migration and border control (category 7) -- does your agent process asylum or visa applications?
8. Administration of justice (category 8) -- does your agent assist judicial decisions?

**Where to find it:**
- Annex III full text
- Recitals 50-60 for interpretive context on each category
- Cross-reference with the AI Act Service Desk category-specific guidance

**For each category:** Provide 2-3 concrete agentic AI examples showing why a system IS or IS NOT in scope. Focus on the boundary cases that are genuinely ambiguous.

---

### Section 3: Decision tree (1200 words -- core deliverable)

A step-by-step decision tree that an engineering team can run their system through:

**Step 1:** Does your system use AI techniques as defined in Article 3(1)?
**Step 2:** Does it fall under any Annex III category? (use Section 2 analysis)
**Step 3:** If yes to Step 2 -- does the Article 6(2) derogation apply?
  - Does it perform a narrow procedural task?
  - Is it preparatory to a human decision?
  - Does a human review the output before acting?
**Step 4:** If the derogation does NOT apply -- classify as high-risk. Proceed to conformity assessment.
**Step 5:** If the derogation applies -- classify as non-high-risk. Document the reasoning for audit.

**For agentic AI specifically:** The derogation is hard to claim because:
- Agents do NOT perform "narrow procedural tasks" -- they chain multiple decisions
- Agents often act autonomously WITHOUT human review of each step
- The "preparatory" exemption is weak when the agent's output IS the action (e.g., executing a Docker command, sending an API call)

This means: most agentic AI systems that touch Annex III categories will be classified as high-risk.

---

### Section 4: 20+ worked classification examples (800 words)

Table format. Each row: System description | Annex III category | Derogation applicable? | Classification | Reasoning

**Examples to include:**
- MCP agent that queries a HR database to screen CVs (Category 4, high-risk)
- RAG-powered chatbot answering customer support questions (likely non-high-risk, derogation applies)
- AI agent that approves/denies loan applications (Category 5, high-risk)
- Code review agent in CI/CD pipeline (not in Annex III, non-high-risk)
- AI agent managing cloud infrastructure scaling (Category 2 boundary case)
- MCP agent that generates compliance reports (preparatory, derogation likely applies)
- Autonomous security scanning agent (not in Annex III unless law enforcement context)
- AI-powered medical triage chatbot (Category 1/health, likely high-risk)
- AI agent that drafts legal contracts (Category 8 boundary case)
- Content moderation agent on social platform (Category 1 potential, depends on biometric use)

Plus 10+ more examples covering each Annex III category with boundary cases.

**Source for examples:** Draw from real deployment patterns seen in MCP server registries, LangChain/CrewAI templates, and enterprise use cases discussed in the OWASP Agentic community.

---

### Section 5: Documenting your classification for audit (300 words)

When a regulator asks "how did you classify this system?", you need a documented decision trail.

**Template to provide:**
- System name and description
- Annex III category assessment (which categories were considered and why)
- Derogation assessment (each Article 6(3) condition evaluated)
- Classification decision with date and decision-maker
- Evidence references (system architecture diagram, tool list, human oversight design)

---

### Closing (300 words)

Three actions:
1. Run every AI system through the decision tree this week. Document the classification.
2. For systems on the boundary: classify conservatively (high-risk) until Article 6 guidelines arrive.
3. For confirmed high-risk systems: start EUAI-001 deployer obligations immediately.

---

## Cross-references to include

- [GPAI Meets Agentic AI](https://aminrj.com/posts/gpai-meets-agentic-ai/) (EUAI-001 -- deployer obligations for classified systems)
- [OWASP Agentic Top 10 in Practice](https://aminrj.com/posts/owasp-agentic-top-10-in-practice/) (risk identification framework)
- EUAI-002 (logging requirements for high-risk systems)
- Forward reference to EUAI-011 (OWASP ASI x EU AI Act cross-reference)

## Lab reuse

No lab required. Decision tree + worked examples + audit documentation template.
