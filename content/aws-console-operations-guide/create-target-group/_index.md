---
title: "Step 4 - Create Target Group"
date: 2026-04-22
weight: 4
chapter: false
---

## Goal of This Step

Create a Target Group so ALB knows how to route traffic to ECS backends.

```text
Client -> ALB -> Target Group -> ECS Tasks
```

---

## What Is a Target Group?

```text
Target Group = the backend list ALB forwards requests to
```

It defines how ALB calls backends: protocol, port, and health checks.

### Health Check Flow

![Target group health check diagram](_diagrams/health-check.png)

### ECS Auto Registration

![Target group auto registration diagram](_diagrams/auto-registration.png)

### Port Alignment

![Target group port alignment diagram](_diagrams/port-alignment.png)

---

## Screens by UI Phase

### Phase 1: Define target group

![Target group settings showing IP target type, name, protocol, port, VPC, and HTTP1](_diagrams/target-group-settings.webp)

### Phase 2: Register targets

![Register targets screen showing no manually added IP addresses](_diagrams/target-group-register-targets-empty.webp)

### Phase 3: Review

![Review screen showing target group details and health check settings](_diagrams/target-group-review-health-check.webp)

---

## A. Step 1 - Target group details

### 1. Target type

Choose:

```text
IP addresses
```

Why:

* `Instances` for EC2
* `IP addresses` for ECS Fargate/container workloads
* `Lambda` for Lambda functions

For SnakeAid on ECS Fargate, choose `IP addresses`.

### 2. Name

```text
snakeaid-api-tg
```

This is a label for management, not runtime behavior.

### 3. Protocol and Port

```text
HTTP : 8080
```

Critical rule:

```text
Target group port must match container port
```

If container listens on 8080, target group should use 8080.

### 4. VPC

```text
vpc-xxx
```

Target Group VPC must align with ECS service and ALB.

### 5. Protocol version

```text
HTTP1
```

Default is fine for this stage.

---

## B. Health Check

Set:

```text
Protocol: HTTP
Path: /health
```

ALB will call:

```text
http://<task-ip>:8080/health
```

Endpoint should return `200 OK`.

If path is wrong or route does not exist, targets will be marked `UNHEALTHY`.

![Review summary showing the configured health check path and success code](_diagrams/target-group-review-health-check.webp)

---

## C. Step 2 - Register targets (common confusion)

For ECS Fargate at this step:

```text
Do NOT manually enter IP addresses
```

Keep:

```text
Targets = 0
```

Reason:

```text
ECS Service will auto-register task IPs into the target group when service runs
```

---

## D. Step 3 - Review and Create

Seeing `Targets (0)` in review is still correct for ECS flow.

Click:

```text
Create target group
```

![Review screen confirming that Targets (0) is still valid before creation](_diagrams/target-group-review-zero-targets.webp)

---

## Common Mistakes to Avoid

* manually entering IPs in register target step
* port mismatch between target group and container
* wrong or missing health check path

---

## TL;DR

```text
Target Group = how ALB calls backends
Register targets = skip (ECS auto-registers)
```

---

## Next Step

Go back to ECS Cluster and create Service to bind tasks into Target Group.
