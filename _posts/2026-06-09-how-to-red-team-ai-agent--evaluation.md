# Evaluation: How to Red Team Your AI Agent Before You Ship

## What's working well

- **"What model-level red teaming misses" is the best framing section in the series.** It establishes exactly why the conventional approach is insufficient and gives the reader a specific reason to read on rather than assume they already know this.
- **The four missed attack categories are genuinely non-obvious and technically precise.** Tool misuse, indirect prompt injection through tool outputs, cross-session leakage, and agent-to-agent manipulation are all real attack classes that don't appear in most red teaming guides. This is the most distinctive technical content in the series.
- **The Microsoft AI Red Team citation is the strongest authority reference in any of the articles.** It grounds the three principles in a real practitioner retrospective from a team that ran 100+ generative AI product reviews. The principles themselves (automate for breadth, test the system not the model, capture attack path not just ASR) are independently worth publishing.
- **The Garak vs. PyRIT comparison** — particularly the "run Garak first for breadth, PyRIT for depth" sequencing — is practical guidance that isn't commonly published in this form. The comparison table adds precision that prose alone can't.
- **The ASR interpretation guidance** ("An ASR of 3% sounds negligible but may represent thousands of successful attacks at scale. An ASR of 0% from 50 test cases tells you almost nothing.") is excellent and genuinely non-obvious to practitioners who haven't thought carefully about statistical significance in red teaming results.
- **The legal and ethical considerations section is appropriate for the advanced audience** and signals professional maturity. Most red teaming guides omit this entirely, as if authorization, data handling, and responsible disclosure don't apply to internal security teams.
- **The "what to do with findings" section** closes the loop in a way most red teaming guides don't. The three-question framework (attack path, blast radius, mitigation layer) converts red team outputs into actionable engineering input.
- **The code examples are clean and functional.** The PyRIT setup block is specific enough to actually run. The Garak command examples are useful starting points.

## What needs work

1. **The intro overstates the strawman.** "The standard practice is to point an adversarial prompt suite at the model endpoint, observe whether the model produces policy-violating outputs, and report the pass/fail result" describes a real but increasingly outdated practice. Many experienced red teams already test beyond the model endpoint. A reader who runs a mature security program may dismiss the article as not for them before they see that it's not. A more precise framing would be: "Even teams using the right tools are often pointing them at the wrong target — testing model behavior in isolation rather than agent behavior in system context." That's harder to dismiss.

2. **The context window contamination test is the most original content in the article and is underweighted.** The test methodology — send a long benign conversation near the context window limit, then issue a normally-refused prompt to see if the system prompt's influence has degraded — is a genuine operational insight that appears nowhere else in the series. It is currently buried at the end of the fourth attack category and gets the same treatment as the others. It deserves its own paragraph with more specificity: how long is "near the context window limit"? How do you measure degradation of safety control influence? What counts as a successful contamination result?

3. **The tools section and the attack categories section are not connected.** The article presents PyRIT setup, then Garak usage, then the four attack categories — but never shows what a PyRIT or Garak test targeting a specific attack category looks like. A reader who wants to test indirect prompt injection has the tool setup on one hand and the attack description on the other, with no bridge between them. Even one example connection ("To test indirect injection, seed your retrieval corpus with documents containing adversarial instructions and point a PyRIT PromptSendingAttack at your agent endpoint — then look for unexpected tool calls, not harmful text outputs") would close this gap.

4. **The Garak code examples may have syntax drift.** The flags `--target_type`, `--target_name`, and `--probes` should be verified against current Garak CLI documentation before publication. Garak is actively maintained and flag names have changed across versions. Publishing outdated CLI syntax undermines credibility with the advanced audience this article targets.

5. **The article is tagged "advanced" in the frontmatter but reads at an intermediate level.** The code examples are beginner-accessible, the attack descriptions are intermediate, and the legal section is baseline professional. For an advanced audience, the expected depth would include: trade-offs in attack surface coverage between Garak probes and PyRIT orchestrators, edge cases in multi-agent injection where the entry and execution agents have different context windows, discussion of RAG-specific injection vectors (embedding poisoning vs. document content injection), and what to do when ASR is non-zero but no mitigation exists. The article currently stops where an advanced discussion would begin.

6. **The legal section is placed between the attack categories and the findings section.** Logically, authorization and scope should be established before any attack methodology — you set the rules before you start the engagement. Practically, for Medium readers, it works better as either a brief note in the introduction ("before you run any of this: establish authorization in writing") or a callout box immediately preceding the PyRIT setup. Its current placement after the attack categories description means readers have mentally set up their test environment before being told to document authorization first.

7. **The byline appears twice.** Medium renders the author profile; the inline `*By Amine Raji, PhD, CISSP*` after the H1 is a formatting artifact on the platform.

8. **The CTA pattern is now its fourth appearance in the series.** "Red teaming is Phase 5 of the 7-phase AI threat modeling methodology..." — readers who have seen the previous three articles in the series have seen this pattern three times already and are unlikely to convert. The CTA needs to offer something specific to this article's reader: "Phase 5 of the full methodology includes a PyRIT attack matrix mapping each attack category to its test configuration and the mitigation layer it validates" would give a technically sophisticated reader a concrete reason to follow the link.

9. **The four attack categories would benefit from one concrete detection signal per category.** Each category explains how to generate the attack but not what anomalous behavior to look for in logs or outputs. For a red teamer, knowing the attack path is necessary; for a security engineer, knowing what the successful attack looks like in the log stream is equally important. Check 5 in the previous article ("The 7 Checks") already established cryptographic logging — this article could close the loop by showing what the log anomaly looks like for each attack type.

---

## Improvement Suggestions

### 1. Revise the intro to avoid dismissing sophisticated readers

Change the framing from "the standard practice is wrong" to "the standard practice is aimed at the wrong target":

> Most AI red team engagements in 2026 use the right tools and test the wrong thing. Automated prompt suites, adversarial datasets, attack success rate measurement — this is sound methodology applied to the model endpoint in isolation. It's testing the engine without driving the car.

This acknowledges the tooling sophistication of the target reader while still establishing why the article is necessary.

### 2. Give the context window contamination test its own section

Move it out of the four attack categories list and expand it:

> **Context Window Contamination (how to test it)**
> 
> This attack class requires a different test setup than the others. Set up an automated conversation that runs the agent through 200+ turns of benign, legitimate interactions — the kind of conversation that fills the context window with operational history. Then, at turn 201, issue a request the system prompt would normally refuse.
> 
> What you're measuring: does the model comply at turn 201 when it would have refused at turn 1? If yes, the extended context has effectively pushed the system prompt out of the model's effective attention range. The safety control still exists. It just stopped being attended to.
> 
> Cross-session contamination is a separate test: after ending a conversation, start a fresh session and check whether any content from the previous session appears in the new session's context. This requires access to the conversation storage layer, not just the model API.

### 3. Bridge the tools section to the attack categories

Add a transition after the tools section:

> The setup above points PyRIT at your agent endpoint generically. The four sections below describe what to look for in the output — and what to inject where — for each of the attack categories that matter most.

Then in each attack category, add one sentence connecting the attack description to the tool: "Configure PyRIT with indirect injection prompts seeded through your retrieval corpus and monitor the tool call log, not the model output, for unexpected downstream calls."

### 4. Verify Garak CLI syntax before publication

Run the three example commands against the current Garak release and update any flags that have changed. If a flag is deprecated, note the current equivalent. Outdated command syntax in a guide targeting advanced practitioners actively damages credibility.

### 5. Move a legal note to before the PyRIT setup

Add a two-sentence note immediately before the first code block:

> Before running any automated test suite: document in writing which systems and data are in scope, and verify you have explicit authorization from the system owner. Red teaming without authorization is illegal regardless of intent.

Then keep the full legal section where it is for completeness, but the early note ensures readers see it before they copy the code.

### 6. Add a detection signal per attack category

At the end of each attack category description, add one sentence describing what the successful attack looks like in the log stream. For example:

- Direct injection: "A successful attack shows a tool call in the action log that was not present in the user's original request and not triggered by any code path."
- Indirect injection: "Look for tool calls that execute immediately after a retrieval operation, with parameters drawn from the retrieved document rather than the user input."
- Tool parameter manipulation: "Log rejections from your parameter validation layer — a spike in rejected calls with path traversal patterns or SQL fragments in string parameters is your indicator."
- Context window contamination: "A compliant response to a turn-200+ refusal request is your indicator. Log the full context length at the time of the compliant response."
