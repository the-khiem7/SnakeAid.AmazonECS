---
title: "Step 3 - Tạo Application Load Balancer (ALB)"
date: 2026-04-22
weight: 3
chapter: false
---

## Mục tiêu bước này

Tạo ALB làm public entry point cho hệ thống backup trên ECS.

```text
Internet -> ALB -> Target Group -> ECS Tasks
```

---

## ALB là gì trong kiến trúc này?

ALB đóng vai trò:

* cổng vào public
* router theo listener/rule
* forward request xuống target group

Lưu ý: ALB không chứa backend, ALB chỉ forward.

### Các thành phần bên trong ALB

![Sơ đồ các thành phần bên trong ALB](/images/diagrams/create-application-load-balancer/alb-components.png)

### Luồng request đi qua ALB

![Sơ đồ luồng request đi qua ALB](/images/diagrams/create-application-load-balancer/request-routing.png)

### Vị trí network của ALB

![Sơ đồ vị trí network của ALB](/images/diagrams/create-application-load-balancer/network-placement.png)

---

## Ảnh màn hình theo từng phase

### Phase 1: Basic configuration

![Create ALB - Step 1](/images/aws-console-operations-guide/ALB/1.%20create-application-load-balancer/alb-create-1.png)

### Phase 2: Network, security, listener

![Create ALB - Step 2](/images/aws-console-operations-guide/ALB/1.%20create-application-load-balancer/alb-create-2.png)

### Phase 3: Review

![Create ALB - Step 3](/images/aws-console-operations-guide/ALB/1.%20create-application-load-balancer/alb-create-3.png)

---

## A. Basic configuration

Điền:

```text
Load balancer name: snakeaid-alb
Scheme: Internet-facing
IP type: IPv4
```

Giải thích nhanh:

* `Internet-facing` = client ngoài internet gọi được
* `Internal` = chỉ dùng private trong VPC

Với use case SnakeAid backup, chọn `Internet-facing`.

---

## B. Network mapping

Chọn:

```text
VPC: vpc-xxx
Subnets: ap-southeast-1a, ap-southeast-1b
```

Nguyên tắc:

* ALB nên chạy trên >= 2 AZ để tăng availability
* subnet phải là public subnet (có route ra IGW)
* VPC này cần match với ECS service và target group

---

## C. Security groups

Ví dụ hiện tại:

```text
default security group
```

Điểm bắt buộc cần kiểm tra:

```text
Inbound: HTTP 80 from 0.0.0.0/0
```

Nếu thiếu rule inbound phù hợp, ALB tạo xong vẫn không truy cập được.

---

## D. Listeners and routing (quan trọng nhất)

Set listener mặc định:

```text
Listener: HTTP :80
Action: Forward -> snakeaid-api-tg
```

Hiểu bản chất:

```text
Client -> ALB:80 -> Rule -> Target Group
```

Đây là lớp routing chính của hệ thống.

---

## E. Advanced services

Giai đoạn hiện tại có thể skip:

* CloudFront
* WAF
* Global Accelerator

---

## F. Review trước khi tạo

Checklist tối thiểu:

* Name: `snakeaid-alb`
* Scheme: `Internet-facing`
* Subnets: 2 AZ
* Listener: `HTTP:80`
* Action: forward đến `snakeaid-api-tg`

Sau đó bấm:

```text
Create load balancer
```

---

## Insight quan trọng

Nếu target group chưa có target (Targets = 0), ALB chưa thể forward traffic thành công ngay.

```text
ALB created -> Target Group (empty) -> wait ECS Service attach
```

---

## TL;DR

```text
ALB = entry point
Target Group = backend pool
ECS Service = compute thực tế
```

---

## Bước tiếp theo

Chuyển sang step tạo Target Group hoặc Create Service để bind container vào ALB.
