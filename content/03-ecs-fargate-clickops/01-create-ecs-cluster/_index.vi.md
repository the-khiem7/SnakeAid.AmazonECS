---
title: "Step 1 - Tạo ECS Cluster"
date: 2026-04-22
weight: 1
chapter: false
---

## Màn hình thao tác

Điều hướng: `Amazon Elastic Container Service > Create cluster`

![Form tạo cluster hiển thị cluster name và lựa chọn Fargate only](_diagrams/ecs-cluster-form-name-infrastructure.webp)

---

## ECS Cluster là gì?

Trong Amazon Elastic Container Service:

> **Cluster = không gian logic để chạy containers**

* Không phải server
* Không tốn tiền trực tiếp
* Chỉ là nơi "gom" các service lại

Cách hiểu dễ nhất là: cluster là ranh giới runtime để chứa service và task, chứ không phải chính phần compute.

### Sơ đồ phạm vi của cluster

![Sơ đồ phạm vi của ECS cluster](_diagrams/cluster-scope.png)

---

## Mục tiêu của bạn ở bước này

Tạo một cluster để:

* chạy backup system (API + AI)
* không quản lý server
* dễ attach ALB sau này

### Cluster trong bối cảnh hệ thống

![Sơ đồ cluster trong bối cảnh hệ thống](_diagrams/cluster-in-context.png)

---

## 1. Cluster name

### Vì sao cần đặt tên rõ ràng?

Sau này bạn có thể có:

* dev cluster
* staging cluster
* backup cluster

Nên đặt tên có nghĩa ngay từ đầu.

### Cấu hình đề xuất

```text
snakeaid-backup-cluster
```

---

## 2. Infrastructure (phần quan trọng nhất)

### Bạn đang chọn cái gì?

Bạn đang chọn **cách AWS chạy container cho bạn**.

| Option  | Ý nghĩa                                   |
| ------- | ----------------------------------------- |
| Fargate | AWS chạy container, bạn không quản server |
| EC2     | bạn tự quản server                        |
| Hybrid  | mix cả 2                                  |

### Mục tiêu của bạn

* không muốn quản server
* chỉ cần backup instance
* không tuning performance sâu

### Chọn

```text
Fargate only
```

### Giải thích dễ hiểu

Fargate là chế độ bạn chỉ khai báo cấu hình container, còn AWS lo phần máy phía dưới.

Bạn chỉ cần:

* image
* RAM / CPU

![Sơ đồ các quyết định tối thiểu thực sự quan trọng khi tạo cluster này](_diagrams/cluster-creation-minimum.png)

---

## 3. Monitoring

### Container Insights là gì?

Đây là hệ thống monitor:

* CPU, RAM
* network
* log analytics

### Với bạn

* đây là backup system
* không cần observability phức tạp
* ưu tiên đơn giản + tiết kiệm

### Chọn

```text
Turned off
```

### Khi nào bật?

* khi debug performance
* khi production scale lớn

Hiện tại: chưa cần.

![Phần Monitoring cho thấy Container Insights đang để Turned off và ECS Exec logging giữ mặc định](_diagrams/ecs-cluster-form-monitoring.webp)

---

## 4. ECS Exec và Logging

### Đây là gì?

* ECS Exec = SSH vào container
* Logging = log command

### Với bạn

* chưa cần debug sâu
* chưa cần remote exec

### Hành động

```text
Giữ default
```

---

## 5. Encryption

### Đây là gì?

* mã hóa storage bằng KMS
* dùng trong hệ thống compliance cao

### Với bạn

* không xử lý dữ liệu cực kỳ nhạy cảm ở layer này
* đang focus infra setup

### Hành động

```text
Bỏ qua (skip)
```

---

## 6. Tags

### Tags dùng để làm gì?

* quản lý resource theo:
  * project
  * team
  * cost tracking

### Với bạn

* chưa cần tracking phức tạp

### Hành động

```text
Skip
```

![Phần cuối form tạo cluster hiển thị Encryption mặc định và Tags đang để trống](_diagrams/ecs-cluster-form-encryption-tags.webp)

---

## Final cấu hình

Bấm **Create**.

## Kết quả mong đợi

Sau khi tạo xong, danh sách cluster trong ECS cần hiển thị `snakeaid-backup-cluster`.

![Danh sách ECS clusters hiển thị cluster vừa tạo](_diagrams/ecs-cluster-created-list.webp)

---

## Sau bước này bạn có gì?

Bạn đã có một ECS cluster rỗng sẵn sàng để nhận service về sau. Ở thời điểm này vẫn chưa có workload nào chạy.

---

## Bước tiếp theo (quan trọng hơn)
Sau đây mới là các resource thật sự quyết định hành vi runtime: task definition, đường ALB, rồi tới ECS service.

---

## Insight quan trọng

Rất nhiều người mới bị nhầm:

> "Cluster là thứ quan trọng nhất"

Sai. Thực tế:
Cluster chủ yếu chỉ là nơi chứa. Phần quyết định hành vi thật sự nằm ở Task Definition, Service, và ALB khi chúng đi cùng nhau.

---

## TL;DR

Đặt tên, chọn Fargate, tắt monitoring ở giai đoạn hiện tại, rồi tạo cluster.
