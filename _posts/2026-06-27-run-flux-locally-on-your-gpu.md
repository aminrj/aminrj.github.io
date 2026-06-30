---
title: "Stop Paying Per Image: Run FLUX on a GPU You Already Own"
date: 2026-06-27
uuid: 202606270000
status: published
published: true
content-type: article
target-audience: intermediate
categories: [AI, Local LLM, Developer Guide]
tags:
  [
    AI,
    FLUX,
    ComfyUI,
    Local Inference,
    RTX 3090,
    Image Generation,
    GGUF,
    WSL2
  ]
image:
  path: /assets/media/ai/run-flux-locally.png
description: The HuggingFace variant maze (quants, support files, gated VAEs) is the only thing standing between a fresh RTX 3090 and your first local image. Here's the path that actually worked, and the FLUX.2 license detail that quietly changes the whole calculation.
mermaid: true
---

I wanted newsletter covers and course diagrams generated locally: on hardware I own, with no per-image API cost and no terms-of-service question about who owns the output. The models to do this are right there, free to download, genuinely good. That part is solved.

What nobody tells you is that the models aren't the hard part. The hard part is the maze you have to cross before your first image renders: a thicket of model variants, quantization formats, and support files with cryptic names that are gated, mislabeled, or three clicks deep in a discussion thread. I lost most of a day in that maze. You don't have to.

Here's the path that worked on a single RTX 3090, in order, plus the licensing detail in the current FLUX.2 lineup that matters more than any benchmark if you're making images you intend to use commercially.

## Picking a model without drowning

Open the FLUX family on HuggingFace and you're immediately underwater. FLUX.1-dev, FLUX.2-dev, FLUX.2 Klein (in 4B and 9B), Pro, Max, plus a dozen community quants of each in FP16, FP8, NF4, and a ladder of GGUF sizes from Q2 to Q8. The natural reaction is paralysis, so here's the decision tree I wish I'd had.

<pre class="mermaid">
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#ede9fe", "primaryBorderColor": "#7c3aed", "fontSize": "14px", "fontFamily": "system-ui, -apple-system, sans-serif"}}}%%
flowchart TB
    S["Want local FLUX on a 3090"] --> D1["Start on FLUX.1-dev<br/>best-documented, runs comfortably"]
    D1 --> Q{"Need commercial license<br/>+ better text rendering?"}
    Q -->|yes| K["FLUX.2 Klein 4B<br/>Apache 2.0 · ~13 GB · output is yours"]
    Q -->|no| STAY["Stay on FLUX.1-dev<br/>(boring, working infrastructure)"]
    classDef n fill:#ede9fe,stroke:#7c3aed,color:#1a202c,stroke-width:1.5px
    classDef win fill:#e6f4ea,stroke:#1e7e34,color:#1a202c,stroke-width:1.5px
    class S,D1,Q,STAY n
    class K win
</pre>

FLUX.1-dev (12B, August 2024) is still the community quality standard and the most-documented. Every workflow, every troubleshooting thread, every LoRA assumes it. It runs comfortably on a 3090. If your goal is "get a good image today," it's the safe pick, and it's the one I got working first.

FLUX.2-dev is the natural upgrade: better prompt accuracy and dramatically better text rendering (it can actually put legible words on an image, which FLUX.1 struggles with). On a 3090 it runs at 4-bit/GGUF in roughly 18–24 GB. Full FP16 needs about 80 GB, which nobody runs locally; ignore that number, it's not for you.

FLUX.2 Klein is the one with the detail that actually matters. It's size-distilled and comes in 4B and 9B. The 4B is Apache 2.0 (fully open, commercially usable, your output is yours) and it fits in about 13 GB, comfortably on a 3090 with room to spare. The 9B is larger and carries a more restrictive non-commercial research license. For newsletter covers and course material that I publish, the 4B's Apache license isn't a footnote. It's the headline: it removes the licensing question from commercial use entirely.

So the honest recommendation: get FLUX.1-dev working first because it's the best-documented path to a working pipeline, then move to FLUX.2 Klein 4B when you care about commercial licensing and better text rendering. Don't start on the newest, biggest thing. Start on the thing with the most troubleshooting threads, then upgrade once you have a working baseline to compare against.

## The support-file scavenger hunt

This is where the day goes. A FLUX model file is not enough to generate anything. It needs support files, and they're the genuinely confusing part because their names look like noise and they live in different places depending on which model version you picked.

For FLUX.1-dev, the trio you need:

- `clip_l.safetensors`: the CLIP text encoder
- `t5xxl_fp8_e4m3fn.safetensors`: the T5 text encoder (FP8 to save VRAM)
- `ae.safetensors`: the VAE (the autoencoder that turns the latent into pixels)

The VAE is the one that trips people: it's gated. You have to accept the license on the FLUX.1-dev model page before HuggingFace will let you download `ae.safetensors`, and the error you get if you skip that step is unhelpful, a 403 or a silently truncated file, not "accept the license first." Accept the license, then download.

For FLUX.2 the scavenger hunt changed, and mixing the two versions' files is a classic time-sink. FLUX.2 dropped the old clip_l + t5xxl combo for a Mistral-based text encoder (`mistral_3_small_flux2_*.safetensors`) plus a `flux2-vae.safetensors`. If you carry FLUX.1's clip_l/t5xxl files into a FLUX.2 workflow, nothing works and the error won't tell you why. The rule: your support files must match your model version. Pick a version, gather its files, don't cross the streams.

Where to actually find the GGUF builds and matching files: city96 is the canonical source for FLUX GGUF quants on HuggingFace, and Unsloth publishes the Klein GGUFs. Those two are where to look first, not whatever a random thread links to.

## ComfyUI from source in WSL2

ComfyUI is the standard interface for FLUX. It supports every quantization format (FP16, FP8, GGUF, NF4) and gets new FLUX features first. There's a managed-install path (Stability Matrix) that's genuinely the fastest way in if you just want it running, and it's worth a mention as the easy button. But I run it from source in WSL2 because I want control over the Python environment and the GPU passthrough, and because the rest of my stack lives there.

Two gotchas cost me time.

The venv gotcha. ComfyUI's dependencies are particular about versions, and if you install into a polluted environment you get import errors that look like ComfyUI bugs but are dependency conflicts. Use a fresh virtual environment, full stop. Don't install ComfyUI's requirements into the same venv as your other ML projects; the torch/CUDA version pins will fight.

The ComfyUI-GGUF custom node is required for GGUF builds. Base ComfyUI can't load a GGUF model file; you need the ComfyUI-GGUF custom node, which adds the `UNETLoader (GGUF)` node. Without it, you'll stare at a model file ComfyUI refuses to load and wonder what's wrong with the download. Install the custom node, restart, and the GGUF loader appears.

```bash
# rough shape of the from-source path in WSL2
git clone https://github.com/comfyanonymous/ComfyUI
cd ComfyUI
python -m venv venv && source venv/bin/activate   # fresh venv, non-negotiable
pip install -r requirements.txt
# then, for GGUF:
cd custom_nodes
git clone https://github.com/city96/ComfyUI-GGUF
pip install -r ComfyUI-GGUF/requirements.txt
```

Drop the model into `models/unet/` (GGUF) or `models/checkpoints/`, the text encoders into `models/clip/`, and the VAE into `models/vae/`. ComfyUI is picky about which folder, and a file in the wrong folder simply doesn't appear in the node's dropdown, another silent failure to know about.

## The workflow settings that actually work

Once the files are placed, the workflow is the last place to get stuck, because the defaults aren't right and the right values differ between FLUX versions.

<pre class="mermaid">
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#ede9fe", "primaryBorderColor": "#7c3aed", "fontSize": "13px", "fontFamily": "system-ui, -apple-system, sans-serif"}}}%%
flowchart LR
    M["UNETLoader (GGUF)"] --> C["Dual CLIP<br/>clip_l + T5 (FP8)"]
    C --> G["FluxGuidance 3.5"]
    G --> K["KSampler<br/>euler · sgm_uniform · 20 steps"]
    K --> V["VAE decode<br/>(ae.safetensors)"]
    V --> IMG["1216×832 image<br/>~12–15s on a 3090"]
    classDef n fill:#ede9fe,stroke:#7c3aed,color:#1a202c,stroke-width:1.5px
    classDef out fill:#e6f4ea,stroke:#1e7e34,color:#1a202c,stroke-width:1.5px
    class M,C,G,K,V n
    class IMG out
</pre>

For FLUX.1-dev, the settings that gave me clean output:

- **FluxGuidance: 3.5.** FLUX uses a guidance-distilled approach; 3.5 is the community sweet spot. Higher gets you over-baked, lower gets you mushy.
- **Steps: 20.** Diminishing returns past this for dev. 20 is the speed/quality balance.
- **Sampler: euler, Scheduler: sgm_uniform.** The reliable pairing for FLUX.1.
- **Resolution: 1216×832.** A 3:2-ish landscape that suits newsletter covers; FLUX handles non-square fine.

The critical caveat: do not carry these onto FLUX.2. FLUX.2-dev's built-in ComfyUI workflow uses CFG 1.0, not a FluxGuidance of 3.5. The guidance mechanism differs between versions, and pasting FLUX.1 settings onto a FLUX.2 graph gives you bad output and a confusing debugging session. When you move to FLUX.2, start from its template workflow and tune from there.

On a 3090, FLUX.1-dev produces an image in roughly 12–15 seconds at these settings; a GGUF Q5 build with FP8 T5 sits around 12 GB and is "very close to full quality." If you have VRAM headroom, Q6 buys a little fidelity; if you're tight, Q4/Q5 fits comfortably and the quality drop is minor.

## What it's actually for

The setup is a means, not the point. Here's where local generation earns its keep in my workflow.

Newsletter covers. A consistent visual identity, generated on demand, zero per-image cost, and (with Klein 4B's Apache license) no question about commercial rights. This alone paid back the setup time.

Course diagrams and illustrations. Concept art and section headers for written material, in a consistent style, without a stock-image subscription or a per-generation API meter running.

Agent-integrated generation. Because it's a local endpoint, I can call it from automation. My n8n flows and my personal agent (Milo) can generate an image as a step in a larger workflow: draft a post, generate its cover, all on hardware I own.

That last one is the real unlock. An API image generator is something you visit. A local endpoint is something your other systems call. Once it's a service on your network, it composes with everything else you've automated.

## Choosing a quant without guessing

The GGUF quant ladder (Q2 through Q8, plus the FP8 and NF4 variants) is its own small maze, and the instinct is to grab the biggest one that fits and hope. There's a cleaner rule.

For FLUX on a 24 GB card, the quality difference between Q8 and Q5 is small enough that most people can't pick the higher one in a blind test, while the VRAM difference is large enough to matter for headroom. So:

- Q6 if you have VRAM to spare. Marginally better fidelity, and on a 3090 running FLUX.1-dev you do have room.
- Q5 with an FP8 T5 encoder is the sweet spot: roughly 12 GB total and, in the words of practitioners who've A/B'd it, "very close to full quality." This is what I run for production covers.
- Q4 when you're tight on VRAM (running other things, or on a 16 GB card). Still good, with a quality drop visible only on close inspection.

The non-obvious part: the text encoder quant matters as much as the model quant for VRAM, and less for quality. Dropping the T5 encoder to FP8 buys you a lot of headroom for almost no visible cost, because the encoder's precision affects prompt understanding more than image fidelity, and FP8 is plenty for understanding. So the efficient configuration isn't "lower the model quant," it's "keep a decent model quant, drop the encoder to FP8." That ordering is the thing nobody tells you, and it's why a Q5 model with an FP8 T5 outperforms a Q4 model with a full-precision encoder at similar total VRAM.

## A short troubleshooting field guide

The failures in this pipeline are almost all silent: no stack trace, just a wrong or absent result. Here's how to read them.

Garbled, noisy, or solid-color output means wrong or mismatched support files. You're almost certainly mixing FLUX.1 and FLUX.2 encoders, or your VAE didn't download fully (the gated one). Re-check that every support file matches your model version.

Model doesn't appear in the node dropdown means it's in the wrong folder. GGUF goes in `models/unet/`, encoders in `models/clip/`, VAE in `models/vae/`. ComfyUI scans specific folders and silently ignores files elsewhere.

"Can't load GGUF" or no GGUF loader node means the ComfyUI-GGUF custom node isn't installed or ComfyUI wasn't restarted after installing it.

Over-baked, plasticky, or burnt images mean guidance too high. Drop FluxGuidance toward 3.5 for FLUX.1; if you're on FLUX.2, you're probably carrying FLUX.1 settings onto it, so switch to CFG 1.0 and the FLUX.2 template.

Out-of-memory at load means the quant is too large for remaining VRAM. Drop the T5 to FP8 first, then the model quant, in that order.

## Why I didn't chase FLUX.2 immediately

A confession that's also advice: I stayed on FLUX.1-dev longer than the "newest is best" instinct wanted, and it was the right call.

The trap with this whole space is that a better model ships every few weeks, and chasing each one means you never have a working pipeline. You have a permanent construction site. FLUX.1-dev was thoroughly documented, every error I hit had a thread, and once it worked end-to-end it became boring infrastructure I stopped thinking about. That's the goal: boring, working, callable.

FLUX.2 Klein 4B is the upgrade I'm actually making now, and notice why: not because it's newer, but because of one concrete reason. The Apache 2.0 license makes the commercial-use question disappear for content I publish. That's a real, specific reason to move, not novelty-chasing. When you upgrade, have a reason like that. "It's the new one" is not a reason.

## The takeaway

The models are free and good. The maze before them (variants, quants, gated VAEs, version-mismatched support files, silent failures with unhelpful errors) is the entire actual difficulty, and it's a navigation problem, not a hard one, once someone hands you the map.

The boring, correct move: get one model working end to end before you touch quants or chase the newest release. Accept the gated VAE license. Match your support files to your model version. Use a fresh venv. Install ComfyUI-GGUF for GGUF builds. Start from the right workflow template for your FLUX version. Do that, and "generate a local image" goes from a lost day to a callable service on your network, at which point it stops being a tool and becomes infrastructure that your agents and automations can use for free, forever, on a GPU you already own.

---

### References & sources

- FLUX.2 local setup, VRAM by GPU, ComfyUI (FLUX.2-dev 4-bit on 3090): [Botmonster](https://botmonster.com/ai/how-to-set-up-flux-2-dev-locally-in-2026/)
- FLUX.2 Klein 4B = Apache 2.0 / commercially usable; 9B more restrictive; ~13 GB on a 3090: [InsiderLLM FLUX guide](https://insiderllm.com/guides/flux-locally-complete-guide/), [Apatero Klein consumer-GPU guide](https://apatero.com/blog/flux-2-klein-consumer-gpu-guide)
- Klein 4B GGUF builds: [unsloth/FLUX.2-klein-4B-GGUF](https://huggingface.co/unsloth/FLUX.2-klein-4B-GGUF); FLUX GGUF canonical source: city96 on HuggingFace
- ComfyUI supports all quant formats and gets FLUX features first; ComfyUI-GGUF required for GGUF: [StableDiffusionTutorials FLUX.2 Klein](https://www.stablediffusiontutorials.com/2026/01/flux2-klein.html)

*FLUX moves monthly. Model versions, VRAM figures, and the exact license terms above are accurate as of mid-2026. Verify the current license on the model's own HuggingFace page before relying on it for commercial work, since license terms in particular can change between releases.*

---

*Amine Raji, PhD, CISSP. Local AI infrastructure and homelab automation.*
