---
title: "Qwen3.6 on 24GB VRAM: Benchmark, Config, and Every Mistake"
date: 2026-04-18
uuid: 202604180000
content-type: article
target-audience: advanced
categories: [AI Security, LLM, Developer Guide]
tags:
  [
    llama.cpp,
    Ollama,
    Qwen3.6,
    Mixture of Experts,
    RTX 3090,
    Local LLM,
    GPU Optimization,
    Benchmark,
  ]
image:
  path: /assets/media/ai/qwen3-6-on-24gb-vram.png

description: "24GB of VRAM. A 35B-parameter model. 65k context window. It shouldn't work on paper — but KV cache quantization, flash attention, and Mixture of Experts make it not just possible but fast. Here's every knob I turned, every obstacle I hit, and the numbers that prove 24GB is enough."
---

## TL;DR — the honest numbers

| Model | Backend | Short | Medium | Long | Context | VRAM |
|---|---|---|---|---|---|---|
| Qwen3.5-35B-A3B | Ollama | 98.9 | 99.0 | 96.3 tok/s | 32k | 23.4 GB |
| Qwen3.5-35B-A3B | **llama.cpp** | **142.2** | **136.3** | **133.1 tok/s** | **65k** | **21.7 GB** |
| Qwen3.6-35B-A3B | Ollama | — | — | — | N/A | N/A |
| Qwen3.6-35B-A3B | **llama.cpp** | **101.7** | **98.9** | **80.9 tok/s** | **65k** | **24.2 GB** |

**Three findings that hold up:**
- llama.cpp is ~**1.4× faster** than Ollama on Qwen3.5 (not 2.4× — that was a flawed benchmark)
- llama.cpp gives **2× the context** at **lower VRAM** via KV cache quantization
- Qwen3.6 **only runs on llama.cpp** — Ollama doesn't support it yet

---

## Contents

1. [Why move beyond Ollama](#1-why-move-beyond-ollama)
2. [The theory: what actually matters](#2-the-theory-what-actually-matters)
3. [The setup: what I built](#3-the-setup-what-i-built)
4. [The obstacles I hit](#4-the-obstacles-i-hit)
5. [Benchmark methodology](#5-benchmark-methodology)
6. [The real numbers](#6-the-real-numbers)
7. [Qwen3.6: a new requirement](#7-qwen36-a-new-requirement)
8. [Daily workflow reference](#8-daily-workflow-reference)
9. [OpenCode integration](#9-opencode-integration)
10. [Conclusions](#10-conclusions)

---

## 1. why move beyond Ollama

Ollama is great for getting started. `ollama run qwen3-coder:30b` and you have a local model in 30 seconds. I used it happily until I read a Reddit post where someone was getting 100+ tok/s on a 35B MoE model with a 4090 — same VRAM budget as my 3090. They were using llama.cpp directly, not Ollama, with explicit control over parameters Ollama doesn't expose.

I was getting ~55-60 tok/s. There was a gap worth investigating.

**What Ollama hides from you:** Ollama wraps llama.cpp but strips the knobs. No KV cache quantization, no explicit flash attention control, no batch size tuning, no expert offloading strategy, no context size guarantee. For a 24GB card where every MB matters, this leaves real performance on the table.

There's also a compatibility ceiling that only became apparent when Qwen3.6 dropped: Ollama doesn't support the latest multimodal models because of how it handles separate vision projector files. As models get more capable and multimodal, the abstraction becomes a constraint.

---

## 2. the theory: what actually matters

### MoE — why 35b runs like 3.6b

Both Qwen3.5 and Qwen3.6 are Mixture of Experts models with **35B total parameters but only 3.6B active per forward pass**. The "A3B" means exactly this. A router activates only the relevant experts per token. Inference cost ≈ a 3.6B dense model. Quality ≈ a 35B dense model. This is why 100+ tok/s is achievable on consumer hardware.

### KV cache quantization — the silent VRAM killer

The KV cache stores computed attention keys and values for every context token. At f16 (Ollama's default), a 65k context window consumes ~10-15GB on top of model weights — blowing the 24GB budget. With q8_0 quantization (`--cache-type-k q8_0`), that footprint halves. This is how llama.cpp fits Qwen3.5 at **65k context in 21.7GB** while Ollama needs **32k context and still uses 23.4GB**.

| Format | Bits/weight | Quality | 35B model size |
|---|---|---|---|
| f16 | 16 | Reference | ~70 GB |
| Q8_0 | 8 | Near-lossless | ~37 GB |
| **Q4_K_M / UD-Q4_K_XL** | **4.5** | **Very good** | **~21–23 GB** |
| IQ3_XXS | 3.5 | Good for large | ~15 GB |

### Flash attention

A fused kernel that computes attention without materializing the full N×N matrix in HBM. Cuts VRAM for attention computation by ~30%, improves throughput by keeping data on-chip. One flag: `--flash-attn on`. Free performance on the 3090 (compute capability 8.6, fully supported).

### GPU layer offloading

With `--n-gpu-layers 99`, llama.cpp pushes as many transformer layers as VRAM allows to GPU. For MoE models, attention layers are compute-bound and live on GPU; expert weights can spill to RAM with tolerable speed loss since only 8 of 256 experts activate per token.

---

## 3. the setup: what I built

The goal: Ollama stays available for quick tasks and model management, while llama.cpp handles serious sessions — with zero friction to switch and zero re-downloads.

### One model file, two tools

Ollama stores models as sha256-named blobs in `/usr/share/ollama/.ollama/models/blobs/` (native Linux install). These blobs are actual GGUFs with opaque names. llama.cpp can mount and load them directly. A small script reads the manifest JSON, extracts the digest, and creates a human-readable symlink. No re-download.

### Repo structure

```
local-llm-ops/
├── compose/                    # Docker track (Qwen3.5 and older)
│   ├── base.yml                # shared GPU + volume config
│   ├── qwen3.5-35b-a3b.yml     # model-specific flags
│   └── qwen3-coder-30b.yml
├── scripts/
│   ├── build-llamacpp.sh       # build from source
│   ├── run-qwen3.6-35b-a3b.sh  # native binary track
│   ├── link-from-ollama.sh     # symlink blob → readable path
│   ├── download-qwen3.6.sh     # hf download wrapper
│   └── benchmark.sh
├── models/
│   ├── qwen3.5-35b-a3b.Modelfile
│   └── qwen3.6-35b-a3b-gpu.Modelfile
└── Makefile                    # the daily driver UX
```

### Two tracks for two realities

**Docker track (stable)** — works for Qwen3.5 and older, reproducible, no build required, lags behind new model releases.

**Native track (current)** — required for Qwen3.6 and newer, built from source, always latest, supports mmproj for vision models.

### Key config — qwen3.5 (docker)

```yaml
# compose/qwen3.5-35b-a3b.yml
command: >
  -m /blobs/sha256-f25d60...
  --port 8080 --host 0.0.0.0
  --ctx-size     65536       # 64k context
  --n-gpu-layers 40          # all layers on GPU
  --cache-type-k q8_0        # KV cache quantized → half footprint
  --cache-type-v q8_0
  --cache-ram    4096        # prevent OOM on parallel tool calls
  --flash-attn   on          # free perf on RTX 3090
  --parallel     1           # single inference slot
  --temp 0.6 --top-p 0.95 --top-k 20
```

### Key config — qwen3.6 (native binary)

```bash
# scripts/run-qwen3.6-35b-a3b.sh
~/llama.cpp/llama-server \
  --model  .../Qwen3.6-35B-A3B-UD-Q4_K_XL.gguf \
  --mmproj .../mmproj-F16.gguf \   # vision projector — required for 3.6
  --alias  "qwen3.6-35b-a3b" \
  --port 8081 --host 0.0.0.0 \
  --ctx-size     65536 \
  --n-gpu-layers 99 \
  --cache-type-k q8_0 \
  --cache-type-v q8_0 \
  --cache-ram    4096 \
  --flash-attn   on \
  --parallel     1 \
  --temp 0.6 --top-p 0.95 --top-k 20 --min-p 0.0
```

---

## 4. the obstacles I hit

Documenting these because they cost hours and are easy to miss.

**1. Docker Desktop WSL integration conflict**
Docker Desktop was running on Windows, not WSL. Enabling Ubuntu-24.04 as both "default" and "additional" caused a write conflict on `~/.docker/config.json`. Fix: install native Docker Engine in WSL via `get.docker.com`, disable Docker Desktop WSL integration entirely.

**2. nvidia-container-toolkit GPG key**
The standard install instructions need a `sed` command to inject `signed-by=...` into the apt source line. Without it, apt rejects the repo as unsigned.
```bash
curl -fsSL .../nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
```

**3. Port 8080 held by Yamaha Device Center on Windows boot**
A Windows audio app auto-binds port 8080 on startup. Fix: move llama.cpp to port 8081 permanently. Check with `netstat -ano | findstr :8080` in PowerShell. Kill with `taskkill /PID <PID> /F`.

**4. --flash-attn flag changed in newer llama.cpp**
Newer builds require an explicit value: `--flash-attn on`, not just `--flash-attn`. The container restarts silently with a usage error if you use the old form.

**5. Docker image too old for Qwen3.6**
The `ghcr.io/ggml-org/llama.cpp:server-cuda` image was built before Qwen3.6's architecture change (3-element vs 4-element rope sections). Error: `rope.dimension_sections has wrong array length; expected 4, got 3`. Fix: build llama.cpp from source.

**6. Ollama silently splits CPU/GPU**
My first Ollama benchmark showed 53-61 tok/s. `ollama ps` showed `17%/83% CPU/GPU` and `SIZE: 28GB on a 24GB card`. The model was overflowing to RAM. The real Ollama speed with a clean environment is ~99 tok/s — very different.

**7. CUDA toolkit not installed in WSL**
The Windows NVIDIA driver provides GPU access via WSL passthrough, but the CUDA toolkit still needs to be installed separately to build CUDA code.
```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update && sudo apt-get install -y cuda-toolkit-12-8
```

---

## 5. benchmark methodology

### What was wrong in v1

The first benchmark showed Ollama at 53-61 tok/s vs llama.cpp at 130-136 tok/s — a 2.4× gap. This was flawed because Ollama was silently splitting CPU/GPU. Not a fair comparison.

### The clean protocol

```bash
# 1. Verify VRAM is fully clear before each run
nvidia-smi --query-gpu=memory.used --format=csv,noheader  # expect ~700 MiB

# 2. Confirm Ollama is 100% GPU
ollama ps  # check PROCESSOR column

# 3. Include a warm-up request (not measured)
curl -s "$URL/chat/completions" \
  -d '{"model":"...","messages":[...],"max_tokens":5}' > /dev/null
sleep 2

# 4. Pass identical sampling params to both backends
-d "{...,\"temperature\":0.6,\"top_p\":0.95,\"top_k\":20}"

# 5. Sleep between prompts
sleep 3
```

Three prompts, 512 token output cap, same model file (same GGUF blob for Qwen3.5), VRAM snapshot at end of each run.

---

## 6. the real numbers

### Generation speed (tok/s)

```
Qwen3.5 — Short prompt ("Write a fibonacci function in Rust")
  llama.cpp  ████████████████████████████████████████  142.2
  Ollama     ████████████████████████████              98.9

Qwen3.5 — Medium prompt ("Thread-safe LRU cache in Rust with Arc and Mutex")
  llama.cpp  ██████████████████████████████████████    136.3
  Ollama     ████████████████████████████              99.0

Qwen3.5 — Long prompt ("JWT middleware across Rust, TypeScript, Python")
  llama.cpp  █████████████████████████████████████     133.1
  Ollama     ███████████████████████████               96.3

Qwen3.6 — Short prompt
  llama.cpp  ████████████████████████████              101.7
  Ollama     N/A — model not supported

Qwen3.6 — Long prompt
  llama.cpp  ███████████████████████                   80.9
  Ollama     N/A — model not supported
```

### What these numbers actually mean

**Finding 1 — Speed: llama.cpp is 1.4× faster on Qwen3.5**
136 vs 99 tok/s, not 2.4×. Over a long session: a 512-token response takes 3.7s vs 5.2s. Across dozens of exchanges this accumulates into a real difference in flow.

**Finding 2 — Context: llama.cpp gives 2× the window at lower VRAM**
65k context at 21.7GB (llama.cpp) vs 32k context at 23.4GB (Ollama). The q8_0 KV cache quantization halves the cache footprint, giving double the context window while using less VRAM simultaneously. For repo-level coding tasks, 65k vs 32k is the difference between fitting the whole codebase or not.

**Finding 3 — Qwen3.6 is ~30% slower than Qwen3.5**
101 vs 142 tok/s at peak. The hybrid attention mechanism (Gated Delta Net) adds compute per token, and the model is slightly larger (22GB vs 21.7GB weights). You're paying a speed tax for the capability upgrade.

**Finding 4 — Qwen3.6 requires llama.cpp**
The newest frontier model only runs on the better stack. If you want to use current models as they drop, you need infrastructure that can keep up.

---

## 7. qwen3.6: a new requirement

Qwen3.6 dropped April 16, 2026. It introduced a new rope encoding format that broke every existing llama.cpp Docker image. The `server-cuda` tag on ghcr.io was already behind on release day.

This exposed the structural problem with the Docker approach: **floating image tags lag behind model releases**. For staying current with frontier models, you need a binary you control.

### Build llama.cpp from source — one time

```bash
# Install CUDA toolkit (~2GB, one-time)
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update && sudo apt-get install -y cuda-toolkit-12-8

# Add to PATH
echo 'export PATH=/usr/local/cuda/bin:$PATH' >> ~/.zshrc
source ~/.zshrc

# Clone and build (~5-10 minutes)
git clone https://github.com/ggml-org/llama.cpp ~/llama.cpp
cmake ~/llama.cpp -B ~/llama.cpp/build \
    -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON
cmake --build ~/llama.cpp/build \
    --config Release -j$(nproc) --target llama-server
cp ~/llama.cpp/build/bin/llama-server ~/llama.cpp/llama-server

# Verify
~/llama.cpp/llama-server --version
```

### Qwen3.6 requires mmproj

Qwen3.6 is a vision model. You must pass `--mmproj mmproj-F16.gguf` when running it. Ollama's blob doesn't include this file — download from Unsloth's repo directly.

```bash
# hf is the HuggingFace CLI (~/.local/bin/hf)
hf download unsloth/Qwen3.6-35B-A3B-GGUF \
    --local-dir /usr/share/ollama/.ollama/models/Qwen3.6-35B-A3B \
    --include "*UD-Q4_K_XL*" \
    --include "*mmproj-F16*"
```

> **Note:** Do NOT use CUDA 13.2 with Qwen3.6 — it produces gibberish outputs. NVIDIA is working on a fix. Check your version with `nvidia-smi | grep "CUDA Version"`.

---

## 8. daily workflow reference

### Starting models

| Task | Command |
|---|---|
| Qwen3.5 via llama.cpp (Docker) | `make run-qwen3.5-35b-a3b` |
| Qwen3.6 via native binary | `make run-qwen3.6-35b-a3b` |
| Quick task via Ollama | `ollama run qwen3-coder:30b` |
| Wait until llama.cpp is ready | `make wait` |

### Checking status

| What | Command |
|---|---|
| Is llama.cpp running? | `docker ps --filter name=llama-server` |
| Is the server ready? | `curl http://localhost:8081/v1/models` |
| Which model is loaded? | `curl -s localhost:8081/v1/models \| python3 -m json.tool` |
| Is Ollama running a model? | `ollama ps` |
| VRAM usage right now | `nvidia-smi --query-gpu=memory.used,memory.free --format=csv,noheader` |
| Watch VRAM live | `watch -n 2 nvidia-smi --query-gpu=memory.used --format=csv,noheader` |
| Full GPU stats | `nvidia-smi` |

### Testing inference

```bash
# llama.cpp (port 8081)
curl -s http://localhost:8081/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"local","messages":[{"role":"user","content":"reply WORKING"}],"max_tokens":5}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['choices'][0]['message']['content'])"

# Ollama (port 11434)
curl -s http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen3-coder:30b","messages":[{"role":"user","content":"reply WORKING"}],"max_tokens":5}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['choices'][0]['message']['content'])"
```

### Stopping and unloading

| Task | Command |
|---|---|
| Stop llama.cpp (Docker track) | `make stop` |
| Stop llama.cpp (native track) | `pkill -f llama-server` |
| Unload Ollama model from VRAM | `ollama stop qwen3-coder:30b` |
| Confirm VRAM cleared | `nvidia-smi --query-gpu=memory.used --format=csv,noheader` |

### Switching models cleanly

```bash
# Always stop first, verify VRAM clears, then start next
make stop
nvidia-smi --query-gpu=memory.used --format=csv,noheader  # expect ~700 MiB
make run-qwen3.6-35b-a3b
make wait
```

### Keeping the binary current

```bash
# Update and rebuild (~5-10 min)
make update-llamacpp

# Check current build number
~/llama.cpp/llama-server --version
```

### Adding a new model

1. Pull via Ollama if available: `ollama pull model:tag`
2. Or download from HuggingFace: `hf download repo/model --local-dir /path --include "*.gguf"`
3. Get the blob hash: `make link-<model>` — extracts sha256 from manifest
4. Copy nearest compose yml or run script, update the model path
5. Add Makefile target and OpenCode entry

### Debugging

| Problem | Command |
|---|---|
| View server logs | `docker logs llama-server --tail 30` |
| Port already in use | `sudo ss -tlnp \| grep 8081` |
| Port held by Windows process | `netstat -ano \| findstr :8081` (PowerShell) |
| Kill Windows process | `taskkill /PID <PID> /F` (PowerShell) |
| Model not loading | `docker logs llama-server 2>&1 \| grep -i "error\|failed"` |
| Native binary crash | Run without `&` to see output directly |
| Check VRAM before/after | `nvidia-smi --query-gpu=memory.used --format=csv,noheader` |

---

## 9. opencode integration

Both backends are configured as separate providers. Switching is a `/model` command mid-session — no restart needed.

```json
// ~/.config/opencode/config.json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "ollama": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Ollama",
      "options": { "baseURL": "http://localhost:11434/v1" },
      "models": {
        "qwen3-coder:30b":         { "name": "qwen3-coder:30b" },
        "qwen3.5:35b-a3b-q4_K_M": { "name": "qwen3.5:35b-a3b-q4_K_M" },
        "gemma4:26b":              { "name": "gemma4:26b" }
      }
    },
    "llamacpp": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "llama.cpp",
      "options": { "baseURL": "http://localhost:8081/v1" },
      "models": {
        "qwen3.5-35b-a3b": { "name": "qwen3.5-35b-a3b" },
        "qwen3.6-35b-a3b": { "name": "qwen3.6-35b-a3b" }
      }
    }
  }
}
```

### Switching providers in session

| Task | Command |
|---|---|
| Switch to llama.cpp Qwen3.6 | `/model llamacpp/qwen3.6-35b-a3b` |
| Switch to Ollama quick model | `/model ollama/qwen3-coder:30b` |
| Switch to Claude | `/model anthropic/claude-sonnet-4-6` |

### Which model for what

| Task | Model | Why |
|---|---|---|
| Long coding session, repo-level | llama.cpp + Qwen3.6 | 65k context, latest model, best agentic coding |
| Complex refactor, architecture | llama.cpp + Qwen3.5 | Faster than 3.6, still 65k context |
| Quick question, small task | Ollama + qwen3-coder:30b | Instant start, no container overhead |
| Embedding generation | Ollama + mxbai-embed-large | No reason to run embeddings through llama.cpp |
| When local isn't enough | Claude Sonnet 4.6 | Some things still need the frontier |

---

## 10. conclusions

The honest gains from moving to llama.cpp on a 3090:

- **1.4× faster generation** (not 2.4× — that was wrong)
- **2× context window** at lower VRAM, via q8_0 KV cache
- **Day-one support** for new models like Qwen3.6

The speed gain is real but modest. The context gain matters more for coding. The compatibility requirement is the strongest argument: if you want to run frontier models as they drop, you need infrastructure that can keep up. Ollama will catch up to Qwen3.6 eventually — but eventually isn't day one.

Ollama isn't gone from the setup. It handles quick tasks, manages the model library, and serves embedding models. llama.cpp handles everything serious. The repo makes switching between them a single `make` command.

Everything described here — compose files, Makefile, benchmark script, run scripts, download helpers — is at [github.com/aminrj/local-llm-ops](https://github.com/aminrj/local-llm-ops). Adding a new model when it drops is two files and one Makefile target.

---

*Published on [aminrj.com](https://aminrj.com) · AI Security Intelligence newsletter*