---
title: "Step 3 - Tạo Application Load Balancer (ALB)"
date: 2026-04-22
weight: 3
chapter: false
---

## Mục tiêu bước này

Tạo ALB làm public entry point cho hệ thống backup trên ECS.

![Sơ đồ luồng request đi qua ALB](_diagrams/request-routing.png)

---

## ALB là gì trong kiến trúc này?

ALB đóng vai trò:

* cổng vào public
* router theo listener/rule
* forward request xuống target group

Lưu ý: ALB không chứa backend, ALB chỉ forward.

### Các thành phần bên trong ALB

![Sơ đồ các thành phần bên trong ALB](_diagrams/alb-components.png)

Cách dễ hiểu nhất về ALB là: nó nhận traffic public, áp listener rule, rồi forward request vào target group.

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

![Phần cấu hình cơ bản của ALB hiển thị name, scheme và lựa chọn IPv4](_diagrams/alb-basic-configuration.webp)

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

Đây là chỗ network placement quan trọng hơn chính ALB setting: load balancer nên nằm ở public subnet, còn backend task phía sau có thể theo thiết kế runtime cuối cùng.

![Sơ đồ vị trí network của ALB](_diagrams/network-placement.png)

![Phần network mapping của ALB hiển thị VPC và hai public subnet](_diagrams/alb-network-mapping-subnets.webp)

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

![Cấu hình ALB hiển thị security group đã chọn và listener forward về target group](_diagrams/alb-security-listener-routing.webp)

---

## D. Listeners and routing (quan trọng nhất)

Set listener mặc định:

```text
Listener: HTTP :80
Action: Forward -> snakeaid-api-tg
```

Đây mới là lớp routing cốt lõi của hệ thống: listener nhận traffic, rule quyết định đích đến, còn target group trở thành backend pool mà ECS sẽ nạp target vào sau.

![Sơ đồ luồng request đi qua ALB](_diagrams/request-routing.png)

---

## E. Advanced services

Giai đoạn hiện tại có thể skip:

* CloudFront
* WAF
* Global Accelerator

![Các dịch vụ nâng cao như CloudFront, WAF và Global Accelerator có thể bỏ qua ở giai đoạn này](_diagrams/alb-advanced-services.webp)

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

![Màn hình review tóm tắt cấu hình ALB trước khi tạo](_diagrams/alb-review-summary.webp)

---

## Insight quan trọng

Nếu target group chưa có target (Targets = 0), ALB chưa thể forward traffic thành công ngay.

![Sơ đồ cho thấy ALB có thể tạo xong trước khi ECS service đăng ký target vào target group](_diagrams/empty-target-group-state.png)

---

## TL;DR

ALB là public entry point, target group là backend pool, còn ECS Service là lớp sẽ cung cấp các target đang chạy thật sự.

---

## Bước tiếp theo

Chuyển sang step tạo Target Group hoặc Create Service để bind container vào ALB.
