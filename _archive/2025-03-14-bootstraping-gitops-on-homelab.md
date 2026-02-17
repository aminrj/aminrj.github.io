---
title: "Bootstrapping GitOps with Terraform and ArgoCD"
categories:
  - DevOps
  - GitOps
  - Kubernetes
tags:
  - Terraform
  - ArgoCD
  - GitOps
  - Infrastructure as Code
  - Kubernetes
image:
  path: /assets/media/devops/gitops_bootstrap_terraform_argocd.png
---

GitOps has been around for quite some time now.
I have been using it at work but it was all setup by other teams.
Once I have my homelab up and running and deployed my Kubernetes cluster, I
want to get my own GitOps setup.
And it was far from a smooth ride.

In this article I explain different steps required to get a working setup.
Most importantly, I will explain the logic behind each step.
Let's go then, shall we?

## The tech stack

I decided to go with Terraform and ArgoCD.
These are the two tools that I am already familiar with (or I thought I was).
Terraform will deploy the required tools on the newly created cluster.
ArgoCD will take over and start deploying applications on that cluster.

A key element in this setup is the Infrastructure as Code part.
We don't want to be writing imperative commands on the cluster.
Once deployed, everything should be done declaratively.
So that everything is stored in a git repository and version controlled.

So, no `kubectl apply` commands allowed in this setup.
We want to be able to rebuild everything from scratch if something bad happen.
Or we want to build another cluster similar to the one we had.

## Bootstraping the necessary tools on the cluster

Once Kubernetes cluster is up and running, there are a few things to have:

1. Ingress controller: We don't want to have to need an external IP address for
   each of our services (or a dedicated Load Balancer). Ingress controller will
   allow us to provide proper routing and reverse proxy to our services (through
   Ingress).
2. Certification manager: For that we want to get valid certificates for our
   services, we need something to provision such certificates automatically.
   That thing is called `cert-manager`.
3. External DNS: If we want our services to have nice domain names, no IP
   addresses, we need to setup DNS records correctly for them. Thankfully, with
   External DNS, this is done automatically for us (once setup correctly of
   course).
4. Load Balancer: For those who are using a Cloud Service Provider such as AWS,
   GCP or Azure or others... This step is not needed since they provide one. For
   the weirdos who are running their Kubernetes cluster on bare metal (or almost),
   we need a load balancer that would provide public IPs to our Ingress
   controller services. This is the role of Metallb.
5. Last but not least, we will need ArgoCD. The last thing that we need is
   someone messing with our cluster. Deploying or altering existing services
   without traceability or repeatability. Ideally everything needs to be done
   through code. And that code need to be stored and versioned in a git
   repository. That's the job of ArgoCD.

## Terraform modules for the tools

For simplicity, I have one git repository that will hole both our infrastructure
and our gitops setup.
Ideally, they should be separated.
However, I will have some sort of separation through Terraform modules.

All the tools listed above are deployed in separated folders to be applied by
Terraform.
These are called modules in the Terraform language.
Each module will be responsible of deploying one tool.
Our main Terraform file will be lined to the environment we are trying to build.
With this setup, we can choose what tools goes into what environment.
For instance, we might not need DNS records for our dev environment.
Or we want to use fake certificates for our staging cluster.

## ArgoCD

This is where the fun begins.
We want the following from our CICD pipeline:

- No imperative commands on the cluster
- Limited to no need to configure ArgoCD setup with each new application to be
  deployed.
- Ability to reuse manifests between different environments.

So, to fulfill these requirement, we will build the following setup:

1. Apps folder: where all our applications' Kubernetes manifests will live. All
   our deployments, services, ingresses and the rest of Kubernetes resources.
   For each application, we can have several environments (dev, staging,
   prod...) as needed.
2. ArgoCD folder: this is where ArgoCD applications will be created. We want to
   have our ArgoCD application created automatically as we add application
   manifests. (TODO: add more details here)

## Applications source code

This is where the source code of our applications will live.
We don't want to deal with any infrastructure details here.
Only focus on the application itself.
Except that we will define a workflow (or CI pipeline) that will automatically
build docker images and update the GitOps repo with the newly built image
details.
ArgoCD will take it from there and deploy the new version on our cluster.

## Other noteworthy stuff

> [!NOTE]
> After deploying the terraform script, we need to add the github tokens so that
> ArgoCD can read the right gitops repository (if it is private):
> For this we need to run:

```bash
❯ kubectl create secret generic argocd-repo-https \
  --namespace argocd \
  --from-literal=username="aminrj" \
  --from-literal=password="github_pat_................"

secret/argocd-repo-https created

 environments/dev │ main ──────────────────────────────── microk8s ○ │ 21:27:09
❯ kubectl patch secret argocd-repo-https \
  -n argocd \
  -p '{"metadata": {"labels": {"argocd.argoproj.io/secret-type": "repository"}}}'

secret/argocd-repo-https patched
```
