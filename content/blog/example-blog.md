---
title: "Kubernetes Cost Optimization: 7 Strategies That Saved Us $50K/Month"
excerpt: "Practical techniques to reduce your Kubernetes cloud spend without sacrificing reliability. From right-sizing pods to spot instances, these strategies work."
date: "2025-01-02"
modified: "2025-01-02"
author: "Ahmed"
tags:
  - Kubernetes
  - Cost Optimization
  - Cloud
  - FinOps
  - AWS
  - DevOps
featured: true
# SEO enhancements (optional - override defaults)
# image: "/static/blog/k8s-cost-og.png"
# canonical: "https://ummahrican.com/blog/kubernetes-cost-optimization-strategies"
faqs:
  - question: "How much can Kubernetes cost optimization save?"
    answer: "Most organizations can reduce Kubernetes cloud costs by 40-70% through right-sizing, autoscaling, and spot instances. Our clients typically see $10,000-50,000/month in savings depending on cluster size."
  - question: "Is it safe to use spot instances in production?"
    answer: "Yes, for stateless, fault-tolerant workloads. Spot instances can be interrupted with 2 minutes notice, so use them for batch jobs, stateless APIs behind load balancers, and development environments."
  - question: "What tools help monitor Kubernetes costs?"
    answer: "The top options are Kubecost (open source, most granular), AWS Cost Explorer with container insights, and CloudHealth for multi-cloud. Kubecost provides per-pod cost attribution."
  - question: "What's the quickest Kubernetes cost win?"
    answer: "Right-sizing resource requests. Most pods request 10x more CPU/memory than they use. Run 'kubectl top pods' to find the biggest offenders—you can often cut requests by 80% with no impact."
---

**Kubernetes costs can be reduced by 40-70%** using seven proven strategies: right-sizing pods, cluster autoscaling, spot instances, namespace quotas, storage tiering, off-peak scheduling, and cost monitoring. After managing clusters at Apple and Capital One with combined spend over $2M/month, here's what actually works.

> **TL;DR**: The biggest wins come from right-sizing (20-30% savings), spot instances (60-90% savings on eligible workloads), and cluster autoscaling (removes idle nodes). A typical 100-node cluster can save $30K-50K/month by implementing all seven strategies.

Cloud costs spiral out of control fast. After helping three healthcare startups migrate to Kubernetes, I've seen bills jump from $5K to $50K/month almost overnight. Here's what actually works to bring them back down.

## 1. Right-Size Your Resource Requests

The biggest waste I see: pods requesting 2 CPU cores but using 0.1. Kubernetes reserves what you request, not what you use.

```yaml
# Before: Wasteful
resources:
  requests:
    cpu: "2"
    memory: "4Gi"
  limits:
    cpu: "4"
    memory: "8Gi"

# After: Right-sized based on actual usage
resources:
  requests:
    cpu: "200m"
    memory: "512Mi"
  limits:
    cpu: "500m"
    memory: "1Gi"
```

**How to find the right values:**

```bash
# Install metrics-server, then check actual usage
kubectl top pods -n your-namespace

# Or use Prometheus queries
# avg(rate(container_cpu_usage_seconds_total[5m])) by (pod)
```

**Pro tip:** Use the Vertical Pod Autoscaler (VPA) in recommendation mode first. It analyzes your workloads and suggests optimal values.

## 2. Implement Cluster Autoscaling

Don't pay for idle nodes. The Cluster Autoscaler removes nodes when pods can be rescheduled elsewhere.

```yaml
# cluster-autoscaler deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cluster-autoscaler
spec:
  template:
    spec:
      containers:
        - name: cluster-autoscaler
          image: k8s.gcr.io/autoscaling/cluster-autoscaler:v1.28.0
          command:
            - ./cluster-autoscaler
            - --cloud-provider=aws
            - --scale-down-delay-after-add=10m
            - --scale-down-unneeded-time=10m
            - --scale-down-utilization-threshold=0.5
```

Set `scale-down-utilization-threshold` to 0.5 (50%). Nodes with less than 50% utilization become candidates for removal.

## 3. Use Spot Instances for Non-Critical Workloads

Spot instances cost 60-90% less than on-demand. Perfect for:

- Batch processing jobs
- Development/staging environments
- Stateless workers that can handle interruption

```yaml
# Node pool with spot instances (EKS)
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig
metadata:
  name: my-cluster
managedNodeGroups:
  - name: spot-workers
    instanceTypes: ["m5.large", "m5a.large", "m4.large"]
    spot: true
    minSize: 0
    maxSize: 10
    labels:
      workload-type: spot-tolerant
```

Then use node affinity to schedule appropriate workloads:

```yaml
affinity:
  nodeAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        preference:
          matchExpressions:
            - key: workload-type
              operator: In
              values:
                - spot-tolerant
```

## 4. Set Up Namespace Resource Quotas

Prevent any single team from consuming the entire cluster:

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: team-quota
  namespace: team-frontend
spec:
  hard:
    requests.cpu: "20"
    requests.memory: "40Gi"
    limits.cpu: "40"
    limits.memory: "80Gi"
    pods: "50"
```

Combine with `LimitRange` to set defaults:

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: default-limits
spec:
  limits:
    - default:
        cpu: "500m"
        memory: "512Mi"
      defaultRequest:
        cpu: "100m"
        memory: "128Mi"
      type: Container
```

## 5. Optimize Persistent Volume Usage

Storage costs add up. Use the right storage class:

| Workload         | Storage Class          | Cost |
| ---------------- | ---------------------- | ---- |
| Databases        | io2 (provisioned IOPS) | $$$  |
| Application data | gp3                    | $$   |
| Logs/backups     | sc1 (cold HDD)         | $    |

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: cost-optimized
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  iops: "3000" # gp3 baseline is free
  throughput: "125" # 125 MB/s baseline is free
reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer
```

## 6. Schedule Non-Urgent Workloads Off-Peak

Cloud providers often have lower spot prices during off-peak hours. Use CronJobs strategically:

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: nightly-reports
spec:
  schedule: "0 3 * * *" # 3 AM when spot prices are lowest
  jobTemplate:
    spec:
      template:
        spec:
          nodeSelector:
            workload-type: spot-tolerant
          containers:
            - name: report-generator
              image: myapp/reports:latest
```

## 7. Monitor and Alert on Cost Anomalies

You can't optimize what you don't measure. Set up Kubecost or OpenCost:

```bash
# Install Kubecost
helm install kubecost cost-analyzer \
  --repo https://kubecost.github.io/cost-analyzer/ \
  --namespace kubecost \
  --create-namespace
```

Create alerts for cost spikes:

```yaml
# Prometheus alert rule
groups:
  - name: cost-alerts
    rules:
      - alert: HighNamespaceCost
        expr: |
          sum(
            container_memory_working_set_bytes{namespace!="kube-system"}
          ) by (namespace) > 10e9
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: "Namespace {{ $labels.namespace }} using excessive resources"
```

## Results: What This Looks Like in Practice

For a recent healthcare SaaS client, we implemented all seven strategies:

| Strategy             | Monthly Savings          |
| -------------------- | ------------------------ |
| Right-sizing         | $12,000                  |
| Cluster autoscaling  | $8,000                   |
| Spot instances       | $18,000                  |
| Resource quotas      | $3,000                   |
| Storage optimization | $5,000                   |
| Off-peak scheduling  | $2,000                   |
| Cost monitoring      | $2,000 (prevented waste) |
| **Total**            | **$50,000/month**        |

The key is starting with visibility. Install Kubecost today, understand where your money goes, then prioritize optimizations by ROI.

## Next Steps

1. Run `kubectl top pods` across all namespaces
2. Identify your top 10 resource-consuming workloads
3. Install Kubecost for detailed cost attribution
4. Start with right-sizing—it's the quickest win

## Frequently Asked Questions

### How much can Kubernetes cost optimization save?

Most organizations can reduce Kubernetes cloud costs by **40-70%** through right-sizing, autoscaling, and spot instances. The exact savings depend on your current inefficiency level—clusters with default resource requests typically have the most room for improvement. Our clients typically see $10,000-50,000/month in savings.

### Is it safe to use spot instances in production?

Yes, for stateless, fault-tolerant workloads. Spot instances can be interrupted with 2 minutes notice (AWS provides an interruption warning via instance metadata). Safe workloads include:

- Batch processing jobs
- Stateless API servers behind load balancers
- Worker queues that can resume processing
- Development and staging environments

Avoid spot for: databases, stateful services, and single-instance deployments.

### What tools help monitor Kubernetes costs?

The top options ranked by capability:

| Tool                  | Best For                             | Cost                |
| --------------------- | ------------------------------------ | ------------------- |
| **Kubecost**          | Per-pod attribution, recommendations | Free tier available |
| **AWS Cost Explorer** | AWS-native, container insights       | Included with AWS   |
| **CloudHealth**       | Multi-cloud enterprises              | Enterprise pricing  |
| **OpenCost**          | Open-source Kubecost alternative     | Free                |

Kubecost provides the most granular cost attribution and is my recommendation for most teams.

### What's the quickest Kubernetes cost win?

**Right-sizing resource requests**. Most pods request 10x more CPU/memory than they actually use because developers copy-paste defaults or over-provision "just in case."

Quick win process:

1. Run `kubectl top pods -A` to see actual usage
2. Compare against `kubectl describe pod` resource requests
3. Reduce requests to 1.5x actual usage (leaves headroom)
4. Monitor for a week, adjust if needed

This alone typically saves 20-30% with zero performance impact.

### How long does it take to implement these optimizations?

| Strategy             | Implementation Time | Savings Impact        |
| -------------------- | ------------------- | --------------------- |
| Right-sizing         | 1-2 days            | 20-30%                |
| Cluster autoscaling  | 2-4 hours           | 10-20%                |
| Spot instances       | 1 week              | 30-50% on eligible    |
| Resource quotas      | 1 day               | Prevents future waste |
| Storage optimization | 1-2 days            | 5-15%                 |
| Off-peak scheduling  | 2-4 hours           | 5-10%                 |
| Cost monitoring      | 1 day               | Ongoing visibility    |

Start with right-sizing and autoscaling for quick wins, then tackle spot instances for maximum impact.

---

<!-- *Last updated: January 2025. Have questions about implementing these strategies?  -->
