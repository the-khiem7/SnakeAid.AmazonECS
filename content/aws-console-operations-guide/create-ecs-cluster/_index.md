---
title: "Step 1 - Create ECS Cluster"
date: 2026-04-22
weight: 1
chapter: false
---

## Console Screen

![Create ECS Cluster in AWS Console](/images/aws-console-operations-guide/ECS/1.%20create-cluster/create-ecs-cluster.png)

> Tip: place the screenshot at `static/images/aws-console-operations-guide/ECS/1. create-cluster/create-ecs-cluster.png` so this image renders correctly.

---

## What Is an ECS Cluster?

In Amazon Elastic Container Service:

> **Cluster = a logical space to run containers**

* It is not a server
* It does not cost money directly
* It is mainly where services are grouped

Simple mental model:

```text
Cluster = folder that holds container services
```

### Cluster Scope Diagram

![ECS cluster scope diagram](/images/diagrams/create-ecs-cluster/cluster-scope.png)

---

## Goal of This Step

Create a cluster to:

* run the backup system (API + AI)
* avoid server management
* make ALB attachment easier later

### Cluster In Context

![ECS cluster in context diagram](/images/diagrams/create-ecs-cluster/cluster-in-context.png)

---

## 1. Cluster Name

### Why naming matters

Later, you may have:

* dev cluster
* staging cluster
* backup cluster

So use a clear, meaningful name from the start.

### Recommended value

```text
snakeaid-backup-cluster
```

---

## 2. Infrastructure (most important part)

### What are you choosing?

You are choosing **how AWS runs containers for you**.

| Option  | Meaning                                   |
| ------- | ----------------------------------------- |
| Fargate | AWS runs containers, no server management |
| EC2     | you manage servers                        |
| Hybrid  | mix of both                               |

### Your goal

* no server management
* only backup instances needed
* no deep performance tuning yet

### Choose

```text
Fargate only
```

### Easy explanation

```text
Fargate = "Docker while AWS handles the machines"
```

You only define:

* image
* RAM / CPU

---

## 3. Monitoring

### What is Container Insights?

Monitoring for:

* CPU, RAM
* network
* log analytics

### For your case

* this is a backup system
* no complex observability required now
* prioritize simplicity and cost

### Choose

```text
Turned off
```

### When to enable later

* performance debugging
* larger production scale

For now: not needed.

---

## 4. ECS Exec and Logging

### What is this?

* ECS Exec = remote shell into container
* Logging = command logs

### For your case

* no deep debugging needed now
* no remote exec need yet

### Action

```text
Keep default
```

---

## 5. Encryption

### What is this?

* storage encryption with KMS
* often needed for stricter compliance workloads

### For your case

* this layer is not handling highly sensitive data
* current focus is infrastructure setup

### Action

```text
Skip
```

---

## 6. Tags

### Why tags exist

Resource grouping by:

* project
* team
* cost tracking

### For your case

* detailed tracking is not required yet

### Action

```text
Skip
```

---

## Final Configuration

```text
Cluster name: snakeaid-backup-cluster

Infrastructure:
  Fargate only

Monitoring:
  Turned off

Other sections:
  default / skip
```

Click **Create**.

---

## What You Get After This Step

You will have:

```text
1 empty ECS Cluster
```

No workloads are running yet.

---

## Next Step (more important)

```text
1. Create Task Definition (container config)
2. Create ALB
3. Create ECS Service
```

---

## Key Insight

Many beginners think:

> "Cluster is the most important thing"

Not exactly. In practice:

```text
Cluster = just a container holder
Real core = Task + Service + ALB
```

---

## TL;DR

```text
Create cluster = set name + choose Fargate + turn off monitoring -> Create
```
