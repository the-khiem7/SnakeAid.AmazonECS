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

![Sơ đồ các thành phần bên trong ALB](_diagrams/alb-components.png)

### Luồng request đi qua ALB

![Sơ đồ luồng request đi qua ALB](_diagrams/request-routing.png)

### Vị trí network của ALB

![Sơ đồ vị trí network của ALB](_diagrams/network-placement.png)

---

## Ảnh màn hình theo từng phase

### Phase 1: Basic configuration

![Phần cấu hình cơ bản của ALB hiển thị name, scheme và lựa chọn IPv4](_diagrams/alb-basic-configuration.webp)

### Phase 2: Network mapping

![Phần network mapping của ALB hiển thị VPC và hai public subnet](_diagrams/alb-network-mapping-subnets.webp)

### Phase 3: Security groups và listener routing

![Cấu hình ALB hiển thị security group đã chọn và listener forward về target group](_diagrams/alb-security-listener-routing.webp)

### Phase 4: Dịch vụ nâng cao có thể bỏ qua

![Các dịch vụ nâng cao như CloudFront, WAF và Global Accelerator có thể bỏ qua ở giai đoạn này](_diagrams/alb-advanced-services.webp)

### Phase 5: Review

![Màn hình review tóm tắt cấu hình ALB trước khi tạo](_diagrams/alb-review-summary.webp)

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
