---
title: "Why Choose ECS Fargate (Standard) Over Express Mode"
date: 2026-04-22
weight: 1
chapter: false
pre: " <b> 1.1. </b> "
---

## Short Answer

Choose **ECS Fargate (standard)** and avoid **Express Mode** for the current SnakeAid architecture.

---

## Why Express Mode Looks Convenient but Is Not a Fit

Amazon ECS Express Mode is a fast path to deploy one container with automatic setup.

It is suitable for:

* quick demos
* simple apps
* short-lived testing

---

## Problem for the SnakeAid Architecture

SnakeAid currently includes:

* multi-service design:
  * `snakeaid-api`
  * `snakeai`
* ALB routing
* dual RabbitMQ (local + Amazon MQ)
* need for network, environment, and failover control

With this setup, Express Mode has practical limits:

* difficult to attach and tune ALB behavior in detail
* harder to separate multiple services cleanly
* networking is abstracted too much for deep debugging
* not a strong fit for your hybrid self-host + cloud backup model

---

## ECS Fargate (Standard) Is the Right Deployment Model

Recommended layout:

```text
ECS Cluster
 ├── Service: snakeaid-api
 └── Service: snakeai
```

---

## Direct Benefits for Your Case

* Full ALB control:
  * dedicated target groups
  * `/health` checks
* Flexible env configuration:
  * Doppler
  * dual RabbitMQ config
* Clear networking model:
  * VPC
  * security groups
* Standby strategy control:
  * scale = 0 (cold standby)
  * scale = 1 (warm standby)

---

## Requirement Fit Matrix

| Requirement         | Express   | Fargate |
| ------------------- | --------- | ------- |
| Multi service       | ❌         | ✅       |
| ALB integration     | ❌ limited | ✅       |
| Hybrid architecture | ❌         | ✅       |
| Failover control    | ❌         | ✅       |
| Debug / control     | ❌         | ✅       |

---

## Key Insight

Express Mode is a developer convenience layer.

SnakeAid is solving infrastructure design and failover operations.

These are different levels of control and responsibility.

---

## When Express Mode Is Actually Appropriate

Use it only when:

* there is a single container
* no advanced ALB requirement
* no custom networking requirement
* no hybrid or failover control requirement

Examples:

* demo API
* quick container test

---

## Conclusion

```text
Use ECS Fargate (standard) + ALB
Avoid Express Mode
```

---

## Recommended Next Steps

1. Create an ECS Cluster (Fargate)
2. Create Task Definitions for:
   * snakeaid-api
   * snakeai
3. Create an ALB with 2 target groups
4. Create ECS Services and attach them to ALB
5. Connect Amazon MQ
6. Run end-to-end failover testing
