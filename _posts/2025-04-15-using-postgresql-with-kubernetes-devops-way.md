---
title: "How you Should Deploy and Use Postgres in Kubernetes"
categories:
  - PostgresQL
  - GitOps
  - Kubernetes
  - Secrets
tags:
  - Terraform
  - ArgoCD
  - GitOps
  - Infrastructure as Code
  - Kubernetes
image:
  path: /assets/media/cloud-native/linkding-cnpg-deployment.png
  # path: /assets/media/devops/gitops_bootstrap_terraform_argocd.png
---

Bootstrapping a Per‑Application Highly‑Available PostgreSQL Cluster
with CloudNativePG, Terraform & GitOps:

_A step‑by‑step tutorial using the **Linkding** bookmark manager as an
illustration example._

> **TL;DR** – In ~30 minutes you will spin‑up an application **and** its
> own highly‑available Postgres cluster using nothing but Git commits
> and Terraform.
> We will rely on **CloudNativePG (CNPG)** for the database layer,
> **ArgoCD** for GitOps continuous delivery, **External‑Secrets**
> to bridge secrets from Azure Key Vault, and a few battle‑tested **DevSecOps** patterns.

## Table of Contents

1. [Why per‑app HA Postgres?](#why)
2. [Reference architecture](#architecture)
3. [Prerequisites](#prereq)
4. [Repository & GitOps layout](#layout)
5. [Terraform – bootstrap the operators](#terraform)
6. [Kustomize manifests](#kustomize)
7. [Argo CD ApplicationSets](#applicationsets)
8. [Bootstrapping the database](#bootstrap)
9. [Deploying Linkding](#deploy‑app)
10. [Back‑ups & disaster‑recovery](#backup)
11. [Monitoring & observability](#monitor)
12. [Testing HA & fail‑over](#ha‑test)
13. [Going further](#future)

<a id="why"></a>

## 1 – Why per‑app HA Postgres?

First, let's briefly present some arguments on why such setup is sound in the
first place:

- **Blast radius** — a rogue migration or `DELETE FROM` only harms its own cluster.
- **Tuned resources** — memory/CPU, WAL settings, and retention match the workload.
- **Security boundaries** — each namespace can enforce distinct RBAC & network policies.
- **Lifecycle independence** — upgrade, snapshot, or drop a database without downtime for others.

Yes, the trade‑off is more clusters to manage – However CNPG makes that almost trivial.

---

<a id="architecture"></a>

## 2 – Reference architecture

```
┌──────────────────────┐              ┌────────────────────────────┐
│  Developers          │  git         │  Git repository            │
│  push YAML/TF        ├─────────────▶│  apps/   databases/        │
└──────────────────────┘              │  argocd/                   │
          ▲ gitops sync               └──────────▲─────────────────┘
          │                                       │
┌─────────┴────────┐                          ┌───┴─────────────┐
│     Argo CD      │  applies manifests     . │  Kubernetes     │
│ (ApplicationSet) ├──────────────────────── ▶│  cluster        │
└─────────┬────────┘                          └────┬────────────┘
          │ Helm / CRDs                            │
┌─────────▼────────┐                         ┌────▼──────────────────────────┐
│ Terraform        │  installs operators     │  CNPG operator (HA PG)        │
│ (cluster‑admin)  ├────────────────────────▶│  External‑Secrets operator    │
└──────────────────┘                         └───────────────────────────────┘
```

Operators, CRDs and namespaces are installed once via Terraform.

Everything application‑specific lives in Git and is reconciled by ArgoCD.

---

<a id="prereq"></a>

## 3 – Prerequisites

| Tool                      | Version tested | Purpose                           |
| ------------------------- | -------------- | --------------------------------- |
| Kubernetes                | ≥ 1.27         | Where everything runs             |
| Terraform                 | ≥ 1.5          | Cluster bootstrap & Day‑0 ops     |
| ArgoCD                    | ≥ 2.8          | GitOps engine                     |
| CloudNativePG             | ≥ 1.21         | PostgreSQL operator               |
| External‑Secrets Operator | ≥ 0.9          | Sync secrets from Azure Key Vault |
| Azure Key Vault           | any            | Secret backend                    |

You also need _kubectl_, _kustomize_ and a Git repo.

---

<a id="layout"></a>

## 4 – Repository & GitOps layout

Our repo holds **three** top‑level domains:

```
apps/                 # application manifests
  └─ linkding/
       ├─ base/
       │   ├─ deployment.yaml
       │   ├─ service.yaml
       │   └─ kustomization.yaml
       └─ overlays/
           └─ dev/
               ├─ namespace.yaml
               ├─ secrets.yaml        # ExternalSecret → Azure KV
               └─ kustomization.yaml

# A symmetrical layout for the database
Databases/
  └─ linkding/
       ├─ base/
       │   ├─ database.yaml          # CNPG Cluster
       │   └─ kustomization.yaml
       └─ overlays/
           └─ dev/
               ├─ scheduled-backup.yaml
               ├─ secrets.yaml        # S3 / Azure Blob creds
               └─ kustomization.yaml

# Argo CD owns the sync‑loops
argocd/
  ├─ applicationset.yaml          # applications/
  ├─ db‑applicationset.yaml       # databases/
  └─ external-secret-application.yaml
```

The **base** directory contains vendor‑agnostic manifests; **overlays** patch environment‑specific details ([Kustomize](https://kustomize.io)).

---

<a id="terraform"></a>

## 5 – Terraform – bootstrap the operators

Day‑0 steps are performed **once** per cluster:

```terraform
# terraform/main.tf
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    helm = {
      source  = "hashicorp/helm"
      version = ">= 2.9.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.22.0"
    }
  }
}

variable "kubeconfig" {
  description = "Path to your kubeconfig file"
  type        = string
  default     = "~/.kube/config"
}

provider "helm" {
  kubernetes {
    config_path = var.kubeconfig
  }
}

# CloudNativePG operator
resource "helm_release" "cnpg" {
  name             = "cloudnative-pg"
  repository       = "https://cloudnative-pg.github.io/charts"
  chart            = "cloudnative-pg"
  version          = "0.20.1"  # matches CNPG 1.22.x
  namespace        = "cnpg-system"
  create_namespace = true

  set {
    name  = "monitoring.enabled"
    value = true
  }
}

# External‑Secrets operator
resource "helm_release" "external_secrets" {
  name             = "external-secrets"
  repository       = "https://charts.external-secrets.io"
  chart            = "external-secrets"
  version          = "0.9.16"
  namespace        = "external-secrets"
  create_namespace = true

  set {
    name  = "installCRDs"
    value = true
  }
}

# (Optional) Argo CD
resource "helm_release" "argo_cd" {
  name             = "argocd"
  repository       = "https://argoproj.github.io/argo-helm"
  chart            = "argo-cd"
  version          = "5.51.6"
  namespace        = "argocd"
  create_namespace = true

  # Reduce footprint for a lab / homelab
  set {
    name  = "configs.params.server.insecure"
    value = true
  }
}
```

Running `terraform apply` would get the initial infrastructure up and running in
the Kubernetes:

## ![Bootstraping the infrastructure with Terraform](/assets/media/cloud-native/initial-bootstrapping-with-tf.png)

<a id="kustomize"></a>

## 6 – Kustomize manifests

### `apps/linkding/base/deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: linkding
spec:
  replicas: 1
  selector:
    matchLabels:
      app: linkding
  template:
    metadata:
      labels:
        app: linkding
    spec:
      containers:
        - name: linkding
          image: sissbruecker/linkding:latest
          ports:
            - containerPort: 9090
          env:
            - name: LD_DB_ENGINE
              value: django.db.backends.postgresql
            - name: LD_DB_HOST
              value: pg-dev-rw.cnpg-dev.svc.cluster.local
            - name: LD_DB_PORT
              value: "5432"
            - name: LD_DB_NAME
              value: linkding
            - name: LD_DB_USER
              valueFrom:
                secretKeyRef:
                  name: linkding-db-secret
                  key: username
            - name: LD_DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: linkding-db-secret
                  key: password
          volumeMounts:
            - name: linkding-data
              mountPath: /etc/linkding/data
      volumes:
        - name: linkding-data
          emptyDir: {}
```

### `databases/linkding/base/database.yaml`

```yaml
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: linkding-db-dev-cnpg-v1
spec:
  description: Postgres cluster for the linkding application
  imageName: quay.io/enterprisedb/postgresql:16.1
  instances: 3 # High‑availability

  storage:
    size: 5Gi

  monitoring:
    enablePodMonitor: true

  inheritedMetadata:
    labels:
      app: linkding-database
      policy-type: database

  bootstrap:
    initdb:
      database: linkding
      owner: linkding
      secret:
        name: linkding-db-creds

  resources:
    requests:
      memory: 600Mi

  backup:
    barmanObjectStore:
      destinationPath: https://myblob.blob.core.windows.net/linkding-db
      azureCredentials:
        storageAccount:
          name: linkding-db-storage
          key: container-name
        storageSasToken:
          name: linkding-db-storage
          key: blob-sas
      wal:
        compression: gzip
      data:
        compression: gzip
    retentionPolicy: 14d
```

> With CNPG a **read–write service** (`*-rw`) and a **read‑only service** (`*-ro`) are generated for you – we point `LD_DB_HOST` to the former.

---

<a id="applicationsets"></a>

## 7 – ArgoCD ApplicationSets

A single ApplicationSet per domain keeps things DRY:

```yaml
# argocd/applicationset.yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: apps
spec:
  generators:
    - git:
        repoURL: https://github.com/aminrj/devops-labs.git
        revision: main
        directories:
          - path: 80-cnpg/apps/*/overlays/*
  template:
    metadata:
      name: "{{path[2]}}-{{path[4]}}" # example: commafeed-dev, listmonk-qa...
    spec:
      project: default
      source:
        repoURL: https://github.com/aminrj/devops-labs.git
        targetRevision: main
        path: "80-cnpg/apps/{{path[2]}}/overlays/{{path[4]}}" #Example: apps/nextjs-app/dev
      destination:
        server: https://kubernetes.default.svc
        namespace: "{{path[4]}}" # dev, qa, prod as namespace (simpler - for now)
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

Repeat the same for `databases/*`.

![ArgoCD Applications](/assets/media/cloud-native/argocd-apps.png)

<a id="bootstrap"></a>

## 8 – Bootstrapping the database

1. **Create secrets** in Azure Key Vault (`linkding-db-username`, `password`, blob SAS…).
2. Commit the `external-secrets.yaml` manifest in both **app** and **database** overlays – EKS will automatically generate Kubernetes `Secret`s.
3. Merge to _main_ ➜ ArgoCD applies everything ➜ CNPG operator spins‑up the cluster.
4. CNPG initialises `linkding` database & role using the provided secret.

Creating secrets in Azure Key Vault can be automated using Terraform:

```terraform
# Linkding DB credentials
resource "random_password" "db_pwd" {
  length  = 32
  special = true
}

resource "azurerm_key_vault_secret" "db_user" {
  name         = "linkding-db-username"
  value        = var.db_username
  key_vault_id = azurerm_key_vault.this.id
}

resource "azurerm_key_vault_secret" "db_password" {
  name         = "linkding-db-password"
  value        = random_password.db_pwd.result
  key_vault_id = azurerm_key_vault.this.id
}

```

You can watch the progress:

```bash
kubectl -n cnpg-dev get clusters
kubectl -n cnpg-dev get pods -l cnpg.io/cluster=linkding-db-dev-cnpg-v1
```

---

<a id="deploy-app"></a>

## 9 – Deploying Linkding

With the database ready, ArgoCD synchronises the `apps/linkding` Application:

```bash
kubectl -n linkding-dev get svc,pods
```

Port‑forward and log‑in at `http://localhost:9090`.

---

<a id="backup"></a>

## 10 – Back‑ups & disaster‑recovery

- **Point‑in‑time recovery** – WAL archives are pushed to Azure Blob on every segment.
- **Scheduled full backups** – `ScheduledBackup` CRD kicks in daily at 03:00.
- **Retention** – `14d` keeps your bucket tidy.

Restore from any point:

```yaml
bootstrap:
  recovery:
    source: clusterBackup
    database: linkding
    owner: linkding
    secret:
      name: linkding-db-creds
```

![ArgoCD Linkding Application Deployment](/assets/media/cloud-native/argocd-linkding-app.png)

---

<a id="monitor"></a>

## 11 – Monitoring & observability

CNPG exports a **Prometheus PodMonitor** out‑of‑the‑box. Wire it to your Prometheus stack and import the official Grafana dashboard (ID 18630). External‑Secrets also ships metrics at `/metrics`.

![External Secret Deployment App](/assets/media/cloud-native/argocd-external-secrets.png)

---

<a id="ha-test"></a>

## 12 – Testing HA & fail‑over

Kill the primary:

```bash
kubectl -n cnpg-dev delete pod linkding-db-dev-cnpg-v1-0
```

Within seconds a replica is promoted – check with:

```bash
kubectl -n cnpg-dev get clusters linkding-db-dev-cnpg-v1 -o jsonpath='{.status.currentPrimary}'
```

Your application keeps running because its Service always targets the `*-rw` endpoint.

---

<a id="future"></a>

## 13 – Going further

- **Instance = 5** – geo‑replicated clusters.
- **StorageClass** – use SSD vs HDD tiers per workload.
- **OPA Gatekeeper** – enforce labels & annotations across all clusters.
- **Kyverno** – auto‑inject `PodDisruptionBudget` or certificate rotation.
- **Cross‑plane** – provision cloud infra via CRDs entirely inside GitOps.

---

## Conclusion

There you have it, our Linkding application is up and running using its own
PostgresQL Cluster.

> You can get access to the full code example here: [Github repo](https://github.com/aminrj/devops-labs/tree/main/80-cnpg).

With ~250 lines of YAML and minimal Terraform glue we achieved:

- IAM‑less secret management via External‑Secrets;
- dedicated, HA Postgres for every application;
- immutable, auditable deployments powered by Git;
- automated backups and disaster‑recovery.

Happy hacking – and remember: **`kubectl delete pod` is the new `pull‑the‑plug` chaos test!**
