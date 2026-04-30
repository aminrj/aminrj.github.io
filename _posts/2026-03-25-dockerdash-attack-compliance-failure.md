---
title: "The DockerDash Attack Is Also an Article 14 Compliance Failure"
date: 2026-03-25
uuid: 202603250000
draft: true
status: draft
published: false
content-type: article
target-audience: advanced
categories: [AI Security, EU AI Act, Compliance]
tags:
  [
    EU AI Act,
    Article 14,
    Article 15,
    Article 26,
    Human Oversight,
    MCP,
    Docker,
    Agentic AI,
    Supply Chain,
  ]
description: "A poisoned Docker image label triggered autonomous container kills and data exfiltration. No human saw any of the agent's decisions. Under Article 14, that is not just an attack -- it is a compliance failure."
---

In the [DockerDash attack lab](https://aminrj.com/posts/docker-dash-mcp-attack/), a single line of text in a Docker image label caused an AI assistant to autonomously run `docker_ps`, identify running containers, execute `docker_stop` on each one, and exfiltrate a complete infrastructure inventory to an attacker-controlled server. The AI assistant reported: "The image is safe to use."

That article demonstrated two threat models: label injection alone (attacker controls only the Docker image) and label injection combined with a covert MCP tool (attacker also controls one MCP server). Both succeeded. Both ran to completion without any human intervention or awareness.

This article examines the same attack through the EU AI Act. Three articles are directly violated. The one that matters most is Article 14 -- because the DockerDash scenario is the clearest example of what "absence of human oversight" looks like in an agentic AI system.

---

## Article 14: human oversight was absent

[Article 14](https://artificialintelligenceact.eu/article/14/) requires that high-risk AI systems "be designed and developed in such a way, including with appropriate human-machine interface tools, that they can be effectively overseen by natural persons during the period in which they are in use."

Article 14(4) specifies that human oversight measures must enable the individual to:

- (a) Understand the relevant capacities and limitations of the AI system
- (b) Remain aware of possible automation bias
- (c) Correctly interpret the system's output
- (d) Decide not to use the system or to disregard, override, or reverse its output
- (e) Intervene in the operation or stop the system

In the DockerDash scenario, every one of these requirements was violated:

**(a)** The user did not understand that asking "is this image safe?" would trigger container operations. The AI's capacity to execute `docker_stop` based on a label instruction was not visible.

**(b)** The user trusted the AI's assessment ("the image is safe") without awareness that the answer was generated while the agent was simultaneously executing hidden instructions.

**(c)** The user could not interpret the output correctly because the output concealed what the agent actually did. The response said the image was safe. The reality was that containers were stopped and data was exfiltrated.

**(d)** The user had no opportunity to override or reverse. The autonomous tool chain completed in under a second. By the time the user saw the response, the damage was done.

**(e)** No mechanism existed to intervene or stop the agent mid-execution.

This is not a marginal compliance gap. It is a complete absence of the oversight Article 14 requires.

---

## Article 15(3): environmental resilience failure

[Article 15(3)](https://artificialintelligenceact.eu/article/15/) requires high-risk AI systems to be "resilient as regards errors, faults, or inconsistencies that may occur within the system or the environment in which the system operates."

A poisoned Docker image label is an inconsistency in the environment. The image metadata contains instructions that are not part of the image's intended function. A resilient system would detect that the label content is anomalous -- either by validating label schemas, scanning for instruction patterns, or limiting which metadata fields the model can process.

The AI assistant processed the label content without validation. The system was not resilient to an environmental inconsistency. Article 15(3) was not satisfied.

**The control that satisfies Article 15(3):** Input validation on Docker image metadata before the model processes it. Restrict which label fields the agent can read. Scan label content for instruction patterns (the same pattern-matching approach used in prompt injection detection). This adds minimal latency and prevents the entire label injection attack vector.

---

## Article 26(5): deployer was blind

[Article 26(5)](https://artificialintelligenceact.eu/article/26/) requires deployers to "monitor the operation of the high-risk AI system."

In both threat models, the deployer (the person or organization running Docker Desktop with the AI assistant) had no visibility into the agent's autonomous tool calls. There was no log of the `docker_stop` execution. There was no alert when the agent accessed the `docker_ps` inventory. The exfiltration to the external server generated no notification.

The deployer could not monitor what they could not see. Article 26(5) requires that monitoring capability to exist.

---

## What an Article 14-compliant dockerdash would look like

The fix is not "add a confirmation dialog for every tool call." That destroys the product. The fix is choosing the right oversight pattern for the risk level of each tool.

**For `docker_stop` (destructive operation):** Approval gate. The agent proposes the action, the user sees "Agent wants to stop container X -- approve?" before execution. This satisfies Article 14(4)(d) -- the human can decide not to use or reverse. The attack fails because the user sees the unexpected action before it executes.

**For `docker_ps` (read-only, low risk):** Scope limitation. The agent can call `docker_ps` freely but the output is logged and restricted from being passed to external-facing tools in the same chain. This satisfies Article 14(4)(a) -- the user understands that the agent can read container lists but cannot chain that data to external endpoints.

**For the covert MCP tool (exfiltration channel):** Network egress policy. The MCP server configuration restricts which external hosts the agent can contact. If the covert tool tries to reach an attacker-controlled server, the egress policy blocks it. This is both an Article 15(4) resilience control and an Article 14(4)(e) stop mechanism.

These three controls layer to create a defense-in-depth posture that simultaneously prevents the attack and satisfies three EU AI Act articles.

The full set of human oversight engineering patterns -- approval gates, confidence thresholds, scope limitations, and killswitch architecture -- is covered in an upcoming article in this series. The technical detail of the DockerDash attack, including both threat models and every failed attempt along the way, is at [Attacking Docker Desktop via MCP](https://aminrj.com/posts/docker-dash-mcp-attack/).

---

## Action items for teams running ai-assisted Docker tooling

1. **Audit your MCP tool permissions.** Which tools can the AI assistant call? Which are destructive? Classify each by risk level.

2. **Add approval gates for destructive operations.** `docker_stop`, `docker_rm`, `docker_exec` should require explicit user confirmation. This is a configuration change, not a code rewrite.

3. **Implement network egress control.** If your AI assistant does not need to contact external servers, block outbound connections from the MCP server container. A single Docker Compose network policy line prevents the exfiltration channel.

4. **Log every tool call.** Even `docker_ps`. The logging schema does not need to be perfect -- it needs to exist. Start with tool name, timestamp, and parameters.

For the complete Docker hardening approach including tool policies and blast radius control, see [How I Deployed OpenClaw as an AI Security Researcher](https://aminrj.com/posts/openclaw-secure-deployment/). For the full MCP threat model, see [MCP Security Top 10](https://aminrj.com/posts/owasp-mcp-top-10/).

---

*This article is part of a series mapping agentic AI security research to EU AI Act compliance requirements. The full attack walkthrough is at [Attacking Docker Desktop via MCP: From Theory to PoC](https://aminrj.com/posts/docker-dash-mcp-attack/). The deployer obligation chain is at [GPAI Meets Agentic AI](https://aminrj.com/posts/gpai-meets-agentic-ai/).*
