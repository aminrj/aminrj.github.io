# Evaluation: The 7 AI Security Checks That Catch Most Production Incidents

## What's working well

- **The four-part structure per check (what it is / what failure looks like / how to run it / what most teams do instead) is the best format in the series.** It is complete, actionable, and scannable. Each section answers a specific reader question in a predictable place.
- **"What most teams do instead" is the article's key differentiator.** This is what elevates a checklist into a teaching instrument. Naming the specific mistake — not just the right behavior — is what makes the article memorable and shareable. This framing should be emphasized in the intro and probably in the title.
- **The Cisco stat (73% of audited production AI deployments have prompt injection vulnerabilities)** is the right kind of concrete credibility signal. It tells the reader why this matters before they've committed to reading all seven checks.
- **The internal cross-link in Check 6** ("The full attack chain this check defends against is documented here") is the most natural and reader-serving CTA in the series. It adds value without feeling promotional.
- **The prioritization tip** ("If you can only do 3 of the 7, start with Check 1, Check 2, and Check 4") is the single most actionable sentence in the article. It respects the reader's real-world constraints and makes the article immediately useful even for teams that can't do everything.
- **The "what these 7 checks don't cover" section is well-scoped.** It names specific missing items (training data security, RAG access controls, agent-to-agent authentication) without undercutting the article's premise. Honest scoping builds more trust than overclaiming.

## What needs work

1. **Title inconsistency between frontmatter and H1.** The frontmatter title says "That Catch 80% of Production Incidents" but the H1 says "That Catch Most Production Incidents." These are two different claims. The "80%" version is stronger and would drive more clicks on Medium, but it needs a citation. The "most" version is defensible but weaker. Pick one and be consistent throughout the article.

2. **The opening frames this as personal practice rather than industry-derived findings.** "These 7 checks are what I run first on a constrained pre-production review" positions the article as one practitioner's habit. The Cisco citation and the incident post-mortem framing that follows are more authoritative than the personal intro. Lead with the authoritative frame: "These 7 checks address the controls most frequently absent in production incident post-mortems." The personal framing works better in the conclusion, after the authority has been established.

3. **Check 5 (cryptographic log signing) gives the least actionable implementation guidance.** "Apply a cryptographic hash or HMAC to each log entry at write time" — which HMAC? SHA-256? What about cloud-native logging services (AWS CloudTrail, GCP Cloud Audit Logs) that handle log integrity automatically? A team that decides to implement this check needs more scaffolding than one sentence. Either expand with two or three concrete options, or narrow the scope to what can be meaningfully implemented in a pre-launch window.

4. **Check 7 (output validation) is the most vague in the "how to run it" section.** "Implement a post-generation filter that scans every output against those patterns" — what kind of filter? Regex matching for PII patterns? A secondary model call? A blocklist? A DLP service integration? The check is right but the implementation guidance is generic enough that most teams won't know what to actually build. Even one concrete example ("use a regex scan for SSN, credit card, and email patterns as a starting point, then layer on a secondary model call for contextual PII") would make this actionable.

5. **Check 3 and Check 2 overlap conceptually without enough separation.** Check 2 restricts which tools an agent can call; Check 3 restricts what parameters those tools accept. This is a genuine and important distinction, but the article doesn't explicitly call it out. Readers may conflate them. A single sentence at the start of Check 3 ("Check 2 controls the tool surface; this check controls what the model passes into it") would prevent confusion.

6. **The byline appears twice.** Medium renders the author profile; the inline `*By Amine Raji, PhD, CISSP*` after the H1 is a formatting artifact on the platform.

7. **The CTA is formulaic by this point in the series.** "The full production checklist, 40+ controls organized by MAESTRO layer and mapped to OWASP LLM Top 10 and Agentic Top 10... is on my website here" is the same exit pattern as every other article. Readers who have followed the series are immune to it. Consider varying the value proposition of the CTA: "The checklist expands Check 1 into a full PyRIT setup guide and Check 4 into an IAM policy template" gives a reader a specific reason to click rather than a generic promise of "more content."

---

## Improvement Suggestions

### 1. Resolve the title inconsistency

If using "80%": find or cite a source for that figure, or reframe it as "the controls missing in most incident post-mortems" (which is what the intro says anyway and is defensible without a specific stat).

If using "most": make it specific — "Most AI Production Incidents Trace to These 7 Missing Controls" — which is more provable and more compelling than "most production incidents."

### 2. Move personal framing to the conclusion, lead with the incident data

Current opening:
> Most AI security checklists are long. [...] These 7 checks are what I run first on a constrained pre-production review.

Revised opening:
> Most AI security checklists have 40+ items. If you're three days from launch and have one afternoon, that list is not the tool you need.
> These 7 checks target the controls whose absence appears most frequently in production incident post-mortems. Cisco's 2026 audit found prompt injection vulnerabilities in 73% of production AI deployments. The majority of those could have been caught by Check 1 alone.

This reorders the same information but leads with why it matters rather than why you wrote it.

### 3. Give Check 5 concrete implementation options

Add three tiers:
- **Cloud-native (easiest):** If running on AWS, GCP, or Azure, route agent action logs to CloudTrail, GCP Cloud Audit Logs, or Azure Monitor — these services provide integrity protection by default.
- **Self-hosted (medium):** Use an append-only log store (e.g., OpenSearch with index lifecycle management) with HMAC-SHA256 on each entry using a key the agent cannot access.
- **Minimal viable:** At minimum, log to a separate service account with no agent write permissions and verify hashes manually before any investigation relies on the logs.

### 4. Give Check 7 a concrete starting pattern

> At minimum: scan every response with a regex for common PII patterns (SSN, credit card numbers, email addresses, phone numbers) and block if matched. Layer on a secondary model call for contextual PII ("is this response describing a specific real person's personal details?") if your system handles health or financial data. For regulated environments, integrate with your existing DLP provider rather than building a custom filter.

### 5. Add one bridging sentence at the start of Check 3

> "Check 2 restricted which tools the agent can call. This check restricts what the model can pass into those tools once called. Both controls are necessary; neither is sufficient alone."

### 6. Vary the CTA with specific value

Replace the generic "40+ controls on my website" with what the reader gets specifically from following it:
> "The full checklist expands these 7 into 40+ controls with named owners and acceptance criteria — including a PyRIT configuration template for Check 1 and IAM policy templates for Check 4. [Read it here.](/posts/...)"
