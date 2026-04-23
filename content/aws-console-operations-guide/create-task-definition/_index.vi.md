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

![Sơ đồ cấu trúc của task definition](/images/diagrams/create-task-definition/task-definition-anatomy.png)

### Task Definition đi vào runtime như thế nào

![Sơ đồ task definition đi vào runtime](/images/diagrams/create-task-definition/task-to-runtime.png)

### Profile task của API và AI

![Sơ đồ profile task của API và AI](/images/diagrams/create-task-definition/task-profiles.png)

### IAM role trong quá trình chạy task

![Sơ đồ IAM role trong quá trình chạy task ECS](/images/diagrams/create-task-definition/iam-roles.png)

---

## Kiểm tra điều kiện trước khi làm

Bạn nên xác nhận cluster backup đã tạo thành công ở Step 1 trước khi tạo task definition.

![ECS Clusters Created](/images/aws-console-operations-guide/ECS/1.%20create-cluster/ecs-clusters-created.png)

---

## Quy ước reference screenshot

Trong markdown của Hugo, chỉ dùng đường dẫn public dạng root-relative:

* `/images/aws-console-operations-guide/ECS/1.%20create-cluster/ecs-clusters-created.png`
* `/images/aws-console-operations-guide/ECS/2.%20create-task-definition/task-definition.png`
* `/images/aws-console-operations-guide/ECS/2.%20create-task-definition/task-definition-create.png`
* `/images/aws-console-operations-guide/ECS/3.%20task-definition-results/task-snakeaid-api-rev1.png`
* `/images/aws-console-operations-guide/ECS/3.%20task-definition-results/task-snakeai.png`
* `/images/aws-console-operations-guide/ECS/2.%20create-task-definition/ecs-services.png`

Không dùng đường dẫn filesystem như `static/images/...` trong nội dung page.

---

## A. Vào màn Task Definitions

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

![Task Definition List](/images/aws-console-operations-guide/ECS/2.%20create-task-definition/task-definition.png)

---

## B. Step 2A - Tạo Task Definition cho API

Bạn đang ở đúng phần quan trọng nhất của ECS. Màn này dài, nên chỉ cần tập trung vào các field cần thiết để tránh bị ngợp.

### Mục tiêu hiện tại

```text
Task Definition cho snakeaid-api
```

Chỉ cần điền khoảng 20% field là đủ chạy.

![Create Task Definition](/images/aws-console-operations-guide/ECS/2.%20create-task-definition/task-definition-create.png)

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

![ECS Task snakeaid-api rev1](/images/aws-console-operations-guide/ECS/3.%20task-definition-results/task-snakeaid-api-rev1.png)

### Screenshot: snakeai

![ECS Task snakeai](/images/aws-console-operations-guide/ECS/3.%20task-definition-results/task-snakeai.png)

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

![ECS Services Screen](/images/aws-console-operations-guide/ECS/2.%20create-task-definition/ecs-services.png)
