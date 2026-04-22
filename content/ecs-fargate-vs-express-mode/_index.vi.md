---
title: "Vì sao chọn ECS Fargate (Standard) thay vì Express Mode"
date: 2026-04-22
weight: 2
chapter: false
---

## Kết luận ngắn gọn

Chọn **ECS Fargate (standard)**, không dùng **Express Mode** cho kiến trúc SnakeAid hiện tại.

---

## Vì sao Express Mode nhìn tiện nhưng không hợp

Express Mode của Amazon ECS là mô hình triển khai nhanh 1 container với nhiều cấu hình tự động.

Nó phù hợp cho:

* demo nhanh
* ứng dụng đơn giản
* bài test ngắn hạn

---

## Vấn đề khi áp dụng vào SnakeAid

Kiến trúc SnakeAid đang có:

* đa dịch vụ:
  * `snakeaid-api`
  * `snakeai`
* ALB routing
* dual RabbitMQ (local + Amazon MQ)
* nhu cầu kiểm soát network, environment, failover

Vì vậy, Express Mode sẽ có các giới hạn:

* khó gắn ALB theo cách chi tiết
* khó tách nhiều service sạch và rõ trách nhiệm
* networking bị trừu tượng hóa, khó debug sâu
* không phù hợp kiến trúc hybrid self-host + cloud backup

---

## ECS Fargate (standard) là lựa chọn đúng

Mô hình nên dùng:

```text
ECS Cluster
 ├── Service: snakeaid-api
 └── Service: snakeai
```

---

## Ưu điểm trực tiếp cho case này

* Kiểm soát đầy đủ ALB:
  * target group riêng
  * health check `/health`
* Cấu hình env linh hoạt:
  * Doppler
  * dual RabbitMQ config
* Networking rõ ràng:
  * VPC
  * security group
* Điều khiển chế độ standby:
  * scale = 0 (cold standby)
  * scale = 1 (warm standby)

---

## Mức độ phù hợp theo yêu cầu

| Requirement         | Express   | Fargate |
| ------------------- | --------- | ------- |
| Multi service       | ❌         | ✅       |
| ALB integration     | ❌ hạn chế | ✅       |
| Hybrid architecture | ❌         | ✅       |
| Failover control    | ❌         | ✅       |
| Debug / control     | ❌         | ✅       |

---

## Insight quan trọng

Express Mode là lớp tiện lợi cho developer.

Trong khi đó, SnakeAid đang làm bài toán thiết kế hạ tầng và vận hành failover.

Hai nhu cầu này khác cấp độ kiểm soát.

---

## Khi nào nên dùng Express Mode

Chỉ nên dùng khi:

* chỉ có 1 container
* không cần ALB phức tạp
* không cần custom network
* không cần hybrid hoặc failover chi tiết

Ví dụ:

* demo API
* test container nhanh

---

## Kết luận

```text
Use ECS Fargate (standard) + ALB
Avoid Express Mode
```

---

## Next Steps đề xuất

1. Tạo ECS Cluster (Fargate)
2. Tạo Task Definition cho:
   * snakeaid-api
   * snakeai
3. Tạo ALB với 2 target groups
4. Tạo ECS Services và attach ALB
5. Kết nối Amazon MQ
6. Test failover end-to-end
