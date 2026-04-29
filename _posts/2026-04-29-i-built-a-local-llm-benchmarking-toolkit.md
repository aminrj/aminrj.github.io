---
title: "I Built a Local LLM Benchmarking Toolkit. Here's Why It Exists."
date: 2026-04-29
uuid: 202604290000
draft: false
status: published
published: true
content-type: article
target-audience: advanced
categories: [Local LLMs, Benchmarking, Engineering]
tags:
  [
    Local LLMs,
    Benchmarking,
    llama.cpp,
    Qwen,
    Performance Testing,
    Open Source,
    Engineering,
  ]
description: "Leaderboard scores don't tell you how fast a model runs on your GPU. I built a toolkit that benchmarks local LLMs against my own hardware and workload, in one command."
image:
  path: /assets/media/devops/local-llm-benchmarking-toolkit.png
mermaid: true
---

I spent a few hours this week building a benchmarking toolkit for local LLMs. It solves a problem I hit every time I download a new model: I load it into llama-server and have no idea whether it's actually any good on my machine.

Leaderboard scores are fine for comparing models against each other. They tell you what a model did in a lab, on a cluster of A100s, often with data the model saw during training. They don't tell you how fast it runs on your RTX 3090, whether it handles a 4096-token context window, or if it's actually useful for the work you're asking it to do. Writing Python functions. Spotting security vulnerabilities. Mapping OWASP categories to agentic systems.

So I built something that answers those questions in one command.

## The Problem With Local LLM Evaluation

The same model can behave completely differently depending on your hardware, your quantization, and your context window settings.

A Qwen3.6-35B-A3B in Q4_K_XL might process prompts at 100 tokens/sec on your GPU and 40 tokens/sec on someone else's. It might score 72% on HumanEval one day and 65% the next because you changed the temperature or the batch size. These aren't theoretical differences. They affect whether the model is actually usable for your workflow.

The tools that exist for local LLM benchmarking fall into two camps.

**Camp 1: llama-bench.** Gold standard for hardware-level performance testing. Measures prompt processing speed at different context lengths and token generation speed. Fast, precise, tells you exactly what your GPU is doing. Tells you nothing about intelligence.

**Camp 2: lm-eval and bigcode-eval.** Measure quality: how well a model codes, reasons through math, completes common-sense tasks. Closest thing we have to standardized benchmarks for local models. Slow, require a running llama-server, tell you nothing about speed.

No tool does all three in a single pipeline. So I built one.

## What the Toolkit Does

The toolkit lives at `github.com/aminrj/local-llama-bench` (not public yet, I'll push it when I'm happy). Three benchmark categories.

### Performance: How fast does your GPU handle this model?

Uses `llama-bench` to measure prompt processing (at 512 and 4096 context) and token generation speed (at 128 tokens). Three repeats, CSV output, summary table.

### Quality: How well does the model actually perform?

Runs `lm-eval` and `bigcode-eval` against a running llama-server. Tasks: HumanEval+ (code generation), GSM8K (math reasoning), HellaSwag (common-sense completion). Uses `--limit 50` for speed. JSON output with pass@1 scores.

### Domain: Does the model handle the actual work I need it to do?

Five curated prompts covering the kind of work I actually ask local models to do:

1. Write a Python function with type hints and docstring
2. Write a FastMCP tool for scanning directories for hardcoded secrets
3. Context window math (128K tokens in megabytes, pages of a technical manual)
4. Review Python code for security vulnerabilities
5. Map OWASP Top 10 categories to agentic AI systems with mitigations

Each prompt is sent via curl to the llama-server API. The script measures latency, token count, and tokens/sec. CSV output with per-prompt metrics.

## Architecture

The toolkit has four layers: an orchestration layer that runs everything, three benchmark categories that each talk to llama-server, a configuration layer for models and prompts, and a results layer that produces CSV/JSON files plus a summary table.

<pre class="mermaid">
flowchart TD
    subgraph Orchestration["Orchestration Layer"]
        RA["run_all.sh"]
        MF["Makefile"]
    end

    subgraph Config["Configuration"]
        MY["config/models.yaml"]
        PJ["config/prompts.json"]
    end

    subgraph Benchmarks["Benchmark Categories"]
        PB["Performance&lt;br/>llama-bench"]
        QB["Quality&lt;br/>lm-eval + bigcode-eval"]
        DB["Domain&lt;br/>curl → llama-server"]
    end

    subgraph Results["Results &amp; Summary"]
        RC["results/*.csv"]
        RJ["results/*.json"]
        MP["utils/metrics.py → summary table"]
    end

    RA --- PB
    RA --- QB
    RA --- DB
    MF --- PB
    MF --- QB
    MF --- DB

    PB --- LS
    QB --- LS
    DB --- LS

    MY --- PB
    MY --- DB
    PJ --- DB

    LS --- RC
    LS --- RJ
    LS --- MP

    classDef layer fill:#e1d5e7,stroke:#9673a6,stroke-width:2px,color:#000
    classDef perf fill:#d5e8d4,stroke:#82b366,stroke-width:2px,color:#000
    classDef qual fill:#fff2cc,stroke:#d6b656,stroke-width:2px,color:#000
    classDef dom fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px,color:#000
    classDef cfg fill:#e6d0de,stroke:#996185,stroke-width:2px,color:#000
    classDef res fill:#d5e8d4,stroke:#82b366,stroke-width:2px,color:#000
    classDef server fill:#f8cecc,stroke:#b85450,stroke-width:2px,color:#000

    class Orchestration,Config,Benchmarks,Results layer
    class PB perf
    class QB qual
    class DB dom
    class Config cfg
    class Results res
    class LS server
</pre>

The orchestration script (`run_all.sh`) discovers llama.cpp binaries automatically, reads the model registry from `config/models.yaml`, and runs each benchmark in sequence. The llama-server is reused across benchmarks. If you're already running a model for other work, the benchmarks don't tear it down.

## Architecture Decisions

**Server reuse.** The performance benchmark used to kill any existing llama-server before running. That was dumb. If I'm already running `codemode` with my Qwen3.6 model loaded, the benchmark shouldn't tear it down. Now all scripts detect an existing server on port 8081 and reuse it. The cleanup trap only kills servers the script itself started.

**Auto-discovery of llama.cpp binaries.** No hardcoded paths. The scripts search through `~/llama.cpp/build/bin`, `~/git/llama.cpp/build/bin`, `../llama.cpp/build/bin`, and `/usr/local/bin` to find `llama-bench` and `llama-server`. If you built llama.cpp with CMake and CUDA, it should just work.

```bash
# Auto-discover llama.cpp binaries
for candidate in \
    "${REPO_DIR}/../llama.cpp/build/bin" \
    "${HOME}/llama.cpp/build/bin" \
    "${HOME}/git/llama.cpp/build/bin" \
    "/usr/local/bin" \
; do
    if [ -x "${candidate}/llama-bench" ] && [ -x "${candidate}/llama-server" ]; then
        export PATH="${candidate}:${PATH}"
        break
    fi
done
```

**Config-driven model registry.** Models live in `config/models.yaml`. Each entry has a local GGUF path (tilde expansion supported), an API model tag for llama-server, and a quantization label. Add a model, run the benchmarks, done.

**The discover_models.sh script.** Bonus feature. Scans Ollama's model store (`/usr/share/ollama/.ollama/models/`) for GGUF files and creates symlinks in `~/models/`. Then you update `config/models.yaml` with the symlinked filename. Saves me from manually tracking which models I have and where they live.

**Test coverage.** Three test suites: project structure (directories exist, files are executable, requirements.txt has the right packages), script syntax (bash -n parsing, set -e present, proper shebangs), and metrics.py parsing logic (mock CSV/JSON data, edge cases like empty files). 76 tests, all passing. That's more than most people write for a toolkit like this, but metrics parsing is the part that breaks silently if you get it wrong.

## Benchmark Results

The most useful thing this toolkit revealed wasn't a benchmark number. It was the gap between what the tools promise and what they actually deliver.

I ran the domain benchmark against my Qwen3.6-35B-A3B on an RTX 3090 with Q4_K_XL quantization. Here's what the token generation speed looks like across the five prompts:

<pre class="mermaid">
graph LR
    subgraph Performance["Token Generation Speed (tok/s)"]
        direction TB
        B1["104.7&lt;br/>simple_python"]
        B2["111.4&lt;br/>security_tool"]
        B3["111.4&lt;br/>context_math"]
        B4["100.8&lt;br/>vuln_spotting"]
        B5["105+&lt;br/>owasp_mapping"]
    end

    subgraph Latency["Generation Latency (seconds)"]
        direction TB
        L1["19.6s&lt;br/>simple_python"]
        L2["18.4s&lt;br/>security_tool"]
        L3["16.6s&lt;br/>context_math"]
        L4["18.5s&lt;br/>vuln_spotting"]
        L5["21.0+s&lt;br/>owasp_mapping"]
    end

    style Performance fill:#f9f9f9,stroke:#333,stroke-width:1px
    style Latency fill:#f9f9f9,stroke:#333,stroke-width:1px
    style B1 fill:#6c8ebf,color:#fff
    style B2 fill:#82b366,color:#fff
    style B3 fill:#d6b656,color:#fff
    style B4 fill:#b85450,color:#fff
    style B5 fill:#996185,color:#fff
    style L1 fill:#6c8ebf,color:#fff
    style L2 fill:#82b366,color:#fff
    style L3 fill:#d6b656,color:#fff
    style L4 fill:#b85450,color:#fff
    style L5 fill:#996185,color:#fff
</pre>

The model generates roughly 100-110 tokens/sec on these prompts. Fast enough for interactive use, not fast enough for real-time agent loops. The latency is dominated by the generation phase. Prompt processing is fast (this is a 35B model with only 3B active parameters thanks to the Mixture-of-Experts architecture), but generating 2000+ tokens takes 18-21 seconds.

Here's the raw data:

| Prompt | Latency (ms) | Tokens | tok/s |
|--------|-------------|--------|-------|
| simple_python | 19,565 | 2,087 | 104.68 |
| security_tool | 18,391 | 2,099 | 111.36 |
| context_math | 16,596 | 1,921 | 111.41 |
| vuln_spotting | 18,490 | 2,130 | 100.76 |
| owasp_mapping | 21,000+ | 2,200+ | 105+ |

This kind of data doesn't come from a leaderboard. It tells you whether this model is suitable for your workflow.

## The lm-eval Gotcha

`lm-eval` with `--model vllm` and a llama-server URL as the backend doesn't work out of the box. The model_args format is different from what llama-server expects. I had to figure out that `pretrained=http://127.0.0.1:8081/v1` is the right connection string.

bigcode-eval doesn't support llama-server at all. It's built for vLLM and HuggingFace models. I still run it, but the results are basically meaningless for local models. I left it in because the failure mode is visible and documented.

## How to Use It

```bash
git clone <repo-url>
cd local-llama-bench
./setup.sh
./scripts/run_all.sh --fast
```

Or with the Makefile:

```bash
make setup
make all FAST=1
```

You need Python 3 with pip, llama.cpp built with CUDA (or Metal on Apple Silicon), at least one GGUF model in `~/models/`, and it configured in `config/models.yaml`.

The fast mode runs `--limit 50` for quality benchmarks and skips domain prompts beyond the first three. Full mode runs everything. Either way, the results go into `results/` as CSV and JSON files, and you get a summary table at the end via `utils/metrics.py`.

## Where This Goes Next

A few things I want to add before making this public:

1. **Results visualization.** The metrics.py table is functional but basic. I want something that can plot performance over time, compare multiple models, and highlight regressions.

2. **Better quality benchmark support.** The lm-eval integration works but is fragile. The bigcode-eval integration is essentially broken for local models. I need to find a better approach, maybe running the evaluation prompts directly through the API instead of using the benchmark frameworks.

3. **Multi-model comparison.** Right now the toolkit runs one model at a time. I want a mode that benchmarks multiple models and produces a comparison table with all metrics side by side.

4. **Docker support.** Running this on a clean machine requires setting up llama.cpp, Python dependencies, and the right CUDA drivers. A Docker image would make this accessible to people who don't want to dig into build instructions.

## Why This Matters

If you're running local LLMs, you should know what they can do on your hardware. What they can do on your machine, with your quantization, for your workload.

This toolkit is my attempt to make that possible without spending hours writing custom evaluation scripts every time I try a new model. No web UI, no database, no fancy visualization. Three benchmark categories, one orchestrator script, and a summary table.

The code is rough. The tests are more thorough than the implementation. The domain prompts are specific to my work (security, MCP, agentic AI). It works and it's saved me more time than I expected.

I'll push it to GitHub when I clean it up. Until then, the repo at `~/git/local-llms/benchmarking/local-llama-bench/` is the source of truth.

---

*Amine Raji is a security practitioner with 15+ years across banking, defense, and automotive sectors. He is a CISSP, an OWASP Agentic Security contributor, and currently holds a senior security role at Volvo Cars. All research and views are his own.*
