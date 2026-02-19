---
layout: page
title: Free AI Security Assessment
permalink: /consultation/
---

<div style="background: linear-gradient(135deg, #f8f9fc 0%, #e3edf7 100%); border: 1px solid #e1e8ed; padding: 3rem 2rem; margin: -2rem -2rem 3rem -2rem; border-radius: 15px;">
  <div style="max-width: 800px; margin: 0 auto; text-align: center;">
    <p style="font-size: 1.15rem; margin-bottom: 1.5rem; color: #5a6c7d; line-height: 1.6;">
      30-minute technical review of your AI deployment to identify the attack surface you may not know you've created.
    </p>
    <p style="font-size: 1rem; color: #6b7280;">
      For security teams and CTOs deploying LLM and agentic AI systems at enterprise or mid-market scale.
    </p>
  </div>
</div>

## The Problem

Most organizations discover AI security gaps after deploying to production—or after an incident. The questions that should have been answered during architecture:

- Where can a prompt injection attack reach in your agent's tool chain?
- Can a malicious document in your RAG pipeline manipulate model behavior?
- Are your tenants' data and context properly isolated in the vector database?
- What can your AI agents actually do—and what's stopping them from doing it unintentionally?
- How do you audit LLM decisions for compliance and regulatory requirements?
- Which of your MCP servers exposes internal systems to manipulation through AI interfaces?

Your existing security frameworks—SOC2, ISO 27001, your Kubernetes policies—weren't designed to answer these questions. Neither was your CISO's standard vendor assessment checklist.

**You don't have to discover this the expensive way.**

---

## What You Get

**AI Attack Surface Analysis**
A clear map of where your LLM or agentic system is vulnerable: prompt injection paths, data leakage vectors, agent privilege scope, and tenant isolation gaps specific to your architecture.

**Threat Model for Your Use Case**
Not a generic checklist—an actual threat model based on what your system does, what data it touches, and what your agents can reach. Relevant to your compliance posture and threat environment.

**Prioritized Remediation Roadmap**
What to fix before you ship, what to fix in the next sprint, and what you can address over time. Concrete actions, not a PDF of best practices.

**Production-Proven Patterns**
Real architectural solutions from banking, defense, aerospace, and automotive environments. What actually works in production at scale, not what sounds good in a framework document.

---

## Who This Is For

- **Security teams** evaluating AI systems before production deployment or responding to a security review request
- **CTOs and engineering leaders** who need to understand what new risks their AI deployment introduces
- **Platform and infrastructure teams** building Kubernetes-based AI/ML platforms who need to scope LLM workloads correctly
- **Compliance and risk officers** who need to extend existing programs (SOC2, ISO 27001, GDPR, HIPAA) to cover LLM and agentic systems
- **Enterprise and mid-market organizations** where an AI-related security incident means regulatory consequences, not just a bug report

---

## What We'll Cover

### Current State Assessment (10 minutes)

- Your AI/ML architecture: models, agents, data flows, integrations
- What your agents can do—tools, APIs, internal systems they can reach
- Existing security controls and where they don't apply to your AI stack
- Compliance requirements and constraints

### Risk Identification (15 minutes)

- Prompt injection and indirect prompt injection attack paths
- Data privacy risks: training data, RAG context, output leakage
- Agent privilege scope and sandboxing gaps
- Multi-tenant isolation at the model, vector database, and infrastructure layers
- Monitoring, audit, and observability gaps for AI decisions

### Action Plan (5 minutes)

- Highest-priority findings with specific remediation approaches
- Quick wins versus strategic architecture changes
- What to bring back to your security or engineering team
- Logical next steps if deeper engagement makes sense

---

## Background

**Amine Raji, PhD, CISSP** — AI/LLM security specialist with 15+ years securing production systems in banking (Société Générale), defense, aerospace (Airbus), and automotive (Volvo Cars).

I've built production LLM applications and agentic systems. I understand how these systems work from the inside—which is what makes me able to identify attack vectors that a traditional security consultant won't recognize. I've also written extensively on AI security risks, including [hidden MCP server vulnerabilities](/posts/hidden-risk-of-MCP-servers/) and production LLM deployment patterns.

Most security consultants audit what's wrong. I help you understand why it's wrong, what an attacker could actually do with it, and how to fix it with working code and architectural patterns that scale.

### Recent Results

**Prevented Architecture Refactor**
Advised SaaS company on multi-tenant LLM isolation design at architecture stage, preventing a 6-month refactor estimated at $500K in engineering cost.

**Accelerated Compliance**
Helped healthcare technology startup implement SOC2-compliant AI infrastructure in 30 days instead of 6 months by starting with the right architecture.

**Production Deployment with Zero Incidents**
Guided an enterprise automotive company through deployment of AI features on Kubernetes with zero security incidents in the first year.

---

## Schedule Your Assessment

<div style="background: linear-gradient(135deg, #f8f9fc 0%, #e3edf7 100%); border: 1px solid #e1e8ed; padding: 2.5rem 2rem; border-radius: 12px; text-align: center; margin: 2rem 0;">
  <h3 style="color: #2c3e50; margin-bottom: 1.5rem; font-size: 1.3rem;">30-Minute AI Security Assessment</h3>

  <div style="margin-bottom: 1.5rem;">
    <a href="https://calendly.com/molntek0/30min" target="_blank" style="background: #4f46e5; color: white; padding: 14px 32px; text-decoration: none; border-radius: 8px; font-weight: 600; font-size: 1rem; display: inline-block; transition: all 0.2s;">
      Choose Your Time Slot
    </a>
  </div>

  <p style="color: #5a6c7d; margin-bottom: 0.8rem; font-size: 0.95rem;">
    <strong>Prefer email?</strong> <a href="mailto:amine@molntek.com?subject=AI%20Security%20Assessment%20Request" style="color: #4f46e5;">amine@molntek.com</a>
  </p>

  <p style="color: #6b7280; font-size: 0.85rem;">
    All consultations are confidential. NDA available upon request.
  </p>
</div>

## Frequently Asked Questions

**Is this really free?**
Yes. I offer these assessments because the industry is making the same "ship first, secure later" mistakes with AI that we made with web applications 20 years ago. Thirty minutes of honest technical review now is worth far more than six months of incident response later.

**Will you try to sell me something?**
This is a technical assessment, not a sales call. I'll tell you what I find, including if your architecture is solid. We can discuss ongoing engagement if it makes sense after the call, but there's no pressure.

**We're a security team—won't we already know these issues?**
Possibly. But most enterprise security programs weren't built to evaluate LLM and agentic systems. Prompt injection, indirect prompt injection through RAG, agent tool misuse, and vector database isolation are categories that don't map cleanly to your existing threat frameworks. A second perspective from someone who builds these systems is usually useful.

**What if our AI system is already in production?**
Useful timing—I can map your actual attack surface against your live architecture and give you a prioritized remediation plan focused on what presents immediate risk.

**What if we're still evaluating AI vendors or planning deployment?**
Even better. Security built into architecture from the start costs a fraction of what it costs to retrofit. I can help you ask the right questions of vendors and make architecture decisions you won't have to undo.

**What do we need to prepare?**
A working understanding of your architecture: what LLM services or models you're using, what your agents can do, what data flows through the system, and where it runs. I'll ask questions during the call.

**What if we're under NDA?**
Standard for this work. We can sign an NDA before the call. I work regularly with defense, banking, and automotive clients with strict confidentiality requirements.

**Do you work with organizations outside the US/Europe?**
Yes. I work with organizations globally. Compliance requirements differ by region and I adjust accordingly.

---

<div style="text-align: center; margin: 3rem 0 2rem;">
  <a href="https://calendly.com/molntek0/30min" target="_blank" style="background: #4f46e5; color: white; padding: 16px 36px; text-decoration: none; border-radius: 8px; font-weight: 600; font-size: 1.05rem; display: inline-block; transition: all 0.2s;">
    Schedule Your Assessment
  </a>
</div>

_Want AI security insights in your inbox? [Subscribe to my newsletter](/subscribe/) for practical analysis of LLM vulnerabilities, agentic system risks, and what security teams actually need to know about AI deployment._
