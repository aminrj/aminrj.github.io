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

Let's build a local, production ready, Kubernetes cluster using Infrastructure
as Code and GitOps.

Tools that will be deployed on a freshly installed Microk8s cluster are:

- LoadBalancer: with Metallb
- Ingress Controller: with nginx ingress controller
- External-DNS: for automatic DNS records provisioning and sync
- Certificates: with cert-manager
- Monitoring: with Prometheus, Grafana and later Loki
- CICD: with GitLab and ArgoCD
- Storage: with Cloud-Native PostgresQL

Let's get to it!

## 0. Perquisite: Having a multi-node Microk8s cluster

I won't be starting from zero as this differ largely from one setup to the next.
It depends on what hardware you have and how you plan on deploying your cluster.

There are plenty of documentation on the Microk8s website to help with that.
So, to continue, you will need a fresh Microk8s with default configuration.

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

With this structure, we aim to have several environments (dev, qa, prod) where
we can select and configure each Terraform module we want in a specific
environment.

Later, we can use `Kustomize` to configure apps to be deployed on those
environments.

## 2. LoadBalancing with Metallb

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

Here is my Metallb configuration:

```terraform
resource "helm_release" "metallb" {
  name       = "metallb"
  chart      = "metallb"
  repository = "https://metallb.github.io/metallb"
  version    = "0.14.9"
  namespace  = "metallb-system"

  create_namespace = true
  wait             = false
}

resource "terraform_data" "metallb_configs" {
  depends_on = [helm_release.metallb]
  input      = file("${path.module}/metallb-config.yaml")

  provisioner "local-exec" {
    command     = "echo '${self.input}' | kubectl apply -f -"
    interpreter = ["/bin/bash", "-c"]
  }
  provisioner "local-exec" {
    when        = destroy
    command     = "echo '${self.input}' | kubectl delete -f -"
    interpreter = ["/bin/bash", "-c"]
  }
}
```

And the configuration file needs to define the IP pool to lease IPs from:

```terraform
# metallb-config.yaml
---
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: lb-addresses
  namespace: metallb-system
spec:
  addresses:
    - 10.0.30.200-10.0.30.220
---
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: lb-addresses
  namespace: metallb-system
spec:
  ipAddressPools:
    - lb-addresses
```

Once deployed, the module will install the Metallb controller and the speakers.

- Controller: Watches kubernetes servicies of type `LoadBalancer` to assign IPs
- Speaker: Advertise the assigned IPs to the local network using Layer 2 (ARP)
  or BGP.

```bash
❯ kubectl get all -n metallb-system
NAME                                      READY   STATUS    RESTARTS         AGE
pod/metallb-controller-8474b54bc4-qv4hf   1/1     Running   0                4d7h
pod/metallb-speaker-7cgm5                 4/4     Running   0                4d7h
pod/metallb-speaker-9k78q                 4/4     Running   0                4d7h
pod/metallb-speaker-kc6nw                 4/4     Running   0                4d7h
pod/metallb-speaker-lvtrn                 4/4     Running   0                4d7h

NAME                              TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE
service/metallb-webhook-service   ClusterIP   10.152.183.134   <none>        443/TCP   4d7h

NAME                             DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
daemonset.apps/metallb-speaker   4         4         4       4            4           kubernetes.io/os=linux   4d7h

NAME                                 READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/metallb-controller   1/1     1            1           4d7h

NAME                                            DESIRED   CURRENT   READY   AGE
replicaset.apps/metallb-controller-8474b54bc4   1         1         1       4d7h
```

## 3. Reverse proxy with Nginx Ingress Controller

Since public IPs are expansive, we don't want to have to need one for every
service, so a reverse proxy with proper routing to the correct service is also
needed.

This is where an ingress-controller becomes handy.

In Kubernetes, Ingress is the standard way to expose applications via a single
extrernal IP instead of creating multiple LoadBalancer services.
Without an Ingress Controller, every app would need a separate LoadBalancer
service, consuming more IPs 😢.

Thanks to Nginx Ingress, we can expose multiple applications via one
LoadBalancer IP.

We can route requests based on domain names (e.g., app1.example.com,
app2.example.com).
We can enable TLS/HTTPS easily via Cert-Manager.

```terraform
module "nginx-controller" {
  source  = "terraform-iaac/nginx-controller/helm"
  version = "2.3.0"
  wait    = false

  ip_address= "10.0.30.200"
  metrics_enabled= true
}
```

We fix its public IP so that our local network router/firewall routes traffic
from the Internet to our cluster.

Once we include our module in our environment, it deploys the followings:

```bash
❯ kubectl get all -n kube-system
NAME                                           READY   STATUS    RESTARTS        AGE
...
pod/ingress-nginx-controller-f24s8             1/1     Running   0               4d6h
pod/ingress-nginx-controller-t8ccj             1/1     Running   0               4d6h
pod/ingress-nginx-controller-xc2sf             1/1     Running   8 (5h58m ago)   4d6h

NAME                                                         TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)                        AGE
...
service/ingress-nginx-controller                             LoadBalancer   10.152.183.179   10.0.30.200   80:30417/TCP,443:30541/TCP     4d14h
service/ingress-nginx-controller-admission                   ClusterIP      10.152.183.219   <none>        443/TCP                        4d14h
service/ingress-nginx-controller-metrics                     ClusterIP      10.152.183.120   <none>        10254/TCP                      4d6h

NAME                                      DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
daemonset.apps/ingress-nginx-controller   3         3         3       3            3           kubernetes.io/os=linux   4d14h
...
```

## 4. Handling certificates with Cert-Manager

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
  provider.
- Multi-Environment Support: Managers different certs for Dev, Staging and Prod.

To deploy `cert-manager`, we create the `Terraform` module with:

```terraform
resource "helm_release" "cert_manager" {
  name       = "cert-manager"
  repository = "https://charts.jetstack.io"
  chart      = "cert-manager"
  version    = "v1.17.0"
  namespace  = "cert-manager"
  create_namespace = true

  wait       = false
  set {
      name  = "installCRDs"
      value = "true"
    }
}
```

This will create:

```bash
❯ kubectl get all -n cert-manager
NAME                                           READY   STATUS    RESTARTS   AGE
pod/cert-manager-665948465f-b4mzr              1/1     Running   0          4d14h
pod/cert-manager-cainjector-7c8f7984fb-rf7m5   1/1     Running   0          4d14h
pod/cert-manager-webhook-7594bcdb99-5gns8      1/1     Running   0          4d14h

NAME                              TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)            AGE
service/cert-manager              ClusterIP   10.152.183.155   <none>        9402/TCP           4d14h
service/cert-manager-cainjector   ClusterIP   10.152.183.181   <none>        9402/TCP           4d14h
service/cert-manager-webhook      ClusterIP   10.152.183.49    <none>        443/TCP,9402/TCP   4d14h

NAME                                      READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/cert-manager              1/1     1            1           4d14h
deployment.apps/cert-manager-cainjector   1/1     1            1           4d14h
deployment.apps/cert-manager-webhook      1/1     1            1           4d14h

NAME                                                 DESIRED   CURRENT   READY   AGE
replicaset.apps/cert-manager-665948465f              1         1         1       4d14h
replicaset.apps/cert-manager-cainjector-7c8f7984fb   1         1         1       4d14h
replicaset.apps/cert-manager-webhook-7594bcdb99      1         1         1       4d14h
```

Once we have the certificate manager in place, we need to define
`ClusterIssuers`for staging and production in separate yaml files.
Preferably, managed by Terraform and ArgoCD.

Here is the process:

1. Create two ClusterIssuers:

   - letsencrypt-staging (for dev/staging)
   - letsencrypt-prod (for prod)

2. Store issuer manifests in your GitOps repo.
3. Reference the right issuer in each Certificate resource based on environment.
4. Automate deployment:

   - Use Terraform to template env-specific values.
   - ArgoCD syncs them per environment (via separate ArgoCD Applications).

So, we define our issuers:

Staging issuer for dev/staging environments:

```terraform
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-staging
spec:
  acme:
    server: https://acme-staging-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-staging-key
    solvers:
      - http01:
          ingress:
            class: nginx
```

And Production issuer:

```terraform
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-prod-key
    solvers:
      - http01:
          ingress:
            class: nginx
```

And we reference the right `issuerRef` using ArgoCD apps or Kustomize overlays:

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: my-app-cert
  namespace: my-app-namespace
spec:
  secretName: my-app-tls
  issuerRef:
    name: letsencrypt-staging # or letsencrypt-prod
    kind: ClusterIssuer
  commonName: my-app.example.com
  dnsNames:
    - my-app.example.com
```

## 5. Managing DNS records with ExternalDNS

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

In a nutshell, ExternalDNS watches Kubernetes services and/or Ingress resources.
Once it detect that one has an external IP, it automatically updates our DNS
provider to create (or update) A and CNAME records.
It also sync DNS Records when IPs change.

To deploy `ExternalDNS`, we create the following Terraform module:

```terraform
resource "helm_release" "external-dns" {
  name       = "external-dns"
  chart      = "external-dns"
  repository = "https://kubernetes-sigs.github.io/external-dns"
  version    = "1.15.2"
  namespace  = "external-dns"

  create_namespace = true

  wait       = false
}
```

This will deploy:

```bash
❯ kubectl get all -n external-dns
NAME                                READY   STATUS    RESTARTS   AGE
pod/external-dns-745b66b8d6-ktdkc   1/1     Running   0          4d14h

NAME                   TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
service/external-dns   ClusterIP   10.152.183.96   <none>        7979/TCP   4d14h

NAME                           READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/external-dns   1/1     1            1           4d14h

NAME                                      DESIRED   CURRENT   READY   AGE
replicaset.apps/external-dns-745b66b8d6   1         1         1       4d14h
```

However, we need more than that to configure automatic domain names with our DNS
provider (In my case: Cloudflare) and have it sync with our ingress configuration.
Here is the process:

1. Create a Cloudflare API token

   - With permissions:
     - `Zone:Read`
     - `DNS:Edit`
   - Scope it to your domain(s).

2. Store the token as a Kubernetes secret

   ```bash
   kubectl create secret generic cloudflare-api-token-secret \
     --from-literal=CF_API_TOKEN=<your-token> \
     -n external-dns
   ```

3. Configure `external-dns` with Cloudflare provider

   Update our Terraform Helm release:

   ```terraform
   resource "helm_release" "external-dns" {
     name       = "external-dns"
     chart      = "external-dns"
     repository = "https://kubernetes-sigs.github.io/external-dns"
     version    = "1.15.2"
     namespace  = "external-dns"

     create_namespace = true

     set {
       name  = "provider"
       value = "cloudflare"
     }

     set {
       name  = "cloudflare.apiTokenSecret"
       value = "cloudflare-api-token-secret"
     }

     set {
       name  = "cloudflare.apiTokenSecretKey"
       value = "CF_API_TOKEN"
     }

     set {
       name  = "sources"
       value = "{ingress}"
     }

     set {
       name  = "policy"
       value = "sync"
     }

     set {
       name  = "txtOwnerId"
       value = "my-cluster"
     }

     set {
       name  = "domainFilters[0]"
       value = "yourdomain.com"
     }
   }
   ```

4. Annotate your Ingress

   ```yaml
   metadata:
     annotations:
       external-dns.alpha.kubernetes.io/hostname: app.yourdomain.com
   ```

Once that’s done, ExternalDNS will pick up the ingress hostnames and sync them
to Cloudflare automatically.

## 6. Diagram of the current setup

Here is a little diagram of what we achieved so far.

```code
        Internet
            │
    +----------------+
    |  Cloudflare    |  (DNS & Proxy, points to Public IP)
    +----------------+
            │
    Public IP (x.x.x.x)  (ISP Assigned)
            │
    +--------------------+
    |   pfSense Firewall |  (NAT & Port Forwarding)
    +--------------------+
            │
    +--------------------+
    |  MetalLB          |  (Assigns private IP 10.0.30.211)
    |  LoadBalancer     |
    +--------------------+
            │
    +--------------------------------------------------+
    |           MicroK8s Cluster (DMZ)                 |
    |--------------------------------------------------|
    | +----------------------------------------------+  |
    | | NGINX Ingress Controller                     |  |  (Handles HTTP/S)
    | | (Service: LoadBalancer, External IP: 10.0.30.211) |
    | +----------------------+-----------------------+  |
    |                        │                          |
    | +----------------------+-----------------------+  |
    | | Kubernetes Ingress    |  (whoami.aminrj.com) |  |  (Routes domain traffic)
    | +----------------------+-----------------------+  |
    |                        │                          |
    | +----------------------+-----------------------+  |
    | | Kubernetes Service    |  (ClusterIP or LB)   |  |  (Routes to App)
    | +----------------------+-----------------------+  |
    |                        │                          |
    | +----------------------+-----------------------+  |
    | | Whoami Pod           |  (Application)        |  |  (App runs here)
    | +----------------------+-----------------------+  |
    +--------------------------------------------------+
            │
    +--------------------------------------------------+
    |  External-DNS (Cloudflare Updater)               |
    |  - Monitors Ingress & Service External IPs       |
    |  - Updates Cloudflare A record with Public IP    |
    +--------------------------------------------------+
```

## 7. Deploy ArgoCD

The final step in our infrastructure setup is ArgoCD.
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
> That one took me sometime to figure out 😰.

## 8. Automating deployments with ArgoCD

This is where we configure our setup to automatically pick our applications and
deploy them on the cluster.

Setting-up everything together in the tools described above.

The goal is to handle the deployment part for us and let us focus on building
cool apps without spending time on the plumbing necessary for them to work.

This is what part 2 of this article is all about.
[[bootstraping-gitops-with-terraform-argocd]]
