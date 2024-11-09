---
title: ArgoCD Deployment Patterns
categories:
  - cloud native
  - CICD
tags:
  - cloud
  - argo-cd
  - kubernetes
  - cloud-native
image:
  path: /assets/media/argocd/ArgoCD-deployment-patterns.png
description: How ArgoCD deploy applications into Kubernetes cluster and the differences between different deployment patterns.
preview: /media/argocd/ArgoCD-deployment-patterns.png
date: 2023-08-21T07:13:34.000Z
---

Kubernetes has emerged as the de-facto platform for modern containerized applications.

However, managing the deployment, configuration, and lifecycle of applications on Kubernetes can be a complex and error-prone task.

This is where ArgoCD, a declarative GitOps continuous delivery tool for Kubernetes, comes into play.

Here we explore how ArgoCD deploy applications into Kubernetes cluster and explain the differences between different deployment patterns.

## Why ArgoCD

ArgoCD provides a centralized repository for defining the desired state of applications, ensuring that the actual state of the cluster matches the desired state.

This eliminates the need for manual intervention and reduces the risk of human error.
It also offers some benefits that we can list as follow:

1. **Declarative GitOps:** ArgoCD adheres to the GitOps philosophy, using Git repositories as the single source of truth for application configurations. This promotes collaboration and visibility among development teams.
2. **Automated Reconciliation:** ArgoCD continuously monitors the differences between the desired application state defined in Git and the actual state of the cluster. It automatically reconciles these differences, applying any necessary changes to ensure consistency.
3. **Centralized Configuration Management:** ArgoCD provides a centralized platform for managing application configurations, eliminating the need for multiple configuration repositories scattered across different teams or environments.
4. **Improved Release Management:** ArgoCD simplifies the release management process by automating deployments, rollbacks, and canary deployments. This reduces the risk of downtime and disruptions.

## What is a deployment pattern

An ArgoCD Application serves as a representation of the collection of Kubernetes-native manifests (usually YAML) that form the core components of an application. This Custom Resource Definition (CRD) defines the source type, which specifies the deployment tool (Helm or Git) and the location of those manifests. However, this approach presents certain challenges:

1. **Bootstrapping:** Deploying GitOps applications in a "GitOps-friendly" manner can be a hurdle. How does one deploy the ArgoCD Application CR manifest in a GitOps way, particularly during the initial setup phase (day 0)?
2. **Source Type Limitations:** An ArgoCD Application can only have a single source type defined (though it might change in the coming versions). This restriction prevents the combination of Helm charts and YAML manifests within a single application definition.

To address these challenges, users have employed a workaround: creating an ArgoCD Application that deploys other ArgoCD Applications. This approach offers several advantages:

1. **Massive Deployments:** It enables the deployment of multiple applications simultaneously. Instead of deploying numerous ArgoCD Application objects individually, a single application can manage the deployment of all the others.
2. **Logical Application Grouping:** It facilitates the logical grouping of real-world applications comprising YAML manifests and Helm charts within ArgoCD.
3. **Convenient Monitoring:** It provides a centralized "watcher" application that monitors the deployment and health of all the underlying applications.

The "App of Apps" pattern, mentioned in the original text, exemplifies this approach.
It provides a practical solution for managing complex application landscapes and simplifying deployment processes.
For further details, refer to the Argo Project website for comprehensive information on the "App of Apps" pattern. ([App of Apps from the Argo Project website](https://argoproj.github.io/argo-cd/operator-manual/cluster-bootstrapping/#app-of-apps-pattern).)

## ArgoCD ApplicationSets

ArgoCD ApplicationSets, represent a significant advancement of the "App of Apps" deployment pattern.
This enhancement builds upon the existing concept of managing multiple applications within a single application manifest, introducing greater flexibility and addressing a broader spectrum of use cases.
The ApplicationSets controller operates as a separate entity, complementing the functionality of the ArgoCD Application CRD.

Unlike traditional "App of Apps" manifests, which are static and require manual updates, ArgoCDApplicationSets offer dynamic capabilities.
They can automatically generate application manifests based on templates or Git repositories, enabling the management of complex application landscapes with ease.
This approach eliminates the need to manually define and manage individual application manifests.

## Why use ApplicationSets

ArgoCD ApplicationSets also simplify the deployment and management of multi-cluster applications.

They can simultaneously manage the deployment and configuration of applications across multiple Kubernetes clusters, ensuring consistency and reliability.
This feature is particularly beneficial for organizations with geographically dispersed or hybrid cloud environments.

The ApplicationSet [controller](https://argocd-applicationset.readthedocs.io/en/stable/#introduction) 
is made up of “generators”. These “generators” instruct the ApplicationSet how to generate Applications by the provided repo or repos, and it also instructs where to deploy the Application. There are 3 “generators” that I will be exploring are:

- List Generator
- Cluster Generator
- Git Generator

Each “generator” tackles different scenarios and use cases. Every “generator” gives you the same end result: Deployed ArgoCD Applications that are loosely coupled together for easy management. What you use would depend on a lot of factors like the number of clusters managed, git repo layout, and environmental differences.

## Hands on tutorial

I made a video tutorial using both ArgoCD deployment patterns presented in this article.

**TODO : Link to the YouTube video**

## Conclusion

ArgoCD is a powerful tool that simplifies and automates application deployments on Kubernetes. By adopting a declarative GitOps approach, ArgoCD ensures that the actual state of the cluster matches the desired state defined in Git, reducing the risk of downtime, inconsistencies, and human errors. The "app of apps" pattern and the Applicationsets controller offer different ways to define and manage application groups, providing flexibility and control for managing complex application landscapes. As Kubernetes adoption continues to grow, ArgoCD is poised to become an indispensable tool for organizations that want to streamline their application delivery pipelines and achieve continuous delivery excellence.

Overall, ArgoCD ApplicationSets provide a powerful and versatile tool for managing application groups in Kubernetes. They address the limitations of the traditional "App of Apps" pattern and offer a more comprehensive solution for managing complex application landscapes. With their dynamic nature, multi-cluster support, and automated generation capabilities, ArgoCD ApplicationSets are poised to become a go-to choice for organizations seeking to streamline their application delivery processes.