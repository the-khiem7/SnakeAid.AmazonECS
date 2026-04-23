---
title: "SnakeAid Disaster-Aware Hybrid Architecture"
date: 2026-04-22
weight: 1
chapter: false
---

# SnakeAid Disaster-Aware
# Hybrid Architecture

SnakeAid follows a practical hybrid model: keep the main runtime on self-hosted infrastructure, and keep AWS as a backup path when the primary system is unavailable.

## Goals

* Keep the service reachable during self-host outages
* Avoid full dependence on cloud cost and control
* Stay operationally lean
* Leave room for gradual production hardening

The AWS backup track is being explored through two deployment options:

* **ECS Fargate Classic** for deeper infrastructure control
* **ECS Express Mode** for faster, more opinionated setup

---

## Architecture at a Glance

The system is built around a simple rule: normal traffic stays on ZimaOS, and failover traffic can be redirected to AWS when needed.

![SnakeAid hybrid architecture diagram](_diagrams/snakeaid-hybrid-architecture-diagram.png)

---

## Traffic and Runtime Roles

### Primary path

The self-hosted environment on ZimaOS remains the main runtime:

* `snakeaid-api`
* `snakeai`
* local RabbitMQ
* NGINX reverse proxy

### Backup path

AWS acts as a standby environment:

* ALB as entry point
* Amazon ECS as compute layer
* Amazon MQ as backup queue source

![SnakeAid traffic failover diagram](_diagrams/traffic-failover.png)

| State | Routing |
| ----- | ------- |
| Normal | Cloudflare -> ZimaOS |
| Failover | Cloudflare -> ALB -> ECS |

---

## Messaging Strategy

SnakeAid does not treat local RabbitMQ and Amazon MQ as a replicated pair. They are two separate queue sources serving two different runtime paths.

* Primary runtime prefers local RabbitMQ
* Backup runtime uses Amazon MQ
* Pending local messages may be lost during failover
* The system therefore depends on idempotent consumers and best-effort recovery

![SnakeAid messaging behavior diagram](_diagrams/messaging-behavior.png)

---

## Deployment Options on AWS

The backup stack is now documented in two parallel directions:

* **Fargate Classic**
  Best when we need explicit ALB, target group, networking, and troubleshooting control.
* **Express Mode**
  Best when we want a faster path to a running service with fewer infrastructure decisions.

For now, the detailed hands-on flow is centered on Fargate Classic.

---

## What This Architecture Optimizes For

* Practical disaster recovery without rewriting the whole system
* Clear failover separation between self-host and cloud
* Lower ops burden than a heavier platform approach
* A path from cold standby toward more automated resilience later

![SnakeAid failure transition diagram](_diagrams/failure-sequence.png)

Current assumptions:

* standby may be cold or warm depending on cost tolerance
* failover is not fully automated yet
* this is not multi-region high availability

---

## Documentation Map

This documentation is organized into three tracks:

1. **Fargate vs Express**
2. **Hands-on ClickOps for ECS Fargate**
3. **Hands-on ClickOps for ECS Express**

{{% children description="true" /%}}

---

## Roadmap

The near-term plan is to keep failover practical and understandable before adding more automation.

### Near term

* Manual failover with a stable backup path
* ECS auto scaling where needed

### Later

* Cloudflare Load Balancer for automated failover
* Better message durability patterns
* Multi-region or more advanced AI scaling only if justified

In short, Cloudflare stays in front, ZimaOS remains the primary runtime, and AWS provides the backup execution path when failover is needed.
