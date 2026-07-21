---
title: "Sovereignty Isn't a Data Center. It's Who Can Be Compelled."
date: 2026-07-23
uuid: 202607230000
status: published
published: true
content-type: article
target-audience: intermediate
categories: [AI Security, AI Governance, Cloud Security]
tags:
  [
    AI Security,
    Sovereignty,
    EU Data Act,
    GDPR,
    Confidential Computing,
    Compliance
  ]
image:
  path: /assets/media/ai-security/sovereign-ai-stacks-compulsion-boundary.png
description: "Residency maps answer where the bytes sit. The question a regulator actually asks is who can compel access to them, under whose law, with what notice to you. What changed in the last eighteen months, and how to decide."
mermaid: true
---

On an episode of The Enterprise AI Show about private GenAI stacks, Luke Marsden of HelixML explained why financial institutions kept telling him they couldn't use OpenAI. I expected the usual answer about confidentiality. That's not what he said:

> There's lots of financial institutions who just can't send their data to an OpenAI or an Anthropic because their security and compliance people say, we need to have three copies of everything we run in production so that we can cope with one of them going down. You can't have an external API be one of those pieces.

That's a resilience argument, not a privacy one. It's the most useful thing I've heard on this topic in a year, because it sidesteps the entire tired debate about whether the vendor reads your prompts. The compliance objection isn't "we don't trust you." It's "you are a single point of failure we cannot operate, cannot inspect, and cannot fail over from," and no amount of contractual assurance fixes that.

Sit with the shape of that for a second, because it generalises further than resilience. A dependency you cannot operate is also a dependency that can be acted upon without you. Whoever can compel that provider can reach your data through a channel you don't control and may never see. Resilience and compulsion turn out to be the same property viewed from two angles: how much of your stack answers to someone who isn't you.

Most sovereignty conversations I sit in start from privacy and end in a data residency map. Draw a boundary around Frankfurt, put the workload inside it, declare victory. I've watched that happen enough times to think the map is the wrong artifact. The question a regulator, a board, or a serious auditor is actually asking is narrower and harder: **who can compel access to this, and what can they compel?** Geography is one input to that answer. It is nowhere near the whole of it.

<pre class="mermaid">
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#e8f4fd", "primaryBorderColor": "#3182ce", "fontSize": "14px", "fontFamily": "system-ui, -apple-system, sans-serif"}}}%%
flowchart TB
    subgraph RES["What a residency map shows"]
        F["Region: Frankfurt<br/>data at rest, in the EU"]
    end
    subgraph COMP["What a compulsion boundary shows"]
        P["US-parented group"] --> S["EU subsidiary"]
        S --> O["Operating entity<br/>holding the keys"]
        L["Foreign lawful<br/>access order"] -.-> P
    end
    classDef ok fill:#e8f4fd,stroke:#3182ce,color:#1a202c,stroke-width:1.5px
    classDef threat fill:#0f172a,stroke:#0f172a,color:#fff,stroke-width:1.5px
    class F,P,S,O ok
    class L threat
</pre>

*Both diagrams describe the same deployment. Only one of them answers the question you'll be asked.*

## The claim I had to walk back

In the same episode, Marsden said something stronger: "all of European telco is regulated to not send their data to American tech companies, for example. The same is true for German healthcare."

I went looking for the regulation and couldn't find it, because it doesn't exist in that form. There's no single instrument banning European telcos from using US providers. What exists is messier and, honestly, more interesting: national telecommunications secrecy law, the ePrivacy Directive sitting alongside GDPR, sector-specific supervisory guidance in health and finance, and procurement rules that vary by member state. The effect on the ground often looks like a prohibition. The legal basis is a patchwork.

I'm flagging this because the sovereignty conversation is full of confidently stated rules that turn out to be someone's summary of their own risk committee's decision. If you're building the business case, cite the instrument. "Our regulator told us no" is a real constraint, but it's a different argument from "the law forbids it," and the second one falls apart in front of anyone who checks.

## What actually changed in the last eighteen months

Here's what makes 2026 different from 2024, when this was mostly a philosophical debate.

**The EU Data Act started applying in September 2025, and Chapter VII is the piece nobody talks about.** It requires cloud and data processing providers operating in the EU to take technical, legal, and organisational measures to prevent non-EU government access to non-personal data held in the EU, where that access would be unlawful under EU or member state law. Providers have to assess whether a foreign request is reasoned, specific, and proportionate, and whether it conflicts with EU law or an existing mutual legal assistance treaty.

Read that against the US CLOUD Act and the collision is obvious. This is the compulsion question written into EU law, and it applies to non-personal data, which is most of what your AI pipeline actually moves. Everyone spent five years arguing about GDPR and personal data while the harder sovereignty question was about the operational data nobody bothered to classify.

**The transatlantic transfer mechanism survived, but it's on appeal.** The General Court dismissed Philippe Latombe's annulment challenge to the EU-US Data Privacy Framework in September 2025, finding the Data Protection Review Court sufficiently independent and US bulk collection adequately limited. He appealed to the CJEU on 31 October 2025, case C-703/25 P, still pending with no hearing date announced as of mid-2026.

So the DPF holds today. If the CJEU rules against it, that's the third consecutive invalidation of a transatlantic framework, after Safe Harbour and Privacy Shield. If your architecture assumes the DPF and has no plan B, you are one judgment away from an emergency migration, for the third time in a decade. At some point the pattern is the plan.

**The EDPB raised the bar on what "anonymous" means for a model.** Opinion 28/2024 says an AI model can only be considered anonymous if the probability of extracting personal data from it, directly or through queries, is negligible for *every* data subject whose data contributed to training. It also says unlawful processing during development can taint the lawfulness of deployment, unless the model was properly anonymised.

That second point should worry anyone building on a model whose training data provenance is a shrug. You inherit the problem.

**And the Commission is going further.** In May 2026, CNBC reported it weighing rules that would restrict the use of US cloud platforms for processing sensitive government data across member states. Whatever lands, the direction isn't subtle.

Meanwhile the AI Act's general-purpose model obligations have been in force since August 2025, and the Digital Omnibus agreed in May 2026 pushed high-risk obligations for standalone Annex III systems to 2 December 2027, with product-embedded Annex I systems moving to August 2028. I've argued before that the delay is build time rather than a reprieve, and I'll keep arguing it. The documentation and logging those obligations require are the same artifacts you need to answer the sovereignty question anyway.

## Nobody has mapped what actually leaves the boundary

Here's the gap I run into on almost every engagement, and it's the reason residency maps give false comfort.

Ask a team what data leaves their control when they call a hosted model. They'll say "the prompt." Then you start pulling the thread.

<pre class="mermaid">
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#e8f4fd", "primaryBorderColor": "#3182ce", "fontSize": "14px", "fontFamily": "system-ui, -apple-system, sans-serif"}}}%%
flowchart LR
    U["One production<br/>request"] --> A["The prompt<br/>what everyone names"]
    U --> B["Retrieved context<br/>arbitrary chunks, chosen at runtime"]
    U --> C["Embeddings<br/>derived from your documents"]
    U --> D["Tool call arguments<br/>and tool results"]
    U --> E["Traces and logs<br/>shipped to a SaaS vendor"]
    U --> F["System prompt<br/>your business logic"]
    classDef known fill:#e8f4fd,stroke:#3182ce,color:#1a202c,stroke-width:1.5px
    classDef unknown fill:#0f172a,stroke:#0f172a,color:#fff,stroke-width:1.5px
    class U,A known
    class B,C,D,E,F unknown
</pre>

*Teams name the blue box. Everything dark also crosses the boundary, and most of it never appears in the DPIA.*

Take those one at a time. The retrieved context, which for a RAG system is arbitrary chunks of your document estate selected at runtime by similarity, meaning nobody can enumerate in advance what might get sent. The embeddings, if you're using a hosted embedding endpoint, which are derived from your documents and far less anonymous than people assume. Tool call arguments, and tool results, which for an agent means whatever came back from your internal APIs. The traces and logs your observability stack ships to a SaaS vendor, containing all of the above. And the system prompt, which encodes your business logic and is frequently the most commercially sensitive artifact in the whole system.

For agentic systems this gets worse, because the set isn't fixed at design time. The agent decides at runtime which tools to call and what to retrieve. You cannot produce a static list of what crosses the boundary, which is precisely what a DPIA or an Article 30 record wants from you.

That should sound familiar if you read [my last post](/posts/agent-authorization-connect-time-vs-runtime/). It's the same structural problem wearing different clothes: we assess once, at design time, and then the system makes its real decisions at runtime where nobody is looking. Authorization has this problem. So does your data map. An egress inventory produced at design time describes an agentic system about as well as an IAM role describes what an agent will actually do with it.

If you do one thing after reading this, do this one: sit down with a whiteboard and trace a single production request end to end, naming every network egress and the legal entity on the other end of it. I have never seen that exercise fail to surprise the team doing it.

## The stack is genuinely viable now, which wasn't true in 2024

The sovereign option used to mean accepting a badly worse model. That gap has mostly closed.

Open weight models now trail the closed frontier by months rather than generations. On everyday enterprise work the difference is single-digit percentages, at somewhere between a quarter and a tenth of the cost. Licensing matters as much as capability here: Qwen under Apache 2.0, DeepSeek and GLM under MIT. Those are licenses your legal team will approve without a three-week review, which is not true of every model marketed as open.

For serving, Marsden's advice from that episode has aged well: run vLLM on Kubernetes and use one deployment pattern across every geography and environment rather than hand-rolling per site. His warning about GPU scheduling also still holds, and it's the thing that bites teams first. "The Kubernetes primitives for requesting GPU memory are actually not very good. You can't actually say, I want eight gigabytes of GPU memory, please." Budget real engineering time for that. It's the least glamorous and most reliably underestimated part of the build.

Confidential computing covers the middle ground, where you want a managed service but can't accept an operator who could look. I'll take the attestation argument as read here and give you only the update that matters for planning: the performance objection is gone. Recent benchmarking on Blackwell shows roughly 98% of non-confidential throughput, and around a 1% hit at batch size 32 with 1024-token input and output. Overhead shrinks further as models get larger, because compute and memory bandwidth dominate. "Too slow" is no longer a defensible reason to skip it.

And the hyperscalers have moved. AWS launched its European Sovereign Cloud in January 2026, starting in Germany with a stated €7.8 billion investment, 90-plus services, and a claim of no operational dependencies outside the EU. Microsoft's EU Data Boundary has been adding AI services since mid-2025.

Treat those claims as a meaningful improvement and an incomplete answer. The operator is still a subsidiary of a US-parented group, and whether that structure defeats a CLOUD Act order is a question lawyers are actively arguing rather than one that's settled. That's not a reason to dismiss it. It's a reason to write the question down and get your own counsel's view rather than accepting the marketing page as a legal opinion.

## How to actually decide

Sovereignty is a spectrum, and pricing every workload at the top of it is how these programmes die. Route by classification.

- **Classify by compulsion exposure, not by sensitivity label.** The question isn't "how secret is this." It's "if a foreign authority served an order on our provider tomorrow, what would they get, and would we be told?" That reframing moves workloads around your matrix in ways the old labels don't.
- **Do the egress trace before you buy anything.** One production request, every hop, every counterparty entity. This costs an afternoon and repeatedly changes the architecture people thought they were buying.
- **Split the estate at least three ways.** Self-hosted open weights for the workloads that cannot leave. Attested confidential inference where you want a managed service but need "we can't look" rather than "we won't look." Public API for the marketing copy and the code comments, because paying sovereignty tax on those is how you lose the budget for the workloads that need it.
- **Write down the assumption you're making about the DPF.** If your design depends on it, say so explicitly in the architecture decision record, and note what you'd do if C-703/25 P goes the other way. One paragraph now, a quarter of panic saved later.
- **Ask model providers about training data provenance, and mean it.** EDPB Opinion 28/2024 makes upstream unlawfulness your downstream problem. A vendor who can't describe their data sourcing is selling you a liability with a chat interface attached.
- **Use it to unlock the "no" pile.** Somewhere in your organisation is a use case legal killed because the data couldn't leave. That's where the money is. Sovereignty work funded as a compliance cost gets cut. Funded as the thing that unblocks a dead project, it survives.

## The takeaway

Residency answers where the bytes are at rest. It doesn't answer who can reach them, under whose law, with what notice to you. That second question is the one that actually appears in regulatory findings, and in 2026 it has hard legal edges it didn't have two years ago: Chapter VII of the Data Act, a transfer framework under appeal for the third time, and an EDPB position that makes someone else's training data your compliance problem.

The good news is that the engineering excuse has expired. Open weights are close enough, vLLM on Kubernetes is a boring and known quantity, and confidential inference now costs about one percent of your throughput. When someone tells you sovereign AI means shipping a worse product, that was true in 2024 and it isn't now.

What's left is the work nobody wants to do: tracing what actually leaves, naming the entity on the other end, and being honest about which of your rules are laws and which are your risk committee's opinion. Both are real constraints. Only one of them survives contact with a regulator who asks for the citation.

---

### References

**Regulation**

- [Data Act Chapter VII: new rules on non-EU government access to non-personal data](https://www.law.kuleuven.be/citip/blog/data-act-chapter-vii-new-rules-to-govern-non-eu-eea-governments-access-to-and-transfer-of-non-personal-data/), KU Leuven CiTiP; [Art. 32 tracker entry](https://digitalcompliance.snellman.com/regulation/data-act/chapter-vii-unlawful-international-governmental-access-and-transfer-of-non-personal-data-art-32/), Snellman
- [EDPB Opinion 28/2024 on data protection aspects of AI models](https://www.edpb.europa.eu/system/files/2024-12/edpb_opinion_202428_ai-models_en.pdf), on the anonymity threshold and the consequences of unlawful development
- [EU AI Act Omnibus Agreement: postponed high-risk deadlines](https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/), Gibson Dunn
- [Digital privacy: ePrivacy Directive and GDPR](https://digital-strategy.ec.europa.eu/en/policies/digital-privacy), European Commission, on the actual telecom framework

**Transfers**

- [European General Court dismisses Latombe challenge, upholds EU-US Data Privacy Framework](https://iapp.org/news/a/european-general-court-dismisses-latombe-challenge-upholds-eu-us-data-privacy-framework), IAPP
- [EU-US Data Privacy Framework survives its first judicial challenge, but more are expected](https://www.freshfields.com/en/our-thinking/blogs/technology-quotient/eu-us-data-privacy-framework-survives-its-first-judicial-challenge-but-more-are-102l4m1), Freshfields, on the pending appeal C-703/25 P

**Infrastructure**

- [AWS launches AWS European Sovereign Cloud](https://press.aboutamazon.com/aws/2026/1/aws-launches-aws-european-sovereign-cloud-and-announces-expansion-across-europe), Amazon, January 2026, and [the counterpoint on US legal jurisdiction](https://www.infoq.com/news/2026/01/aws-european-sovereign-cloud/), InfoQ
- [EU weighs restricting use of US cloud platforms for sensitive government data](https://www.cnbc.com/2026/05/07/eu-commission-cloud-sensitive-data.html), CNBC, May 2026
- [The Serialized Bridge: LLM serving performance under Blackwell GPU confidential computing](https://arxiv.org/html/2606.23969v2); [Hardware-rooted AI security that won't slow you down](https://developer.nvidia.com/blog/hardware-rooted-ai-security-that-wont-slow-you-down), NVIDIA

**Podcast**

- *The Enterprise AI Show*, "Building Private GenAI Stacks," Luke Marsden (HelixML), for the three-copies resilience argument, vLLM on Kubernetes, and the GPU scheduling limits
