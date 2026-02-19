---
layout: about
icon: fas fa-info-circle
order: 4
title: "About Amine Raji"
subtitle: "I help engineering and security teams deploy AI agents without creating new attack surfaces. PhD in Computer Science, CISSP certified, 15+ years in the world's most security-critical industries."
---

## The Short Version

I'm Amine Raji, founder of [Molntek](https://molntek.com) and a specialist in AI/LLM security for organizations deploying agentic and LLM-powered systems. I help CTOs and security teams understand the attack surface they're creating when they deploy AI—and how to close it before it becomes an incident.

My background spans the most demanding security environments on the planet: banking, defense, aerospace, automotive, and government. I've built and secured production AI systems from the inside. I know what breaks.

---

## Why AI/LLM Security Is Different—And Why It Matters Now

When your team deploys an AI agent or LLM-powered feature, you're not just adding a new service. You're adding a new class of attack surface that most existing security frameworks weren't designed to handle:

- **Prompt injection** attacks that manipulate model behavior the same way SQL injection manipulated databases
- **Agent privilege escalation** when an AI with system access is compromised through its inputs
- **Data exfiltration through model outputs**—training data, RAG context, and user data leaking through seemingly benign completions
- **Multi-tenant vector database isolation failures** where one tenant's data surfaces in another's queries
- **MCP server vulnerabilities** that expose your internal tools and systems to manipulation through AI interfaces
- **Agentic loops and tool misuse** when autonomous agents execute unintended actions with real consequences

Your SOC2 audit doesn't have questions about prompt injection. Your Kubernetes policies don't know how to scope LLM inference workloads. Your compliance team has never reviewed a vector database for tenant isolation. **This is the gap I close.**

---

## The Journey: From Critical Systems to AI Security

### The Foundation

My career started with a question that still drives everything I do: **How do we help organizations produce secure and reliable software in environments where failure has real consequences?**

That question became my PhD research focus, pursued through collaborative work with Airbus and other aerospace partners. Security and reliability aren't features you add after the fact—they're architectural decisions that determine whether you can ship, scale, and survive an incident.

### Five Industries, One Consistent Pattern

Over 15 years, I've secured systems across five of the most demanding environments:

**Banking** (Société Générale): Where a breach means immediate regulatory action and lasting customer trust destruction. Compliance isn't bureaucracy—it's forcing you to think through edge cases before they become incidents.

**Defense & Government**: Where threat models include nation-state actors and the consequences of failure are measured in lives, not dollars. Security has to work even when attackers have unlimited time and resources.

**Aerospace** (Airbus): Where systems must function reliably for 20+ years. I learned to architect for the long term and design systems that degrade gracefully under attack.

**Automotive** (Volvo Cars): Leading cloud security for connected vehicles—millions of internet-connected endpoints that can't be easily patched. Modern cloud-native security principles apply even to cars.

**SaaS & AI Products**: Through Molntek, helping mid-market and enterprise companies deploy AI systems that can scale from prototype to production without a security rewrite.

### The Pattern I Keep Seeing

Across all these industries, the same mistake repeats:

> **Organizations optimize for speed to market, then discover their AI architecture won't support the security controls they actually need.**

A team builds a working LLM prototype. It works in demos. Then they try to add multi-tenancy, audit logging, rate limiting, prompt validation, and compliance controls to code that was never designed for any of it. The refactor takes 6 months and costs hundreds of thousands. Or worse, they ship it anyway.

### What's Different About AI

AI systems amplify this problem in ways traditional software doesn't. An AI agent isn't just serving data—it's making decisions, calling external APIs, reading from your internal knowledge base, and acting on behalf of users. When that agent is compromised through a malicious prompt in a document it was asked to summarize, the consequences aren't a 404 error. They're unauthorized actions with real-world effects.

This is the security challenge I focus on: **not just hardening the infrastructure, but securing the model's behavior, the data it touches, and the systems it can reach.**

---

## My Approach: Security That Enables Speed

Security done right doesn't slow you down. It accelerates your path to production by eliminating the 6-month security refactor that kills most AI deployments.

### 1. Architecture First, Not Compliance Checklists

Most security consultants hand you a PDF of requirements. I start by understanding your system—what models you're running, what data flows through them, what your agents can do, and what your threat model actually looks like.

Then I design security controls that fit how you work: native Kubernetes constructs, proper LLM gateway patterns, agent sandboxing, prompt validation pipelines, and vector database isolation—built into the architecture, not bolted on afterward.

### 2. Production-Proven, Not Theoretical

Every recommendation I make has been implemented and tested in production. I write the code, deploy the systems, and document what actually works versus what sounds good in a framework document.

You'll get reference architectures, working code examples, and operational playbooks—not a list of CIS benchmarks.

### 3. Security Built Into the Workflow

Security that requires monthly audits doesn't scale. I help you embed security into your CI/CD pipeline, infrastructure-as-code, and automated testing. Developers ship securely by default because the guardrails are part of the platform.

### 4. Business Language, Not Security Jargon

I translate security decisions into business outcomes. Not "implement pod security policies"—but "this prevents a compromised container from reaching your database, which is the difference between a contained incident and a reportable breach."

Enterprise CTOs and security teams make better decisions when they understand the actual risk and business consequence.

---

## What Makes Me Different

**I understand how LLM systems work from the inside.**

I've built production AI applications—not just reviewed them. I understand prompt engineering, RAG architectures, agent frameworks, and vector database patterns. That means I can identify attack vectors that a traditional security consultant won't recognize, because they've never seen a ReAct agent loop or a multi-tool orchestration pipeline in production.

**I've secured systems in the world's most demanding environments.**

When a defense contractor asks "what if the attacker has root access?", when a bank asks "what if regulators audit us tomorrow?", when an automotive OEM asks "what if we can't patch for 5 years?"—I've been in those rooms. The threat models I've worked with are harder than anything most enterprise AI teams will face.

**I build in public.**

My [blog](/) shows exactly how I think about these problems: production architectures, real attack scenarios, and working code. The [procurement-ai project](https://github.com/aminrj/procurement-ai) is an open-source example of an LLM application built with security from day one. You can see how I work before you hire me.

**I have research depth, not just practitioner experience.**

Multiple peer-reviewed publications, conference presentations across four continents, and a PhD research foundation. When I make a recommendation, I can explain the underlying threat model, not just cite a checklist.

---

## Who I Work With

**Enterprise and mid-market security teams** evaluating or hardening AI systems before or after deployment. You have compliance requirements, existing security programs, and complex environments. I help you extend your security program to cover LLM and agentic systems specifically—the parts your current frameworks don't address.

**CTOs and engineering leaders** at organizations deploying AI into production. You need to move fast but can't afford a security incident that triggers regulatory scrutiny or destroys customer trust. I help you architect AI systems that are secure from day one, not after the breach.

---

## Recognition & Background

- **International Speaker**: Presented at conferences across 4 continents on cloud-native security, critical systems, and AI deployment patterns
- **Published Researcher**: Multiple peer-reviewed publications in cybersecurity and distributed systems
- **Industry Certifications**: CISSP, Kubernetes security specialist
- **Open Source**: Active in cloud-native and AI security communities

---

## Let's Work Together

If you're deploying AI/LLM systems and need security guidance from someone who understands both the security fundamentals and how these systems actually work, let's talk.

**Three Ways to Work With Me:**

**1. Free 30-Minute AI Security Assessment** → [Book here](/consultation/)
Technical review of your AI deployment with specific findings on your actual attack surface

**2. Architecture Review & Strategy** → [Email me](mailto:amine@molntek.com?subject=AI%20Security%20Architecture%20Review)
Deep-dive into your system design with documented security architecture and implementation roadmap

**3. Hands-On Implementation Partnership** → [Email me](mailto:amine@molntek.com?subject=AI%20Security%20Implementation%20Partnership)
Embedded consulting to build security into your AI systems from the ground up

---

**Current Availability**: Accepting new clients for Q2 2026

All consultations are confidential. NDA available upon request.
