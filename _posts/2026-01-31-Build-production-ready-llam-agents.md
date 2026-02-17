---
title: Build Production-Ready LLM Agents
date: 2026-01-31
uuid: 202512180000
status: published
content-type: article
target-audience: intermediate
categories: [LLM]
image:
  path: /assets/media/n8n/n8n_automation_patterns.png
description: Build LLM agents that work reliably in production. Step-by-step guide covering error handling, structured outputs, and testing strategies for AI systems.
---

# Build Production-Ready LLM Agents

This article walks through building a multi-agent system from scratch

Amine Raji
I built a system that processes government tenders using LLM agents. It filters thousands of procurement opportunities, scores them, and generates bid documents.

The code works: calling an LLM is easy. Making it work reliably 1,000 times in a row is the actual problem.

This article walks through building a multi-agent system from scratch.
I’ve published all the code as interactive notebooks you can run yourself.
I’ll explain why certain patterns matter and what breaks when you skip them.

The Problem with “Hello LLM”

Most tutorials show you this:

response = requests.post("<http://localhost:1234/v1/chat/completions>",
json={"messages": [{"role": "user", "content": "Is this tender relevant?"}]})
print(response.json()["choices"][0]["message"]["content"])
It works. You get text back. But run this 100 times and you’ll get:

Different formats each time
Occasional JSON that can’t be parsed
Random markdown formatting
Answers that don’t match what you asked for
The real work begins when you need the same input to produce predictable output. Notebook 01 covers the basics, but Notebook 02 is where things get interesting.

Structured Outputs: Making LLMs Predictable

The solution is to stop treating LLM responses as free text. Instead, define exactly what you want back using Python’s type system.

Here’s where Pydantic comes in.
Pydantic is a Python library that lets you define data structures with validation rules. Think of it as a way to describe “I need a response with these exact fields, and these specific types.”

from pydantic import BaseModel, Field
from typing import List

class FilterResult(BaseModel):
is_relevant: bool = Field(description="Is tender relevant?")
confidence: float = Field(ge=0, le=1) # ge=0, le=1 means "between 0 and 1"
categories: List[str]
reasoning: str
This defines a FilterResult that must have four fields: a boolean, a float between 0 and 1, a list of strings, and a string. If the LLM returns anything else, Pydantic will raise an error.

Now you tell the LLM about this structure in your prompt:

schema = FilterResult.model_json_schema() # Pydantic generates JSON schema
prompt = f"""
{user_question}

Respond with ONLY valid JSON matching this schema:
{json.dumps(schema, indent=2)}
"""
When the LLM responds, you validate it:

data = json.loads(response_text)
result = FilterResult.model_validate(data) # Crashes if data doesn't match schema
This matters because:

Your code now knows result.confidence is always a float between 0 and 1
Invalid responses fail immediately during development, not in production
You can pass these objects between different parts of your system without parsing strings
But there’s a problem: LLMs still occasionally return malformed JSON. About 3–5% of the time in my testing. That’s where retries come in.

Retry Logic: When LLMs Mess Up

LLMs fail sometimes. Not often — about 3–5% of the time in my testing — but that’s 50 failures per 1,000 requests.

You can’t ship a system that crashes 50 times a day.

The fix isn’t better prompts. It’s accepting that failures happen and retrying:

for attempt in range(max_retries):
try:
return await call_llm(prompt, model)
except (JSONDecodeError, ValidationError):
if attempt == max_retries - 1:
raise # Give up after max attempts
await asyncio.sleep(retry_delay \* (2 \*\* attempt)) # Wait longer each time
This is exponential backoff: wait 1 second, then 2 seconds, then 4 seconds.
Second attempts succeed about 95% of the time.
Third attempts catch almost everything else.

Your failure rate drops from 3% to 0.01%.

Build retries in from the start — see the full implementation in Notebook 07.

Building Your First Agent

An “agent” sounds complicated. It’s really just a function with well-defined inputs and outputs:

async def filter_agent(tender: Tender) -> FilterResult:
prompt = build_prompt(tender)
return await llm.generate_structured(prompt, FilterResult, temperature=0.1)
That’s it. Take a Tender object, build a prompt, call the LLM, return a FilterResult.

The trick is in the details — Notebook 03 walks through three decisions that matter:

1. Temperature choice: Use 0.1 for classification tasks. You want consistency, not creativity. Same tender should get same result every time.

2. Prompt engineering: This controls randomness in the LLM’s output. Use 0.1 for classification tasks — you want the same tender to get the same result every time. Higher values (0.7+) are for creative tasks where you want variety.

3. Prompt specificity: Don’t say “analyze this tender.” Tell the LLM exactly what you’re looking for:

CRITERIA FOR RELEVANCE:
A tender is relevant if it involves:

1. Cybersecurity (threat detection, pentesting, security audits)
2. AI/ML (AI solutions, automation, ML models)
3. Software Development (custom software, web/mobile apps)

NOT relevant if only:

- Hardware procurement
- Physical infrastructure
- Non-technical services
  Vague prompts get vague results. Specific criteria get consistent classification.

1. Reasoning field: Always ask the LLM to explain its answer. This actually improves accuracy (researchers call it “chain-of-thought prompting”), and you get Binary yes/no decisions are easy.

Business decisions need nuance. That’s why Notebook 04 introduces multi-dimensional scoring:

class RatingResult(BaseModel):
overall_score: float = Field(ge=0, le=10)
strategic_fit: float = Field(ge=0, le=10)
win_probability: float = Field(ge=0, le=10)
effort_required: float = Field(ge=0, le=10)
strengths: List[str]
risks: List[str]
recommendation: str
A single score hides critical information. A 6/10 could mean “great fit but low win probability” or “likely to win but terrible strategic fit.”
Those lead to different decisions. Breaking it into dimensions gives you the full picture.

Two more tricks here:

Require both strengths and risks: LLMs are optimistic by default. They’ll tell you why something is great. Force them to also explain what could go wrong by making both fields required.

Calibrate in the prompt: Tell the LLM “most opportunities should score 5–7, not 8–10.” Otherwise everything gets rated 8.5 and the scores become meaningless.

Creative Generation: When You Need Variety

Document generation is different from classification.
You don’t want the same tender to produce identical bid documents every time — that’s robotic.

Notebook 05 shows how to get controlled creativity.

Temperature 0.7: Higher temperature means more randomness.
For documents, you want variety in how ideas are expressed while keeping them professional.
The same analysis might say “cutting-edge cybersecurity” one time and “advanced threat detection” another time.
Both work.

Constraints keep it sane: Higher temperature can produce gibberish. Prevent that with specific guidelines:

WRITING GUIDELINES:

- Professional but approachable tone
- Specific details, not vague claims
- Active voice, clear language
- Focus on client benefits
- No clichés or buzzwords
  Structure the output: Even creative content needs structure. Use Pydantic to define sections:

class BidDocument(BaseModel):
executive_summary: str = Field(description="2-3 paragraphs")
technical_approach: str
value_proposition: str
timeline_estimate: str
You get creative writing that fits a predictable format. The content varies, but you always get all four sections.

Orchestration: Connecting the Agents

You now have three agents: one filters, one rates, one generates documents. Notebook 06 shows how to connect them:

async def process_tender(tender: Tender) -> ProcessedTender: # Stage 1: Filter
filter_result = await filter_agent.filter(tender)

    if not filter_result.is_relevant or filter_result.confidence < 0.6:
        return ProcessedTender(status="filtered_out", filter_result=filter_result)

    # Stage 2: Rating
    categories = [c.value for c in filter_result.categories]
    rating_result = await rating_agent.rate(tender, categories)

    if rating_result.overall_score < 7.0:
        return ProcessedTender(status="rated_low", rating_result=rating_result)

    # Stage 3: Document generation
    doc = await generator_agent.generate(tender, categories, rating_result.strengths)

    return ProcessedTender(status="complete", bid_document=doc)

This is just a sequential pipeline with early exits. The important patterns:

Conditional branching: Don’t waste expensive LLM calls on low-quality opportunities. Filter first, then rate, then generate.
Data flow: Each stage passes information to the next. The filter finds categories, the rater uses those categories, the generator uses the strengths.
Status tracking: Record where each tender stopped and why. You’ll need this for debugging.
This simple sequential approach works for most cases.
You only need complex graph-based orchestration (like LangGraph or similar frameworks) when you need agents to loop back, retry with different strategies, or work in parallel.

Start simple, and keep it simple whenever possible.

Production Readiness: The Last 50% of the Work

Code that works on your laptop isn’t production-ready. Notebook 07 covers what needs to change:

Configuration management: Move all hardcoded values to environment variables. Different deployments (local, staging, production) need different settings:

import os

class Config:
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "<http://localhost:1234/v1>")
MIN_CONFIDENCE = float(os.getenv("MIN_CONFIDENCE", "0.6"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
Now you can change settings without changing code.

Logging: Replace every print() statement with proper logging. You need to know what's happening in production:

import logging

logger = logging.getLogger(**name**)
logger.info(f"Processing tender {tender.id}")
logger.warning(f"Retry {attempt} after validation error")
logger.error(f"All retries exhausted", exc_info=True)
Error categories: Not all errors are the same. Some you retry, some you don’t:

try:
return await call_llm(...)
except (JSONDecodeError, ValidationError): # Retryable - LLM returned bad format, try again
retry()
except TimeoutError: # Fatal - infrastructure problem, give up
raise
Metrics: Track what’s happening. You need numbers to debug production issues:

self.metrics = {
"total_processed": 0,
"filtered_out": 0,
Here’s what broke when I moved from local testing to production:

Rate limits: Local LLMs (like LM Studio) don’t have rate limits. Cloud APIs (OpenAI, Anthropic, Groq) do. I hit rate limits immediately. Solution: add rate limiting in your LLM service, not in individual agents.

Timeouts: 60 seconds worked fine locally. In production, complex prompts under load need 120+ seconds. Don’t hardcode timeouts — make them configurable.

Model differences: Prompts that worked perfectly on Llama locally failed on GPT-4 in production. Different models need different prompting styles. Test on your production model early.

Cost: Processing 10,000 tenders locally is free. In production with API calls, it’s hundreds of dollars. Aggressive filtering before expensive operations isn’t optimization — it’s survival.

Nondeterminism: Temperature 0.1 isn’t truly deterministic. Same input occasionally produces different outputs. You can’t prevent this — design your system to handle Rate limits.

Local LLMs don’t have them. Production APIs do. Add rate limiting at the service layer, not in individual agents.
Why This Progression Matters

Each notebook builds on the previous one:

Notebook 01 — Make your first LLM call
Notebook 02 — Add Pydantic validation
Notebooks 03–05 — Build individual agents
Notebook 06 — Connect them into a pipeline
Notebook 07 — Add production patterns
Here’s why this approach works: each step builds on the previous one without breaking it.

Start with raw LLM calls (Notebook 01)
Add structured outputs (Notebook 02)
Build single agents (Notebooks 03–05)
Connect them (Notebook 06)
Harden for production (Notebook 07)
Running the Code Yourself

All code is in the GitHub repository. The learning path covers zero to production in 7 notebooks, about 6 hours total.

Requirements:

Python 3.9+
LM Studio running locally (or an API key for Groq/OpenAI/Anthropic)
About 30 minutes per notebook
Start with 01_hello_llm.ipynb. Each notebook solves a problem you’ll hit in the previous one, so do them in order.

The Real Takeaway

Building LLM agents isn’t about prompt engineering or picking the best model. It’s about accepting that LLMs are unreliable and designing around it.

LLMs return the wrong format sometimes. They time out. They give slightly different answers to the same question. They work 100 times in a row and fail on request 101.

Production systems accept this and design accordingly: Pydantic validation to catch format errors, retries with backoff for transient failures, clear type contracts between components, logging to debug weird failures.

The complete code and all notebooks are available at github.com/aminrj/procurement-ai. Each notebook includes detailed explanations, runnable code, and real examples.

Follow the learning path to build this yourself, or jump directly to the production code to see the final architecture.

Like what you read ?

Want to discuss more around AI and how to code with LLM strategies?

Connect with me on [LinkedIn] or follow my journey on [Medium] where I share real-world insights from my experiments and research.

Also, make sure to start ⭐️ the Git repo for this article 😉.

Thanks for reading.
