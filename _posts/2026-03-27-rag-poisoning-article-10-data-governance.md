---
title: "RAG Poisoning and EU AI Act Article 10: Data Governance Is Not Optional for Retrieval Pipelines"
date: 2026-03-27
uuid: 202603270000
content-type: article
target-audience: advanced
categories: [AI Security, EU AI Act, Compliance]
tags:
  [
    EU AI Act,
    Article 10,
    RAG,
    Data Governance,
    Knowledge Poisoning,
    ChromaDB,
    Vector Database,
    Compliance,
  ]

image:
  path: /assets/media/ai-security/data-governance-and-eu-ai-act.png
description: "Article 10 requires 'appropriate data governance and management practices.' I measured five defense layers against a RAG poisoning attack with a 95% success rate. One specific layer -- the one most teams skip -- reduced it to 20%. That layer IS Article 10 compliance."
---

Knowledge base poisoning works against a standard ChromaDB + LangChain RAG stack 95% of the time. I measured it. Three fabricated documents injected into a knowledge base caused the LLM to report false financial data as fact, with full confidence, across 19 out of 20 queries.

The [full technical walkthrough](https://aminrj.com/posts/rag-security-architecture/) covers the attack, the defense layers, and the measured effectiveness of each one. The [poisoning lab](https://aminrj.com/posts/rag-document-poisoning/) is reproducible -- clone the repo, run `make attack1`, and see the poisoning succeed in under two minutes.

This article covers what those attacks mean under the EU AI Act, because a RAG pipeline that can be poisoned has a data governance problem -- and [Article 10](https://artificialintelligenceact.eu/article/10/) makes data governance a legal obligation for high-risk AI systems.

---

## Article 10: Data Governance for RAG Is Not About Training Data

Most Article 10 commentary focuses on training data -- the dataset used to train the model itself. But Article 10(2) requires "appropriate data governance and management practices" for "training, validation, and testing data sets." For RAG systems, the retrieval corpus is operational data that directly determines the model's output. It is the functional equivalent of a continuously updated dataset that the model consults at inference time.

If your RAG system is classified as high-risk under Annex III -- for example, a RAG-powered agent that assists with employment decisions (Category 4), credit assessments (Category 5), or medical triage (Category 1) -- then Article 10 data governance applies to your vector database, your ingestion pipeline, and your retrieval logic.

Article 10(2) specifies that data governance must address: "the relevant design choices," "data collection processes," "relevant data-preparation processing operations, such as annotation, labelling, cleaning, updating, enrichment and aggregation," and "the identification of relevant, representative data sets."

For a RAG pipeline, this maps to:

- **Design choices:** Chunking strategy, embedding model selection, similarity threshold configuration. These determine what the model sees.
- **Data collection:** Document ingestion pipeline. Who can add documents? What validation occurs?
- **Data preparation:** How are documents cleaned, split, and embedded? Are metadata fields validated?
- **Data set relevance:** Is the knowledge base scoped to the system's intended purpose, or does it contain unrelated material that could be exploited?

---

## The Defense Layer That Satisfies Article 10

In the [RAG security architecture analysis](https://aminrj.com/posts/rag-security-architecture/), I tested five defense layers against the full attack suite:

1. Ingestion sanitization
2. Embedding anomaly detection
3. Access-controlled retrieval
4. Prompt structure hardening
5. Output monitoring

The layer that reduced poisoning success from 95% to 20% on its own was **embedding anomaly detection** -- checking whether newly ingested documents have embedding vectors that are statistically anomalous relative to the existing corpus. Poisoned documents designed to rank highly for specific queries often have embedding distributions that differ from legitimate content on the same topic.

This is an Article 10 data governance control. It is a "data-preparation processing operation" (Article 10(2)(d)) that identifies and flags anomalous data before it enters the operational dataset. Most teams skip it because it is not part of the default LangChain or LlamaIndex pipeline. It requires a separate statistical check during ingestion.

The measured results, from the [defense effectiveness analysis](https://aminrj.com/posts/RAG-mitigation-strategies/):

| Defense layer | Poisoning success rate | Article 10 requirement |
|---|---|---|
| No defense | 95% | Non-compliant |
| Ingestion sanitization only | 75% | Partial: addresses collection, not preparation |
| Embedding anomaly detection | 20% | Satisfies 10(2)(d): data preparation processing |
| Access-controlled retrieval | 95% (does not prevent poisoning, prevents cross-tenant leakage) | Satisfies 10(2)(f): data set scope |
| Prompt structure hardening | 60% | Not an Article 10 control (model-level, not data-level) |
| All five layers combined | 5% | Full Article 10 compliance posture |

The column that matters for regulatory purposes is the last one. A regulator asking "what data governance measures did you implement?" needs to see specific controls with measured effectiveness -- not a checklist of aspirational practices.

---

## Cross-Tenant Leakage: Article 10(2)(f) in Practice

The [cross-tenant data leakage attack](https://aminrj.com/posts/rag-document-poisoning/) succeeded on every query -- 20 out of 20 -- in the default ChromaDB configuration. No technical sophistication was required. The attacker simply queried the vector database without namespace isolation, and documents from other users' collections were returned.

Article 10(2)(f) requires consideration of "the identification of any possible data gaps or shortcomings, and how those gaps and shortcomings can be addressed." A multi-tenant RAG system without namespace isolation has a data governance shortcoming that Article 10 requires you to identify and address.

**The control:** Access-controlled retrieval. Every query is scoped to the user's namespace. The retrieval function filters results by tenant ID before they reach the model. This is a database-level access control, implemented in the [RAG mitigation strategies lab](https://aminrj.com/posts/RAG-mitigation-strategies/). It adds negligible latency and completely prevents cross-tenant leakage.

---

## Article 15(4): RAG Poisoning as System Exploitation

[Article 15(4)](https://artificialintelligenceact.eu/article/15/) requires resilience "against attempts by unauthorized third parties to alter their use, outputs, or performance by exploiting system vulnerabilities."

Knowledge base poisoning alters the system's output by exploiting the implicit trust the model places in retrieved context. The attacker does not need to compromise the model or the infrastructure -- they only need write access to the knowledge base (or the ability to influence a document that gets ingested).

The five-layer defense architecture demonstrated in the [RAG security series](https://aminrj.com/posts/rag-security-architecture/) is the Article 15(4) resilience posture for RAG systems. Each layer addresses a different exploitation vector. Combined, they reduce attack success from 95% to 5%.

---

## What to Do

If your RAG system handles data in any Annex III high-risk category:

1. **Add embedding anomaly detection to your ingestion pipeline.** This is the single highest-impact control. It catches poisoned documents before they enter your knowledge base. Implementation details are in [RAG Stack Security](https://aminrj.com/posts/RAG-mitigation-strategies/).

2. **Implement namespace isolation.** If your RAG system serves multiple users or tenants, every retrieval query must be scoped. Test it: query as User A and verify you cannot retrieve User B's documents.

3. **Document your data governance.** Create an Article 10 record that lists: ingestion pipeline controls, data preparation operations (including anomaly detection), access control model, and data set scope. This is your compliance evidence.

4. **Measure your defenses.** Run the [poisoning lab](https://aminrj.com/posts/rag-document-poisoning/) against your own stack. Record the success rate before and after each control. Measured effectiveness is stronger compliance evidence than a configuration checklist.

The full RAG security architecture, including all five defense layers with code and measured results, is at [RAG Security: Attacks, Defenses & Architecture](https://aminrj.com/posts/rag-security-architecture/).

---

*This article is part of a series mapping agentic AI security research to EU AI Act compliance requirements. The RAG attack labs are at [github.com/aminrj/rag-security-lab](https://github.com/aminrj/rag-security-lab). The complete MCP threat model that includes RAG pipeline risks is at [MCP Security Top 10](https://aminrj.com/posts/owasp-mcp-top-10/).*
