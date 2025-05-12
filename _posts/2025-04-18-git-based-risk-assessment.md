---
title: "Git-Based Risk Assessments: A Developer-Centric Approach to Security at Scale"
categories:
  - Cybersecurity
  - Risk Assessment
tags:
  - Risks
  - Developers
image:
  path: /assets/media/cybersecurity/git-based-risk-assessment-thumb.png
---

In most enterprise environments, security risk assessments are still managed via
outdated workflows — static web pages, scattered spreadsheets, or rigid
GRC platforms that feel completely detached from how modern software teams work.

These tools were not built for developers. They’re built for compliance teams.

And while auditability matters, so does usability and adoption or buy-in from
developers.

## Why We Want to Rethink Risk Management

We were facing the same problem you probably are:

- Multiple teams building microservices at high velocity.
- Risk assessments managed in a web page with inconsistent formatting.
- Difficult to track who changed what, and when.
- No automation, no CI/CD integration, no versioning.

So we flipped the model.

Instead of dragging developers into slow and clunky GRC systems, we brought risk
management to where they already are: **Git**.

## The Git-Based Risk Assessment Model

Here’s the TL;DR:

- Risks are documented as **YAML files** in Git.
- System context (architecture, components, security controls) is versioned alongside.
- All changes are auditable by design.
- Validation, aggregation, and dashboards are automated via CI pipelines.
- Visualization is handled through a static dashboard using Chart.js + GitLab Pages.

It’s fast, transparent, version-controlled, and developer-friendly.

## What the Structure Looks Like

```bash
risk-assessments/
├── systems/
│   └── sample-app/
│       ├── metadata.yaml
│       ├── architecture.md
│       └── security-profile.yaml
├── risks/
│   └── sample-app/
│       └── RISK-0100.yaml
├── scripts/
│   ├── validate.py
│   └── aggregate.py
├── schemas/
│   └── risk.schema.json
├── dashboards/
│   ├── index.html
│   ├── dashboard.js
│   └── aggregated.json
└── .gitlab-ci.yml
```

## Sample Risk Definition (YAML)

```yaml
id: RISK-0100
title: Admin panel exposed without IP restriction
description: >
  The /admin panel is publicly accessible and does not enforce IP allowlisting.
owner: team-sample
likelihood: Medium
impact: High
status: Open
mitigation_steps:
  - Restrict /admin to internal IP ranges
  - Implement 2FA for admin accounts
reference:
  - threat_library: mitre-attck
    id: T1069
```

Everything from likelihood to MITRE ATT\&CK mapping is explicit, validated, and versioned.

## System Context Is Not Optional

Here’s the thing: documenting a risk without knowing the system is useless.

That’s why every application gets a `/systems/<app>/` folder that includes:

### `metadata.yaml`

```yaml
id: sample-app
name: sample Web Application
owner: team-sample
business_impact: Medium
data_classification: PII
deployment_envs:
  - production
  - dev
```

### `architecture.md`

```markdown
## Architecture Overview

- Node.js backend, EJS frontend
- PostgreSQL database
- Public login + admin panel

![Diagram](./sample-arch.png)
```

### `security-profile.yaml`

```yaml
authentication: Local username/password
authorization: Basic role-based
data_encryption:
  at_rest: true
  in_transit: true
external_dependencies:
  - sendgrid.com
  - postgres (self-managed)
```

This is what sets the stage for meaningful risk identification.

## Automation : CI/CD + GitLab

We added a simple `.gitlab-ci.yml`:

```yaml
validate_risks:
  image: python:3.10
  script:
    - pip install pyyaml jsonschema
    - python scripts/validate.py

aggregate_risks:
  script:
    - python scripts/aggregate.py
  artifacts:
    paths:
      - aggregated.json
      - aggregated.csv
```

This gives us:

- Schema validation of all risk files on every commit
- Artifacts for downstream processing or reporting
- Immediate feedback to the team if something breaks

## Publish Dashboards Automatically

We publish the dashboard with Chart.js using GitLab Pages.

It visualizes:

- Risk status counts
- Likelihood & impact distributions
- Heatmap (likelihood × impact)

And the best part? It auto-deploys every time a new risk is committed.

> URL format: `https://<group>.gitlab.io/<project>/`

## Why It Works in the Real World

This approach nails the things auditors and engineers both care about:

| Requirement            | Solution                    |
| ---------------------- | --------------------------- |
| Audit trail of changes | Git history + blame         |
| Schema validation      | JSON schema in CI           |
| Team accountability    | Code ownership + MR reviews |
| Cross-team visibility  | Aggregation + dashboards    |
| Compliance linkage     | MITRE, OWASP references     |

It’s simple, robust, and scalable.

## What It’s Not

- It’s not a replacement for enterprise GRC platforms if you're chasing
  ISO/PCI ready dashboards.
- It’s not a ticketing system.
- It’s not a one-click "compliance in a box".

But it **is** a fast, auditable, and developer-first way to **treat risk like code**.

## Next Steps

We’re already evolving the tool to:

- Validate references against MITRE and CSA CCM
- Add RBAC and secure a front-end SaaS-hosting
- Integrate with local LLMs for automated risk suggestions

This is the kind of solution that gets real adoption — because it fits into
the way developers work, not against it.

Let me know if you’re adopting something similar — I would love to collaborate.
