---
title: "Monitoring Kafka on Kubernetes with Grafana: Step-by-Step"
categories:
  - cloud native
  - event-driven
tags:
  - Kafka
  - Kubernetes
  - Cloud-native
  - Event-driven
  - Grafana
image:
  path: /assets/media/kafka-k8s/banner2.png
description: Deploy a Kafka cluster within Kubernetes using Strimzi Kafka Operator and enable monitoring of usefull Kafka metrics with Prometheus and Grafana.
date: 2024-07-16T07:19:50.000Z
preview: /media/kafka-k8s/banner2.png
---

With Kubernetes, Kafka clusters can be managed declaratively, reducing the
operational overhead of setting up Kafka components and keeping them up-to-date.
Kubernetes Operators like Strimzi automate complex tasks such as broker
configuration, rolling upgrades, and scaling.

This tutorial walks through how to:

- Deploy a Kafka cluster within Kubernetes using Strimzi Kafka Operator
- Enable monitoring of usefull Kafka metrics with Prometheus and Grafana

## Deploy Kafka on Kubernetes (using Minikube)

### A new Minikube cluster

```shell
$ minikube start -p kafka-cluster
😄  [kafka-cluster] minikube v1.33.1 on Darwin 14.5 (arm64)
✨  Using the docker driver based on existing profile
👍  Starting "kafka-cluster" primary control-plane node in "kafka-cluster" cluster
🚜  Pulling base image v0.0.44 ...
🔄  Restarting existing docker container for "kafka-cluster" ...
🐳  Preparing Kubernetes v1.30.0 on Docker 26.1.1 ...
🔎  Verifying Kubernetes components...
    ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
🌟  Enabled addons: default-storageclass, storage-provisioner
🏄  Done! kubectl is now configured to use "kafka-cluster" cluster and "default" namespace by default
```

### Infrastructure As Code with Terraform

To ease our deployment, we use Terraform as our Infrastructure As Code tool.

> :memo: **Note: on IaC**
> If you’re not familiar with Terraform, don’t be scared, it is just an automation tool that uses code to declare infrastructures. [Install](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) Terraform on you machine and run the two terraform commands bellow in the same folder where you put the \*.tf files. that’s it.

This Terraform code declares the necessary providers, and creates the namespaces before installing the “strimiz-cluster-operator” helm-chart:

```terraform
# Initialize terraform providers
provider "kubernetes" {
  config_path = "~/.kube/config"
}
provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"
  }
}

# Create a namespace for observability
resource "kubernetes_namespace" "kafka-namespace" {
  metadata {
    name = "kafka"
  }
}

# Create a namespace for observability
resource "kubernetes_namespace" "observability-namespace" {
  metadata {
    name = "observability"
  }
}

# Helm chart for Strimzi Kafka
resource "helm_release" "strimzi-cluster-operator" {
  name = "strimzi-cluster-operator"
  repository = "https://strimzi.io/charts/"
  chart = "strimzi-kafka-operator"
  version = "0.42.0"
  namespace = kubernetes_namespace.kafka-namespace.metadata[0].name
  depends_on = [kubernetes_namespace.kafka-namespace]
}
```

{: file="strimzi-kakfa.tf"}

- Apply terraform script to create the namespace and install Strimzi Kafka Operator

```shell
terraform init
...
terraform apply --autor-approve
```

- Apply kubernetes yamls to create kafka resources:

```shell
  kubectl apply -f kafka
```

```shell
   $ kubectl -n kafka get po
   NAME                                        READY   STATUS    RESTARTS   AGE
   strimzi-cluster-operator-6948497896-swlvp   1/1     Running   0          77s
```

## Kafka Cluster with Strimzi

Now that our Strimzi-Kafka-Operator is up and running in our newly created Kubernetes cluster, we create the Kafka cluster by applying the following yaml file with the command :

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: my-cluster
spec:
  kafka:
    version: 3.7.1
    replicas: 3
    listeners:
      - name: plain
        port: 9092
        type: internal
        tls: false
      - name: tls
        port: 9093
        type: internal
        tls: true
    config:
      offsets.topic.replication.factor: 3
      transaction.state.log.replication.factor: 3
      transaction.state.log.min.isr: 2
      default.replication.factor: 3
      min.insync.replicas: 2
      inter.broker.protocol.version: "3.7"
    storage:
      type: jbod
      volumes:
        - id: 0
          type: persistent-claim
          size: 100Gi
          deleteClaim: false
  zookeeper:
    replicas: 3
    storage:
      type: persistent-claim
      size: 100Gi
      deleteClaim: false
  entityOperator:
    topicOperator: {}
    userOperator: {}
```

{: file="kafka-persistent.yaml"}

```shell
kubectl apply -n kafka -f kafka-persistent.yaml
```

That’s all that we need to deploy a fully operational Kafka cluster on Kubernetes.

In the kafka namespace, we see that our cluster is up and running and that we have 3 replicas of our cluster as well as 3 replicas of the zookeeper:

```shell
➜  $ kubectl -n kafka get po
NAME                                         READY   STATUS    RESTARTS   AGE
my-cluster-entity-operator-5d7c9f484-94zdt   2/2     Running   0          22s
my-cluster-kafka-0                           1/1     Running   0          45s
my-cluster-kafka-1                           1/1     Running   0          45s
my-cluster-kafka-2                           1/1     Running   0          45s
my-cluster-zookeeper-0                       1/1     Running   0          112s
my-cluster-zookeeper-1                       1/1     Running   0          112s
my-cluster-zookeeper-2                       1/1     Running   0          112s
strimzi-cluster-operator-6948497896-swlvp    1/1     Running   0          4m9s
```

To create Kafka entities (producers, consumers, topics), we use the Kubernetes CRD installed by the Strimzi Operator to do so.

For instance, we create a Kafka topic named `my-topic` by applying the following yaml code:

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: my-topic
  labels:
    strimzi.io/cluster: my-cluster
spec:
  partitions: 1
  replicas: 1
  config:
    retention.ms: 7200000
    segment.bytes: 1073741824
```

{: file="kafka-topic.yaml"}

```shell
kubectl -n kafka apply -f kafka/kafka-topic.yaml kafkatopic.kafka.strimzi.io/my-topic created
```

To produce some events to our topic, we run the following command:

```shell
echo "Hello KafkaOnKubernetes" | kubectl -n kafka exec -i my-cluster-kafka-0 -c kafka -- \
    bin/kafka-console-producer.sh --broker-list localhost:9092 --topic my-topic
```

To test consuming this event, we run:

```shell
➜  kubectl -n kafka exec -i my-cluster-kafka-0 -c kafka -- bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic my-topic --from-beginning
Hello KafkaOnKubernetes
```

At this point, our Kafka cluster is up and running and we can already send and receive events between different microservices running within Kubernetes.

## Monitoring our Kafka Cluster with Grafana

> **Collecting metrics is critical for understanding the health and performance of our Kafka cluster.**
> {: .prompt-warning }

This is important to identify issues before they become critical and make informed decisions about resource allocation and capacity planning.

For this, we will use Prometheus and Grafana to monitor Strimzi.

> Prometheus consumes metrics from the running pods in your cluster when configured with Prometheus rules.
> Grafana visualizes these metrics on dashboards, providing better interface for
> monitoring.
> {: .prompt-info }

### Setting-up Prometheus

To deploy the Prometheus Operator to our Kafka cluster, we apply the YAML bundle resources file from the Prometheus CoreOS repository:

```shell
  curl -s https://raw.githubusercontent.com/coreos/prometheus-operator/master/bundle.yaml > prometheus-operator-deployment.yaml
```

Then we update the namespace with our `observability` namespace:

```shell
sed -i '' -e '/[[:space:]]*namespace: [a-zA-Z0-9-]*$/s/namespace:[[:space:]]*[a-zA-Z0-9-]*$/namespace: observability/' prometheus-operator-deployment.yaml
```

> **For Linux, use this command instead:**

```shell
sed -E -i '/[[:space:]]*namespace: [a-zA-Z0-9-]*$/s/namespace:[[:space:]]*[a-zA-Z0-9-]*$/namespace: observability/' prometheus-operator-deployment.yaml
```

{: .prompt-info}

Then, deploy the Prometheus Operator:

```shell
kubectl -n observability create -f prometheus-operator-deployment.yaml
customresourcedefinition.apiextensions.k8s.io/alertmanagerconfigs.monitoring.coreos.com created
customresourcedefinition.apiextensions.k8s.io/alertmanagers.monitoring.coreos.com created
customresourcedefinition.apiextensions.k8s.io/podmonitors.monitoring.coreos.com created
customresourcedefinition.apiextensions.k8s.io/probes.monitoring.coreos.com created
customresourcedefinition.apiextensions.k8s.io/prometheusagents.monitoring.coreos.com created
customresourcedefinition.apiextensions.k8s.io/prometheuses.monitoring.coreos.com created
customresourcedefinition.apiextensions.k8s.io/prometheusrules.monitoring.coreos.com created
customresourcedefinition.apiextensions.k8s.io/scrapeconfigs.monitoring.coreos.com created
customresourcedefinition.apiextensions.k8s.io/servicemonitors.monitoring.coreos.com created
customresourcedefinition.apiextensions.k8s.io/thanosrulers.monitoring.coreos.com created
clusterrolebinding.rbac.authorization.k8s.io/prometheus-operator created
clusterrole.rbac.authorization.k8s.io/prometheus-operator created
deployment.apps/prometheus-operator created
serviceaccount/prometheus-operator created
service/prometheus-operator created
```

![Pods in the observability namespace](assets/media/kafka-k8s/observability-pods.png)

Now that we have the operator up and running, we need to create the Prometheus server and configure it to watch for Strimzi CRDs in the `kafka` namespace.

Note here that the name of the namespace must match otherwise Prometheus Operator won't scrap any resources we deploy.

### Create the PodMonitor objects for Kafka resources

In order to tell Kafka CRDs to expose Prometheus metrics, we must create the PodMonitor objects for the metrics we want to monitor:

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: cluster-operator-metrics
  labels:
    app: strimzi
spec:
  selector:
    matchLabels:
      strimzi.io/kind: cluster-operator
  namespaceSelector:
    matchNames:
      - kafka
  podMetricsEndpoints:
    - path: /metrics
      port: http
---
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: entity-operator-metrics
  labels:
    app: strimzi
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: entity-operator
  namespaceSelector:
    matchNames:
      - kafka
  podMetricsEndpoints:
    - path: /metrics
      port: healthcheck
---
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: kafka-resources-metrics
  labels:
    app: strimzi
spec:
  selector:
    matchExpressions:
      - key: "strimzi.io/kind"
        operator: In
        values:
          ["Kafka", "KafkaConnect", "KafkaMirrorMaker", "KafkaMirrorMaker2"]
  namespaceSelector:
    matchNames:
      - kafka
  podMetricsEndpoints:
    - path: /metrics
      port: tcp-prometheus
      relabelings:
        - separator: ;
          regex: __meta_kubernetes_pod_label_(strimzi_io_.+)
          replacement: $1
          action: labelmap
        - sourceLabels: [__meta_kubernetes_namespace]
          separator: ;
          regex: (.*)
          targetLabel: namespace
          replacement: $1
          action: replace
        - sourceLabels: [__meta_kubernetes_pod_name]
          separator: ;
          regex: (.*)
          targetLabel: kubernetes_pod_name
          replacement: $1
          action: replace
        - sourceLabels: [__meta_kubernetes_pod_node_name]
          separator: ;
          regex: (.*)
          targetLabel: node_name
          replacement: $1
          action: replace
        - sourceLabels: [__meta_kubernetes_pod_host_ip]
          separator: ;
          regex: (.*)
          targetLabel: node_ip
          replacement: $1
          action: replace
```

{: file="strimzi-pod-monitor.yaml"}

Then we create the Prometheus object and configure it to look for all pods with
the labels `app: strimzi`

```shell
➜  kubectl -n observability apply -f strimzi-pod-monitor.yaml
podmonitor.monitoring.coreos.com/cluster-operator-metrics created
podmonitor.monitoring.coreos.com/entity-operator-metrics created
podmonitor.monitoring.coreos.com/bridge-metrics created
podmonitor.monitoring.coreos.com/kafka-resources-metrics created
```

Note that for this to work, we also need the corresponding ServiceAccount, and RBAC objects as follow:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: prometheus-server
  labels:
    app: strimzi
rules:
  - apiGroups: [""]
    resources:
      - nodes
      - nodes/proxy
      - services
      - endpoints
      - pods
    verbs: ["get", "list", "watch"]
  - apiGroups:
      - extensions
    resources:
      - ingresses
    verbs: ["get", "list", "watch"]
  - nonResourceURLs: ["/metrics"]
    verbs: ["get"]

---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: prometheus-server
  labels:
    app: strimzi

---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: prometheus-server
  labels:
    app: strimzi
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: prometheus-server
subjects:
  - kind: ServiceAccount
    name: prometheus-server
    namespace: observability

---
apiVersion: monitoring.coreos.com/v1
kind: Prometheus
metadata:
  name: prometheus
  labels:
    app: strimzi
spec:
  replicas: 1
  serviceAccountName: prometheus-server
  podMonitorSelector:
    matchLabels:
      app: strimzi
  serviceMonitorSelector: {}
  resources:
    requests:
      memory: 400Mi
  enableAdminAPI: false
```

{: file="prometheus.yaml"}

Then:

```shell
➜  kubectl -n observability create -f observability/prometheus-install/prometheus.yaml
clusterrole.rbac.authorization.k8s.io/prometheus-server created
serviceaccount/prometheus-server created
clusterrolebinding.rbac.authorization.k8s.io/prometheus-server created
prometheus.monitoring.coreos.com/prometheus created
```

### Configuring our Kafka cluster to expose metrics

To enable and expose metrics in Strimzi for Prometheus, we use metrics configuration properties using the `metricsConfig` configuration property or our Kafka cluster.

```yaml
metricsConfig:
  type: jmxPrometheusExporter
  valueFrom:
    configMapKeyRef:
      name: kafka-metrics
      key: kafka-metrics-config.yml
```

Once configured, we apply the new config which will restart our cluster with the updated configuration:

For the configured kafka yaml file, you can find an example in the [Strimi
examples folder](https://github.com/strimzi/strimzi-kafka-operator/tree/main/examples/kafka) “kafka-metrics.yaml”.
Otherwise, you can always refer to the git
repository of this project referenced below.

```shell
kubectl apply -f kafka-metrics.yaml -n kafka
```

> :memo: **After running this command, Kafka Zookeeper pods start restarting one by one followed by the Kafka brokers pods until all the pods are running the updated configuration. Hence the rolling upgrade of our Kafka cluster with zero-down-time powered by Kubernetes. (check in the figure below the age value of the my-cluster-kafka-2 compared to the other two, it will be terminated then restarted last).**

![Pods in the kafka namespace](assets/media/kafka-k8s/kafka-ns-pods.png)

For more details on how monitor Strimzi Kafka using Prometheus and Grafana, check the [Strimzi documentation](https://strimzi.io/docs/operators/latest/deploying#proc-metrics-kafka-deploy-options-str).

### Deploy and Configure Grafana

At this point, our Kafka cluster is up and running and exposes metrics for Prometheus to collect.

Now we need to install Grafana using the `grafana.yaml` file then configure
the our Prometheus as data source.

```shell
kubectl -n observability apply -f grafana-install/grafana.yaml
```

Once deployed, we can access the UI using port-forward, or directly using our Minikube:

```shell
$ minikube -p kafka service grafana -n observability
😿  service observability/grafana has no node port
❗  Services [observability/grafana] have type "ClusterIP" not meant to be exposed, however for local development minikube allows you to access this !
🏃  Starting tunnel for service grafana.
|---------------|---------|-------------|------------------------|
|   NAMESPACE   |  NAME   | TARGET PORT |          URL           |
|---------------|---------|-------------|------------------------|
| observability | grafana |             | http://127.0.0.1:61909 |
|---------------|---------|-------------|------------------------|
🎉  Opening service observability/grafana in default browser...
❗  Because you are using a Docker driver on darwin, the terminal needs to be open to run it.
```

This will open the browser to the login page of Grafana.
The default login/password are : admin/admin.

We head to the `Configuration > Data Sources` tab and add Prometheus as a data source.
In the URL field we put the address of our prometheus service :
`http://prometheus-operated:9090`.

After `Save & Test` we should have a green banner indicating that our Prometheus source is up and running.

Now is time to add a dashboard in order to visualize our Kafka metrics.
In the Dashboard tab, we click on `Import` and point to our `strimzi-kafka.json` file.
Once imported, the dashboard should look something similar to the following figure:

![Grafana Dashboard for Strimzi Kafka](assets/media/kafka-k8s/strimzi-monitoring-grafana-dashboard.png)
_Strmizi Kafka Grafana Dashboard_

## Generating some Kafka events

At this time, since there is no traffic going on in our Kafka cluster, some panels migh show `No Data`. To resove this, we will generate some events using Kafka performance tests.

First, we create our first topic thanks to our Kafka Operator which is watching for any Kafka CRDs.

```shell
kubectl apply -f kafka/kafka-topic.yaml
```

This will create our first topic `my-topic` so we can generate some events.

Head to the terminal and past the following command:

```shell
kubectl -n kafka exec -i my-cluster-kafka-0 -c kafka -- \
    bin/kafka-producer-perf-test.sh --topic my-topic --num-records 1000000 --record-size 100 --throughput 100 --producer-props bootstrap.servers=my-cluster-kafka-bootstrap:9092 --print-metrics
501 records sent, 100.2 records/sec (0.01 MB/sec), 8.3 ms avg latency, 301.0 ms max latency.
501 records sent, 100.1 records/sec (0.01 MB/sec), 1.4 ms avg latency, 8.0 ms max latency.
500 records sent, 99.9 records/sec (0.01 MB/sec), 1.8 ms avg latency, 35.0 ms max latency.
501 records sent, 100.0 records/sec (0.01 MB/sec), 1.8 ms avg latency, 39.0 ms max latency.
500 records sent, 100.0 records/sec (0.01 MB/sec), 1.6 ms avg latency, 8.0 ms max latency.
...
```

Then, we run the consumer with:

```shell
kubectl -n kafka exec -i my-cluster-kafka-0 -c kafka -- \
    bin/kafka-consumer-perf-test.sh --bootstrap-server my-cluster-kafka-bootstrap:9092 --topic my-topic --from-latest --messages 100000000 --print-metrics --show-detailed-stats
```

This will generate some traffic that we can observe on our Grafana dashboards.

That’s it. 🎉🥳

We have created a fully functional Kafka cluster of 3 brokers on a newly created Kubernetes cluster and started monitoring thanks to Prometheus and Grafana.

Here is my Github repository containing all the codes for this step-by-step guide.

[Github repo of this project](https://github.com/aminrj/devops-labs/tree/main/70)

<!-- ## Configure Kubernetes audit logs for Minikube

To enable audit logs on a Minikube:

### 1. Configure Kube-apiserver

Using the official [kubernetes documentation](https://kubernetes.io/docs/tasks/debug/debug-cluster/audit/) as reference, we login into our minikube VM and configure the `kube-apiserver` as follow:

```shell
$ minikube -p kafka-cluster ssh
# we create a backup copy of the kube-apiserver manifest file in case we mess things up 😄
docker@minikube:~$ sudo cp /etc/kubernetes/manifests/kube-apiserver.yaml .
# edit the file to add audit logs configurations
docker@minikube:~$ sudo vi /etc/kubernetes/manifests/kube-apiserver.yaml
```

We need to instruct the `kube-apiserver` to start using an `audit-policy` that
will define what logs we want to capture, then where to which file we want to send them.
This is done by adding these two lines bellow the kube-apiserver command:

```shell
  - command:
    - kube-apiserver
    # add the following two lines
    - --audit-policy-file=/etc/kubernetes/audit-policy.yaml
    - --audit-log-path=/var/log/kubernetes/audit/audit.log
    # end
    - --advertise-address=192.168.49.2
    - --allow-privileged=true
    - --authorization-mode=Node,RBAC
```

With both files, we need need to configure the `volumes` and `volumeMount` into the
`kube-apiserver` container. Scroll down into the same file and add these lines:

```shell
...
volumeMounts:
  - mountPath: /etc/kubernetes/audit-policy.yaml
    name: audit
    readOnly: true
  - mountPath: /var/log/kubernetes/audit/
    name: audit-log
    readOnly: false
```

And then:

```shell
...
volumes:
- name: audit
  hostPath:
    path: /etc/kubernetes/audit-policy.yaml
    type: File

- name: audit-log
  hostPath:
    path: /var/log/kubernetes/audit/
    type: DirectoryOrCreate
```

Be carefull with the number of spaces you add before each line, this can prevent
the `kube-apiserver` from starting.

However, at this point, even if you are super carefull, it wont start... 😈

### 2. Create the audit-policy

This is because, we need to create the audit-policy file at the location we gave to the `kube-apiserver`.
To keep things simple, we will use the audit-policy provided by the kubernetes documentation.

```shell
docker@minikube:~$ cd /etc/kubernetes/
docker@minikube:~$ sudo curl -sLO https://raw.githubusercontent.com/kubernetes/website/main/content/en/examples/audit/audit-policy.yaml
```

Now, everything should be Ok for the `kuber-apiserver` pod to come back to a running state.

```shell
docker@minikube:~$ exit
$ kubectl get po -n kube-system
NAME                               READY   STATUS    RESTARTS   AGE
coredns-5dd5756b68-mbtm8           1/1     Running   0          1h
etcd-minikube                      1/1     Running   0          1h
kube-apiserver-minikube            1/1     Running   0          13s
kube-controller-manager-minikube   1/1     Running   0          1h
kube-proxy-jcn6v                   1/1     Running   0          1h
kube-scheduler-minikube            1/1     Running   0          1h
storage-provisioner                1/1     Running   0          1h
```

### 3. Check audit logs are generated

Now, we can log back to the Minikube VM to check that our audit logs are
correctly generated in the provided audit.log file.

```shell
$ minikube ssh
docker@minikube:~$ sudo cat /var/log/kubernetes/audit/audit.log
...
{"kind":"Event","apiVersion":"audit.k8s.io/v1","level":"Metadata", ...
"authorization.k8s.io/reason":"RBAC:
allowed by ClusterRoleBinding \"system:public-info-viewer\" of ClusterRole
{"kind":"Event","apiVersion":"audit.k8s.io/v1","level":"Request", ...
...
```

Yes, we have our logs. 🥳

## Configure Kafka to produce event-streams from the audit logs

 -->
