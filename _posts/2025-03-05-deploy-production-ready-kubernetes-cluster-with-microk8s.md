---
title: "Building a Production-Ready Kubernetes Cluster with Infrastructure as Code and GitOps"
categories:
  - Kubernetes
  - DevOps
  - GitOps
tags:
  - MicroK8s
  - Terraform
  - ArgoCD
  - GitOps
  - Infrastructure as Code
  - Kubernetes
image:
  path: /assets/media/devops/production_ready_kubernetes_iac_gitops.png
---

Let's build a production ready cluster using Infrastructure as Code and GitOps.

Tools that will be deployed on a freshly install microk8s cluster:

- LoadBalancer: with Metallb
- Ingress Controller: with nginx ingress controller
- ExternalDNS: for automatic DNS records provisioning and sync
- Certificates: with cert-manager
- Monitoring: with Prometheus, Grafana and Loki
- CICD: with GitLab and ArgoCD
- Storage ???
- Security:...

Let's get to it!

## 1. Setting-up the stage with Terraform

Configure Terraform to target our cluster.

```bash
export KUBECONFIG=~/.kube/microk8s-config
export KUBE_MASTER=10.0.30.10
export KUBE_CONFIG_PATH=~/.kube/microk8s-config #Needed by ArgoCD
```

Setup the Terraform project structure.
This setup starts by deploying ArgoCD first in its own namespace.

```bash
❯ tree
.
├── README.md
├── environments
│   └── dev
│       ├── main.tf
│       ├── terraform.tfstate
│       ├── terraform.tfstate.backup
│       ├── terraform.tfvars
│       └── variables.tf
├── modules
│   ├── argocd
│   │   ├── main.tf
│   │   ├── values.yaml
│   │   └── variables.tf
│   └── kubernetes
│       ├── main.tf
│       ├── outputs.tf
│       └── variables.tf
├── providers.tf
└── terraform.tfstate
```

### Deploy ArgoCD

ArgoCD deployment is straightforward.
Just add the terraform files, specify the desired values to configure it.
Then apply to have ArgoCD deployed.

There is a common issue when deploying ArgoCD via Terraform and Helm, and
it usually happens due to:

- Helm release drift (Terraform keeps trying to update it)
- CRDs not being deleted properly
- A timeout issue with the Helm release
- A failed installation that Terraform keeps retrying

To solve these issues, the found solution is to set `wait=false` in the Helm
release configuration.

> [!NOTE]
> That one took me sometime to figure it out.

### LoadBalancing with Metallb

When deploying Kubernetes on a local cluster (not on Provided Cloud such as
AWS), we need something that would provision Load Balancers for our services.
This something is achieved by Metallb.
It handles LoadBalancing services in our bar-metal Kubernetes.

Specifically, services that needs external access (e.g., Web apps, Grafana,
ArgoCD...).
Without Metallb, those won't be assigned an external IP.

Remember that Kubernetes has three ways to expose applications:

1. ClusterIP (default): Only accessible inside the cluster.
2. NodePort: Accessible via <NodeIP>:<Port> but not for production.
3. LoadBalancer: Require a cloud provider OR Metallb for bare-metal clusters.

### Reverse proxy with Nginx-Ingress-Controller

And since public IPs are expansive, we don't want to have to need one for every
service, so a reverse proxy with proper routing to correct service is also
needed.
This is where an ingress-controller becomes handy.

In Kubernetes, Ingress is the standard way to expose applications via a single
extrernal IP instead of creating multiple LoadBalancer services.
Without an Ingress Controller, every app would need a separate LoadBalancer
service, consuming more IPs.

Thanks to Nginx Ingress, we can expose multiple applications via one
LoadBalancer IP.
We can route requests based on domain names (e.g., app1.example.com,
app2.example.com).
We can enable TLS/HTTPS easily via Cert-Manager.

### Handling certificates with Cert-Manager

Thanks to Cert-Manager, we can automate the process of issuing, renewing and
managing TLS/SSL certificates in Kubernetes.
Without it, managing HTTPS for our applications would require manually obtaining
and updating certificates, which is inefficient and error-prone.

In other words, here is what Cert-Manager really do:

- Automatic TLS Certificates: issues certificates from Let's Encrypt or custom
  CAs.
- Auto-Renewal: Prevents downtime by renewing certificates before they expire
- Integrate with Ingress: Enables HTTPS for Nginx, Traefik, Istio, etc.
- Works with MetalLb & LoadBalancer: Secures services without needing a cloud
  proficer.
- Multi-Environment Support: Managers different certs for Dev, Staging and Prod.

### Managing DNS records with ExternalDNS

Once we have set our Ingress Controller to route traffic to our services,
provided it with a public IP from our MetalLb and configured TLS certificates
with Cert-Manager, we still need to update DNS records every time an
application's external IP changes.
We also need to configure domain-to-service mapping (A and CNAME records).
This could lead to downtime when MetalLb or LoadBalancer IPs change.

Thankfully, there is ExternalDNS that would automate this process to ensure that
domain names always point to the correct external IPs.
Without requiring manual updates in our DNS provider (e.g., Cloudflare,
Route53).

In a nutshell, ExternalDNS watches Kubernetes services and Ingress resources.
Once it detect that one has an external IP, it automatically updates our DNS
provider to create (or update) A and CNAME records.
It also sync DNS Records when IPs change.

### Automating deployments with ArgoCD

This is where we configure our setup to automatically pick our applications and
deploy them on the cluster.
Setting-up everything together in the tools described above.
The goal is to handle the deployment part for us and let us focus on building
cool apps without spending time on the plumbing necessary for them to work.
This is what part 2 of this article is all about.
[[bootstraping-gitops-with-terraform-argocd]]
