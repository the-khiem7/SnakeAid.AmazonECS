---
title: "Step 4 - Tạo Target Group"
date: 2026-04-22
weight: 4
chapter: false
---

## Mục tiêu bước này

Tạo Target Group để ALB biết cách gọi backend của ECS.

![Sơ đồ quan hệ các port của target group](_diagrams/port-alignment.png)

---

## Target Group là gì?

Target Group là phần định nghĩa backend pool để ALB biết request cần được đẩy về đâu.

Nó định nghĩa cách ALB gọi backend: protocol, port, health check.

### Luồng health check

![Sơ đồ luồng health check của target group](_diagrams/health-check.png)

### ECS tự động đăng ký target

![Sơ đồ ECS tự động đăng ký target](_diagrams/auto-registration.png)

### Quan hệ các port

![Sơ đồ quan hệ các port của target group](_diagrams/port-alignment.png)

Ba góc nhìn này đi cùng nhau để giải thích trọn vai trò của target group: định nghĩa hợp đồng backend, kiểm tra health, và chờ ECS đăng ký task IP thật về sau.

---

## A. Step 1 - Target group details

### 1. Target type

Chọn:

```text
IP addresses
```

Vì sao:

* `Instances` dùng cho EC2
* `IP addresses` dùng cho ECS Fargate/container
* `Lambda` dùng cho Lambda function

Với SnakeAid chạy ECS Fargate, bắt buộc chọn `IP addresses`.

![Cấu hình target group hiển thị target type IP, name, protocol, port, VPC và HTTP1](_diagrams/target-group-settings.webp)

### 2. Name

```text
snakeaid-api-tg
```

Tên này là label để quản lý, không ảnh hưởng logic runtime.

### 3. Protocol và Port

```text
HTTP : 8080
```

Cực kỳ quan trọng:

```text
Port target group phải khớp container port
```

Nếu container lắng nghe 8080 thì target group cũng phải là 8080.

![Sơ đồ quan hệ các port của target group](_diagrams/port-alignment.png)

### 4. VPC

```text
vpc-xxx
```

VPC của target group phải cùng môi trường với ECS service và ALB.

### 5. Protocol version

```text
HTTP1
```

Giữ mặc định là phù hợp cho case hiện tại.

---

## B. Health Check

Set:

```text
Protocol: HTTP
Path: /health
```

ALB sẽ gọi:

```text
http://<task-ip>:8080/health
```

Yêu cầu endpoint trả về `200 OK`.

Nếu sai path hoặc app không có route này, target sẽ bị `UNHEALTHY`.

![Sơ đồ luồng health check của target group](_diagrams/health-check.png)

![Phần review cho thấy health check path và success code đã được cấu hình](_diagrams/target-group-review-health-check.webp)

---

## C. Step 2 - Register targets (điểm hay nhầm)

Ở bước này với ECS Fargate:

```text
KHÔNG cần nhập IP thủ công
```

Giữ trạng thái:

```text
Targets = 0
```

Lý do:

ECS Service sẽ tự động register task IP vào target group khi service chạy.

![Sơ đồ ECS tự động đăng ký target](_diagrams/auto-registration.png)

![Màn Register targets cho thấy chưa thêm IP thủ công nào](_diagrams/target-group-register-targets-empty.webp)

---

## D. Step 3 - Review và Create

Nếu bạn thấy `Targets (0)` ở màn review thì vẫn đúng cho flow ECS.

Bấm:

```text
Create target group
```

![Sơ đồ cho thấy Targets = 0 vẫn là trạng thái hợp lệ ở màn review trước khi ECS Service tồn tại](_diagrams/target-group-empty-review-state.png)

![Màn review xác nhận rằng Targets (0) vẫn là trạng thái đúng trước khi tạo](_diagrams/target-group-review-zero-targets.webp)

---

## Lỗi phổ biến cần tránh

* Nhập IP thủ công ở bước register target
* Port mismatch giữa target group và container
* Health check path sai hoặc không tồn tại

---

## TL;DR

Target Group định nghĩa cách ALB gọi backend, còn bước register targets có thể để trống vì ECS sẽ nạp target về sau.

---

## Bước tiếp theo

Quay lại ECS Cluster và tạo Service để bind task vào Target Group.
