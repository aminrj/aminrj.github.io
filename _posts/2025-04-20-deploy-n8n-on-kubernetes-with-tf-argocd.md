---
title: "Deploy n8n on Kubernetes using GitOps with Terraform and ArgoCD"
categories:
  - Automation
  - Kubernetes
  - GitOps
  - Workflows
tags:
  - Kubernetes
  - n8n
  - Automation
  - Infrastructure as Code
  - External Secrets
  - Terraform
  - ArgoCD
image:
  path: /assets/media/n8n/n8n-cnpg-deployment.png
---

Bootstrapping a Scalable, GitOps‑Driven n8n Automation Platform on Kubernetes.

_A production‑grade guide to deploying n8n on Kubernetes using CloudNativePG, ArgoCD, and Terraform._

> **TL;DR** – In under an hour, you'll have n8n running on Kubernetes with:
>
> - A dedicated, highly‑available PostgreSQL cluster using CloudNativePG
> - Secrets securely managed in Azure Key Vault via External Secrets Operator
> - CI-friendly, declarative deployment via ArgoCD & Kustomize overlays
> - Resilient, observable infrastructure with built-in failover and backups

![n8n Start Screen (dark mode)](/assets/media/n8n/n8n-dashboard-dark.png)

## Why Self-Host n8n in Kubernetes?

n8n is a powerful open-source automation tool.

We use automation tools like n8n to simplify our workflows — but what about
the deployment and management of n8n itself?

In the era of cloud-native applications, delivering a reliable, scalable
automation platform demands more than docker run.

It demands GitOps.

While you can run it with Docker, Kubernetes offers much more:

- **Persistence and scalability** for real workloads
- **Secrets management** via external vaults (no plaintext in Git)
- **HA Postgres** via CloudNativePG (each app gets its own cluster)
- **GitOps workflow** — push YAML to deploy and recover fast

This tutorial shows how to deploy n8n like a cloud-native service
— Git first, API-secured, and production-ready.

## Why Automating Automation Itself Matters

## 2 – Architecture Overview

```
┌──────────────────────┐              ┌────────────────────────────┐
│  Developers          │  git         │  Git repository            │
│  push YAML/TF        ├─────────────▶│  apps/   databases/        │
└──────────────────────┘              │  argocd/                   │
          ▲ gitops sync               └──────────▲─────────────────┘
          │                                       │
┌─────────┴────────┐                          ┌───┴─────────────┐
│     ArgoCD       │  applies manifests       │  Kubernetes     │
│ (ApplicationSet) ├─────────────────────────▶│  cluster        │
└─────────┬────────┘                          └────┬────────────┘
          │ Helm / CRDs                            │
┌─────────▼────────┐                         ┌────▼──────────────────────────┐
│ Terraform        │  installs operators     │  CNPG operator (HA PG)        │
│ (cluster-admin)  ├────────────────────────▶│  External-Secrets operator    │
└──────────────────┘                         └───────────────────────────────┘
```

## 3 – Prerequisites

| Tool                      | Version tested | Purpose                     |
| ------------------------- | -------------- | --------------------------- |
| Kubernetes                | ≥ 1.27         | Where everything runs       |
| Terraform                 | ≥ 1.5          | Infrastructure provisioning |
| ArgoCD                    | ≥ 2.8          | GitOps sync engine          |
| CloudNativePG             | ≥ 1.22         | PostgreSQL operator         |
| External-Secrets Operator | ≥ 0.9          | Secret sync from Azure KV   |
| Azure Key Vault           | Any            | Secret backend              |

Also needed: `kubectl`, `kustomize`, and a Git repo.

## 4 – Repository Layout

We follow a **Kustomize base/overlay** GitOps layout:

```
apps/
  └── n8n/
      ├── base/
      │   ├── deployment.yaml
      │   ├── service.yaml
      │   └── kustomization.yaml
      └── overlays/
          └── dev/
              ├── secrets.yaml  # ExternalSecret → Azure KV
              ├── namespace.yaml
              └── kustomization.yaml

databases/
  └── n8n/
      ├── base/
      │   └── database.yaml     # CloudNativePG cluster
      └── overlays/
          └── dev/
              ├── secrets.yaml  # Azure blob backup secrets
              ├── scheduled-backup.yaml
              └── kustomization.yaml

argocd/
  ├── applicationset.yaml
  ├── db-applicationset.yaml
  └── external-secret-application.yaml
terraform/
  └── main.tf
```

This structure allows multiple environments (`dev`, `qa`, `prod`) to share base
logic and override only the differences.

## 5 – Terraform Bootstrap

The `terraform/main.tf` file installs all cluster-level operators:

```terraform
resource "helm_release" "cnpg" {
  name       = "cloudnative-pg"
  repository = "https://cloudnative-pg.github.io/charts"
  chart      = "cloudnative-pg"
  version    = "0.20.1"
  namespace  = "cnpg-system"
  create_namespace = true
}

resource "helm_release" "external_secrets" {
  name       = "external-secrets"
  repository = "https://charts.external-secrets.io"
  chart      = "external-secrets"
  version    = "0.9.16"
  namespace  = "external-secrets"
  create_namespace = true
}

resource "helm_release" "argo_cd" {
  name       = "argocd"
  repository = "https://argoproj.github.io/argo-helm"
  chart      = "argo-cd"
  version    = "5.51.6"
  namespace  = "argocd"
  create_namespace = true
  set {
    name  = "configs.params.server.insecure"
    value = true
  }
}
```

Run `terraform apply` to provision these foundational components.

Then watch the happy pods come to life:

![n8n-running-pods](/assets/media/n8n/n8n-running-pods.png)

## 6 – Deploy the PostgreSQL Cluster for n8n

`databases/n8n/base/database.yaml` defines the per-app CloudNativePG cluster:

```yaml
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: n8n-db-cnpg-v1
spec:
  imageName: quay.io/enterprisedb/postgresql:16.1
  instances: 3
  storage:
    size: 5Gi
  bootstrap:
    initdb:
      database: n8n
      owner: n8n
      secret:
        name: n8n-db-creds
  backup:
    barmanObjectStore:
      destinationPath: https://<yourblob>.blob.core.windows.net/n8n-db
      azureCredentials:
        storageAccount:
          name: n8n-db-storage
          key: container-name
        storageSasToken:
          name: n8n-db-storage
          key: blob-sas
    retentionPolicy: 14d
```

The `*-rw` service is created automatically by CNPG — we’ll use it in our deployment.

Here are the pods of our highly-available PostgresQL cluster:

![n8n-cnpg-cluster-pods](/assets/media/n8n/n8n-cnpg-cluster.png)

## 7 – n8n Deployment with Kustomize

### `apps/n8n/base/deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: n8n
spec:
  replicas: 1
  selector:
    matchLabels:
      app: n8n
  template:
    metadata:
      labels:
        app: n8n
    spec:
      containers:
        - name: n8n
          image: docker.n8n.io/n8nio/n8n:latest
          ports:
            - containerPort: 5678
          env:
            - name: DB_TYPE
              value: postgresdb
            - name: DB_POSTGRESDB_HOST
              value: n8n-db-cnpg-v1-rw.cnpg-dev.svc.cluster.local
            - name: DB_POSTGRESDB_DATABASE
              value: n8n
            - name: DB_POSTGRESDB_SCHEMA
              value: public
            - name: N8N_ENCRYPTION_KEY
              valueFrom:
                secretKeyRef:
                  name: n8n-encryption
                  key: key
            - name: N8N_DEFAULT_EDITION
              value: community
            - name: N8N_RUNNERS_MODE
              value: internal
            - name: N8N_DIAGNOSTICS_ENABLED
              value: "false"
          volumeMounts:
            - name: n8n-data
              mountPath: /home/node/.n8n
      volumes:
        - name: n8n-data
          emptyDir: {}
```

## 8 – ApplicationSets in ArgoCD

Use a Git-based generator in `argocd/applicationset.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: apps
spec:
  generators:
    - git:
        repoURL: https://github.com/your-org/homelab-gitops.git
        revision: main
        directories:
          - path: apps/*/overlays/*
  template:
    metadata:
      name: "{{path.basename}}"
    spec:
      source:
        repoURL: https://github.com/your-org/homelab-gitops.git
        targetRevision: main
        path: "{{path}}"
      destination:
        server: https://kubernetes.default.svc
        namespace: "{{path.basename}}"
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

## 9 – First Git Push ➜ Running Stack

Once your Git repo is ready:

```bash
git add apps/n8n databases/n8n
git commit -m "feat(n8n): deploy app and db"
git push
```

ArgoCD will pick it up, apply manifests, and in a few minutes:

```bash
kubectl get pods -n n8n-dev
kubectl port-forward svc/n8n 5678:80 -n n8n-dev
```

![Argocd applications for n8n app and db](/assets/media/n8n/argocd-n8n.png)

Go to `http://localhost:5678` and sign up.

![n8n sign-up screen](/assets/media/n8n/n8n-register-screen.png)

## 10 – Backup and Restore

CloudNativePG handles:

- Daily full backups
- WAL-based point-in-time recovery

To test a restore:

```yaml
bootstrap:
  recovery:
    source: clusterBackup
    database: n8n
    owner: n8n
    secret:
      name: n8n-db-creds
```

## 11 – Monitoring

CNPG exports Prometheus metrics by default.

Use `PodMonitor` and Grafana dashboard ID `18630` to visualize cluster health.

## Conclusion

In this guide, we showed how to deploy n8n on Kubernetes the right way:
with its own dedicated, HA PostgreSQL database, managed secrets in Azure Key Vault,
automated backups, and declarative GitOps delivery via ArgoCD.

Whether you’re building automations for a startup or an enterprise platform team,
this approach ensures you can deploy n8n with confidence, resilience, and
repeatability — all from a single Git commit.

In other words, with GitOps + Terraform, you now have:

- n8n with HA Postgres
- External secret management
- ArgoCD-powered continuous deployment
- Azure-based, encrypted backups

> Get the full code: [GitHub](https://github.com/aminrj/devops-labs/tree/main/90-n8n)

Happy automating!

![n8n Dashboard (light)](/assets/media/n8n/n8n-dashboard-light.png)
