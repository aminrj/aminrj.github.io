---
title: "From Prompts to Loops: How We Got Here, and Why It Changes the Way You Work"
date: 2026-06-12
uuid: 202606120001
status: published
published: true
content-type: article
target-audience: advanced
categories: [AI, Agent Engineering, Software Development]
image:
  path: /assets/media/ai/prompts-to-loops-hero.png
tags:
  [
    AI,
    Agent Engineering,
    Loop Engineering,
    Claude Code,
    OpenCode,
    Autonomous Coding,
    Prompt Engineering,
    Software Development
  ]
description: "The entire arc from autocomplete to autonomous coding loops happened in roughly five years, and most of it in the last eighteen months. Here is how we got here, what a loop actually is, and what you gain when you stop prompting and start designing."
mermaid: false
---

# From Prompts to Loops: How We Got Here, and Why It Changes the Way You Work

*By Amine Raji, PhD, CISSP*

If you have ever pasted a question into ChatGPT, copied the answer into your editor, run it, watched it break, and pasted the error back in, you already understand most of this post. That copy-paste-fix dance is where almost everyone started. What changed is not that the dance got faster. It is that you can now hand the whole dance to the machine and walk away.

This post traces how we got from "type a question into a chat box" to "design a loop that works without you," with real dates, real product names, and a concrete before-and-after example at every step. Then it explains what a loop is, why it differs from everything before it, and what you actually gain. It is the on-ramp. If you want the hands-on build afterward, including how to run all of this on hardware you own, that is the companion guide: [Loop Engineering on Your Own Hardware](/2026/06/12/loop-engineering-on-your-own-hardware.html).

The thing worth noticing first is the pace. The entire arc below happened in roughly five years, and most of it in the last eighteen months.

<a href="/assets/diagrams/ai-coding-evolution.svg" class="popup img-link shimmer"><img src="/assets/diagrams/ai-coding-evolution.svg" alt="AI Coding Evolution: Five Steps from 2021 to 2026" width="800" height="620"></a>

<figcaption class="caption">The shift from autocomplete to autonomous verification. Each step reduces human involvement in the mechanical work.</figcaption>

## Step 1: Autocomplete in the editor (2021)

The first mainstream AI coding tool predates the chatbot era. GitHub Copilot launched as a technical preview on June 29, 2021, and reached general availability on June 29, 2022, built on an OpenAI model and trained on public code ([GitHub / Wikipedia](https://en.wikipedia.org/wiki/GitHub_Copilot)). It did something narrow: it autocompleted code inline as you typed.

The interaction looked like this. You wrote a comment or a function signature, and Copilot guessed the rest:

```python
# given a list of numbers, return the average
def average(nums):
    # Copilot suggests the next line in gray; you press Tab to accept
    return sum(nums) / len(nums)
```

Useful, but the shape of the work was entirely manual. Copilot had no idea whether its suggestion ran, no access to your tests, no memory of your project beyond the open file. It got conversational later: GitHub announced Copilot X with a GPT-4-powered chat interface in March 2023, and Copilot Chat reached general availability in December 2023 ([TechCrunch](https://techcrunch.com/2023/03/22/githubs-copilot-goes-beyond-code-completion-adds-a-chat-mode-and-more/); [SiliconANGLE](https://siliconangle.com/2023/12/29/github-copilot-chat-launches-general-availability/)). But it still only suggested. You decided, and you ran it.

## Step 2: The chat box (late 2022)

For most people the starting gun was ChatGPT, released by OpenAI on November 30, 2022, as a free research preview built on GPT-3.5. It reached one million users in five days and an estimated 100 million within two months, making it the fastest-growing consumer application in history at the time ([History.com](https://www.history.com/this-day-in-history/november-30/chatgpt-released-openai); [TechCrunch](https://techcrunch.com/2025/11/30/chatgpt-launched-three-years-ago-today/)).

You opened a browser tab, described what you wanted, and got back text. If you wanted working code, the loop went like this, and every arrow in it was you:

```
You:  "Write a Python function to fetch a URL and return the JSON."
ChatGPT:  [returns a function using requests.get(...)]
You:  [copy it into your editor, run it]
Terminal:  ModuleNotFoundError: No module named 'requests'
You:  [paste the error back into ChatGPT]
ChatGPT:  "Run pip install requests first. Here is the corrected version..."
```

The model had no access to your files, could not run anything, and had no idea whether its answer worked. You were the runtime: the one carrying output from the chat box to the terminal and the errors back again.

<a href="/assets/diagrams/human-as-runtime.svg" class="popup img-link shimmer"><img src="/assets/diagrams/human-as-runtime.svg" alt="Step 2: You Are the Runtime - the manual copy-paste loop" width="800" height="400"></a>

<figcaption class="caption">In Step 2, every arrow is you. The model is just a text generator. You carry output from the chat to the terminal and the errors back again.</figcaption>

## Step 3: The model gets hands (2023)

The first real crack in the manual model came when the assistant could run its own code. OpenAI announced Code Interpreter on March 23, 2023, as part of its ChatGPT plugins release, and rolled it out broadly to Plus users beginning July 6, 2023 ([Search Engine Journal](https://www.searchenginejournal.com/openai-introduces-plugin-support-for-chatgpt/483053/); [OpenAI Help Center](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)). It gave the model a sandboxed Python environment: it could write code, execute it, see the result, and correct itself, all inside one conversation. The Wharton professor Ethan Mollick described it at the time as "less a tool for coders and more a coder who works for you" ([BigDATAwire](https://www.bigdatawire.com/2023/07/11/openai-releases-chatgpt-code-interpreter-your-personal-data-analyst/)).

The change is visible if you compare the two transcripts. In Step 2, you ran the code and reported the error. Now the model closes that small loop itself:

```
You:  "Here is a CSV. Plot revenue by month."
Model:  [writes pandas code, runs it]
Sandbox:  KeyError: 'Revenue'
Model:  [sees the error itself, inspects the columns, finds 'revenue' is lowercase, fixes it, re-runs]
Model:  "Here is the chart. Note your column was lowercase 'revenue'."
```

You did not touch the error. The model tried, observed the failure, and fixed it on its own. This was the conceptual turning point even if few clocked it at the time: the question stopped being "can the model write code" and became "can the model check its own work."

Around the same period the connective tissue arrived. Anthropic introduced the Model Context Protocol on November 25, 2024, an open standard for giving models a uniform way to reach external tools and data, adopted over the following months by OpenAI and Google ([Anthropic](https://www.anthropic.com/news/model-context-protocol); [Wikipedia](https://en.wikipedia.org/wiki/Model_Context_Protocol)). Tool use was becoming a standard feature rather than a bespoke hack.

## Step 4: Agents in the terminal (2025)

In 2025 the assistant moved out of the chat box and into your actual development environment as an agent: something that reads your real files, runs your real tests, and edits across your codebase from the command line.

The releases came fast and close together:

- OpenAI announced **Codex** as a cloud agent on May 16, 2025, initially powered by a version of its o3 reasoning model ([Wikipedia](https://en.wikipedia.org/wiki/OpenAI_Codex_(AI_agent))).
- Anthropic's **Claude Code**, which Boris Cherny had started as a side project in September 2024, reached general availability in May 2025 ([Emojot Engineering](https://medium.com/emojot-engineering/claude-code-vs-openai-codex-the-real-verdict-2026-6e2aabab6842)).
- Open-source **OpenCode**, built by the SST team, launched in June 2025 and grew past 160,000 GitHub stars in under a year ([Medium](https://medium.com/@unicodeveloper/claude-code-vs-codex-vs-opencode-which-ai-coding-agent-is-actually-the-best-in-2026-baa9f6fd5374)).

This is the stage most working developers are at right now. The transcript looks genuinely different from Step 3, because the agent acts on your real project:

```
You:  "Add input validation to the signup endpoint and make the tests pass."
Agent:  [reads src/routes/signup.js, edits it]
Agent:  [runs `npm test`]
Tests:  1 failing — "rejects empty email"
Agent:  "The test expects a 422 status. May I update the error handler?"
You:  "Yes, go ahead."   <- you approve
Agent:  [edits, re-runs tests, all pass]
```

A real leap. But look at what you are still doing: approving each step, answering when it pauses, and re-prompting when it stalls or loses the thread. You have offloaded the typing. You are still the loop.

## Step 5: Loops (2026)

The last step is the smallest conceptual change with the biggest practical payoff. Instead of you sitting inside the loop, approving each pass and re-prompting on failure, you design the loop once and let the agent run inside it.

The idea crystallized publicly in early 2026. Peter Steinberger, creator of the OpenClaw agent, posted that you should stop prompting coding agents and start designing loops that prompt them. Boris Cherny, who leads Claude Code at Anthropic, said much the same on stage at the Acquired Unplugged event on June 2, 2026: he does not prompt anymore, his job is to write loops ([Medium summary](https://medium.com/mountain-movers/what-a-loop-actually-is-boris-chernys-three-stage-definition-33dd2bfe01b3)). When the people building the two leading agents independently land on the same framing, it is worth a closer look.

The same signup task as Step 4, now as a loop, with the human stepping out:

```
You:  [write the goal once in a file: "all tests pass, validation on every endpoint"]
You:  [start the loop, walk away]
  iteration 1: agent edits signup.js, runs tests -> 1 failing -> loop feeds the error back
  iteration 2: agent fixes the status code, runs tests -> all pass
  loop: commits the work, stops
You:  [come back, read the diff, approve the pull request]
```

Nobody approved iteration 1 before iteration 2 began. The loop carried the failure forward on its own. You defined the goal and reviewed the result; the mechanical middle ran without you.

<a href="/assets/diagrams/human-out-of-loop.svg" class="popup img-link shimmer"><img src="/assets/diagrams/human-out-of-loop.svg" alt="Step 4 vs Step 5: Human in the Loop vs Human Out of the Loop" width="800" height="480"></a>

<figcaption class="caption">In Step 4 you sit inside the loop, approving each pass. In Step 5 the loop carries failures forward on its own. You define the goal and review the result.</figcaption>

## So what actually is a loop?

Here is the honest, deflating answer first: a loop is a `while` loop. The pattern is old. Anthropic described it in a December 2024 engineering post, "Building Effective Agents," defining an agent as an LLM using tools based on environmental feedback in a loop, and naming the exact patterns going viral now, including the generate-then-critique-then-repeat "evaluator-optimizer" loop ([Anthropic](https://www.anthropic.com/research/building-effective-agents)). The developer Geoffrey Huntley popularized a bare-bones version he called the "Ralph" loop in July 2025: a bash one-liner that pipes the same prompt into a coding agent over and over. He reportedly built an entire programming language with it for around $300 ([Dev Interrupted](https://linearb.io/dev-interrupted/podcast/inventing-the-ralph-wiggum-loop)).

So if the pattern is old, why does it suddenly matter? Two things changed.

First, the models got good enough. An agent in a loop has to look at the current state, decide the next action, do it, check the result, and decide whether to continue. That requires judgment the 2023 models did not reliably have. The 2026 models do.

Second, and this is the part people miss: a loop is not a cron job. A cron job runs a fixed script on a schedule and does the same thing every time, regardless of what it finds. A loop has a decision-maker inside it. It looks at where things stand, picks the next move, and chooses whether to keep going, retry, roll back, or stop. The script is the outer shell. The model is the worker making decisions inside it. That difference, a thinking agent inside the loop instead of a fixed script, is the whole thing.

A loop needs only two things to exist:

1. **A trigger.** Something that starts it: a schedule, a failing test run, a message, or you typing one command.
2. **A verifiable goal.** A defined finish line it can check itself against after every pass. "All tests pass" is a real goal. "Make it better" is not, because nothing can ever confirm it, and the loop will run forever.

That second requirement separates a useful loop from an expensive disaster, and we will come back to it.

## How a loop runs, step by step

Picture the simplest useful loop. Its goal is "all tests pass." One pass looks like this:

1. The agent reads the current state of the code and the task.
2. It makes one change: writes a function, fixes a bug, adds a test.
3. The loop runs the test suite. This is the check, done by the machine, not by the agent's say-so.
4. If the tests pass, the goal is met. The loop commits the work and stops.
5. If they fail, the loop feeds the error back in and starts another pass.
6. This repeats until the tests pass, or until a safety limit stops it.

In about fifteen lines of bash, the skeleton is literally this:

```bash
for i in $(seq 1 15); do                 # hard cap: never more than 15 tries
  agent run "$(cat goal.md)"             # one pass: the agent makes a change
  if npm test; then                      # the verifier, not the agent, decides
    git commit -am "done in $i tries"    # goal met: save and stop
    exit 0
  fi
done
echo "Hit the cap. Stopping for review." # safety brake fired
```

The magic is not in any single line, all of which existed before. It is that no human carries information between the steps. The agent tries, the machine checks, the result flows back automatically, and it goes again.

Compare that to Step 4. The difference is exactly the carrying. In Step 4 you notice the test failed, copy the error, and tell the agent to try again. In a loop, that handoff is the `if npm test` line. You wrote it once. You are not in it anymore.

## What you actually gain

Three things, concretely.

**You stop babysitting.** The repetitive part of working with an agent, watching it run, pasting errors back, nudging it when it stalls, is precisely the part a loop automates. You spend your attention on defining the goal and reviewing the result. The framing that helped me: if you find yourself doing the same mechanical thing over and over to keep the agent moving, that mechanical thing is what the loop is for.

**Work happens while you are gone.** A loop can run on a schedule or off a trigger. It can wake up in the morning, read yesterday's failing tests, pick one, attempt a fix, and either open a pull request or leave the problem in your inbox if it gets stuck. Because the state lives in files and git rather than in the agent's memory, each pass is a fresh start that picks up where the last one left off. The loop survives your laptop closing. That is the literal point: it should work without you.

**It compounds.** Once you have written your project's rules and conventions in a place the agent reads automatically, every future run starts from that knowledge instead of rediscovering it. A loop with no reusable knowledge re-learns your project from zero on every pass and burns effort doing it. A loop with that knowledge written down gets cheaper and more reliable over time.

## The two things that go wrong

This is not magic, and the honest version of the pitch includes the failure modes, because both are real and both are avoidable.

**A fuzzy goal is worse than no loop.** A loop optimizes relentlessly toward whatever you defined as "done." If that definition is vague, it will produce confident, fast, wrong work, and keep producing it. Huntley documented the classic failure: an agent that is supposed to signal "finished" only when truly done signals it early, and the loop exits on a half-finished job ([AlphaSignal](https://alphasignalai.substack.com/p/most-developers-do-not-need-agent)). The fix is a finish line the machine can check without the agent's opinion: a passing test, a clean type-check, a green build. If you cannot write your goal as a command that either passes or fails, you are not ready to build a loop for it yet. Define the finish line first.

**Cost can run away.** An agent that prompts itself, retries, and spawns helpers can burn an enormous number of tokens unattended, especially overnight when nobody is watching the meter. This is why every serious loop needs hard brakes: a maximum number of iterations, a way to detect when it is making no progress and stop, and a budget ceiling. This particular problem is also the strongest argument for running loops on a local model you own, where the marginal cost of one more iteration is close to zero. That is a central theme of the companion guide.

A useful figure to stay grounded: a 2025 survey of 306 practitioners across 26 domains found that 68% of production agents run ten steps or fewer before a human steps in ([AlphaSignal](https://alphasignalai.substack.com/p/most-developers-do-not-need-agent)). Full unattended autonomy is still the exception, not the rule. Loops are a tool for specific, bounded, verifiable tasks, not a replacement for your judgment.

## When to reach for a loop, and when not to

A simple rule of thumb:

- **One-off task?** Just prompt the agent directly. A loop is overhead you do not need.
- **Repetitive task with a clear pass/fail signal?** This is the sweet spot. Raise test coverage past a threshold, fix failing builds, migrate a pattern across many files. Build a loop.
- **Vague or creative task?** Do not hand "design a better architecture" to a loop and walk away. The goal is not verifiable, so the loop has nothing to optimize against. Do that thinking yourself first, then maybe loop the bounded pieces that come out of it.

## The takeaway

Prompt engineering is not dead. The leverage just moved. Five years ago you wrote the code yourself. Then you prompted a model to write it. Then you watched an agent write it and approved each step. Now, for the right kind of task, you design the loop that prompts, checks, retries, and stops, and you stay the engineer who defined the goal and owns the result.

The shift is smaller than it sounds and bigger than it looks. You are not learning a new tool. You are moving one rung up a ladder, from doing the work, to directing the work, to designing the system that does the work. Each rung freed up attention for the rung above it. This is just the next one.

If you want to build your first loop, including how to run it on your own GPU so cost and privacy stop being reasons not to, the companion guide picks up exactly here: [Loop Engineering on Your Own Hardware](#).

---

### References

In rough order of appearance.

- GitHub Copilot preview (June 29, 2021) and GA (June 29, 2022): [Wikipedia, "GitHub Copilot"](https://en.wikipedia.org/wiki/GitHub_Copilot).
- Copilot X chat announcement (March 2023): [TechCrunch](https://techcrunch.com/2023/03/22/githubs-copilot-goes-beyond-code-completion-adds-a-chat-mode-and-more/). Copilot Chat GA (December 2023): [SiliconANGLE](https://siliconangle.com/2023/12/29/github-copilot-chat-launches-general-availability/).
- ChatGPT release (November 30, 2022) and early growth: [History.com](https://www.history.com/this-day-in-history/november-30/chatgpt-released-openai); [TechCrunch, three-year retrospective](https://techcrunch.com/2025/11/30/chatgpt-launched-three-years-ago-today/).
- Code Interpreter announced March 23, 2023; broad Plus rollout July 6, 2023: [Search Engine Journal](https://www.searchenginejournal.com/openai-introduces-plugin-support-for-chatgpt/483053/); [OpenAI Help Center release notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes); Mollick quote via [BigDATAwire](https://www.bigdatawire.com/2023/07/11/openai-releases-chatgpt-code-interpreter-your-personal-data-analyst/).
- Model Context Protocol introduced November 25, 2024: [Anthropic announcement](https://www.anthropic.com/news/model-context-protocol); [Wikipedia](https://en.wikipedia.org/wiki/Model_Context_Protocol).
- OpenAI Codex cloud research preview (May 16, 2025): [Wikipedia, "OpenAI Codex (AI agent)"](https://en.wikipedia.org/wiki/OpenAI_Codex_(AI_agent)).
- Claude Code (side project September 2024, GA May 2025) and Boris Cherny's three-stage loop framing (Acquired Unplugged, June 2, 2026): [Emojot Engineering](https://medium.com/emojot-engineering/claude-code-vs-openai-codex-the-real-verdict-2026-6e2aabab6842); [Mountain Movers summary](https://medium.com/mountain-movers/what-a-loop-actually-is-boris-chernys-three-stage-definition-33dd2bfe01b3).
- OpenCode (launched June 2025, 160K+ stars): [Medium comparison](https://medium.com/@unicodeveloper/claude-code-vs-codex-vs-opencode-which-ai-coding-agent-is-actually-the-best-in-2026-baa9f6fd5374).
- "Building Effective Agents," Anthropic engineering (December 2024): [Anthropic research](https://www.anthropic.com/research/building-effective-agents).
- The "Ralph" loop, Geoffrey Huntley (July 2025): [Dev Interrupted, "Inventing the Ralph Wiggum Loop"](https://linearb.io/dev-interrupted/podcast/inventing-the-ralph-wiggum-loop).
- Early-completion failure mode and the 306-practitioner production-agents survey (2025): [AlphaSignal, "Most Developers Do Not Need Agent Loops Yet"](https://alphasignalai.substack.com/p/most-developers-do-not-need-agent).

*Note: model names, version numbers, and prices in this space change almost monthly. The dates above are accurate as of writing in June 2026; the products have likely moved on by the time you read this. Treat any specific version as a snapshot, not a current spec.*
