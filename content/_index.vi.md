---
title: "SnakeAid Disaster-Aware Hybrid Architecture"
date: 2026-04-22
weight: 1
chapter: false
---

# SnakeAid Disaster-Aware 
# Hybrid Architecture

## Mục tiêu

Xây dựng một kiến trúc **hybrid (self-host + cloud backup)** nhằm:

* Đảm bảo **dịch vụ luôn sẵn sàng** khi hạ tầng self-host gặp sự cố (mất điện, mất mạng)
* Giảm phụ thuộc hoàn toàn vào cloud (cost + control)
* Duy trì hệ thống **lean, dễ vận hành (low ops overhead)**
* Cho phép mở rộng dần lên production-grade khi cần

---

## Tổng quan kiến trúc

```mermaid
flowchart TB

subgraph Edge["Cloudflare DNS"]
		CF["api.snakeaid.com"]
end

subgraph Primary["Primary System (ZimaOS - Self-hosted)"]
		NGINX["NGINX Reverse Proxy"]

		subgraph Local["Docker Containers"]
				API1["snakeaid-api"]
				AI1["snakeai"]
				RMQ1["RabbitMQ (local)"]
		end

		NGINX --> API1
		NGINX --> AI1
		API1 --> RMQ1
end

subgraph Backup["AWS Backup System"]
		ALB["Application Load Balancer"]

		subgraph ECS["ECS Fargate"]
				API2["snakeaid-api"]
				AI2["snakeai"]
		end

		ALB --> API2
		ALB --> AI2
end

subgraph MQ["Messaging Layer"]
		RMQ_AWS["Amazon MQ (RabbitMQ managed)"]
end

CF --> NGINX
CF -. failover .-> ALB

API1 -. fallback .-> RMQ_AWS
API2 --> RMQ_AWS
```

---

## Thành phần hệ thống

### Edge Layer

* **Cloudflare DNS**

	* Domain chính: `api.snakeaid.com`
	* Routing:

		* Primary -> ZimaOS
		* Failover -> AWS ALB (manual hoặc tự động trong tương lai)

---

### Primary System (ZimaOS)

Hệ thống self-host hiện tại đóng vai trò **runtime chính**:

* **NGINX Reverse Proxy**

	* Routing theo port/subdomain
* **snakeaid-api (monolith backend)**
* **snakeai (AI inference service)**
* **RabbitMQ (local container)**

Ưu điểm:

* latency thấp
* full control
* không tốn chi phí cloud

---

### Backup System (AWS ECS)

Hệ thống cloud đóng vai trò **standby (active-passive)**

#### Compute:

* **ECS Fargate**

	* Service 1: `snakeaid-api`
	* Service 2: `snakeai`
	* Mỗi service: 1 instance

#### Networking:

* **Application Load Balancer (ALB)**

	* cung cấp endpoint tĩnh
	* health check
	* routing

#### Registry:

* Docker Hub (giảm ops overhead)

---

### Messaging Layer (Dual RabbitMQ)

Hệ thống sử dụng **2 nguồn queue song song**:

#### Local RabbitMQ

* chạy trong ZimaOS
* phục vụ primary workload

#### Amazon MQ (RabbitMQ managed)

* phục vụ backup system (ECS)
* đóng vai trò fallback queue

---

## Chiến lược Disaster Awareness

### Active-Passive Failover

| Trạng thái   | Routing                  |
| ----------- | ------------------------ |
| Bình thường | Cloudflare -> ZimaOS     |
| ZimaOS fail | Cloudflare -> ALB -> ECS |

---

### Dual Queue Strategy

#### Primary (ZimaOS):

```text
Ưu tiên: RabbitMQ local
Fallback: Amazon MQ
```

#### Backup (ECS):

```text
Chỉ sử dụng: Amazon MQ
```

---

### Queue Behavior

* Không có replication giữa 2 queue
* Khi failover:

	* message pending ở local có thể mất
* Hệ thống chấp nhận:

	* **eventual consistency**
	* **best-effort delivery**

---

## Các Trade-offs và Giả định

### Không đồng bộ queue

* RabbitMQ local != Amazon MQ
* Không đảm bảo giữ toàn bộ message

---

### Yêu cầu Idempotency

Backend cần đảm bảo:

* xử lý retry an toàn
* không tạo side-effect duplicate

---

### Cold/Warm Standby

* Cold standby:

	* ECS scale = 0 -> tiết kiệm chi phí
	* có cold start
* Warm standby:

	* ECS luôn chạy -> failover nhanh

---

### Không High Availability đầy đủ

* không multi-region
* không auto failover hoàn toàn (giai đoạn hiện tại)

---

## Ưu điểm của kiến trúc

* Giảm phụ thuộc cloud (cost + control)
* Có disaster recovery thực tế
* Giữ nguyên hệ thống hiện tại (zero rewrite)
* Ops đơn giản (no Kubernetes, no over-engineering)
* Có lộ trình scale rõ ràng

---

## Lộ trình nâng cấp (Future Roadmap)

### Giai đoạn 1 (hiện tại)

* Active-Passive
* Manual failover
* Dual RabbitMQ

---

### Giai đoạn 2

* Cloudflare Load Balancer (auto failover)
* ECS auto scaling

---

### Giai đoạn 3

* Message replication (Outbox / Event sourcing)
* Multi-region deployment

---

### Giai đoạn 4

* AI scaling (GPU / SageMaker)
* Event-driven architecture (Kafka nếu cần)

---

## Kết luận

Kiến trúc đề xuất là một hệ thống:

> **Disaster-aware Hybrid Architecture (Self-host + Cloud Backup)**

Nó đạt được sự cân bằng giữa:

* **Reliability** (có backup cloud)
* **Cost-efficiency** (primary self-host)
* **Operational simplicity** (không over-engineer)

Phù hợp cho:

* startup stage
* capstone project
* hệ thống production quy mô vừa

---

## One-line Summary

```text
Cloudflare DNS -> (Primary: ZimaOS + RabbitMQ local)
							 -> (Backup: ALB -> ECS Fargate + Amazon MQ)
```