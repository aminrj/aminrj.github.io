---
layout: about
icon: fas fa-info-circle
order: 4
title: "About Amine Raji"
subtitle: "I help enterprises deploy AI systems without compromising security. PhD in Computer Science, CISSP certified, with 15+ years securing critical systems in banking, defense, aerospace, and automotive."
---

## The Short Version

I'm Amine Raji, founder of [Molntek](https://molntek.com) and specialist in AI security for production environments. I help CTOs and security teams deploy LLM applications with enterprise-grade security from day one.

My background spans the most security-critical industries on the planet: banking, defense, aerospace, automotive, and government. I've seen what breaks in production—and more importantly, what prevents it.

---

## The Journey: From Critical Systems Research to AI Security

### The Foundation: Building Reliable Software

My career began with a question that still drives me today: **How do we help enterprises produce more secure and reliable software?**

This became my PhD research focus in Computer Science, where I studied critical systems—the kind of software where failure isn't an option. Through my doctoral work with Airbus and other aerospace partners, I learned that security and reliability aren't features you add later. They're architectural decisions you make from the start.

### Five Critical Sectors, One Consistent Pattern

Over 15 years, I've worked across five of the most demanding security environments:

**Banking** (Société Générale): Where a security breach means immediate regulatory consequences and customer trust destruction. I learned that compliance isn't bureaucracy—it's forcing yourself to think through edge cases before they become incidents.

**Defense & Government**: Where threat models include nation-state actors and the consequences of failure are measured in lives, not dollars. This taught me that security has to work even when attackers have unlimited time and resources.

**Aerospace** (Airbus): Where systems must function reliably for 20+ years and updates can't be deployed with `kubectl apply`. I learned to architect for the long term and design systems that degrade gracefully under attack.

**Automotive** (Volvo Cars): Where I currently lead cloud security for connected vehicles, dealing with millions of internet-connected devices that can't be easily patched. This is where I learned that modern "cloud-native" security principles apply even to cars.

**SaaS & Technology**: Through Molntek, where I've helped startups and mid-market companies deploy AI systems that can scale from MVP to enterprise without a security rewrite.

### The Pattern I Keep Seeing

Across all these industries, I noticed the same mistake repeated:

> **Companies optimize for speed to market, then discover their architecture won't support the security they actually need.**

They build a prototype with OpenAI's API, it works great in demos, and suddenly they're trying to add multi-tenancy, audit logging, rate limiting, and compliance controls to code that was never designed for it.

The refactor takes 6 months. Or worse, they ship it anyway and hope nothing breaks.

### Why AI Security Matters Now

When AI/LLM adoption exploded in 2023-2024, I watched this pattern repeat at scale across the industry. Companies were rushing to deploy AI features without understanding the new attack surface they were creating:

- LLM prompts that can be injected like SQL
- Model outputs that can leak training data
- AI agents with system access and no guardrails
- Multi-tenant deployments sharing vector databases
- Production systems calling external LLM APIs with customer data

The scary part? **Most existing security frameworks don't cover this.** Your SOC2 audit probably doesn't have questions about prompt injection. Your Kubernetes security policies don't know how to handle LLM inference workloads. Your compliance team has never thought about vector database isolation.

This is why I built https://aminrj.com and focus my research and writing on AI security: because the industry is repeating the same "ship first, secure later" mistakes we made with web applications 20 years ago.

But this time, the stakes are higher. AI systems don't just serve content—they make decisions, access systems, and process sensitive data at scale.

---

## My Approach: Security That Enables Speed

I don't believe security should slow you down. Done right, it **accelerates** your path to production because you're not refactoring your architecture every 6 months.

Here's how I work with clients:

### 1. **Start with Architecture, Not Compliance**

Most security consultants hand you a 50-page PDF of requirements. I start by understanding your system architecture and designing security that fits how you actually work.

If you're deploying on Kubernetes, we'll use native constructs (network policies, pod security standards, admission controllers). If you're building multi-tenant LLM applications, we'll design tenant isolation at the data layer, not as an afterthought.

### 2. **Production-Proven, Not Theoretical**

Every recommendation I make comes from real implementations in production environments. I've made the mistakes so you don't have to.

You'll get: reference architectures, working code examples, deployment patterns, and operational playbooks—not generic best practices from a framework document.

### 3. **Build Security Into Your Workflow**

Security that requires manual reviews and monthly audits doesn't scale. I help you build security into your CI/CD pipeline, infrastructure-as-code, and automated testing.

The goal: Your developers deploy securely by default because the guardrails are built into the platform.

### 4. **Focus on Business Impact**

I translate security decisions into business outcomes. Instead of "we need to implement pod security policies," I explain "this prevents a compromised container from escalating privileges and accessing our database, which means we avoid the $2M average cost of a data breach."

CTOs and boards understand risk in business terms. I speak both languages.

---

## What Makes Me Different

**I've secured systems in the world's most demanding environments.** 

When a defense contractor asks "what if the attacker has root access?", when an automotive OEM asks "what if we can't patch for 5 years?", when a bank asks "what if regulators audit us tomorrow?"—I've thought through these scenarios because I've been in those rooms.

**I understand both security AND modern development practices.**

I don't just tell you what's secure—I show you how to build it with Kubernetes, Terraform, GitOps, and modern DevSecOps workflows. I write code, deploy systems, and test in production (safely).

**I've published my research internationally.**

Over my career, I've presented at conferences and published in journals across four continents. My work is peer-reviewed and cited by other researchers. This isn't just practical experience—it's research-backed methodology.

**I build in public.**

My [blog](/) shares production-ready code, detailed architectures, and real lessons learned. The [procurement-ai project](https://github.com/aminrj/procurement-ai) is a fully open-source example of how to build LLM applications with security and reliability baked in from day one. You can see exactly how I work before you hire me.

---

## Who I Work With

I help two types of organizations:

**Mid-Market SaaS Companies** deploying AI features for the first time. You need to move fast but can't afford a security incident that destroys customer trust. I help you architect AI systems that scale securely from MVP to enterprise.

**Enterprise Organizations** integrating AI into critical systems. You have compliance requirements, security teams, and complex environments. I help you deploy AI without triggering a 6-month security review or refactoring your entire architecture.

---

## Recognition & Speaking

- **International Speaker**: Presented at conferences across 4 continents on cloud-native security, critical systems, and AI deployment patterns
- **Published Researcher**: Multiple peer-reviewed publications in cybersecurity and distributed systems
- **Open Source Contributor**: Active in cloud-native and AI security communities
- **Industry Certifications**: CISSP (Certified Information Systems Security Professional), Kubernetes security specialist

---

## Let's Work Together

If you're deploying AI/LLM systems and need security guidance from someone who's secured critical systems in the world's most demanding environments, let's talk.

**Three Ways to Work With Me:**

**1. Free 30-Minute Security Assessment** → [Book here](/consultation/)  
Quick audit of your AI deployment architecture with specific recommendations

**2. Architecture Review & Strategy** → [Email me](mailto:amine@molntek.com?subject=AI%20Security%20Architecture%20Review)  
Deep dive into your system design with documented security architecture and implementation roadmap

**3. Hands-On Implementation Partnership** → [Email me](mailto:amine@molntek.com?subject=AI%20Security%20Implementation%20Partnership)  
Embedded consulting to deploy your AI systems with enterprise security from day one

---

**Current Availability**: Accepting new clients for Q2 2026

All consultations are confidential. NDA available upon request.
