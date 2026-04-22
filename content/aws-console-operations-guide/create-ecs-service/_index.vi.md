---
title: "Step 5 - Tạo ECS Service (Bind ALB + Target Group)"
date: 2026-04-22
weight: 5
chapter: false
---

## Mục tiêu bước này

Đây là bước orchestration chính của ECS:

```text
Run task + attach vào ALB + tự heal + scale
```

---

## Màn hình thao tác

![Create ECS Service](/images/aws-console-operations-guide/ECS/4.%20create-service/ecs-services-creation.png)

---

## Tổng thể: bạn đang làm gì ở màn này?

```text
ECS Service = orchestration layer
```

Nó chịu trách nhiệm:

* chạy task theo task definition
* giữ số lượng replica đúng mong muốn
* đăng ký task vào target group
* phối hợp với ALB để health check và routing

---

## 1. Service details

Giá trị điển hình:

```text
Task definition family: snakeaid-api
Revision: Latest
Service name: snakeaid-api-service
```

Ý nghĩa:

* Task definition = cấu hình container
* Service = cơ chế giữ container luôn chạy

---

## 2. Environment

```text
Cluster: snakeaid-backup-cluster
```

Cluster là runtime environment chứa service và task.

---

## 3. Compute configuration

```text
Capacity provider strategy: FARGATE
```

Bạn đang dùng serverless container, không quản EC2.

---

## 4. Deployment configuration

```text
Scheduling: Replica
Desired tasks: 1
```

Nghĩa là luôn giữ 1 task chạy.

Deployment strategy:

```text
Rolling update
Min: 100%
Max: 200%
```

Khi deploy revision mới, ECS tạo task mới, pass health check rồi mới thay task cũ.

---

## 5. Networking (rất quan trọng)

Giá trị hiện tại:

```text
VPC: default
Subnets: 2 AZ
Security group: default
Public IP: Enabled
```

Ý nghĩa thực tế:

* task Fargate có public IP (dễ test)
* production nên ưu tiên private subnet cho task và giữ ALB public

---

## 6. Load balancing (phần mấu chốt)

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

Mapping tổng quát:

```text
ALB:80 -> Target Group -> Container:8080
```

### Health check

```text
Path: /health
Protocol: HTTP
```

Nếu health check fail, task sẽ bị thay thế theo cơ chế tự heal.

---

## 7. Service auto scaling

Có thể để tắt ở giai đoạn này.

```text
Always = 1 instance
```

---

## 8. Volume

API stateless có thể skip phần volume.

---

## 9. Tags

Không ảnh hưởng runtime, có thể điền sau.

---

## Bức tranh kiến trúc sau bước này

```text
Internet
  -> ALB (snakeaid-alb)
  -> Listener :80
  -> Rule "/"
  -> Target Group (snakeaid-api-tg)
  -> ECS Service
  -> Fargate Task
  -> Container (8080)
```

---

## Checklist trước khi bấm Create

1. Task definition expose đúng port `8080`
2. Endpoint `/health` trả `200`
3. Security group cho phép traffic cần thiết
4. Sau deploy có thể gọi `http://<alb-dns>`

---

## TL;DR

```text
Use existing ALB + existing Target Group + đúng container port
=> ECS Service sẽ bind traffic đúng luồng
```

---

## Bước tiếp theo

Sau khi service lên `Healthy`, test end-to-end qua ALB DNS và tiếp tục cấu hình service cho `snakeai`.
