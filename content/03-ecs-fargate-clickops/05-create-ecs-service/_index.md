---
title: "Step 5 - Create ECS Service (Bind ALB + Target Group)"
date: 2026-04-22
weight: 5
chapter: false
---

## Goal of This Step

This is the core ECS orchestration step:

![ECS service orchestration diagram](_diagrams/service-orchestration.png)

---

## Console Entry

Open:

```text
Amazon Elastic Container Service > Clusters > snakeaid-backup-cluster > Services > Create
```

![Services screen showing the Create button used to start ECS service setup](_diagrams/ecs-service-entry-create-button.webp)

---

## What are you doing on this screen?

```text
ECS Service = orchestration layer
```

It is responsible for:

* running tasks from task definition
* keeping desired replica count
* registering tasks into target group
* integrating with ALB health checks and routing

The main shift at this step is that earlier resources stop being isolated pieces and start behaving like one running service path.

### Service Orchestration

![ECS service orchestration diagram](_diagrams/service-orchestration.png)

### ALB Binding

![ECS service ALB binding diagram](_diagrams/alb-binding.png)

### Rolling Update

![ECS service rolling update diagram](_diagrams/rolling-update.png)

### Task Network Placement

![ECS service network placement diagram](_diagrams/network-placement.png)

Together, these four diagrams explain what ECS Service adds on top of Task Definition: orchestration, ALB attachment, rollout behavior, and task placement.

---

## 1. Service details

Typical values:

```text
Task definition family: snakeaid-api
Revision: Latest
Service name: snakeaid-api-service
```

Meaning:

* Task definition = container configuration
* Service = runtime controller that keeps tasks alive

![Service details section showing task definition revision, service name, cluster, and Fargate strategy](_diagrams/ecs-service-details.webp)

---

## 2. Environment

```text
Cluster: snakeaid-backup-cluster
```

Cluster is the runtime environment where services and tasks run.

The service itself is the controller layer that sits between the task definition and actual running tasks.

---

## 3. Compute configuration

```text
Capacity provider strategy: FARGATE
```

This means serverless containers with no EC2 management.

---

## 4. Deployment configuration

```text
Scheduling: Replica
Desired tasks: 1
```

This keeps one task running at all times.

Deployment strategy:

```text
Rolling update
Min: 100%
Max: 200%
```

On new revision, ECS starts new tasks, waits for health checks, then replaces old tasks.

![ECS service rolling update diagram](_diagrams/rolling-update.png)

![Deployment configuration showing replica scheduling, desired tasks, and rolling update thresholds](_diagrams/ecs-service-deployment-configuration.webp)

---

## 5. Networking (very important)

Current values:

```text
VPC: default
Subnets: 2 AZ
Security group: default
Public IP: Enabled
```

Practical meaning:

* Fargate task receives public IP (easy for testing)
* for production, prefer private subnets for tasks and keep ALB public

![ECS service network placement diagram](_diagrams/network-placement.png)

![Networking section showing default VPC, two subnets, default security group, and public IP enabled](_diagrams/ecs-service-networking.webp)

---

## 6. Load balancing (main part)

### Load balancer type

```text
Application Load Balancer
```

### Existing ALB

```text
snakeaid-alb
```

### Listener

```text
HTTP : 80
```

### Listener rule

```text
/ -> forward -> snakeaid-api-tg
```

### Target group

```text
Use existing target group: snakeaid-api-tg
```

### Container mapping

```text
Container: snakeaid-api
Port: 8080
```

### Health check

```text
Path: /health
Protocol: HTTP
```

If health checks fail, ECS replaces unhealthy tasks automatically.

![ECS service ALB binding diagram](_diagrams/alb-binding.png)

![Load balancing section showing existing ALB, target group, listener rule, and container port 8080](_diagrams/ecs-service-load-balancing.webp)

---

## 7. Service auto scaling

Can stay disabled at this stage.

```text
Always = 1 instance
```

---

## 8. Volume

For stateless API, you can skip volume configuration.

---

## 9. Tags

No runtime impact. You can fill later.

---

## Architecture after this step

![Diagram showing the runtime stack after the ECS service is created](_diagrams/service-runtime-stack.png)

---

## Pre-create checklist

1. Task definition exposes port `8080`
2. `/health` endpoint returns `200`
3. Security group allows required traffic
4. After deploy, validate with `http://<alb-dns>`

---

## TL;DR

Use the existing ALB, the existing target group, and the correct container port so ECS can supply healthy running targets into the traffic path.

---

## Next Step

When service is `Healthy`, run end-to-end ALB DNS test and continue with `snakeai` service configuration.
