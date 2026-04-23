---
title: "Khung hướng dẫn thao tác trên AWS Console"
date: 2026-04-22
weight: 3
chapter: false
---

## Mục tiêu trang

Trang này là khung chuẩn để ghi lại từng bước thao tác trên AWS Console cho kiến trúc SnakeAid.

---

## Phạm vi

* Dùng cho các thao tác cấu hình thủ công trên AWS Console
* Ưu tiên theo luồng triển khai thực tế của dự án
* Mỗi mục con sẽ là một tác vụ cụ thể

---

## Mental model cho AWS backup

### Bản đồ luồng thao tác trên Console

![Sơ đồ workflow thao tác trên AWS Console](_diagrams/console-workflow.png)

### Mental model runtime

![Sơ đồ mental model runtime của hệ thống backup AWS](_diagrams/runtime-mental-model.png)

### Quan hệ phụ thuộc giữa các resource

![Sơ đồ quan hệ phụ thuộc giữa các resource AWS backup](_diagrams/resource-dependency.png)

---

## Điều kiện trước khi thao tác

* Có tài khoản AWS và quyền truy cập phù hợp
* Chọn đúng region cho môi trường triển khai
* Chuẩn bị sẵn các thông tin đầu vào (service name, port, image, env)

---

## Cấu trúc mỗi mục con (template)

Mỗi trang con nên theo format sau:

1. **Mục đích**
2. **Input cần chuẩn bị**
3. **Các bước trên Console**
4. **Expected result**
5. **Lưu ý / lỗi thường gặp**
6. **Rollback (nếu có)**

---

## Danh sách mục con dự kiến

1. Tạo ECS Cluster (Fargate)
2. Tạo Task Definition cho `snakeaid-api`
3. Tạo Task Definition cho `snakeai`
4. Tạo ALB và Target Groups
5. Tạo ECS Service và attach ALB
6. Cấu hình kết nối Amazon MQ
7. Kiểm tra health check và failover

---

## Các mục con

{{% children description="true" /%}}

---

## Ghi chú biên soạn

* Mỗi bước nên kèm đường dẫn điều hướng trong Console
* Dùng tên tài nguyên nhất quán để dễ tìm lại
* Nếu có ảnh chụp màn hình, lưu trong `static/images/` và dùng đường dẫn root-relative

---

## Nội dung sẽ cập nhật tiếp

Phần chi tiết cho từng mục con sẽ được bổ sung ở các page con thuộc trang này.
