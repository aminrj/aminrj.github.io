---
title: ArgoCD Deployment Patterns
categories:
  - cloud native
  - CICD
tags:
  - Cloud
  - Argo-cd
  - Kubernetes
  - Cloud-native
image:
  path: /assets/media/argocd/ArgoCD-deployment-patterns.png
description: How ArgoCD deploy applications into Kubernetes cluster and the differences between different deployment patterns.
preview: /media/argocd/ArgoCD-deployment-patterns.png
date: 2023-08-21T07:13:34.000Z
---

Kubernetes is now the de-facto platform for containerized applications. But managing deployments, configuration, and application lifecycle on Kubernetes can get complex quickly.

ArgoCD is a declarative GitOps continuous delivery tool for Kubernetes. Here we look at how it deploys applications and what distinguishes the different deployment patterns.

## Why ArgoCD

ArgoCD gives you a single place to define what your applications should look like, then keeps the cluster in sync with that definition automatically. No manual reconciliation, no configuration drift.

A few things it does particularly well:

- **Declarative GitOps:** Uses Git repositories as the single source of truth for application configuration, making changes versioned, reviewable, and auditable.
- **Automated reconciliation:** Continuously watches for differences between what's defined in Git and what's running. When the cluster drifts, ArgoCD corrects it.
- **Centralized configuration management:** Replaces scattered configuration repos spread across teams and environments with a single consistent place to look.
- **Simplified release management:** Automates deployments, rollbacks, and canary deployments, reducing the manual steps that cause outages.

## What is a deployment pattern

An ArgoCD Application is a Kubernetes Custom Resource that represents a collection of Kubernetes manifests (usually YAML) making up an application. It defines the source type, whether Helm or raw Git, and where those manifests live.

This works fine for simple setups, but two problems come up at scale:

- **Bootstrapping:** How do you deploy an ArgoCD Application CR in a GitOps-friendly way during initial cluster setup? It's a chicken-and-egg problem for day 0.
- **Source type limitation:** Each Application only supports one source type. You can't mix a Helm chart with raw YAML manifests in a single definition (though this may change in future versions).

The common workaround is to create an ArgoCD Application that deploys other ArgoCD Applications. This approach has a few real advantages:

- Deploy dozens of applications simultaneously instead of creating each Application object by hand.
- Group related apps together logically, regardless of whether they're backed by Helm or plain manifests.
- One parent application acts as a watcher, monitoring the health of everything it manages.

This is the "App of Apps" pattern. For more detail, the [App of Apps docs on the Argo Project website](https://argoproj.github.io/argo-cd/operator-manual/cluster-bootstrapping/#app-of-apps-pattern) cover it thoroughly.

## ArgoCD ApplicationSets

ApplicationSets extend the App of Apps idea by making it dynamic. Instead of a static manifest that requires manual updates, an ApplicationSet generates Application objects automatically based on templates or Git repository contents.

The ApplicationSets controller runs as a separate component alongside ArgoCD. It uses "generators" to define what applications to create and where to deploy them. Three generators worth knowing:

- List Generator
- Cluster Generator
- Git Generator

Each handles different scenarios. Which one you reach for depends on how many clusters you manage, your Git repo layout, and how much configuration varies between environments.

## Why use ApplicationSets

ApplicationSets make multi-cluster deployments much more manageable. Instead of maintaining separate configurations per cluster, one ApplicationSet manages deployment across all of them simultaneously.

This matters most for teams running geographically distributed clusters or hybrid cloud setups, where keeping configurations aligned would otherwise mean manual work at every change.

## Hands-on tutorial

I made a video tutorial using both ArgoCD deployment patterns presented in this article.

**TODO : Link to the YouTube video**

## Conclusion

ArgoCD is a solid choice for keeping Kubernetes clusters in sync with what your Git repositories say they should look like. The App of Apps pattern and ApplicationSets are two ways to scale that out: App of Apps is static and explicit, ApplicationSets is dynamic and generator-driven. If you're managing more than a handful of applications, you'll want one of them.

