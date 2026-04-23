---
title: "SnakeAid Disaster-Aware Hybrid Architecture"
date: 2026-04-22
weight: 1
chapter: false
---

# SnakeAid Disaster-Aware 
# Hybrid Architecture

## Objectives

Build a **hybrid architecture (self-host + cloud backup)** to:

* Ensure **service availability** when self-hosted infrastructure fails (power outage, network outage)
* Reduce full dependence on cloud (cost + control)
* Keep the system **lean and easy to operate (low ops overhead)**
* Allow gradual scaling to production-grade when needed

The cloud backup path is being documented along two deployment options:

* **ECS Fargate Classic** for explicit infrastructure control
* **ECS Express Mode** for faster, more opinionated delivery

---

## Architecture Overview

![SnakeAid hybrid architecture diagram](_diagrams/snakeaid-hybrid-architecture-diagram.png)

### Traffic Failover View

![SnakeAid traffic failover diagram](_diagrams/traffic-failover.png)

### Messaging Behavior

![SnakeAid messaging behavior diagram](_diagrams/messaging-behavior.png)

### Failure Transition

![SnakeAid failure transition diagram](_diagrams/failure-sequence.png)

---

## System Components

### Edge Layer

* **Cloudflare DNS**

	* Primary domain: `api.snakeaid.com`
	* Routing:

		* Primary -> ZimaOS
		* Failover -> AWS ALB (manual now, automated in the future)

---

### Primary System (ZimaOS)

The current self-hosted system is the **main runtime**:

* **NGINX Reverse Proxy**

	* Port/subdomain-based routing
* **snakeaid-api (monolithic backend)**
* **snakeai (AI inference service)**
* **RabbitMQ (local container)**

Benefits:

* Low latency
* Full control
* No cloud runtime cost

---

### Backup System (AWS ECS)

The cloud system serves as **standby (active-passive)**.

#### Compute:

* **Amazon ECS deployment path**

	* Option 1: `ECS Fargate Classic`
	* Option 2: `ECS Express Mode`
	* The current detailed hands-on flow is centered on Fargate Classic

#### Networking:

* **Application Load Balancer (ALB)**

	* Provides a stable endpoint
	* Health checks
	* Routing

#### Registry:

* Docker Hub (reduced ops overhead)

---

### Messaging Layer (Dual RabbitMQ)

The system uses **two queue sources in parallel**:

#### Local RabbitMQ

* Runs on ZimaOS
* Serves primary workload

#### Amazon MQ (RabbitMQ managed)

* Serves backup system (ECS)
* Acts as fallback queue

---

## Disaster Awareness Strategy

### Active-Passive Failover

| State       | Routing                  |
| ----------- | ------------------------ |
| Normal      | Cloudflare -> ZimaOS     |
| ZimaOS down | Cloudflare -> ALB -> ECS |

The failover path is intentionally separate from the normal path so the cloud backup can stay passive until needed.

---

### Dual Queue Strategy

#### Primary (ZimaOS):

```text
Priority: local RabbitMQ
Fallback: Amazon MQ
```

#### Backup (ECS):

```text
Use only: Amazon MQ
```

---

### Queue Behavior

* There is no replication between the two queues
* During failover:

	* Pending local messages may be lost
* The system accepts:

	* **eventual consistency**
	* **best-effort delivery**

The messaging diagram above reflects that the local queue and Amazon MQ are two independent sources, not a replicated pair.

---

## Trade-offs and Assumptions

### Queue Non-Synchronization

* Local RabbitMQ != Amazon MQ
* Full message retention is not guaranteed

---

### Idempotency Requirement

The backend must ensure:

* Safe retry handling
* No duplicate side effects

---

### Cold/Warm Standby

* Cold standby:

	* ECS scale = 0 -> cost saving
	* Includes cold start time
* Warm standby:

	* ECS always running -> faster failover

---

### Not Full High Availability Yet

* No multi-region deployment
* No fully automated failover (at current stage)

---

## Architecture Advantages

* Reduced cloud dependence (cost + control)
* Practical disaster recovery path
* Preserves existing system (zero rewrite)
* Simple operations (no Kubernetes, no over-engineering)
* Clear scaling roadmap

---

## Content Map

This documentation is organized into three main tracks:

1. **Fargate vs Express**
2. **Hands-on ClickOps for ECS Fargate**
3. **Hands-on ClickOps for ECS Express**

{{% children description="true" /%}}

---

## Future Roadmap

### Phase 1 (current)

* Active-passive
* Manual failover
* Dual RabbitMQ

---

### Phase 2

* Cloudflare Load Balancer (auto failover)
* ECS auto scaling

---

### Phase 3

* Message replication (Outbox / Event sourcing)
* Multi-region deployment

---

### Phase 4

* AI scaling (GPU / SageMaker)
* Event-driven architecture (Kafka if needed)

---

## Conclusion

The proposed architecture is a:

> **Disaster-aware Hybrid Architecture (Self-host + Cloud Backup)**

It balances:

* **Reliability** (cloud backup available)
* **Cost-efficiency** (self-hosted primary)
* **Operational simplicity** (no over-engineering)

It is suitable for:

* Startup stage
* Capstone project
* Medium-scale production systems

---

## One-line Summary

```text
Cloudflare DNS -> (Primary: ZimaOS + local RabbitMQ)
							 -> (Backup: ALB -> ECS Fargate + Amazon MQ)
```
