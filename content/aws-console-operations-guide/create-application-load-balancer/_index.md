---
title: "Step 3 - Create Application Load Balancer (ALB)"
date: 2026-04-22
weight: 3
chapter: false
---

## Goal of This Step

Create an ALB as the public entry point for the ECS backup system.

```text
Internet -> ALB -> Target Group -> ECS Tasks
```

---

## What Is ALB in This Architecture?

ALB acts as:

* public entry point
* listener/rule-based router
* forwarder to target groups

Important: ALB does not host backends. It only forwards traffic.

### ALB Components

![ALB components diagram](_diagrams/alb-components.png)

### Request Routing

![ALB request routing diagram](_diagrams/request-routing.png)

### Network Placement

![ALB network placement diagram](_diagrams/network-placement.png)

---

## Screens by UI Phase

### Phase 1: Basic configuration

![Create ALB - Step 1](/images/aws-console-operations-guide/ALB/1.%20create-application-load-balancer/alb-create-1.png)

### Phase 2: Network, security, listener

![Create ALB - Step 2](/images/aws-console-operations-guide/ALB/1.%20create-application-load-balancer/alb-create-2.png)

### Phase 3: Review

![Create ALB - Step 3](/images/aws-console-operations-guide/ALB/1.%20create-application-load-balancer/alb-create-3.png)

---

## A. Basic configuration

Set:

```text
Load balancer name: snakeaid-alb
Scheme: Internet-facing
IP type: IPv4
```

Quick meaning:

* `Internet-facing` = reachable from the public internet
* `Internal` = private inside VPC

For SnakeAid backup use case, choose `Internet-facing`.

---

## B. Network mapping

Choose:

```text
VPC: vpc-xxx
Subnets: ap-southeast-1a, ap-southeast-1b
```

Rules:

* ALB should span >= 2 AZs for availability
* subnets should be public (route to IGW)
* VPC must match ECS service and target group

---

## C. Security groups

Current example:

```text
default security group
```

Mandatory check:

```text
Inbound: HTTP 80 from 0.0.0.0/0
```

Without proper inbound rules, ALB can be created but not reachable.

---

## D. Listeners and routing (most important)

Set default listener:

```text
Listener: HTTP :80
Action: Forward -> snakeaid-api-tg
```

Core flow:

```text
Client -> ALB:80 -> Rule -> Target Group
```

This is the main routing layer.

---

## E. Advanced services

At this stage, it is fine to skip:

* CloudFront
* WAF
* Global Accelerator

---

## F. Review before create

Minimum checklist:

* Name: `snakeaid-alb`
* Scheme: `Internet-facing`
* Subnets: 2 AZ
* Listener: `HTTP:80`
* Action: forward to `snakeaid-api-tg`

Then click:

```text
Create load balancer
```

---

## Key Insight

If your target group is still empty (Targets = 0), ALB cannot forward real traffic yet.

```text
ALB created -> Target Group (empty) -> wait ECS Service attach
```

---

## TL;DR

```text
ALB = entry point
Target Group = backend pool
ECS Service = actual compute
```

---

## Next Step

Move to Target Group step or Create Service to bind containers into ALB.
