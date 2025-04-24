---
title: "How You Should Manage Secrets in Kubernetes"
# title: "Managing Secrets in Kubernetes with External Secrets Operator and Azure Key Vault"
categories:
  - DevOps
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
  path: /assets/media/external-secrets/external-secrets-k8s-2.png
  # path: /assets/media/devops/gitops_bootstrap_terraform_argocd.png
---

When managing applications in Kubernetes, one of the most important challenges
is handling secrets securely, cleanly, and in a GitOps-compatible way.

This post walks through how I use [External Secrets Operator](https://external-secrets.io) (ESO) with [Azure Key Vault](https://azure.microsoft.com/en-us/products/key-vault) to manage Kubernetes secrets at scale, in a production-ready setup.

We use Terraform to bootstrap infrastructure and ArgoCD to manage Kubernetes manifests.

If you want secrets to stay out of Git, follow along.

## Why Use External Secrets Operator?

A few clear goals shaped this setup:

- **No secrets in Git**
- **Centralized secret management** using Azure Key Vault (or other provider)
- **GitOps-compliant** secrets synchronization via ArgoCD
- **Multi-environment scalability** with minimal duplication

External Secrets Operator (ESO) solves the missing piece by syncing secrets stored
outside Kubernetes (e.g. Azure Key Vault) into your cluster, securely and automatically.

## High-Level Architecture

Here’s what this setup does:

1. Secrets are stored securely in Azure Key Vault
2. Kubernetes has a one-time bootstrapped secret that lets ESO authenticate with Azure
3. ESO is deployed via Helm and listens for `ExternalSecret` CRDs
4. Secrets are declared in Git and synced via ArgoCD into the cluster

```markdown
Azure Key Vault ← ESO ← ExternalSecret ← ArgoCD
↓
Creates Kubernetes Secret
```

## Getting Started from Scratch

### Prerequisites

- An Azure subscription
- [Terraform](https://developer.hashicorp.com/terraform/downloads)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Rancher Desktop](https://docs.rancherdesktop.io/) (with Kubernetes enabled)
- [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
- [Helm](https://helm.sh/)
- A Git repository for your Kubernetes manifests (for ArgoCD)

### Project Folder Structure

```
my-secrets-setup/
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── manifests/
│   ├── clustersecretstore.yaml
│   └── externalsecret.yaml
```

## Step 1: Configure Rancher Desktop Kubernetes Cluster

1. Start Rancher Desktop and make sure Kubernetes is enabled.
2. Run:

```bash
kubectl get nodes
NAME                   STATUS   ROLES                  AGE   VERSION
lima-rancher-desktop   Ready    control-plane,master   19h   v1.32.3+k3s1

```

This should show your local cluster node.

## Step 2: Provision Azure Infrastructure with Terraform

Create a resource group, Azure Key Vault, and app credentials:

**terraform/main.tf**

```terraform
provider "azurerm" {
  features {}
}

provider "azuread" {}

data "azurerm_client_config" "current" {}

resource "azurerm_resource_group" "this" {
  name     = var.resource_group_name
  location = var.location
}

resource "azuread_application" "eso" {
  display_name = var.app_name
}

resource "azuread_service_principal" "eso" {
  client_id = azuread_application.eso.client_id
}

resource "azuread_application_password" "eso" {
  application_id = azuread_application.eso.id
}

resource "azurerm_key_vault" "this" {
  name                      = var.key_vault_name
  location                  = var.location
  resource_group_name       = azurerm_resource_group.this.name
  tenant_id                 = data.azurerm_client_config.current.tenant_id
  sku_name                  = "standard"
  enable_rbac_authorization = true
}

resource "azurerm_role_assignment" "eso_kv_reader" {
  principal_id         = azuread_service_principal.eso.object_id
  role_definition_name = "Key Vault Secrets User"
  scope                = azurerm_key_vault.this.id
}

resource "azurerm_role_assignment" "secrets_officer" {
  principal_id         = data.azurerm_client_config.current.object_id
  role_definition_name = "Key Vault Secrets Officer"
  scope                = azurerm_key_vault.this.id
}
```

**terraform/variables.tf**

```terraform
variable "resource_group_name" { default = "secrets-rg" }
variable "location"            { default = "westeurope" }
variable "key_vault_name"      { default = "mysecretskv" }
variable "app_name"            { default = "eso-app" }
```

**terraform/outputs.tf**

```terraform
output "client_id" {
  value = azuread_application.eso.client_id
}

output "client_secret" {
  value     = azuread_application_password.eso.value
  sensitive = true
}

output "vault_uri" {
  value = azurerm_key_vault.this.vault_uri
}
```

Run Terraform:

```bash
cd terraform
terraform init
terraform apply -auto-approve
```

After that you should see:

```bash
...
Apply complete! Resources: 5 added, 0 changed, 0 destroyed.

Outputs:

client_id = "4a1d5c4f-903c-4166-b83f-6a262386c"
client_secret = <sensitive>
vault_uri = "https://mysecretskv.vault.azure.net/"
```

---

## Step 3: Install External Secrets Operator with Helm

```bash
> helm repo add external-secrets https://charts.external-secrets.io
> helm repo update

> helm install external-secrets external-secrets/external-secrets \
  --namespace external-secrets \
  --create-namespace \
  --set installCRDs=true

NAME: external-secrets
LAST DEPLOYED: Thu Apr 24 11:09:03 2025
NAMESPACE: external-secrets
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
external-secrets has been deployed successfully in namespace external-secrets!

In order to begin using ExternalSecrets, you will need to set up a SecretStore
or ClusterSecretStore resource (for example, by creating a 'vault' SecretStore).

More information on the different types of SecretStores and how to configure them
can be found in our Github: https://github.com/external-secrets/external-secrets

```

---

## Step 4: Bootstrap Azure Credentials into Kubernetes

Use the Terraform output values:

```bash
❯ kubectl create secret generic azure-secret-creds \
  -n external-secrets \
  --from-literal=client-id="$(terraform output -raw client_id)" \
  --from-literal=client-secret="$(terraform output -raw client_secret)"

secret/azure-secret-creds created
```

---

## Step 5: Define the ClusterSecretStore

**manifests/clustersecretstore.yaml**

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ClusterSecretStore
metadata:
  name: azure-kv-store-dev
spec:
  provider:
    azurekv:
      tenantId: <your-tenant-id>
      vaultUrl: https://mysecretskv.vault.azure.net/
      authSecretRef:
        clientId:
          name: azure-secret-creds
          key: client-id
          namespace: external-secrets
        clientSecret:
          name: azure-secret-creds
          key: client-secret
          namespace: external-secrets
```

Replace `<your-tenant-id>` with your Azure tenant ID (available via `az account show`).

Apply it:

```bash
❯ kubectl apply -f manifests/clustersecretstore.yaml

clustersecretstore.external-secrets.io/azure-kv-store-dev created
```

---

## Step 6: Define an ExternalSecret

**manifests/externalsecret.yaml**

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: demo-secret
  namespace: default
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: azure-kv-store-dev
    kind: ClusterSecretStore
  target:
    name: demo-secret
    creationPolicy: Owner
  data:
    - secretKey: DEMO_KEY
      remoteRef:
        key: demo-secret-key
```

Add the `demo-secret-key` to your Azure Key Vault manually or using:

```bash
❯ az keyvault secret set --vault-name mysecretskv --name demo-secret-key --value "hello-k8s"

{
  "attributes": {
    "created": "2025-04-24T09:20:15+00:00",
    "enabled": true,
    "expires": null,
    "notBefore": null,
    "recoverableDays": 90,
    "recoveryLevel": "Recoverable+Purgeable",
    "updated": "2025-04-24T09:20:15+00:00"
  },
  "contentType": null,
  "id": "https://mysecretskv.vault.azure.net/secrets/demo-secret-key/b757ac4505554ced841b2ac864598ec6",
  "kid": null,
  "managed": null,
  "name": "demo-secret-key",
  "tags": {
    "file-encoding": "utf-8"
  },
  "value": "hello-k8s"
}
```

Then apply:

```bash
❯ kubectl apply -f manifests/externalsecret.yaml
externalsecret.external-secrets.io/demo-secret created

❯ kubectl get externalsecrets.external-secrets.io
NAME          STORETYPE            STORE                REFRESH INTERVAL   STATUS         READY
demo-secret   ClusterSecretStore   azure-kv-store-dev   1h                 SecretSynced   True


```

Verify it synced:

```bash
❯ kubectl get secrets
NAME          TYPE     DATA   AGE
demo-secret   Opaque   1      16s
```

---

## Bonus: A more "GitOps-y" way of doing it

### Install External Secrets Operator with Helm

We’ll use a simple Terraform module to install ESO:

```terraform
resource "helm_release" "external_secrets" {
  name             = "external-secrets"
  namespace        = "external-secrets"
  repository       = "https://charts.external-secrets.io"
  chart            = "external-secrets"
  version          = "0.9.13"
  create_namespace = true

  set {
    name  = "installCRDs"
    value = true
  }
}
```

> You only need to do this once per cluster.

## Provision Azure Key Vault + App Credentials (Terraform)

Then use Terraform to provision an Azure Key Vault, an App Registration, and a
client secret that ESO will use to authenticate as before.

### Declare your ExternalSecrets (per app)

With `ClusterSecretStore` set up, we can declare secrets per application.

Here’s an example that syncs database credentials:

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: myapp-db-credentials
  namespace: myapp-dev
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: azure-kv-store-dev
    kind: ClusterSecretStore
  target:
    name: myapp-db-credentials
    creationPolicy: Owner
  data:
    - secretKey: POSTGRES_USER
      remoteRef:
        key: myapp-db-username
    - secretKey: POSTGRES_PASSWORD
      remoteRef:
        key: myapp-db-password
    - secretKey: POSTGRES_DB
      remoteRef:
        key: myapp-db-name
    - secretKey: POSTGRES_HOST
      remoteRef:
        key: myapp-db-host
```

This syncs secrets from Azure into a Kubernetes `Secret` that your app can consume.

### Use Secrets in Your Application Deployment

You can inject secrets into your app using `envFrom` in your Deployment:

```yaml
envFrom:
  - secretRef:
      name: myapp-db-credentials
```

Your application can then read environment variables like:

```bash
$ echo $POSTGRES_USER
myapp
```

If your app needs a full connection string (e.g., `DATABASE_URL`), you can
create that as a single secret in Key Vault and map it using `remoteRef`.

### Terraform Module to Generate and Store Secrets

For production environments, I prefer generating credentials via Terraform to
avoid manual work.
Here's how:

```terraform
module "myapp_secrets" {
  source       = "../../../modules/azure-secrets"
  key_vault_id = module.azure_keyvault.key_vault_id
  app_name     = "myapp"

  static_secrets = {
    "db-username" = "myapp"
    "db-host"     = "myapp-db.internal"
  }

  random_secrets = [
    "db-password"
  ]
}
```

This creates secrets like:

- `myapp-db-username` → `"myapp"`
- `myapp-db-password` → secure random
- `myapp-db-host` → `"myapp-db.internal"`

All stored in Azure Key Vault.

## Benefits of This Approach

- **No secrets in Git** — everything is pulled securely from Azure
- **Repeatable** — new environments or apps just need Terraform + ArgoCD sync
- **Scalable** — one Key Vault, many apps, zero manual duplication
- **GitOps-friendly** — secrets are managed declaratively
- **Modular** — separate secret generation, storage, and usage

## Final Thoughts

External Secrets Operator is one of the most effective tools I’ve added to my
Kubernetes setup.
It bridges the gap between secure secret storage (Azure Key Vault) and
GitOps-driven Kubernetes workloads.

This setup is now my default for any production cluster.

If you're building GitOps-first, multi-environment Kubernetes systems, ESO should
be part of your toolkit.
