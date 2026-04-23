---
title: "SnakeAid Disaster-Aware Hybrid Architecture"
date: 2026-04-22
weight: 1
chapter: false
---

# SnakeAid Disaster-Aware
# Hybrid Architecture

SnakeAid đi theo một mô hình hybrid thực dụng: giữ runtime chính ở self-host, và duy trì AWS như một đường backup khi hệ thống primary không còn khả dụng.

## Mục tiêu

* Giữ dịch vụ còn truy cập được khi self-host gặp sự cố
* Tránh phụ thuộc hoàn toàn vào cloud về cost và control
* Giữ vận hành gọn và dễ theo dõi
* Chừa chỗ cho việc nâng cấp dần lên production-grade

Phần backup trên AWS hiện được triển khai theo hai hướng song song:

* **ECS Fargate Classic** để giữ quyền kiểm soát hạ tầng sâu hơn
* **ECS Express Mode** để rút ngắn đường đi tới một service chạy được

---

## Toàn cảnh kiến trúc

Hệ thống xoay quanh một nguyên tắc đơn giản: traffic bình thường đi vào ZimaOS, còn traffic failover có thể chuyển sang AWS khi cần.

![Sơ đồ kiến trúc hybrid SnakeAid](_diagrams/snakeaid-hybrid-architecture-diagram.png)

---

## Vai trò traffic và runtime

### Luồng chính

Môi trường self-host trên ZimaOS vẫn là runtime chính:

* `snakeaid-api`
* `snakeai`
* RabbitMQ local
* NGINX reverse proxy

### Luồng backup

AWS đóng vai trò môi trường standby:

* ALB là entry point
* Amazon ECS là compute layer
* Amazon MQ là nguồn queue cho backup path

![Sơ đồ failover traffic của SnakeAid](_diagrams/traffic-failover.png)

| Trạng thái | Routing |
| ---------- | ------- |
| Bình thường | Cloudflare -> ZimaOS |
| Failover | Cloudflare -> ALB -> ECS |

---

## Chiến lược messaging

SnakeAid không coi RabbitMQ local và Amazon MQ là một cặp replicate. Đây là hai nguồn queue tách biệt, phục vụ cho hai runtime path khác nhau.

* Runtime chính ưu tiên RabbitMQ local
* Runtime backup dùng Amazon MQ
* Message pending ở local có thể mất khi failover
* Vì vậy backend cần idempotent và chấp nhận best-effort recovery

![Sơ đồ hành vi messaging của SnakeAid](_diagrams/messaging-behavior.png)

---

## Hai hướng triển khai trên AWS

Stack backup hiện được ghi chép theo hai hướng:

* **Fargate Classic**
  Phù hợp hơn khi cần kiểm soát rõ ALB, target group, networking, và troubleshooting.
* **Express Mode**
  Phù hợp hơn khi ưu tiên tốc độ triển khai và ít quyết định hạ tầng hơn.

Hiện tại, luồng hands-on chi tiết vẫn tập trung vào Fargate Classic.

---

## Kiến trúc này đang tối ưu cho điều gì

* Có disaster recovery thực tế mà không phải viết lại toàn bộ hệ thống
* Tách rõ failover path giữa self-host và cloud
* Giữ ops nhẹ hơn các platform nặng
* Có đường đi từ cold standby tới mức resilience cao hơn sau này

![Sơ đồ chuỗi chuyển trạng thái khi sự cố của SnakeAid](_diagrams/failure-sequence.png)

Các giả định hiện tại:

* standby có thể là cold hoặc warm tùy mức chấp nhận chi phí
* failover chưa tự động hoàn toàn
* đây chưa phải high availability đa vùng

---

## Sơ đồ nội dung

Bộ tài liệu được tách thành ba nhánh:

1. **So sánh Fargate và Express**
2. **Hands-on ClickOps cho ECS Fargate**
3. **Hands-on ClickOps cho ECS Express**

{{% children description="true" /%}}

---

## Lộ trình

Trong giai đoạn gần, mục tiêu là giữ failover ở mức thực dụng và dễ hiểu trước khi bổ sung thêm automation.

### Gần hạn

* Manual failover với backup path ổn định
* ECS auto scaling ở những chỗ cần thiết

### Về sau

* Cloudflare Load Balancer để tự động failover
* Mẫu message durability tốt hơn
* Multi-region hoặc AI scaling nâng cao nếu thật sự cần

Tóm lại, Cloudflare vẫn ở phía trước, ZimaOS giữ vai trò runtime chính, còn AWS cung cấp đường thực thi backup khi cần failover.
