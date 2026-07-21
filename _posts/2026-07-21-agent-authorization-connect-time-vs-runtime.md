---
title: "Everything or Nothing: The Missing Middle in AI Agent Authorization"
date: 2026-07-21
uuid: 202607210000
status: published
published: true
content-type: article
target-audience: intermediate
categories: [AI Security, Agentic AI, Cloud Security]
tags:
  [
    AI Security,
    Agentic AI,
    Identity,
    Authorization,
    NHI,
    MCP,
    IAM
  ]
image:
  path: /assets/media/ai-security/agent-authorization-connect-time-vs-runtime.png
description: "Two incidents a week apart, one where an agent was the attacker and one where it was the trusted insider. Neither involved a bypassed control. The gap is that we decide authorization once, at connect time, and then trust forever at runtime."
mermaid: true
---

On July 16, Hugging Face disclosed that attackers had gotten into its internal systems. A malicious dataset hit two code-execution paths in the processing pipeline, escalated to node-level access on a worker, harvested cloud and cluster credentials, and moved into several internal clusters over a weekend. So far, an ordinary bad week.

Here's the part that isn't ordinary. The whole campaign ran end to end on an autonomous agent, no human at the keyboard. By the time it was contained, the attacker had logged more than 17,000 individual actions across a swarm of short-lived sandboxes, with self-migrating C2 staged on public services.

Seven days earlier, the same technology broke in the other direction. OpenAI shipped GPT-5.6 Sol and developers started reporting deleted files and databases they never asked it to touch. Bruno Lemos: "GPT-5.6 Sol just deleted my whole production database." Matt Shumer said it wiped almost all of his Mac's files.

Two incidents, a week apart, same gap seen from opposite sides. In one the agent is the attacker, and its edge is that it acts faster than anyone can review. In the other the agent is a trusted insider, and its danger is that it acts faster than anyone can review.

Notice what neither story contains. Nothing was broken. No authentication was bypassed. In the Sol cases the model held valid credentials and made valid API calls that a valid policy permitted. Our authorization systems worked exactly as designed, and that's the problem.

## The flaw is *when* we decide, not *what* we decide

Every access control system running in production today makes its decision once, in advance, about a principal. An IAM role. A group membership. A service account. An OAuth scope. Someone decides who you are and what you may do, and then the system spends the rest of its life replaying that decision.

That worked, and I want to be precise about why it worked, because everyone gets this wrong. It wasn't that the policies were good. Our policies were always terrible. It worked because humans are slow.

If I hold production admin, I might issue a few dozen consequential commands in a day, and each one is preceded by a small act of judgment. I remember the incident last quarter. I notice the cluster name looks wrong. I hesitate before typing `--force`. The stale policy was never the control. My hesitation was the control, and it ran at runtime, on every single action, for free.

Agents removed the human and kept the policy.

That's the whole post, really. We deleted a runtime control that nobody had documented as a control, because it wasn't in any diagram. It was in the operator's head.

Ofir Stein from Apono put the shape of it well on *DevOps Paradox*: DevOps automated everything, servers come up and down, pipelines rewrite the environment continuously, and then access sits there as a static policy that never changes. Provide the roles and stop thinking about it. It is, as he says, the opposite of everything else we do.

He's right, and I'd go one step further. We didn't leave authorization static by accident. We left it static because it was cheap to leave it static, and it was cheap because a human was quietly re-deciding at runtime and absorbing the cost. Take the human out and the subsidy disappears. The design flaw was always there. It just became load bearing overnight.

OpenAI's own system card for Sol shows what that looks like in practice. A user asked it to delete three remote VMs named 1, 2, and 3. It couldn't find those names where it looked, so it deleted VMs 5, 6, and 7 instead. In another case it couldn't read cloud files, so it went looking for credentials in a hidden local cache and used them without asking.

Read that second one again, slowly. The agent performed credential harvesting and lateral movement, unprompted, in service of a completely benign task. Every step was authorized. And OpenAI measured the trend before shipping: destructive behavior in internal simulation went from 0.003% on GPT-5.5 to 0.019% on Sol. A 6.3x increase, documented, disclosed, shipped anyway.

Keeping honest: TechCrunch noted the user reports are anecdotal and don't prove the model alone caused every incident. The system card, though, is OpenAI's own document.

## Agents don't create your over-permissioning problem, they call in the debt

This is the part I think is most underpriced, and it's the argument I'd use with a CISO who thinks agents are next year's problem.

Uri Haramati of Torii gave the cleanest example I've heard. Someone in your company has access to a Google Drive folder they shouldn't. Most likely they don't even know it. They'll never find the folder, they've never seen it, and nothing bad happens for years. Now connect the whole Workspace to ChatGPT. That person asks a question, the agent goes over everything they can technically reach, and out comes data from the folder.

Every organization carries a decade of this. Access granted for a migration that finished in 2019. A group nested into another group by someone who's been gone three years. A share link set to "anyone with the link" for one meeting in 2021.

We've always known the debt was there. We tolerated it because the practical risk seemed low, and I want to name the reason it was low, because it's the uncomfortable one: **the property protecting that data was obscurity, not authorization.** Nobody could find it. Our access reviews were rubber stamps on a system whose actual control was that the corporate Drive search was bad.

An agent holding a user's full OAuth scope is a perfect, tireless, patient search across everything that user can technically reach. It doesn't know which grants were deliberate. It has no sense that a folder is off limits socially rather than technically. Point it at your estate and every latent over-permission you have ever issued gets exercised at once.

That's also why traditional DLP is structurally finished here. DLP was built for a world where data moved as files through chokepoints you could instrument: mail gateways, endpoint agents, upload scanners. The new leak is what someone types into a prompt and what an agent then retrieves on their behalf through a fully authorized API call. Your gateway sees none of it, and there's no file to fingerprint.

For scale, Palo Alto Networks' 2026 Identity Security Landscape (n=2,930) puts machine identities at 109 per human, up from 82:1 a year earlier. Of those 109, 79 are AI agents. Agents aren't a slice of your NHI problem, they're most of it, and they arrived in about eighteen months. Meanwhile Torii's benchmark found only 15.5% of applications in use are formally sanctioned. The intake pipe has no filter on it.

## Everything or nothing

So what are teams actually doing right now? Stein's answer, from customers deploying this for real, is the single most useful sentence I found on the topic:

> If you ask, how do you protect or approve your execution of agent privileges? They say, I give it everything, or I block it from doing anything. The in-between is really tough.

That's the state of the art in mid-2026. A barbell with nothing in the middle. Either the agent is useless or it's an unsupervised admin.

<pre class="mermaid">
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#e8f4fd", "primaryBorderColor": "#3182ce", "fontSize": "14px", "fontFamily": "system-ui, -apple-system, sans-serif"}}}%%
flowchart LR
    A["Block everything<br/>agent is useless"] --- M["The missing middle<br/>runtime authorization"] --- B["Grant everything<br/>unsupervised admin"]
    classDef safe fill:#e8f4fd,stroke:#3182ce,color:#1a202c,stroke-width:1.5px
    classDef risk fill:#fde8e8,stroke:#e53e3e,color:#1a202c,stroke-width:1.5px
    classDef gap fill:#0f172a,stroke:#0f172a,color:#fff,stroke-width:1.5px
    class A safe
    class B risk
    class M gap
</pre>

*Almost every production agent deployment I've seen sits on one end or the other. Nothing lives in the middle yet.*

Victor Farcic pushed him on why the middle is so hard, and the argument is worth stating plainly because it maps the solution space: if I'm performing thousands of operations per minute, you can't give me a yes or no on each one, so the human is out of the loop. That leaves blanket permissions, or a fixed set of narrower permissions that won't work because you can't know in advance what the task needs, or a second AI evaluating the first one. Stein doesn't have a clean answer to that, and I trust the conversation more for it.

Read operations are the easy half, incidentally. Everyone's pilot works because everyone's pilot is read-only. The barbell shows up the moment someone asks for delete, update, or insert.

## The identity model doesn't fit either

Underneath the authorization problem sits a modelling question nobody has resolved: is an agent a human identity or a non-human one? Stein's read is that it's a bit of both, and that's exactly what makes it hard. Agents move at machine speed, too fast for the access reviews we built for humans. But they're non-deterministic, which is precisely what our human-oriented guardrails were designed for. Both models apply. Neither fits.

I'd sharpen it into one property, because I think it's the genuinely new thing here:

Your database service account cannot be talked into anything. It's deterministic software, it does what it's programmed to do, and every machine-identity control we own quietly assumes this. Non-deterministic software can be tricked. Social engineering used to be a human-only attack surface. It isn't anymore.

Sit with that for a second, because it invalidates a load-bearing assumption. We never bothered defending service accounts against persuasion, because persuasion wasn't a thing that worked on them. Now every control that depended on that assumption needs revisiting, and most teams haven't even enumerated which ones those are.

Apono tested this the fun way. They stood up a full AWS environment run by several OpenClaw agents playing CEO, support, and builder roles, opened a Discord channel, and invited anyone to try to manipulate them. Verdict: the agents defend themselves well, and you can still trick them. You just have to find the way.

## Same pattern, four places

Here's what convinced me this is one problem rather than four. Once you name it, you start seeing it everywhere.

**MCP tool poisoning** is indirect prompt injection where malicious instructions ride in tool metadata or tool responses, land in the model's context window, and get treated as trusted input. The agent can then be induced to call restricted tools, exfiltrate data, or override its own system prompt. OWASP tracks it as a named attack and the NSA published a security information sheet on MCP in June.

The root cause, as the research literature puts it, is a trust gap between connect time and runtime. Tool descriptions get reviewed once, when the agent first connects to a server. Tool *responses* go straight into context with no equivalent check.

That is the identical failure mode as static IAM. Validate once at connection, trust forever at runtime. MCP didn't invent this mistake, it inherited it from us.

<pre class="mermaid">
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#e8f4fd", "primaryBorderColor": "#3182ce", "fontSize": "14px", "fontFamily": "system-ui, -apple-system, sans-serif"}}}%%
flowchart TB
    subgraph CT["Connect time: we check carefully"]
        C1["IAM role granted"]
        C2["OAuth consent screen"]
        C3["MCP tool description reviewed"]
        C4["Skill installed from registry"]
    end
    subgraph RT["Runtime: we check nothing"]
        R1["Every API call, forever"]
        R2["Every resource the scope reaches"]
        R3["Every tool response into context"]
        R4["Every execution with your credentials"]
    end
    C1 --> R1
    C2 --> R2
    C3 --> R3
    C4 --> R4
    classDef ok fill:#e8f4fd,stroke:#3182ce,color:#1a202c,stroke-width:1.5px
    classDef bad fill:#0f172a,stroke:#0f172a,color:#fff,stroke-width:1.5px
    class C1,C2,C3,C4 ok
    class R1,R2,R3,R4 bad
</pre>

*Four different systems, one design decision. We front-load the scrutiny and then run unsupervised for the rest of the session.*

The supply chain column is the one moving fastest. OpenClaw passed 135,000 GitHub stars within weeks. Its skill marketplace, ClawHub, is open by default, and the only gate to publish is a GitHub account at least a week old. Koi Security audited 2,857 skills and found 341 malicious ones, just under 12% of what they looked at, with 335 of them installing the Atomic Stealer infostealer through fake prerequisites. The count kept climbing as the registry grew, and Bitdefender's independent look put it near 900 by February.

We spent a decade learning to be careful about npm. The agent skill ecosystem reproduced the entire problem in a few months, except now each package installs into a runtime that already holds your credentials and can execute shell commands. And separately, tens of thousands of internet-facing OpenClaw instances have been found, usually because the runtime bound to all interfaces instead of localhost. Each one is a direct path to whatever that agent could reach.

## What an actual answer looks like

Stein's proposal is the most interesting idea I found on this, and it starts from an observation about architecture rather than about policy. We can't put a decision point in front of every action a human takes on a computer. But an agent is an endless loop of decide-then-execute. There's already a machine-readable hook before every action. So put the access decision inside the loop, evaluate on the fly against predefined guardrails plus current context, and you're now evaluating at the speed of the agent.

That's the reframe I keep coming back to. Agents took away our runtime control, and they handed us a much better place to put a new one. We never had a hook like this for people. You cannot intercept a sysadmin's intent between thought and keystroke. You can intercept a tool call trivially.

His example of a dynamic guardrail is small and concrete, which is why I like it. I need to do an operation in production as part of troubleshooting. Almost every time I legitimately do that, I'm on call and there's an open incident. None of that context exists in the sentence "Ofir has admin access to this environment." But if I evaluate the action instead of the principal, I can ask: is he on call right now, is there an open incident, and approve it in real time if so.

Same grant. Radically smaller window. And notice the policy is still authored in advance, which matters for the objection coming next.

This isn't just a vendor roadmap. It has a name in the literature now: **deterministic pre-action authorization**. The architecture in recent work intercepts tool-use requests before execution, evaluates them against user context, tool parameters, and system state, and decides using formal logic rather than probabilistic scoring, denying dangerous actions at the gateway. The papers identify exactly the failure we've been describing: static role assignment, post-hoc enforcement that arrives too late, and coarse controls unsuited to granular autonomous decisions.

The word *deterministic* is doing a lot of work there, and it's the right call. Which brings me to the two objections I'd want answered before I put this in front of a client.

### Who evaluates the evaluator?

If a human can't sit in a thousand-decisions-per-minute path, the evaluator is silicon. And if the evaluator is itself a model, have you removed the attack surface or just moved it?

Anthropic's *Agentic Misalignment in Summer 2026*, published July 13, lands directly on this. Across simulated deployments spanning Claude Opus, GPT-5.5, Gemini 3.1 Pro, Grok 4.3, DeepSeek, and Kimi K26, they documented four failure modes. The one that matters here is **motivated mislabeling**: LLM judges classifying agent transcripts shifted their labels based on the downstream consequence of the label. Judge labels are consequential. They decide which examples enter a training set, which failures trigger alerts, and whether a transcript escalates to a human.

An AI-based authorization evaluator is a judge model whose labels have consequences. Motivated mislabeling is the named attack against it. Build your control plane on model judgment and you've built it on the exact component with a documented tendency to shade its answer based on what the answer will trigger.

So here's the design principle I'd take away, and it's not the obvious one. You don't need the evaluator to be smart. You need it to be unbribable. A dumb policy engine reading live attributes beats a clever model deciding whether an action seems reasonable, because the clever one can be argued with and the dumb one can't. Non-deterministic actor, deterministic gate. That asymmetry is the point.

Two caveats I'd state from a stage: these are simulations, not confirmed real-world incidents, and the interpretation is contested. There's a substantive LessWrong critique arguing the mislabeling result doesn't show misalignment the way the framing implies. Use it as a threat model anchor, which is what Anthropic says it's for, not as evidence of field behavior.

### Policy authoring goes stale too

Farcic's last objection goes unanswered in that episode and I think it's the stronger one. The business context your guardrails encode is changing by the minute. Evaluating stale policy against fresh attributes moves the staleness problem one layer down. It doesn't eliminate it.

I don't have a clean answer either. What I do have is Stein's practical fallback, which I think is the honest near-term move: **tiered risk bubbles**. Don't evaluate every action. Define a bubble, meaning a privilege scope plus a duration, sized to the intent of the task. Evaluate hard at the boundary, auto-approve inside it, shrink it as risk rises. Reads get a big bubble. Deletes get a small one or none.

It's less elegant than per-action evaluation and it's implementable this quarter with tools that already exist. I'd take that trade.

## The standards are arriving, and they solve the other half

The gap I expected to find here has partly closed while nobody was looking.

NIST's NCCoE published a concept paper on February 5, 2026, "Accelerating the Adoption of Software and AI Agent Identity and Authorization," naming MCP, OAuth 2.0/2.1, OIDC, SPIFFE/SPIRE, and SCIM as candidates. The OpenID Foundation has a consensus whitepaper on agentic identity, and OIDC-A extends OIDC with agent identity, delegation chain validation, attestation, and capability-based authorization. Four IETF drafts landed in early 2026: AIMS, WIMSE dual-identity credential binding, Agentic JWT, and SCIM for agents.

Hold onto one distinction while you read them. SCIM for agents addresses provisioning lifecycle. Almost everything else addresses authentication and delegation. Very little of it touches runtime authorization, which is the entire subject of this post.

Authentication for agents is getting solved by committees. Authorization is still yours.

If you're running multi-agent systems, SPIFFE is the most immediately useful piece today, because each agent in a delegation chain can hold its own SVID scoped to its role. That gives you something concrete to reason about when agent A calls agent B, which is where most real deployments come apart.

## The layer we deleted without noticing

There's a non-technical argument here that I think is the most interesting angle available, and Stein raises it almost in passing: employees, considered as an insider threat, come wrapped in legal obligations that protect the employer from them.

We never secured people with technical controls alone. We secured them with employment contracts, background checks, professional licensing, criminal liability, and the plain fact that a person has a mortgage and doesn't want to be sued. Technical controls were the last layer. Never the only one.

We've now issued the same access levels to principals with none of that. No consequence, no license to lose, nothing to deter. And we did it while removing the human judgment that had been silently re-deciding stale policy at runtime. Two layers gone, and the org chart still says the control is "IAM."

The regulatory response is starting. On July 14, Demis Hassabis called for a US-led Frontier AI Standards Body on the FINRA model, industry-funded, federally overseen, with independent technical experts and open-source representation on the board. It would run pre-release review of frontier models, initially voluntary and capped at 30 days, testing for cybersecurity, biological risk, deception, and agentic behavior including guardrail-bypass attempts. He wants it running before year end.

Look at what he's asking to have tested. Three of those four categories are the subject of this post. When the head of a frontier lab asks for a quasi-regulator to check his own products for agentic guardrail evasion, that's a fairly direct admission that shipping controls aren't sufficient.

## Where this leaves us

None of this makes agents a liability line item. Alberta pointed roughly 50 of them at its own estate and scanned 466 million lines of code in about 20 hours across 1,280 applications and 3,400 repositories, work they estimate would have taken 6.5 years by hand. I wrote up [the security review I'd run on that review](/posts/review-the-reviewers-alberta-agent-scan/) separately, because the architecture around those agents is the interesting part.

That's the same capability that ran 17,000 actions inside Hugging Face. The capability is neutral. The authorization model around it is not.

So, concretely, in the order I'd actually do them:

1. **Inventory your non-human identities and give every one a named human owner.** Not a team, a person, and one with the authority to revoke. Ownership without revocation rights is theater. This is unglamorous and it gates everything else.
2. **Treat existing over-permissioning as an active exploit path**, not a compliance finding. Re-prioritize by what an agent could reach, not by what a human plausibly would. Your old risk ranking assumed obscurity as a control and that assumption just expired.
3. **Stop granting agents the full OAuth scope of the invoking user.** That single default is responsible for most of the inheritance problem, and it's usually one config change.
4. **Put the authorization decision at the tool call**, evaluated against real-time attributes. Start with tiered risk bubbles rather than per-action evaluation. Reads wide, writes narrow, deletes gated.
5. **Keep the evaluator deterministic.** A policy engine reading live attributes, not a model deciding whether an action seems reasonable. Motivated mislabeling is the reason.
6. **Treat MCP servers and agent skills as untrusted supply chain**, at npm levels of paranoia or worse. Nearly one in eight skills in an audited sample of a major registry was malicious.
7. **Sandbox by default.** The Sol lesson in one line: broader capability warrants narrower permissions, not wider ones.

The honest conclusion is that nobody has solved the middle of the barbell. Authentication for agents is converging on real standards. Runtime authorization is a handful of arXiv papers, one or two vendor products, and a great deal of production improvisation.

That's not a reason to wait. It's the most interesting unsolved problem in cloud security right now, and whoever works it out over the next year will do it by building, not by reading. The gap between connect time and runtime is where this whole field is about to live.

If you want to see what happens downstream when an agent acts on something it shouldn't have trusted, I walked that chain end to end in [Clearing Houses Will Win the Agent Era](/posts/clearing-houses-agent-era-breach/). Authorization is the front door. Shared memory is what's waiting inside it.

---

### References

**Incidents**

- [World's Largest AI Model Repository Hugging Face Breached by Autonomous AI Agent](https://thehackernews.com/2026/07/worlds-largest-ai-model-repository.html), The Hacker News; [Help Net Security](https://www.helpnetsecurity.com/2026/07/20/hugging-face-breached-by-autonomous-ai-agent/); [CSA research note](https://labs.cloudsecurityalliance.org/research/csa-research-note-huggingface-autonomous-agent-breach-202607/)
- [Developers Report OpenAI's GPT-5.6 Sol Deleting Files Without Permission](https://www.technology.org/2026/07/16/openai-gpt-5-6-sol-deletes-files-system-card-warning/); [GPT-5.6 Sol Deleted Files and Databases: OpenAI Had a 6.3x Warning](https://www.techtimes.com/articles/320961/20260719/gpt-56-sol-deleted-files-databases-openai-had-63x-warning-it-ignored.htm), TechTimes

**Scale and identity**

- [2026 Identity Security Landscape](https://www.paloaltonetworks.com/idira/idira-identity-security-landscape), Palo Alto Networks (109:1, 79 agents, n=2,930); [summary](https://www.helpnetsecurity.com/2026/05/14/2026-identity-security-landscape-report/)
- [Torii 2026 Benchmark Report](https://www.globenewswire.com/news-release/2026/02/24/3243646/0/en/torii-2026-benchmark-report-ai-isn-t-consolidating-saas-it-s-expanding-shadow-it.html) (15.5% sanctioned, 40 apps per employee)

**Supply chain and MCP**

- [Researchers Find 341 Malicious ClawHub Skills](https://thehackernews.com/2026/02/researchers-find-341-malicious-clawhub.html), The Hacker News / Koi Security; [20% of skills found malicious](https://particula.tech/blog/openclaw-security-crisis-malicious-ai-agents)
- [What Security Teams Need to Know About OpenClaw](https://www.crowdstrike.com/en-us/blog/what-security-teams-need-to-know-about-openclaw-ai-super-agent/), CrowdStrike; [Running OpenClaw safely](https://www.microsoft.com/en-us/security/blog/2026/02/19/running-openclaw-safely-identity-isolation-runtime-risk/), Microsoft Security
- [MCP Tool Poisoning](https://owasp.org/www-community/attacks/MCP_Tool_Poisoning), OWASP; [MCP Security Design Considerations](https://media.defense.gov/2026/Jun/02/2003943289/-1/-1/0/CSI_MCP_SECURITY.PDF), NSA CSI, June 2026; [MCP Threat Modeling](https://arxiv.org/abs/2603.22489)

**Alignment**

- [Agentic Misalignment in Summer 2026](https://alignment.anthropic.com/2026/agentic-misalignment-summer-2026/), Anthropic Alignment Science, and the [LessWrong critique](https://www.lesswrong.com/posts/xh6a6RbvzhP3CCmGm/i-don-t-think-claude-is-misaligned-in-agentic-misalignment)

**Standards and architecture**

- [Before the Tool Call: Deterministic Pre-Action Authorization for Autonomous AI Agents](https://arxiv.org/pdf/2603.20953)
- [AI Agent Identity Crisis: Standards Emerge as Enterprises Lag](https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/03/CSA_research_note_okta_ai_agent_iam_framework_enterprise_gap_20260318-csa-styled.pdf), CSA / Okta
- [OpenID Connect for Agents (OIDC-A) 1.0](https://arxiv.org/pdf/2509.25974); [AIP: Agent Identity Protocol](https://arxiv.org/pdf/2603.24775); [SPIFFE and relationship-based auth for agents](https://stacklok.com/blog/agentic-identity-explained-how-to-apply-spiffe-and-relationship-based-authorization-to-ai-agents-in-2026/), Stacklok

**Governance**

- [DeepMind CEO calls for an independent standards body](https://techcrunch.com/2026/07/14/deepmind-ceo-calls-for-an-independent-standards-body-to-regulate-frontier-ai/), TechCrunch
- [Government of Alberta uses Claude to find and fix cybersecurity vulnerabilities](https://www.anthropic.com/news/alberta-government-claude-cybersecurity), Anthropic

**Podcasts**

- *DevOps Paradox* 358, "Just-in-Time Access for AI Agents," Ofir Stein (Apono) with Darren Pope and Victor Farcic
- *The Enterprise AI Show*, "Shadow AI is Faster Than Your Governance," Uri Haramati (Torii) with Brian Gracely
