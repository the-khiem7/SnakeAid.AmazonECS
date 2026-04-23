---
title: "Step 2 - Tạo Task Definition (API + AI)"
date: 2026-04-22
weight: 2
chapter: false
---

## Mục tiêu bước này

Tạo 2 task definition riêng cho kiến trúc SnakeAid:

1. `snakeaid-api`
2. `snakeai`

---

## Task Definition là gì?

Trong Amazon Elastic Container Service:

> **Task Definition = bản mô tả container của bạn**

Hiểu tương đương:

```text
docker-compose (1 service) ≈ Task Definition
```

Nó định nghĩa:

* image
* port
* env
* CPU / RAM

### Cấu trúc của Task Definition

![Sơ đồ cấu trúc của task definition](_diagrams/task-definition-anatomy.png)

### Task Definition đi vào runtime như thế nào

![Sơ đồ task definition đi vào runtime](_diagrams/task-to-runtime.png)

### Profile task của API và AI

![Sơ đồ profile task của API và AI](_diagrams/task-profiles.png)

### IAM role trong quá trình chạy task

![Sơ đồ IAM role trong quá trình chạy task ECS](_diagrams/iam-roles.png)

---

## Kiểm tra điều kiện trước khi làm

Bạn nên xác nhận cluster backup đã tạo thành công ở Step 1 trước khi tạo task definition.

![Danh sách ECS clusters cho thấy backup cluster đã sẵn sàng](_diagrams/task-definition-cluster-created-list.webp)

---

## A. Vào màn Task Definitions

Điều hướng: `Amazon Elastic Container Service > Task definitions`

1. Ở ô Search trên cùng, gõ:

```text
Task definitions
```

2. Click:

```text
Task definitions
```

3. Tại màn danh sách task, click:

```text
Create new task definition
```

Bạn có thể bấm nút ở giữa màn hoặc góc phải, kết quả giống nhau.

![Màn Task definitions với hành động Create new task definition](_diagrams/task-definition-list-create-button.webp)

---

## B. Step 2A - Tạo Task Definition cho API

Bạn đang ở đúng phần quan trọng nhất của ECS. Màn này dài, nên chỉ cần tập trung vào các field cần thiết để tránh bị ngợp.

### Mục tiêu hiện tại

```text
Task Definition cho snakeaid-api
```

Chỉ cần điền khoảng 20% field là đủ chạy.

![Phần đầu form tạo task definition hiển thị family, launch type, CPU, memory và IAM role](_diagrams/task-definition-create-top-config.webp)

### 1. Task definition configuration

Ý nghĩa: thông tin chung của blueprint container.

```text
Task definition family: snakeaid-api
```

### 2. Infrastructure requirements

Ý nghĩa: chọn cách chạy container (serverless hay tự quản server).

```text
Launch type: AWS Fargate
```

### 3. Task size (quan trọng)

Ý nghĩa: CPU và RAM cấp cho container.

```text
CPU: 0.5 vCPU
Memory: 1 GB
```

Mức này đủ cho backend hiện tại.

### 4. Container (phần quan trọng nhất)

Đây là phần tương đương `docker run config`.

![Phần Container hiển thị Image URI và Port mappings](_diagrams/task-definition-create-container-port.webp)

```text
Name: snakeaid-api
Image URI: thekhiem7/snakeaid-api:latest
```

Image từ Docker Hub là phù hợp cho giai đoạn này.

### 5. Port mappings

ECS cần biết ứng dụng listen ở port nào.

```text
Container port: 8080
Protocol: TCP
```

### 6. Environment variables (rất quan trọng)

Đây là phần thay cho env trong docker-compose.

```text
DOPPLER_TOKEN=your_token
DOPPLER_CONFIG=snake-aid/dev
RabbitMq__Host=<Amazon MQ endpoint>
```

Lưu ý quan trọng:

```text
KHÔNG dùng: rabbitmq
```

Vì ECS không có container RabbitMQ local như môi trường self-host.

![Phần Environment variables và CloudWatch log collection trong form task definition](_diagrams/task-definition-create-env-logging.webp)

### 7. Logging

Log sẽ được đẩy về CloudWatch.

```text
Log driver: awslogs
Region: ap-southeast-1
Log group: auto create
```

### 8. Task role và Execution role

Đây là hai IAM role bắt buộc cho task.

```text
Create new role
```

Cho cả hai role:

* Task role
* Execution role

### 9. Các phần skip

Không cần đụng ở bước này:

* GPU
* Storage
* Firelens
* Volumes
* Health check (set sau)
* Container dependency

### 10. Tạo task

```text
Create
```

Kết quả mong đợi:

```text
Task Definition: snakeaid-api (rev 1)
```

---

## C. Step 2B - Lặp lại cho snakeai

Dùng flow y hệt cho AI service với quick config:

```text
Name: snakeai
Image: thekhiem7/snakeaid-snake-detection-ai:8
Port: 8000
CPU: 1 vCPU
Memory: 2 GB
```

Sau khi tạo xong cả hai task (API + AI), gửi screenshot để chuyển sang bước ALB + Service.

---

## D. Xác nhận kết quả

Sau khi hoàn tất, danh sách task cần có đủ:

* `snakeaid-api` (rev 1)
* `snakeai`

### Screenshot: snakeaid-api

![Task definition snakeaid-api đã tạo thành công với revision 1 và environment settings](_diagrams/task-definition-api-created.webp)

### Screenshot: snakeai

![Task definition snakeai đã tạo thành công với revision 1 và task sizing](_diagrams/task-definition-ai-created.webp)

---

## Insight quan trọng

```text
docker-compose -> ECS task definition
```

---

## TL;DR

```text
Điền: Name + Image + Port + Env + CPU/RAM
-> Create
```

---

## Bước tiếp theo

Khi đã có đủ 2 task, chuyển sang bước **ALB + Service**.

![Màn Cluster services với hành động Create service](_diagrams/task-definition-next-step-services.webp)
