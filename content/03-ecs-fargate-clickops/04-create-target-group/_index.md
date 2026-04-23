---
title: "Step 4 - Create Target Group"
date: 2026-04-22
weight: 4
chapter: false
---

## Goal of This Step

Create a Target Group so ALB knows how to route traffic to ECS backends.

![Target group port alignment diagram](_diagrams/port-alignment.png)

---

## What Is a Target Group?

Target Group is the backend pool definition that tells ALB where requests should go.

It defines how ALB calls backends: protocol, port, and health checks.

### Health Check Flow

![Target group health check diagram](_diagrams/health-check.png)

### ECS Auto Registration

![Target group auto registration diagram](_diagrams/auto-registration.png)

### Port Alignment

![Target group port alignment diagram](_diagrams/port-alignment.png)

Together, these three views explain the whole job of a target group: define the backend contract, validate health, and wait for ECS to register real task IPs later.

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

![Target group settings showing IP target type, name, protocol, port, VPC, and HTTP1](_diagrams/target-group-settings.webp)

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

![Target group port alignment diagram](_diagrams/port-alignment.png)

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

![Target group health check diagram](_diagrams/health-check.png)

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

ECS Service will auto-register task IPs into the target group when service runs.

![Target group auto registration diagram](_diagrams/auto-registration.png)

![Register targets screen showing no manually added IP addresses](_diagrams/target-group-register-targets-empty.webp)

---

## D. Step 3 - Review and Create

Seeing `Targets (0)` in review is still correct for ECS flow.

Click:

```text
Create target group
```

![Diagram showing that Targets = 0 is still valid at review time before ECS Service exists](_diagrams/target-group-empty-review-state.png)

![Review screen confirming that Targets (0) is still valid before creation](_diagrams/target-group-review-zero-targets.webp)

---

## Common Mistakes to Avoid

* manually entering IPs in register target step
* port mismatch between target group and container
* wrong or missing health check path

---

## TL;DR

Target Group defines how ALB calls backends, and the register-targets step can stay empty because ECS will populate it later.

---

## Next Step

Go back to ECS Cluster and create Service to bind tasks into Target Group.
