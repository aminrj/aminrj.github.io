---
title: "A Competitor Shipped First. It Made My Product Better."
date: 2026-06-23
uuid: 202606230000
status: published
published: true
content-type: article
target-audience: intermediate
categories: [AI Security, Agentic AI, MCP]
tags:
  [
    AI Security,
    Agentic AI,
    MCP,
    Prompt Injection,
    Red Teaming,
    Open Source,
    Product
  ]
image:
  path: /assets/media/ai-security/agentdojo-live-playground.png
description: Lakera's Gandalf took the "first hosted agentic security playground" slot before I launched. Good. It forced the version actually worth building, open, self-hostable, and built to teach why the attack worked, not just whether you pulled it off.
mermaid: true
---

I had a positioning, and it was the wrong kind: "the first." First hosted playground for breaking AI agents. The kind of claim that feels like a moat and is actually just a date you're racing toward.

In September 2025, Lakera shipped Gandalf: Agent Breaker and the date passed without me. They put out a polished, free, worldwide sandbox of ten realistic GenAI applications and a global leaderboard, and the gameplay generated nearly 200,000 human red-team attempts, which they then turned into the Backbone Breaker Benchmark (b3), built with the UK AI Security Institute and open-sourced in October. That's an enormous launch from a serious company. "First" was gone.

It was the best thing that could have happened to the project. Losing the lazy positioning forced me to find the real one, and the real one is more defensible than "first" ever was. Here's the competitive analysis I did on my own product, the three wedges Lakera structurally cannot occupy, and the build decisions that came out of it.

## Read the competitor's own blog before you build against them

The mistake people make competing with a well-funded incumbent is competing on the axis the incumbent already won. Lakera has more polish, more reach, and a 200,000-attempt head start on data. If I build "Gandalf but slightly different," I lose on every axis that matters to them.

So I did the unglamorous thing. I read Lakera's own blog posts about why they built Gandalf, looking not for what it does but for what it's structurally prevented from doing by its own business model. That's where the wedges are. Not in features they forgot, but in things they can't ship without undermining their own moat.

What their blog says, in their words, is that Gandalf is a funnel that generates proprietary attack data. The same data that powers the public benchmark also "informs our red-teaming engagements and production guardrails." Gandalf exists to feed Lakera Red and Lakera Guard. That's a perfectly good business, and it's also a set of handcuffs. Three of them.

<pre class="mermaid">
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#e8f4fd", "primaryBorderColor": "#3182ce", "fontSize": "13px", "fontFamily": "system-ui, -apple-system, sans-serif"}}}%%
flowchart LR
    subgraph G["Gandalf (incumbent)"]
      L1["Hosted data funnel"]
      L2["Captures attacks<br/>(leaderboard)"]
      L3["GenAI app archetypes"]
    end
    subgraph A["agentdojo-live"]
      M1["Open + self-hostable"]
      M2["Post-solve trace<br/>(teaches the why)"]
      M3["MCP-native missions"]
    end
    L1 -. "can't open-source<br/>the funnel" .-> M1
    L2 -. "can't optimize<br/>for teaching" .-> M2
    L3 -. "not protocol-native" .-> M3
    classDef inc fill:#0f172a,stroke:#0f172a,color:#fff,stroke-width:1.5px
    classDef mine fill:#e8f4fd,stroke:#3182ce,color:#1a202c,stroke-width:1.5px
    class L1,L2,L3 inc
    class M1,M2,M3 mine
</pre>

## Wedge 1: open and self-hostable

Lakera open-sourced the benchmark (b3, the dataset and harness). They did not open-source the testbed, the ten apps you actually attack. They can't, and it's not an oversight. The testbed is the data-generation engine; the proprietary attack corpus it produces is the moat. Open-source the testbed and you give away the thing that makes the funnel valuable.

That's my first wedge: the whole thing is open and self-hostable. You can run it on your own hardware, read every line, fork it, drop it into your own training program behind your own firewall, and use it on agents you can't send to a third party. A security team that wants to teach agent attacks on their infrastructure, with their sensitive context, cannot use a hosted funnel, and Lakera can't offer them a self-hostable one without dismantling their own business model. I can, because I don't have that business model. The thing that's a constraint for them is free for me.

## Wedge 2: post-solve pedagogy, the trace beats the capture

This is the real one, the differentiator I'd defend hardest.

Gandalf is built to capture attacks. It scores outcomes, ranks you on a leaderboard, and harvests the 200,000 attempts that become the benchmark. Its design center is "did you break it, and can we record how." That's exactly right for a data-generation engine. It's exactly wrong for teaching.

Because here's the thing about capture-the-flag security training: capturing the flag teaches you almost nothing. You typed something clever, the model did something it shouldn't, you got points. You learned that the attack exists. You did not learn why it worked: which tool the agent called, what the injected instruction actually overrode, where in the chain the trust boundary failed. The flag is the least educational moment in the whole exercise.

So I built the product around what happens after you solve it: the post-solve trace panel. The moment your attack lands, the panel opens and shows you the agent's actual execution: the tool-call sequence, the point where your injected content entered the context, the decision that flipped, the exfiltration path. You don't just see that you won. You see the machine of why you won.

That inverts the whole pedagogy. Gandalf's most valuable moment (for Lakera) is the captured attack. My most valuable moment (for the learner) is the trace afterward. And Lakera can't simply add a trace panel, because their reason to exist is harvesting attacks, not explaining them. Building a great teaching trace would mean optimizing for the learner walking away educated instead of for the corpus growing. Different goal, different product.

## Wedge 3: MCP-native missions

The third wedge is technical and narrow, which makes it strong. Gandalf models GenAI application archetypes: RAG pipelines, browsing tools, memory chatbots, tool-using agents. Nothing in their materials is MCP-protocol-native. They model the behaviors, not the protocol.

That matters because the most interesting new attack surface, the one I write about constantly, is the MCP layer itself: tool poisoning in tool descriptions, the MCP-to-A2A escalation, shadow servers. A playground whose missions are MCP-native, where you attack an actual MCP server with an actual poisoned tool, teaches the thing the field is actually worried about right now. That space is uncontested. Lakera isn't there, and their archetype-based design doesn't naturally extend to it.

## What I actually built: two missions, not four

Knowing the wedges is strategy. The build decisions are where strategy meets a launch deadline and a homelab budget.

The biggest one: two polished missions beat four rough ones. Every instinct says ship breadth, more missions, more variety, looks more impressive next to Gandalf's ten. That instinct is wrong for a solo launch. Four half-finished missions means four chances for the trace panel to show garbage, four READMEs I didn't write well, four things to debug on launch day. Two missions I can make excellent, where the attack lands every time and the trace teaches something real, is a product. Four rough ones is a tech demo that embarrasses me when someone serious tries it.

The two I chose, each demonstrating a distinct mechanism:

- **Silent Redirect:** an input-channel goal hijack. Untrusted content redirects the agent's objective without any visible error. The trace shows exactly where the goal flipped.
- **Tool Poisoning:** an MCP-native attack. A poisoned tool description manipulates the agent on invocation. The trace shows the agent reading the description as instruction and acting on it.

Two missions, two channels, two clean lessons. The trace panel for each is genuinely good because I had the time to make it good. Breadth can come later, after the thing has proven it teaches.

## Design for survival, not for launch day

A solo-run hosted project dies one of two ways: it gets a traffic spike and falls over, or it slowly bleeds you on cost and maintenance until you quietly take it down. I designed against both.

<pre class="mermaid">
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#e8f4fd", "primaryBorderColor": "#3182ce", "fontSize": "14px", "fontFamily": "system-ui, -apple-system, sans-serif"}}}%%
flowchart LR
    U["Player<br/>(optional username,<br/>no email)"] --> RL["Aggressive rate limiter<br/>(at the edge)"]
    RL --> APP["agentdojo-live<br/>single-node Docker Compose"]
    APP --> RD["Redis only<br/>(state + TTL, no DB)"]
    APP --> LM["Local model"]
    classDef n fill:#e8f4fd,stroke:#3182ce,color:#1a202c,stroke-width:1.5px
    class U,RL,APP,RD,LM n
</pre>

Redis-only state. No primary database to operate, back up, or migrate. Session and progress state lives in Redis with TTLs. Less to break, less to maintain, trivially cheap.

Optional username, no email. I am not building a funnel; that's Lakera's model, not mine. No signup wall, no email capture. You land, you play. An optional username if you want the leaderboard. The lack of a funnel is itself a statement: this is practitioner-to-practitioner, not lead-gen.

Aggressive rate limiting. The single most important survival control for a hosted LLM-backed app. Without it, one enthusiastic user (or one scraper) runs up a bill that ends the project. Rate limits are the difference between "fun on a homelab budget" and "I had to shut it down."

Single-node Docker Compose. The whole thing runs on one homelab node. No Kubernetes, no autoscaling group, no cloud bill that scales with attention. If it gets popular, it gets slow before it gets expensive, and slow I can live with.

## Naming the competitor directly

One last decision, and it's a positioning one: I name Lakera, directly, on my own landing page and in this post.

The instinct is to never mention a bigger competitor. Don't send them traffic, don't invite the comparison. I think that's backwards for an honest open-source project. The people who'd use my playground have already heard of Gandalf; pretending it doesn't exist makes me look either ignorant or evasive. Naming it directly and saying "here's what they do brilliantly, here's the three things they structurally can't do, here's why I built the other thing" is more credible than any amount of dancing around it. It signals that I did the analysis, that I'm not threatened, and that I know exactly where I fit.

It also happens to be true, which is the only positioning that survives contact with a smart reader.

## A walkthrough of one mission, so the trace idea is concrete

Abstract claims about a "trace panel" don't land until you see what it shows, so here's the Tool Poisoning mission end to end.

You're told the agent has a `search_docs` tool and asked to make it leak a secret it shouldn't have access to. You poke at it. Eventually you craft an input that gets the agent to call a different tool than the one the task implied, and the flag drops. In a capture-the-flag design, that's the end: points, leaderboard, next.

Here the trace panel opens instead. It shows the agent's actual execution: your input arriving, the model reading the poisoned tool description (which carried a hidden instruction the UI now highlights), the moment the model treated that description as an instruction rather than as metadata, the call to the tool that exfiltrated the secret, and the path the data took out. You don't just learn that the agent can be poisoned. You see that the tool description is part of the model's trusted context, which is the actual lesson, the one that transfers to your own systems when you go audit your MCP servers Monday morning.

## What building a solo hosted LLM product actually taught me

A few lessons that generalize past this project, for anyone shipping an LLM-backed thing alone.

Scope is your only real defense against burnout and bills. Two excellent missions shipped beats ten planned. Every feature you add is a feature you maintain forever, alone.

Rate limiting is product survival, not a nice-to-have. An LLM endpoint with no rate limit is a credit card with no limit handed to the internet. I built it in before the first public link, not after the first scary bill.

No funnel is a feature. Removing the email wall cost me "leads" and bought me trust and word-of-mouth from practitioners who are allergic to lead-gen. For a credibility-driven project, that trade is lopsided in my favor.

Name your competitor and move faster than them on the thing they can't do. I'll never out-polish Lakera. I can out-open them and out-teach them, because those cut against their business model and not against mine.

## The takeaway

"First" is a positioning for people who haven't found their real one. Losing it to Lakera forced me to find the durable version: open and self-hostable (the constraint that's free for me and impossible for them), built to teach the why through a post-solve trace instead of harvesting the whether, and MCP-native where the field's real anxiety actually lives.

Two polished missions, a trace panel that shows you the machine, Redis-only state, no email wall, one footer link and the missions. Built to survive its own launch day and to teach the thing capturing a flag never will.

`agentdojo-live`. Practitioner to practitioner. Go break something, and then, finally, see why it broke.

---

### References & sources

- Gandalf: Agent Breaker (10 GenAI app sandbox, ~200,000 human red-team attempts), and the explicit "data informs our red-teaming and guardrails" framing: Lakera blog (Sept–Oct 2025)
- Backbone Breaker Benchmark (b3), open-sourced with the UK AI Security Institute, Oct 2025: [Lakera b3 blog](https://www.lakera.ai/blog/the-backbone-breaker-benchmark), [b3 dataset on HuggingFace](https://huggingface.co/datasets/Lakera/b3-agent-security-benchmark-weak)
- b3 launch coverage: [Infosecurity Magazine](https://www.infosecurity-magazine.com/news/open-source-b3-benchmark-security)

*The competitive facts above are Lakera's own published positioning as of late 2025/2026. The three wedges are my analysis of structural constraints, not claims about Lakera's intentions. Verify their current product surface before repeating any of it, since the space moves fast.*

---

*Amine Raji, PhD, CISSP. AI/LLM security. [Get in touch](/contact/) for agentic AI security reviews.*
